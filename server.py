# if needs:
# pip install Flask
#
# How to Run the Server and Use the HTML:
# Run the Flask Server:
#
# sh
# Copy code
# python server.py
# Open Your Browser:
# Open your web browser and go to http://localhost:5000.

from flask import Flask, request, send_from_directory
import os

app = Flask(__name__)

# Serve the index.html file
@app.route('/')
def index():
    return send_from_directory('', 'index.html')

# Serve the src directory
@app.route('/src/<path:filename>')
def serve_static(filename):
    return send_from_directory('src', filename)

# Endpoint to serve the CSV file
@app.route('/ref_table.csv')
def get_csv():
    return send_from_directory('', 'ref_table.csv')

# Endpoint to save the CSV file
@app.route('/save_csv', methods=['POST'])
def save_csv():
    csv_data = request.form['csv']
    with open('ref_table.csv', 'w', newline='') as file:
        file.write(csv_data)
    return 'CSV file saved successfully'

if __name__ == '__main__':
    app.run(debug=True)
