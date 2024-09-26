
import sqlite3
import csv

def insert_assay_data_from_csv(file_path:str):
    """
    This function is used to insert data from a csv file to the database.
    """
    print(f"This will insert data to assay table from {file_path} to the database.")

    conn = sqlite3.connect("data/database/quanti.sqlite")
    cursor = conn.cursor()

    with open(file_path, "r") as f:
        reader = csv.DictReader(f, delimiter=";")

        for row in reader:
            print(row)
            name = row["name"]
            species = row["species"]
            assay_type = row["assay_type"]
            unit = row["unit"]
            description = row["description"] if row["description"] else None
            created_at = row["created_at"] if row["created_at"] else None
            updated_at = row["updated_at"] if row["updated_at"] else None
            cursor.execute("""INSERT INTO assay (name, species, assay_type, unit, description, created_at, updated_at) 
                           VALUES (?, ?, ?, ?, ?, ?, ?);""", 
                           (name, species, assay_type, unit, description, created_at, updated_at))
            conn.commit()

    conn.close()

    print("Data has been inserted.")





if __name__ == "__main__":
    insert_assay_data_from_csv("data/initial data for the database/assay.csv")