import os
from models.database import Database
from models.user import User
from models.currency import Currency
from models.denomination import Denomination
from utils import config


print("   _____          _      _____                  _               _____      _               ")
print("  / ____|        | |    / ____|                | |             / ____|    | |              ")
print(" | |     __ _ ___| |__ | |     ___  _   _ _ __ | |_ ___ _ __  | (___   ___| |_ _   _ _ __  ")
print(" | |    / _\\` / __| '_ \\| |    / _ \\| | | | '_ \\| __/ _ \\ '__|  \\___ \\ / _ \\ __| | | | '_ \\ ")
print(" | |___| (_| \\__ \\ | | | |___| (_) | |_| | | | | ||  __/ |     ____) |  __/ |_| |_| | |_) |")
print("  \\_____\\__,_|___/_| |_|\\_____\\___/ \\__,_|_| |_|\\__\\___|_|    |_____/ \\___|\\__|\\__,_| .__/ ")
print("                                                                                    | |    ")
print("                                                                                    |_|    ")
print("\n" * 3)

# Deleting the DB if it already exists
if os.path.exists(config.DB_NAME):
    os.remove(config.DB_NAME)

# Setting up the DB
print("Creating the database...", end=" ")
db = Database(config.DB_NAME)

db.query(
    """
CREATE TABLE users (
    user_id    INTEGER PRIMARY KEY AUTOINCREMENT
                       UNIQUE
                       NOT NULL,
    first_name TEXT    NOT NULL,
    last_name  TEXT    NOT NULL,
    username   TEXT    NOT NULL
                       UNIQUE,
    password           NOT NULL,
    is_admin   INTEGER NOT NULL
                       CHECK (is_admin IN (0, 1) ) 
);
"""
)  # Setting up the Users table

db.query(
    """
CREATE TABLE currencies (
    currency_id INTEGER PRIMARY KEY AUTOINCREMENT
                        NOT NULL
                        UNIQUE,
    symbol      TEXT    UNIQUE
                        NOT NULL,
    name        TEXT    UNIQUE
                        NOT NULL
);
"""
)  # Setting up the Currencies

db.query(
    """
CREATE TABLE counts (
    count_id INTEGER PRIMARY KEY AUTOINCREMENT
                     UNIQUE
                     NOT NULL,
    user     INTEGER REFERENCES users (user_id) ON DELETE CASCADE
                                                ON UPDATE CASCADE
                     NOT NULL,
    date     TEXT    AS (DATETIME('now') ) 
                     NOT NULL,
    currency INTEGER NOT NULL
                     REFERENCES currencies (currency_id) ON DELETE CASCADE
                                                         ON UPDATE CASCADE
);
"""
)  # Setting up the Counts table

db.query(
    """
CREATE TABLE denominations (
    denomination_id INTEGER PRIMARY KEY AUTOINCREMENT
                            NOT NULL
                            UNIQUE,
    currency                REFERENCES currencies (currency_id) ON DELETE CASCADE
                                                                ON UPDATE CASCADE
                            NOT NULL,
    value           REAL    NOT NULL
);
"""
)  # Setting up the Denominations table

db.query(
    """
CREATE TABLE count_records (
    count_record_id INTEGER PRIMARY KEY AUTOINCREMENT
                            UNIQUE
                            NOT NULL,
    denomination            REFERENCES denominations (denomination_id) ON DELETE CASCADE
                                                                       ON UPDATE CASCADE
                            NOT NULL,
    quantity        INTEGER NOT NULL
);
"""
)  # Setting up the Count_Records table

print("DONE\n")

# Adding default values to the DB
# User
print("Create the Admin User:")
first_name: str = input("First Name: ")
last_name: str = input("Last Name: ")
username: str = input("Username: ")
password: str = input("Password: ")

user: User = User(first_name, last_name, username, True)
user.save(password)

# Currency
print("\nSet Up the Default Currency:")
symbol: str = input("Symbol: ")
name: str = input("Name: ")

currency: Currency = Currency(symbol, name)
currency.save()

# Denominations
print("\nSet Up the Denominations:")
for i in range(int(input(("How Many Denominations Do You Want to Set Up? ")))):
    print(f"\nDenomination #{i + 1}")
    value: float = float(input("Value: "))
    
    denomination: Denomination = Denomination(currency, value)
    denomination.save()

print("\nCashCounter set up successfully!")