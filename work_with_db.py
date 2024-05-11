import csv
import requests

from decorator import db_connection, logger
from validator import *


TOKEN_API = "fca_live_vcgjc1xXwoWY4NV8qVn3fpmbluAioH4HfFvYOmoa"


def get_validated_user_data(data):
    """
    Validate and extract user data.

    :param data: Tuple containing user data (user_full_name, birth_day, accounts).
    :return: Validated user data (name, surname, birth_day, accounts).
    """
    if isinstance(data[0], int):
        name, surname = validate_user_full_name(data[1])
        name, surname = validate_user_full_name(name + ' ' + surname)
        return name, surname, data[2], data[3]
    else:
        name, surname = validate_user_full_name(data[0])
        name, surname = validate_user_full_name(name + ' ' + surname)
        return name, surname, data[1], data[2]


@db_connection
def add_user(cursor, *user_data):
    """
    Add user(s) to the database.

    :param cursor: SQLite cursor object.
    :param user_data: User data, where each tuple contains
        (user_full_name, birth_day, accounts).
    :return: Success or failure message.
    """
    try:
        if not isinstance(user_data[0], tuple):
            cursor.execute("INSERT INTO User (Name, Surname, Birth_day, Accounts) VALUES (?, ?, ?, ?)",
                           get_validated_user_data(user_data))
        else:
            for data in user_data:
                cursor.execute("INSERT INTO User (Name, Surname, Birth_day, Accounts) VALUES (?, ?, ?, ?)",
                               get_validated_user_data(data))

        logger.info("User(s) added successfully.")
        return "User(s) added successfully."
    except Exception as e:
        logger.error(f"Error adding user(s): {e}")
        return f"Error adding user(s): {e}"


@db_connection
def add_users_from_csv(cursor, file_path):
    """
    Add users from a CSV file to the database.

    :param cursor: SQLite cursor object.
    :param file_path: Path to the CSV file.
    :return: Success or failure message.
    """
    try:
        with open(file_path, 'r') as file:
            csv_reader = csv.reader(file)
            next(csv_reader)  # Skip header row
            add_user(cursor, csv_reader)

        return "Users added successfully from CSV file."
    except Exception as e:
        logger.error(f"Error adding users from CSV: {e}")
        return f"Error adding users from CSV: {e}"


@db_connection
def modify_user(cursor, user_id, new_data):
    """
    Modify a user row in the database.

    :param cursor: SQLite cursor object.
    :param user_id: User ID.
    :param new_data: Tuple containing new user data (name, surname, birth_day, accounts).
    :return: Success or failure message.
    """
    try:
        data = get_validated_user_data(new_data)
        cursor.execute("UPDATE User SET Name=?, Surname=?, Birth_day=?, Accounts=? WHERE id=?",
                       (data[0], data[1], data[2], data[3], user_id))
        return "User data modified successfully."
    except Exception as e:
        logger.error(f"Error modifying user data: {e}")
        return f"Error modifying user data: {e}"


@db_connection
def delete_user(cursor, user_id):
    """
    Delete a user row from the database.

    :param cursor: SQLite cursor object.
    :param user_id: User ID.
    :return: Success or failure message.
    """
    try:
        cursor.execute("DELETE FROM User WHERE id=?", (user_id,))
        return "User deleted successfully."
    except Exception as e:
        logger.error(f"Error deleting user: {e}")
        return f"Error deleting user: {e}"


@db_connection
def add_bank(cursor, *bank_data):
    """
    Add bank(s) to the database.

    :param cursor: SQLite cursor object.
    :param bank_data: Bank data, where each tuple contains (name,).
    :return: Success or failure message.
    """
    try:
        for data in bank_data:
            if isinstance(data, tuple):
                data = data[0]
            cursor.execute("INSERT INTO Bank (name) VALUES (?)", (data,))

        logger.info("Bank(s) added successfully.")
        return "Bank(s) added successfully."
    except Exception as e:
        logger.error(f"Error adding bank(s): {e}")
        return f"Error adding bank(s): {e}"


