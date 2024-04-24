import sqlite3
import csv
from prettytable import PrettyTable

conn = sqlite3.connect("wedding_users.db")
c = conn.cursor()


# Enable foreign key support
c.execute("PRAGMA foreign_keys = ON;")

# Create user table
c.execute(
    """CREATE TABLE IF NOT EXISTS users (
    
          username VARCHAR(20) PRIMARY KEY,
          password VARCHAR(15),
          first_name VARCHAR(20),
          last_name VARCHAR(20),
          address_1 VARCHAR(50),
          email VARCHAR(50),
          phone_number INTEGER(9),
          order_history TEXT
          )"""
)

# Create payment information table
c.execute(
    """CREATE TABLE IF NOT EXISTS payment_info (
    
          payment_id VARCHAR(20) PRIMARY KEY,
          credit_card_num INTEGER(16),
          CVC INT(3),
          expiration_date VARCHAR(5),
          FOREIGN KEY (payment_id) REFERENCES users(username) ON DELETE CASCADE
          )"""
)

# Create employee table
c.execute(
    """CREATE TABLE IF NOT EXISTS employees (
          employee_id INTEGER(9) PRIMARY KEY,
          username VARCHAR(20),
          password VARCHAR(15),
          first_name VARCHAR(20),
          last_name VARCHAR(20),
          address VARCHAR(50),
          email VARCHAR(50),
          phone_number INTEGER
          )"""
)

# Create wedding_dress table
c.execute(
    """CREATE TABLE IF NOT EXISTS wedding_dress (
          upc INTEGER(12) PRIMARY KEY,
          name VARCHAR(20),
          price REAL,
          color VARCHAR(20),
          description TEXT
          )"""
)

# Create style table
c.execute(
    """CREATE TABLE IF NOT EXISTS style (
          style_id INTEGER(12) PRIMARY KEY,
          elegant VARCHAR(20),
          vintage VARCHAR(20),
          princess VARCHAR(20),
          boho VARCHAR(20),
          FOREIGN KEY (style_id) REFERENCES wedding_dress(upc) ON DELETE CASCADE
          )"""
)

# Create collection table
c.execute(
    """CREATE TABLE IF NOT EXISTS collection (
          collection_id INTEGER(12) PRIMARY KEY,
          c1 VARCHAR(20),
          c2 VARCHAR(20),
          FOREIGN KEY (collection_id) REFERENCES wedding_dress(upc) ON DELETE CASCADE
          )"""
)


# Create reviews table
c.execute(
    """CREATE TABLE IF NOT EXISTS reviews (
          user_id VARCHAR(20),
          wedding_dress_upc INTEGER(12),
          comment TEXT,
          stars INTEGER,
          PRIMARY KEY (user_id, wedding_dress_upc),
          FOREIGN KEY (user_id) REFERENCES users(username) ON DELETE CASCADE,
          FOREIGN KEY (wedding_dress_upc) REFERENCES wedding_dress(upc) ON DELETE CASCADE
          )"""
)

# Create orders table
c.execute(
    """CREATE TABLE IF NOT EXISTS orders (
          order_num INTEGER PRIMARY KEY,
          user_id VARCHAR(20),
          wedding_dress_upc TEXT,
          tracking_id TEXT,
          arrival_status TEXT,
          FOREIGN KEY (user_id) REFERENCES users(username) ON DELETE CASCADE,
          FOREIGN KEY (wedding_dress_upc) REFERENCES wedding_dress(upc) ON DELETE CASCADE
          )"""
)



#import data
# Function to import data from CSV to database
def import_data_from_csv(csv_file, table_name):
    with open(csv_file, "r") as file:
        csv_reader = csv.reader(file)
        header = next(csv_reader)  # Get header row
        for row in csv_reader:
            # Generate placeholders for the number of columns in the CSV
            placeholders = ",".join(["?" for _ in range(len(row))])
            # Construct INSERT statement dynamically
            insert_sql = f"INSERT INTO {table_name} ({','.join(header)}) VALUES ({placeholders})"
            # Execute INSERT statement with row data
            c.execute(insert_sql, row)


# Function to display table data in a table format
def display_table_data():
    # Query to retrieve table names
    c.execute("SELECT name FROM sqlite_master WHERE type='table'")
    tables = c.fetchall()

    # For each table, retrieve data and display in a table format
    for table in tables:
        # Fetch all rows from the table
        c.execute(f"SELECT * FROM {table[0]}")
        rows = c.fetchall()

        # Get column names
        c.execute(f"PRAGMA table_info({table[0]})")
        column_names = [description[1] for description in c.fetchall()]

        # Create a PrettyTable object
        table_data = PrettyTable(column_names)

        # Add rows to the table
        for row in rows:
            table_data.add_row(row)

        # Display table data
        print(f"\nTable: {table[0]}")
        print(table_data)

# Call the function to display table data
display_table_data()

# Log in query (user)
def u_check_login(username, password):
    """Returns True if the username and password match a user in the database, False otherwise"""
    c.execute(
        "SELECT * FROM users WHERE username=:username AND password=:password",
        {"username": username, "password": password},
    )
    accEntry = c.fetchone()
    return accEntry is not None


# Log in query (employee)
def e_check_login(employee_id, username, password):
    """Returns True if the username and password match a user in the database, False otherwise"""
    c.execute(
        "SELECT * FROM employees WHERE username=:username AND password=:password AND employee_id=:employee_id",
        {"username": username, "password": password, "employee_id": employee_id},
    )
    accEntry = c.fetchone()
    return accEntry is not None


# Sign up query
def create_user(username, password, first_name, last_name,address_1, email, phone_number, order_history):
    """Returns True if the user was successfully created, False otherwise"""
    try:
        with conn:
            # Insert username, password, first name, and last name into database
            c.execute(
                "INSERT INTO users VALUES (:username, :password, :first_name, :last_name, :address_1, :email, :phone_number,:order_history )",
                {
                    "username": username,
                    "password": password,
                    "first_name": first_name,
                    "last_name": last_name,
                    "address_1": address_1,
                    "email": email,
                    "phone_number": phone_number,
                    "order_history": order_history,
                },
            )
        return True
    except sqlite3.Error as error:
        print("Failed to add user into sqlite table:", error)
        return False

# Delete the user
def delete_user(username):
    try:
        with conn:
            c.execute("DELETE FROM users WHERE username=?", (username,))
            conn.commit()
            print(f"User {username} deleted successfully")
    except sqlite3.Error as e:
        print("Error deleting user:", e)
