import os
import json
import sqlite3

# SQLite database directory
sqlite_directory = './db/'

# Configurable export directory for JSON files
export_directory = './export/'


def get_table_names(cursor):
    # Get the list of table names in the SQLite database
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
    return [row[0] for row in cursor.fetchall()]


def sanitize_table_name(table_name):
    # Sanitize the table name to avoid SQL injection
    return "".join(c if c.isalnum() or c == "_" else "_" for c in table_name)


def get_columns(cursor, table_name):
    # Sanitize the table name
    table_name = sanitize_table_name(table_name)

    # Get the column names for the table
    cursor.execute(f"PRAGMA table_info({table_name});")
    return [col[1] for col in cursor.fetchall()]


def fetch_data(cursor, table_name):
    # Fetch data from the table
    cursor.execute(f"SELECT * FROM {table_name};")
    return cursor.fetchall()


def write_json(json_path, data_to_export):
    # Write the data to a JSON file
    with open(json_path, 'w') as json_file:
        json.dump(data_to_export, json_file, indent=2)


def export_sqlite_to_json(sqlite_path, json_path):
    # Connect to the SQLite database
    conn = sqlite3.connect(sqlite_path)
    cursor = conn.cursor()

    try:
        table_names = get_table_names(cursor)
        data_to_export = {}

        # Export each table to JSON
        for table_name in table_names:
            try:
                columns = get_columns(cursor, table_name)
                table_data = fetch_data(cursor, table_name)

                # Convert the data to a list of dictionaries for each row
                rows_data = []
                for row in table_data:
                    row_dict = {columns[i]: value for i,
                                value in enumerate(row)}
                    rows_data.append(row_dict)

                # Save the table data in the dictionary with table_name as the key
                data_to_export[table_name] = rows_data

            except sqlite3.Error as e:
                print(
                    f"Error exporting data from {table_name} in {sqlite_path}: {e}")

        # Write the data to a JSON file in the export directory
        write_json(json_path, data_to_export)

    except sqlite3.Error as e:
        print(f"Error exporting data from {sqlite_path}: {e}")

    finally:
        # Close the connection to the SQLite database
        conn.close()


def main():
    # Step 1: Export SQLite databases to JSON files
    if not os.path.exists(sqlite_directory):
        print("SQLite directory does not exist.")
        return

    if not os.path.exists(export_directory):
        os.makedirs(export_directory)

    for filename in os.listdir(sqlite_directory):
        if filename.endswith(".db"):
            sqlite_path = os.path.join(sqlite_directory, filename)
            json_path = os.path.join(
                export_directory, os.path.splitext(filename)[0] + '.json')

            print(f"Exporting data from {filename} to {json_path}...")
            export_sqlite_to_json(sqlite_path, json_path)
            print(f"Export completed for {filename}.\n")


if __name__ == "__main__":
    main()