@db_connection
def add_banks_from_csv(cursor, file_path):
    """
    Add banks from a CSV file to the database.

    :param cursor: SQLite cursor object.
    :param file_path: Path to the CSV file.
    :return: Success or failure message.
    """
    try:
        with open(file_path, 'r') as file:
            csv_reader = csv.reader(file)
            next(csv_reader)  # Skip header row
            add_bank(csv_reader)

        return "Banks added successfully from CSV file."
    except Exception as e:
        logger.error(f"Error adding banks from CSV: {e}")
        return f"Error adding banks from CSV: {e}"


@db_connection
def modify_bank(cursor, bank_id, new_name):
    """
    Modify a bank row in the database.

    :param cursor: SQLite cursor object.
    :param bank_id: Bank ID.
    :param new_name: New bank name.
    :return: Success or failure message.
    """
    try:
        cursor.execute("UPDATE Bank SET name=? WHERE id=?", (new_name, bank_id))
        return "Bank data modified successfully."
    except Exception as e:
        logger.error(f"Error modifying bank data: {e}")
        return f"Error modifying bank data: {e}"


@db_connection
def add_account(cursor, *account_data):
    """
    Add account(s) to the database.

    :param cursor: SQLite cursor object.
    :param account_data: Account data, where each tuple contains
        (user_id, type, account_number, bank_id, currency, amount, status).
    :return: Success or failure message.
    """
    try:
        for data in account_data:
            data = (data[0],
                    validate_account_type(data[1]),
                    validate_account_number(data[2]),
                    data[3], data[4], data[5],
                    validate_account_status(data[6]))

            cursor.execute("INSERT INTO Account (User_id, Type, Account_Number, Bank_id, Currency, Amount, Status) "
                           "VALUES (?, ?, ?, ?, ?, ?, ?)", data)
        logger.info("Account(s) added successfully.")
        return "Account(s) added successfully."
    except Exception as e:
        logger.error(f"Error adding account(s): {e}")
        return f"Error adding account(s): {e}"


@db_connection
def add_accounts_from_csv(cursor, file_path):
    """
    Add accounts from a CSV file to the database.

    :param cursor: SQLite cursor object.
    :param file_path: Path to the CSV file.
    :return: Success or failure message.
    """
    try:
        with open(file_path, 'r') as file:
            csv_reader = csv.reader(file)
            next(csv_reader)  # Skip header row

            add_account(csv_reader)

        return "Accounts added successfully from CSV file."
    except Exception as e:
        logger.error(f"Error adding accounts from CSV: {e}")
        return f"Error adding accounts from CSV: {e}"


@db_connection
def delete_bank(cursor, bank_id):
    """
    Delete a bank row from the database.

    :param cursor: SQLite cursor object.
    :param bank_id: Bank ID.
    :return: Success or failure message.
    """
    try:
        cursor.execute("DELETE FROM Bank WHERE id=?", (bank_id,))
        return "Bank deleted successfully."
    except Exception as e:
        logger.error(f"Error deleting bank: {e}")
        return f"Error deleting bank: {e}"


@db_connection
def modify_account(cursor, account_id, new_data):
    """
    Modify an account row in the database.

    :param cursor: SQLite cursor object.
    :param account_id: Account ID.
    :param new_data: Tuple containing new account data (user_id, type, account_number, bank_id, currency, amount, status).
    :return: Success or failure message.
    """
    try:
        cursor.execute(
            "UPDATE Account SET User_id=?, Type=?, Account_Number=?, Bank_id=?, Currency=?, Amount=?, Status=? "
            "WHERE id=?", (*new_data, account_id))
        return "Account data modified successfully."
    except Exception as e:
        logger.error(f"Error modifying account data: {e}")
        return f"Error modifying account data: {e}"


@db_connection
def delete_account(cursor, account_id):
    """
    Delete an account row from the database.

    :param cursor: SQLite cursor object.
    :param account_id: Account ID.
    :return: Success or failure message.
    """
    try:
        cursor.execute("DELETE FROM Account WHERE id=?", (account_id,))
        return "Account deleted successfully."
    except Exception as e:
        logger.error(f"Error deleting account: {e}")
        return f"Error deleting account: {e}"


