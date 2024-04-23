import sqlite3

conn = sqlite3.connect("wedding_users.db")
c = conn.cursor()

# Create user table
c.execute(
    """CREATE TABLE IF NOT EXISTS users (
          username VARCHAR(20) PRIMARY KEY,
          password VARCHAR(15),
          first_name VARCHAR(20),
          last_name VARCHAR(20),
          address_1 VARCHAR(50),
          email VARCHAR(50),
          phone_number INTEGER,
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
          FOREIGN KEY (payment_id) REFERENCES user(username) ON DELETE CASCADE
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
          phone_number INTEGER,
          )"""
)

# Create wedding_dress table
c.execute(
    """CREATE TABLE IF NOT EXISTS wedding_dress (
          upc INTEGER(12) PRIMARY KEY,
          name VARCHAR(20),
          price REAL,
          color VARCHAR(20),
          description TEXT,
          )"""
)

# Create style table
c.execute(
    """CREATE TABLE IF NOT EXISTS style (
          style_id INTEGER PRIMARY KEY,
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
          collection_id INTEGER PRIMARY KEY,
          c1 VARCHAR(20),
          c2 VARCHAR(20),
          FOREIGN KEY (collection_id) REFERENCES wedding_dress(upc) ON DELETE CASCADE
          )"""
)

# Create brand table
c.execute(
    """CREATE TABLE IF NOT EXISTS brand (
          brand_id INTEGER PRIMARY KEY,
          b1 VARCHAR(20),
          b2 VARCHAR(20),
          FOREIGN KEY (brand_id) REFERENCES wedding_dress(upc) ON DELETE CASCADE
          )"""
)

# Create reviews table
c.execute(
    """CREATE TABLE IF NOT EXISTS reviews (
          user_id VARCHAR(20),
          wedding_dress_upc TEXT,
          comment TEXT,
          stars INTEGER,
          PRIMARY KEY (user_id, wedding_dress_upc),
          FOREIGN KEY (user_id) REFERENCES user(username) ON DELETE CASCADE,
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
          FOREIGN KEY (user_id) REFERENCES user(username) ON DELETE CASCADE,
          FOREIGN KEY (wedding_dress_upc) REFERENCES wedding_dress(upc) ON DELETE CASCADE
          )"""
)

#import data

# Log in query (user)


# Log in query (employee)


# Sign up query


# Log out query



conn.commit()
conn.close()
