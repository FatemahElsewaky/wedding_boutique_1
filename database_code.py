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
          FOREIGN KEY (user_id) REFERENCES users(username) ON DELETE CASCADE
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


# # Create dress information view as a user
# c.execute(
#     """CREATE VIEW users_info AS
#         SELECT u.username, u.password, u.first_name, u.last_name, u.address_1, u.email, u.phone_number, u.order_history,
#                 p.credit_card_num, p.CVC, p.expiration_date
#                 FROM users u
#                 LEFT JOIN payment_info p ON u.username = p.payment_id"""
# )

# # Create dress information view as an employee
# c.execute(
#     """CREATE VIEW dress_info_employee AS
#             SELECT wd.upc, wd.name, wd.price, wd.color, wd.description,
#                    s.elegant, s.vintage, s.princess, s.boho,
#                    c.c1, c.c2
#             FROM wedding_dress wd
#             LEFT JOIN style s ON wd.upc = s.style_id
#             LEFT JOIN collection c ON wd.upc = c.collection_id"""
# )


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


def display_view_data(view_name):
    try:
        # Fetch all rows from the view
        c.execute(f"SELECT * FROM {view_name}")
        rows = c.fetchall()

        if not rows:
            print(f"No data found in the view {view_name}")
            return

        # Get column names
        c.execute(f"PRAGMA table_info({view_name})")
        column_names = [description[1] for description in c.fetchall()]

        # Create a PrettyTable object
        view_table = PrettyTable(column_names)

        # Add rows to the table
        for row in rows:
            view_table.add_row(row)

        # Display the view data
        print(f"\nView: {view_name}")
        print(view_table)

    except sqlite3.Error as e:
        print(f"Error displaying data from the view {view_name}: {e}")


# Example usage:
display_view_data("dress_info_users")
display_view_data("dress_info_employee")
display_view_data("users_info")


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
def create_user(username, password, first_name, last_name, address_1, email, phone_number, order_history):
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


def fetch_user_data(username):
    # Fetch user data including payment information from the database based on the username
    c.execute(
        "SELECT * FROM users LEFT JOIN payment_info ON users.username = payment_info.payment_id WHERE users.username=?",
        (username,))
    user_data = c.fetchone()
    if user_data:
        return {
            'username': user_data[0],
            'first_name': user_data[2],
            'last_name': user_data[3],
            'address_1': user_data[4],
            'email': user_data[5],
            'phone_number': user_data[6],
            'credit_card_num': user_data[9],
            'CVC': user_data[10],
            'expiration_date': user_data[11]
        }
    else:
        return None


def update_user_data(username, field, new_value):
    if field in ["credit_card_num", "CVC", "expiration_date"]:
        # Check if the user already has payment information
        c.execute("SELECT * FROM payment_info WHERE payment_id=?", (username,))
        existing_payment_info = c.fetchone()

        if existing_payment_info:
            # Update existing payment information
            c.execute(f"UPDATE payment_info SET \"{field}\"=? WHERE payment_id=?", (new_value, username))
        else:
            # Insert new payment information
            c.execute("INSERT INTO payment_info VALUES (?, ?, ?, ?)", (username, None, None, None))
            # Update the newly inserted payment information
            c.execute(f"UPDATE payment_info SET \"{field}\"=? WHERE payment_id=?", (new_value, username))
    else:
        # Update other user information
        c.execute(f"UPDATE users SET \"{field}\"=? WHERE username=?", (new_value, username))

    conn.commit()


def fetch_employee_data(employee_id):
    try:
        # Fetch employee data from the database based on the employee ID
        c.execute("SELECT * FROM employees WHERE employee_id=?", (employee_id,))
        employee_data = c.fetchone()
        if employee_data:
            return {
                'employee_id': employee_data[0],
                'username': employee_data[1],
                'password': employee_data[2],
                'first_name': employee_data[3],
                'last_name': employee_data[4],
                'address': employee_data[5],
                'email': employee_data[6],
                'phone_number': employee_data[7]
            }
        else:
            return None
    except sqlite3.Error as e:
        print("Error fetching employee data:", e)
        return None

def update_employee_data(employee_id, field, new_value):
    try:
        # Update employee data in the database
        c.execute(f"UPDATE employees SET \"{field}\"=? WHERE employee_id=?", (new_value, employee_id))
        conn.commit()
    except sqlite3.Error as e:
        print("Error updating employee data:", e)

def add_review(user_id, wedding_dress_upc, comment, stars):
    try:
        # SQL query to insert a new review into the reviews table
        c.execute("INSERT INTO reviews (user_id, wedding_dress_upc, comment, stars) VALUES (?, ?, ?, ?)",
                  (user_id, wedding_dress_upc, comment, stars))
        # Commit the changes to the database
        conn.commit()

        print("Review added successfully!")

    except sqlite3.Error as error:
        print("Failed to add review:", error)

def fetch_reviews():
    try:
        with conn:

            # Query to fetch reviews
            c.execute("SELECT comment, stars, user_id FROM reviews")
            reviews_data = c.fetchall()

            # Create a list to store reviews
            reviews = []

            # Iterate over the fetched data and convert it to dictionaries
            for review in reviews_data:
                # Create a dictionary for each review
                review_dict = {
                    'comment': review[0],  # Index 0 corresponds to the comment
                    'stars': review[1],    # Index 1 corresponds to the stars
                    'user': review[2]      # Index 2 corresponds to the user
                }
                # Append the dictionary to the list of reviews
                reviews.append(review_dict)

            return reviews

    except sqlite3.Error as e:
        print("Error fetching reviews:", e)
        return []

