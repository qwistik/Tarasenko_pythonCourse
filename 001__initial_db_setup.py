import sqlite3
import sys

# Parse command-line arguments
unique_flag = False
if "--unique" in sys.argv:
    unique_flag = True

# Establish a connection to the SQLite database
connection = sqlite3.connect('bank.db')

# Create a cursor object to execute SQL commands
cursor = connection.cursor()

# Define SQL statements to create tables
create_bank_table_query = """
CREATE TABLE IF NOT EXISTS Bank (
    id INTEGER PRIMARY KEY,
    name TEXT NOT NULL UNIQUE
)
"""

create_transaction_table_query = """
CREATE TABLE IF NOT EXISTS "Transaction" (
    id INTEGER PRIMARY KEY,
    Bank_sender_name TEXT NOT NULL,
    Account_sender_id INTEGER NOT NULL,
    Bank_receiver_name TEXT NOT NULL,
    Account_receiver_id INTEGER NOT NULL,
    Sent_Currency TEXT NOT NULL,
    Sent_Amount REAL NOT NULL,
    Datetime TEXT
)
"""

create_user_table_query = """
CREATE TABLE IF NOT EXISTS User (
    id INTEGER PRIMARY KEY,
    Name TEXT NOT NULL {unique_name},
    Surname TEXT NOT NULL {unique_surname},
    Birth_day TEXT,
    Accounts TEXT NOT NULL
)
""".format(unique_name="UNIQUE" if unique_flag else "", unique_surname="UNIQUE" if unique_flag else "")

create_account_table_query = """
CREATE TABLE IF NOT EXISTS Account (
    id INTEGER PRIMARY KEY,
    User_id INTEGER NOT NULL,
    Type TEXT NOT NULL,
    Account_Number TEXT NOT NULL UNIQUE,
    Bank_id INTEGER NOT NULL,
    Currency TEXT NOT NULL,
    Amount REAL NOT NULL,
    Status TEXT
)
"""

# Execute the SQL statements to create tables
cursor.execute(create_bank_table_query)
cursor.execute(create_transaction_table_query)
cursor.execute(create_user_table_query)
cursor.execute(create_account_table_query)

# Commit the changes to the database
connection.commit()

# Close the cursor and connection
cursor.close()
connection.close()
