import sqlite3

# Open database
conn = sqlite3.connect('ehealth.db')

# Create table
conn.execute('''CREATE TABLE users 
(
    id INTEGER NOT NULL PRIMARY KEY,
    firstName TEXT NOT NULL,
    lastName TEXT NOT NULL,
    username TEXT NOT NULL,
    hash TEXT NOT NULL,
    email TEXT NOT NULL,
    address1 TEXT NOT NULL,
	city TEXT NOT NULL,
	phone TEXT
)''')
conn.execute('''CREATE TABLE products
		(productId INTEGER PRIMARY KEY,
		name TEXT,
		price REAL,
		description TEXT,
		image TEXT,
		stock INTEGER,
		categoryId INTEGER,
		FOREIGN KEY(categoryId) REFERENCES categories(categoryId)
		)''')

conn.execute('''CREATE TABLE cart
		(userId INTEGER,
		productId INTEGER,
		FOREIGN KEY(userId) REFERENCES users(userId),
		FOREIGN KEY(productId) REFERENCES products(productId)
		)''')

conn.execute('''CREATE TABLE Confirm
		(
		cid INTEGER PRIMARY KEY,
		userId INTEGER,
		productId INTEGER, 
		FOREIGN KEY(userId) REFERENCES users(id),
		FOREIGN KEY(productId) REFERENCES products(productId)
		)''')
conn.execute('''CREATE TABLE categories
		(categoryId INTEGER PRIMARY KEY,
		name TEXT
		)''')




conn.close()
