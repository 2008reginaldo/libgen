// src/script.js

document.addEventListener('DOMContentLoaded', function () {
    fetchCSV();
});

let csvData;

function fetchCSV() {
    const url = 'ref_table.csv';  // Hard-coded path to the CSV file

    fetch(url)
        .then(response => response.text())
        .then(text => {
            Papa.parse(text, {
                complete: function (results) {
                    csvData = results.data;
                    displayTable(csvData);
                },
                error: function (error) {
                    console.error('Error:', error);
                }
            });
        })
        .catch(error => console.error('Error fetching the CSV file:', error));
}

function markdownToHTML(text) {
    return text
        .replace(/\*\*(.*?)\*\*/g, '<strong>$1</strong>') // Bold
        .replace(/\n/g, '<br>'); // Line breaks
}

function displayTable(data) {
    let html = '<table>';
    html += `
        <colgroup>
            <col>
            <col>
            <col>
            <col>
            <col>
            <col>
        </colgroup>
    `;
    data.forEach((row, index) => {
        html += '<tr>';
        row.forEach((cell, cellIndex) => {
            if (index === 0) {
                html += `<th>${markdownToHTML(cell)}</th>`;
            } else {
                if (csvData[0][cellIndex] === "TOPICS") {
                    html += `<td contenteditable="true">${markdownToHTML(cell)}</td>`;
                } else {
                    html += `<td>${markdownToHTML(cell)}</td>`;
                }
            }
        });
        html += '</tr>';
    });
    html += '</table>';
    document.getElementById('csvTable').innerHTML = html;
}

function saveCSV() {
    // Get the updated data from the table
    const rows = document.querySelectorAll('#csvTable tr');
    const newCsvData = [];

    rows.forEach((row, rowIndex) => {
        const cells = row.querySelectorAll('th, td');
        const newRow = [];

        cells.forEach(cell => {
            newRow.push(cell.innerText.replace(/<br>/g, '\n').replace(/<strong>(.*?)<\/strong>/g, '**$1**'));
        });

        newCsvData.push(newRow);
    });

    // Convert updated data to CSV string
    const csvString = Papa.unparse(newCsvData);

    // Send the CSV string to the server to save it
    fetch('/save_csv', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/x-www-form-urlencoded',
        },
        body: 'csv=' + encodeURIComponent(csvString)
    })
        .then(response => response.text())
        .then(data => {
            console.log(data);
            alert('CSV file saved successfully');
        })
        .catch(error => console.error('Error saving the CSV file:', error));
}