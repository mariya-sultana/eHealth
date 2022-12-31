-- SQLite
-- CREATE TABLE products(productId INTEGER PRIMARY KEY,
-- 		name TEXT,
-- 		price REAL,
-- 		description TEXT,
-- 		image TEXT,
-- 		stock INTEGER,
-- 		categoryId INTEGER,
-- 		FOREIGN KEY(categoryId) REFERENCES categories(categoryId)
-- 		);
--  DROP TABLE users;
-- CREATE TABLE users (
--     id INTEGER NOT NULL PRIMARY KEY,
--     firstName TEXT NOT NULL,
--     lastName TEXT NOT NULL,
--     username TEXT NOT NULL,
--     hash TEXT NOT NULL,
--     email TEXT NOT NULL,
--     address1 TEXT NOT NULL,
-- 	city TEXT NOT NULL,
-- 	phone TEXT
-- )
-- CREATE TABLE cart
-- 		(userId INTEGER,
-- 		productId INTEGER,
-- 		FOREIGN KEY(userId) REFERENCES users(userId),
-- 		FOREIGN KEY(productId) REFERENCES products(productId)
-- 		);

-- INSERT INTO
-- products(productId, name, price, description, image, stock,categoryId)
-- VALUES
-- ('1',	'Amoxicillin',	'16.6',	'This is an Antibiotic Product.',	'amoxicillin.jpg','NULL',	'1'),
-- ('2',	'ciprofloxacin',	'15.6',	'This product will protect you from kirimi',	'ciprofloxacin.jpg','NULL',	'1'),
-- ('3',	'penicillin',	'8.6',	'This is also an antibiotic product it is mainly used in aged people',	'penicillin.jpg','NULL',	'1'),
-- ('4',	'advil',	'85.0',	'This is an fever based product',	'advil.jpg','NULL',	'2'),
-- ('5',	'capoten',	'26.3',	'This is protect you from fever',	'capoten.jpg','NULL',	'2'),
-- ('6',	'mortrin',	'89.0',	'	This is an heavy product',	'mortrin.jpg','NULL',	'2'),
-- ('7',	'aloe vera',	'5.2',	'This is ayurvetha product',	'aloe_vera.jpg','NULL',	'3'),
-- ('8',	'ginseng',	'78.0',	'This is also natural medicine.It is mainly used for cough',	'ginseng.jpg','NULL',	'3'),
-- ('9',	'milk thistle',	'8.2',	'Naturual medicine',	'milk_thistle.jpg','NULL',	'3'),
-- ('10',	'aspirine',	'66.0',	'This is used for pain killer purpose',	'aspirine.jpg','NULL',	'4'),
-- ('11',	'morphine',	'6.5',	'This is for special treatment',	'morphine.jpg','NULL',	'4'),
-- ('12',	'paracetamol',	'8.5',	'This product mainly used for heavy fever.',	'paracetamol.jpg','NULL',	'4');

-- DROP TABLE cart;

-- CREATE TABLE cart
-- 		(userId INTEGER,
-- 		productId INTEGER,
-- 		FOREIGN KEY(userId) REFERENCES users(userId),
-- 		FOREIGN KEY(productId) REFERENCES products(productId)
-- 		);

-- CREATE TABLE addcart
-- 		(userId INTEGER,
-- 		productId INTEGER,
-- 		quantity INTEGER,
-- 		FOREIGN KEY(userId) REFERENCES users(userId),
-- 		FOREIGN KEY(productId) REFERENCES products(productId)
-- 		);

-- DROP TABLE addcart;


-- CREATE TABLE categories
-- 		(categoryId INTEGER PRIMARY KEY,
-- 		name TEXT
-- 		);

-- DROP TABLE categories;
-- INSERT INTO
-- categories(categoryId,name)
-- VALUES
-- ('1',	'ANTIBIATICS'),
-- ('2',	'FEVER'),
-- ('3',	'NATURAL MEDICINE'),
-- ('4',	'PAIN KILLER');
-- DROP TABLE ConfirmOrder;
-- CREATE TABLE Confirm
-- 		(
-- 		cid INTEGER PRIMARY KEY,
-- 		userId INTEGER,
-- 		productId INTEGER, 
-- 		FOREIGN KEY(userId) REFERENCES users(userId),
-- 		FOREIGN KEY(productId) REFERENCES products(productId)
-- 		);

DELETE FROM Confirm WHERE cid = 10;