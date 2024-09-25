import sqlite3
import os
import re

def makeRefTable(directory):

    def get_names(directory):
        names = {}
        files = os.listdir(directory)
        for filename in files:
            if filename.endswith('.pdf'):
                value, key  = filename.split('__')
                names[key.replace(".pdf", "")] = value
                print(key.replace(".pdf", ""), value)
        return names

    names = get_names(directory)

    # Connect to the SQLite database
    # É necessário conectar-se ao shared.db do sioyek.
    # Geralmente localizado em ~/.local/share/sioyek/shared.db
    conn = sqlite3.connect('shared.db')
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM highlights;")
    with open("ref_table.csv", 'w') as output_file:
        output_file.write(f"key \t year \t annotation_type \t annotation\n".upper())
        for entry in cursor.fetchall():
            key = names[entry[1]]
            year = re.findall(r'\d+', key)[0] #-> extract year from the key
            annotation_type = entry[3]
            annotation = entry[2]
            output_file.write(f"{key} \t {year} \t {annotation_type} \t {annotation}\n")


# makeRefTable("Artigos")