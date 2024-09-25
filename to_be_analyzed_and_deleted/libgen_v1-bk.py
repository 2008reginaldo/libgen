# %%
import sys
import hashlib
import os
import re
import bibtexparser

# %%
def renamePDFs(directory):

    def name_check(filename):
        pattern = r'^[A-Za-z-]+(\-[A-Za-z]+)?[0-9]{4}__[a-f0-9]{32}\.pdf$'
        if re.match(pattern, filename):
            return 0
        else:
            return 1

    def find_and_remove_duplicates(directory):

        def hash_file(filename):
            hasher = hashlib.md5()
            with open(filename, 'rb') as f:
                buf = f.read()
                hasher.update(buf)
            return hasher.hexdigest()

        hashes = {}
        files = os.listdir(directory)

        for filename in files:
            if filename.endswith('.pdf'):
                file_path = os.path.join(directory, filename)
                file_hash = hash_file(file_path)

                if file_hash in hashes:
                    print(f"Deleting duplicate file: {filename}")
                    os.remove(file_path)
                else:
                    hashes[file_hash] = filename

    find_and_remove_duplicates(directory)
    files = os.listdir(directory)
    try:
        with open('/home/regis/Dropbox/Academico/libgen/library.bib') as bibtex_file:
            bib_database = bibtexparser.load(bibtex_file)
    except:
        print('No bibtext file fond')
    os.chdir(directory)
    for file in files:
        if file.endswith('.pdf'):
            if name_check(file):
                print(f'searching name {file} in library.bib')
                msg_buffer = "Filename not found!"
                for entry in bib_database.entries:
                    filenameFromBib = entry.get('file', '').strip()
                    filenameFromBib = os.path.basename(filenameFromBib).replace(':pdf','').strip()
                    if file == filenameFromBib:
                        msg_buffer = ""
                        paper_ID = entry.get('ID', '').strip()
                        md5_hash = hashlib.md5()
                        with open(file, 'rb') as f:
                            print('ok')
                            for chunk in iter(lambda: f.read(4096), b""):
                                md5_hash.update(chunk)
                        md5_checksum = md5_hash.hexdigest()
                        newName = paper_ID + '__' + md5_checksum + '.pdf'
                        try:
                            os.rename(file, newName)
                            print(f"old: {file}, new: {newName}")
                        except Exception as e:
                            print(f"Error processing {file}: {e}")
                print(msg_buffer)

# %%
def makeRefTable(directory):
    import sqlite3

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


    def generate_id(s):
        md5_hash = hashlib.md5()
        md5_hash.update(s.encode('utf-8'))
        hash_hex = md5_hash.hexdigest()
        return '_'+hash_hex[:10]



    # Connect to the SQLite database
    # É necessário conectar-se ao shared.db do sioyek.
    # Geralmente localizado em ~/.local/share/sioyek/shared.db
    conn = sqlite3.connect('/home/regis/Dropbox/Academico/libgen/shared.db')
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM highlights;")
    with open("ref_table.csv", 'w') as output_file:
        output_file.write(f"ID\tkey\tyear\ttype\tannotation\n".upper())
        for entry in cursor.fetchall():
            ID = generate_id(entry[2])
            key = names[entry[1]]
            year = re.findall(r'\d+', key)[0] #-> extract year from the key
            annotation_type = entry[3]
            annotation = entry[2]
            output_file.write(f"{ID}\t{key}\t{str(year)}\t{annotation_type}\t{annotation}\n")

    conn.commit()
    conn.close()

# %%
def main():

    print("Please choose an option:")
    print("1 - Rename articles")
    print("2 - Make reference table")

    choice = input("Enter your choice (1 or 2): ")

    if choice == '1':
        renamePDFs("/home/regis/Dropbox/Academico/Artigos")
        result = 'ok'
    elif choice == '2':
        makeRefTable("/home/regis/Dropbox/Academico/Artigos")
        result = 'ok'
    else:
        print("Invalid choice.")
        return

    print("Result:", result)

if __name__ == "__main__":
    main()
