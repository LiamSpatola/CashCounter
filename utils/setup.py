from models.database import Database


print("   _____          _      _____                  _               _____      _               ")
print("  / ____|        | |    / ____|                | |             / ____|    | |              ")
print(" | |     __ _ ___| |__ | |     ___  _   _ _ __ | |_ ___ _ __  | (___   ___| |_ _   _ _ __  ")
print(" | |    / _\` / __| '_ \| |    / _ \| | | | '_ \| __/ _ \ '__|  \___ \ / _ \ __| | | | '_ \ ")
print(" | |___| (_| \__ \ | | | |___| (_) | |_| | | | | ||  __/ |     ____) |  __/ |_| |_| | |_) |")
print("  \_____\__,_|___/_| |_|\_____\___/ \__,_|_| |_|\__\___|_|    |_____/ \___|\__|\__,_| .__/ ")
print("                                                                                    | |    ")
print("                                                                                    |_|    ")
print("\n" * 3)


# Setting up the DB
print("Creating the database...", end=" ")
db = Database()

db.query("""
CREATE TABLE users (
    user_id    INTEGER PRIMARY KEY AUTOINCREMENT
                       UNIQUE
                       NOT NULL,
    first_name TEXT    NOT NULL,
    last_name  TEXT    NOT NULL,
    username   TEXT    NOT NULL
                       UNIQUE,
    password           NOT NULL
);
""") # Setting up the Users table

db.query("""
CREATE TABLE currencies (
    currency_id INTEGER PRIMARY KEY AUTOINCREMENT
                        NOT NULL
                        UNIQUE,
    symbol      TEXT    UNIQUE
                        NOT NULL
);
""") # Setting up the Currencies

db.query("""
CREATE TABLE counts (
    count_id INTEGER PRIMARY KEY AUTOINCREMENT
                     UNIQUE
                     NOT NULL,
    user     INTEGER REFERENCES users (user_id) ON DELETE CASCADE
                                                ON UPDATE CASCADE
                     NOT NULL,
    date     TEXT    AS (DATETIME('now') ) 
                     NOT NULL,
    currency TEXT    NOT NULL
                     REFERENCES currencies (currency_id) ON DELETE CASCADE
                                                         ON UPDATE CASCADE
);
""") # Setting up the Counts table

db.query("""
CREATE TABLE denominations (
    denomination_id INTEGER PRIMARY KEY AUTOINCREMENT
                            NOT NULL
                            UNIQUE,
    currency_id             REFERENCES currencies (currency_id) ON DELETE CASCADE
                                                                ON UPDATE CASCADE
                            NOT NULL,
    value           REAL    UNIQUE
                            NOT NULL
);
""") # Setting up the Denominations table

db.query("""
CREATE TABLE count_records (
    count_record_id INTEGER PRIMARY KEY AUTOINCREMENT
                            UNIQUE
                            NOT NULL,
    denomination_id         REFERENCES denominations (denomination_id) ON DELETE CASCADE
                                                                       ON UPDATE CASCADE
                            NOT NULL,
    quantity        INTEGER NOT NULL
);
""") # Setting up the Count_Records table

print("DONE\n")

# Adding default values to the DB
# User
print("Create a User:")
first_name: str = input("First Name: ")
last_name: str = input("Last Name: ")
username: str = input("Username: ")
password: str = input("Password: ")

# TODO: Add the logic here

# Currency
print("\nSet Up the Default Currency:")
symbol: str = input("Symbol: ")

# TODO: Add the logic here

# Denominations
print("\nSet Up the Denominations:")
for i in range(int("How Many Denomination Do You Want to Set Up? ")):
    print()
    value: float = float(input("Value: "))
    # TODO: Add the logic here (use the default currency for the denomination currency)