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
                    initializeDataTable();
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
    let tbody = document.querySelector('#csvTable tbody');
    let html = '';
    data.forEach((row, index) => {
        if (index === 0) return;  // Skip the header row
        html += '<tr>';
        row.forEach((cell, cellIndex) => {
            if (csvData[0][cellIndex] === "TOPICS") {
                html += `<td contenteditable="true">${markdownToHTML(cell)}</td>`;
            } else {
                html += `<td>${markdownToHTML(cell)}</td>`;
            }
        });
        html += '</tr>';
    });
    tbody.innerHTML = html;
}

function initializeDataTable() {
    // Initialize DataTables with column search
    let table = $('#csvTable').DataTable({
        paging: true,
        searching: true,
        ordering: true,
        info: true
    });

    // Apply the search
    $('#csvTable thead tr:eq(1) th').each(function (i) {
        $('input', this).on('keyup change', function () {
            if (table.column(i).search() !== this.value) {
                table
                    .column(i)
                    .search(this.value)
                    .draw();
            }
        });
    });
}

function saveCSV() {
    // Get the updated data from the table
    const rows = document.querySelectorAll('#csvTable tbody tr');
    const newCsvData = [csvData[0]];  // Add headers back

    rows.forEach((row) => {
        const cells = row.querySelectorAll('td');
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
