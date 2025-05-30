import sqlite3  # For using SQLite database
import csv  # For reading CSV files
from colorama import init, Fore # For displaying Success and Error messages with colored output
init(autoreset=True)

# Connect to the local SQLite database
conn = sqlite3.connect("C:/Users/Yokii/Desktop/IT-Asset-Management/Database.db")
cursor = conn.cursor()


# Function to view all assets
def view_assets():
    try:
        cursor.execute("SELECT * FROM assets")
        assets = cursor.fetchall()

        print("\n--- ASSETS LIST ---")
        for asset in assets:
            print(asset)
        print()
    except Exception as e:
        print(Fore.RED + f"Error reading assets: {e}\n")


# Function to get an asset by serial number, model, or user
def find_asset():
    try:
        print("\nSearch by:")
        print("1. Serial Number")
        print("2. Model")
        print("3. Assigned to User")
        choice = input("Choose search option: ").strip()

        if choice == "1":
            keyword = input("Enter Serial Number: ").strip()
            cursor.execute("SELECT * FROM assets WHERE serial_number = ?", (keyword,))
        elif choice == "2":
            keyword = input("Enter Model: ").strip()
            cursor.execute("SELECT * FROM assets WHERE model LIKE ?", ('%' + keyword + '%',))
        elif choice == "3":
            keyword = input("Enter User: ").strip()
            cursor.execute("SELECT * FROM assets WHERE assigned_to LIKE ?", ('%' + keyword + '%',))
        else:
            print(Fore.RED + "Invalid option.\n")
            return

        results = cursor.fetchall()
        if results:
            print("\n--- SEARCH RESULTS ---")
            for row in results:
                print(row)
            print()
        else:
            print(Fore.YELLOW + "No matching assets found.\n")

    except Exception as e:
        print(Fore.RED + f"Error during search: {e}\n")

# Function to add a new asset
def add_asset():
    try:
        Serial = input("Serial Number: ").strip()
        Model = input("Model: ").strip()
        Storage = input("Storage: ").strip()
        RAM = input("RAM: ").strip()
        Assigned_to = input("Assigned to (We can leave blank if the machine is in stock): ").strip()
        Date = input("Date: ").strip()
        Status = "Assigned" if Assigned_to else "In Stock"
        Warranty = input("Warranty: ").strip()


        cursor.execute('''
                       INSERT INTO assets (Serial_Number, Model, Storage, RAM, Assigned_to, Date, Status,
                                           Warranty)
                       VALUES (?, ?, ?, ?, ?, ?, ?, ?)
                       ''', (Serial, Model, Storage, RAM, Assigned_to, Date, Status, Warranty))
        conn.commit()
        print(Fore.GREEN + "Asset added successfully.\n")
    except sqlite3.IntegrityError:
        print(Fore.RED + "Error: Duplicate Serial number .\n")

# Function to update asset
def update_asset():
    try:
        serial = input("Asset Serial Number to update: ").strip()
        new_user = input("Assigned to (leave blank to mark as in stock): ").strip()
        new_status = "Assigned" if new_user else "In Stock"
        new_date = input("Enter Date: ").strip()

        cursor.execute('''
                       UPDATE assets
                       SET Assigned_to = ?,
                           Date = ?,
                           Status = ?
                       WHERE Serial_Number = ?
                       ''', (new_user, new_date, new_status, serial))

        if cursor.rowcount == 0:
            print(Fore.YELLOW + "No asset found with that serial number.\n")
        else:
            conn.commit()
            print(Fore.GREEN + "Asset updated.\n")
    except Exception as e:
        print(Fore.RED + f"Error updating asset: {e}\n")

# Function to delete asset
def delete_asset():
    try:
        serial = input("Enter serial number to delete: ").strip()

        # Confirm before deleting
        confirm = input(f"Are you sure you want to delete asset '{serial}'? (yes/no): ").strip().lower()
        if confirm != "yes":
            print(Fore.GREEN + "Delete cancelled.\n")
            return

        # Execute deletion
        cursor.execute("DELETE FROM assets WHERE serial_number = ?", (serial,))
        conn.commit()

        if cursor.rowcount == 0:
            print(Fore.YELLOW + "No asset found with that serial number.\n")
        else:
            print(Fore.GREEN + "Asset deleted successfully.\n")
    except Exception as e:
        print(Fore.RED + f"Error deleting asset: {e}\n")

# Function to bulk import assets from a CSV file
def import_from_csv():
    try:
        file_path = input("Enter CSV file path: ").strip()

        # Open and read the CSV
        with open(file_path, newline='', encoding='utf-8') as csvfile:
            reader = csv.DictReader(csvfile)
            count = 0

            for row in reader:
                try:
                    cursor.execute('''
                                   INSERT INTO assets (Serial_Number, Model, Storage, RAM, Assigned_to, Date,
                                                       Status, Warranty)
                                   VALUES (?, ?, ?, ?, ?, ?, ?, ?)
                                   ''', (
                                       row["Serial_Number"].strip(),
                                       row["Model"].strip(),
                                       row["Storage"].strip(),
                                       row["RAM"].strip(),
                                       row["Assigned_to"].strip(),
                                       row["Date"].strip(),
                                       row["Status"].strip(),
                                       row["Warranty"].strip()
                                   ))
                    count += 1
                except sqlite3.IntegrityError:
                    print(Fore.RED + f"duplicate: {row['Serial_Number']}")
            conn.commit()
            print(Fore.GREEN + f"Imported {count} assets from CSV.\n")
    except Exception as e:
        print(Fore.RED + f"Error importing CSV: {e}\n")


# Application Menu
def main():
    while True:
        print("1. View All Assets")
        print("2. Find Asset")
        print("3. Add Asset")
        print("4. Update Asset")
        print("5. Delete Asset")
        print("6. Import Assets from CSV")
        print("7. Exit")
        choice = input("Choose an option: ").strip()

        if  choice == "1":
            view_assets()
        elif choice == "2":
            find_asset()
        elif choice == "3":
            add_asset()
        elif choice == "4":
            update_asset()
        elif choice == "5":
             delete_asset()
        elif choice == "6":
            import_from_csv()
        elif choice == "7":
            print("Goodbye")
            break
        else:
            print(Fore.YELLOW + "Invalid option. Try again.\n")


# To run the application
if __name__ == "__main__":
    main()