def get_exchange_rates(sender_currency, receiver_currency):
    """
    Get exchange rates from the API.

    :param sender_currency: Currency of the sender.
    :param receiver_currency: Currency of the receiver.
    :return: Exchange rate.
    """
    from freecurrencyapi.client import Client

    debug = False
    client = Client(TOKEN_API)
    try:
        exchange_rates = client.latest(sender_currency, [receiver_currency])
        if not exchange_rates:
            logger.error("Error: Unable to get exchange rates.")
            return "Error: Unable to get exchange rates."
        exchange_rate = exchange_rates['data'][receiver_currency]
        if not exchange_rate:
            logger.error(f"Error: Exchange rate not available for {receiver_currency}.")
            return f"Error: Exchange rate not available for {receiver_currency}."
        return exchange_rate
    except Exception as e:
        logger.error(f"Error getting exchange rates: {e}")
        return None


@db_connection
def money_transfer(cursor, sender_account_id, receiver_account_id, amount, transaction_datetime=None):
    """
    Perform money transfer from one account to another and add transaction record.

    :param cursor: SQLite cursor object.
    :param sender_account_id: ID of the sender's account.
    :param receiver_account_id: ID of the receiver's account.
    :param amount: Amount to transfer.
    :param transaction_datetime: Transaction datetime.
    :return: Success or failure message.
    """
    try:
        # Get sender's account details
        cursor.execute("SELECT Currency, Amount, Account_Number, Bank_id FROM Account WHERE id=?", (sender_account_id,))
        sender_currency, sender_balance, sender_account_number, sender_bank_id = cursor.fetchone()

        # Get receiver's account details
        cursor.execute("SELECT Currency, Account_Number, Bank_id FROM Account WHERE id=?", (receiver_account_id,))
        receiver_currency, receiver_account_number, receiver_bank_id = cursor.fetchone()
        # Validate account numbers
        sender_account_number = validate_account_number(sender_account_number)
        receiver_account_number = validate_account_number(receiver_account_number)

        # Check if sender's balance is sufficient
        if sender_balance < amount:
            return "Error: Insufficient balance for transfer."

        # Convert amount if currencies are different
        if sender_currency != receiver_currency:
            exchange_rate = get_exchange_rates(sender_currency, receiver_currency)
            converted_amount = amount / exchange_rate
        else:
            converted_amount = amount

        # Update sender's balance
        cursor.execute("UPDATE Account SET Amount=Amount-? WHERE id=?", (amount, sender_account_id))

        # Update receiver's balance
        cursor.execute("UPDATE Account SET Amount=Amount+? WHERE id=?", (converted_amount, receiver_account_id))

        cursor.execute('SELECT COUNT(*) FROM "Transaction"')

        # Fetch the result
        row_count = cursor.fetchone()[0]

        # Validate transaction datetime
        transaction_time = validate_transaction_datetime(transaction_datetime)

        cursor.execute('SELECT name FROM Bank WHERE id = ?', (sender_bank_id,))
        bank_sender_name = cursor.fetchone()[0]
        cursor.execute('SELECT name FROM Bank WHERE id = ?', (receiver_bank_id,))
        bank_receiver_name = cursor.fetchone()[0]

        # Add transaction record
        cursor.execute('INSERT INTO "Transaction" (id, Bank_sender_name, Account_sender_id, Bank_receiver_name, '
                       'Account_receiver_id, Sent_Currency, Sent_Amount, Datetime)'
                       "VALUES (?, ?, ?, ?, ?, ?, ?, ?)",
                       (row_count + 1, bank_sender_name, sender_account_id, bank_receiver_name, receiver_account_id,
                        sender_currency, amount, transaction_datetime))
        logger.info("Money transfer successful.")
        return "Money transfer successful."
    except Exception as e:
        logger.error(f"Error performing money transfer: {e}")
        return f"Error performing money transfer: {e}"
