import _sqlite3
import os

# do sqlite3 we need a path to db

db_abspath = os.path.abspath(os.path.dirname(__file__))
db_path = os.path.join(db_abspath, "..", "alegrosz.db")

# connect to db
conn = _sqlite3.connect(db_path)
# db can connect multiple db, now we can talk with db, but we need cursor
c = conn.cursor()

# to run db .execute and it takes sql string
c.execute("DROP TABLE IF EXISTS item")  # in sql columns in single not multiple item not items
# each sql base is divided (we can have multiple base) on tables/orders and we need to clear first
# because of db init, to clean before first run
c.execute("DROP TABLE IF EXISTS category")
c.execute("DROP TABLE IF EXISTS subcategory")
c.execute("DROP TABLE IF EXISTS comment")

#  run new sql to create db CREATE TABLE (typ) - problem because each item can be in different category
#  this is why we create category first because we need it first before item
# TEXT = STRING
c.execute('''CREATE TABLE category (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT
)''')
c.execute('''CREATE TABLE subcategory (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT,
    category_id INTEGER,
    FOREIGN KEY (category_id) REFERENCES category (id)
)''')
# category id integer must know from where it take, so to connect 2 bases we need foreign key
c.execute('''CREATE TABLE item (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    title TEXT,
    description TEXT,
    price REAL,
    image TEXT,
    category_id INTEGER,
    subcategory_id INTEGER,
    FOREIGN KEY (category_id) REFERENCES category (id),
    FOREIGN KEY (subcategory_id) REFERENCES subcategory (id)
    )''')
#  images to keep images - to keep in database,
#  second type is  to keep on server and just provide links (our case this is why text)
#  item need to be in both foreign keys because of question to db

c.execute('''CREATE TABLE comment (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    content TEXT,
    item_id INTEGER,
    FOREIGN KEY (item_id) REFERENCES item(id)
)''')

#  define categories for basic setup of db
categories = [
    ("Food",),
    ("Instruments",),
    ("Drags",),
]
#  TO ADD TO BASE INSERT values (w sql we use food instruments drags but here we put ? as many columns we fill out
c.executemany('INSERT INTO category (name) values (?)', categories)
# if we put ?? we 2 elements tuples

# because of sub connection to cat we need 2 elements tuple and we put id (1)
subcategories = [
    ("Fruit", 1),
    ("Meat", 1),
    ("Sweats", 1),
    ("Guitars", 2),
    ("Drums", 2),
    ("Trumpets", 2),
    ("Painkiller", 3),
    ("Natural", 3),
    ("Vitamins", 3),
]
c.executemany('INSERT INTO subcategory (name, category_id) values (?,?)', subcategories)
#  name disc price img category sub category below
items = [
    ('Bananas', '1 kg of fresh bananas', 6.50, '', 1, 1),
    ('Gibson Les Paul', 'Electric guitar', 4500.00, '', 2, 4),
    ('Candies', ' 0.5kg of candies', 8.95, '', 1, 3),
    ('APP', '12 pills of fresh headache', 10, '', 3, 7),
]

c.executemany('INSERT INTO item (title, description, price, image, category_id, subcategory_id) VALUES (?,?,?,?,?,?)',
              items)

# this will not work yet it still need commit
#  this will run db
conn.commit()
conn.close()

print("Database is created and initialized.")
