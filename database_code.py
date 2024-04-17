import sqlite3

conn = sqlite3.connect("wedding_users.db")
c = conn.cursor()

# Create user table
c.execute(
    """CREATE TABLE IF NOT EXISTS user (
          username VARCHAR(20) PRIMARY KEY,
          password VARCHAR(15),
          first_name VARCHAR(20),
          last_name VARCHAR(20),
          address VARCHAR(50),
          payment_info VARCHAR(20),
          email VARCHAR(50),
          phone_number INTEGER,
          order_history TEXT
          )"""
)

# Create wedding_dress table
c.execute(
    """CREATE TABLE IF NOT EXISTS wedding_dress (
          upc INTEGER PRIMARY KEY,
          name VARCHAR(20),
          price REAL,
          size CHAR[5],
          color VARCHAR(20),
          description TEXT,
          on_hand_count INTEGER
          )"""
)

# Create style table
c.execute(
    """CREATE TABLE IF NOT EXISTS style (
          style_id INTEGER PRIMARY KEY,
          spring VARCHAR(20),
          summer VARCHAR(20),
          fall VARCHAR(20),
          short VARCHAR(20),
          long VARCHAR(20),
          sleeves VARCHAR(20),
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

# Create occasion table
c.execute(
    """CREATE TABLE IF NOT EXISTS occasion (
          occasion_id INTEGER PRIMARY KEY,
          engagement VARCHAR(20),
          bridal_shower VARCHAR(20),
          bachelorette VARCHAR(20),
          FOREIGN KEY (occasion_id) REFERENCES wedding_dress(upc) ON DELETE CASCADE         
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
          return_status TEXT,
          tracking_id TEXT,
          arrival_status TEXT,
          FOREIGN KEY (user_id) REFERENCES user(username) ON DELETE CASCADE,
          FOREIGN KEY (wedding_dress_upc) REFERENCES wedding_dress(upc) ON DELETE CASCADE
          )"""
)

conn.commit()
conn.close()