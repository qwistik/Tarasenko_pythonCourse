import re
from datetime import datetime


def validate_user_full_name(user_full_name):
    """
    Validate the user_full_name field.

    :param user_full_name: Full name of the user.
    :return: Tuple containing the validated name and surname.
    """
    name, surname = re.split(r'\s+', user_full_name.strip())
    name = ''.join(filter(str.isalpha, name))
    surname = ''.join(filter(str.isalpha, surname))
    return name, surname


def validate_account_status(status):
    """
    Validate the account status field.

    :param status: Account status.
    :return: Validated account status.
    :raises ValueError: If the status is not one of "gold", "silver", or "platinum".
    """
    allowed_statuses = ["gold", "silver", "platinum"]
    if status.lower() not in allowed_statuses:
        raise ValueError(f"Not allowed value '{status}' for field 'Status'!")
    return status


def validate_account_type(type):
    """
    Validate the account type field.

    :param type: Account type.
    :return: Validated account type.
    :raises ValueError: If the type is not one of "debit" or "credit".
    """
    allowed_types = ["debit", "credit"]
    if type.lower() not in allowed_types:
        raise ValueError(f"Not allowed value '{type}' for field 'Type'!")
    return type


def validate_account_number(account_number):
    """
    Validate the account number field.

    :param account_number: Account number.
    :return: Validated account number.
    :raises ValueError: If the account number format is invalid.
    """
    # Replace special characters with dash
    account_number = re.sub(r'[#%_?&]', '-', account_number)

    # Check length
    if len(account_number) != 18:
        raise ValueError("Error: Account number should be a string of 18 characters!")

    # Check format
    if not account_number.startswith("ID--"):
        raise ValueError("Error: Account number has wrong format!")

    # Check pattern
    if not re.search(r'[A-Za-z]{1,3}-\d+', account_number):
        raise ValueError(f"Error: Account number({account_number}) has a broken ID pattern! ")

    return account_number


def validate_transaction_datetime(transaction_datetime):
    """
    Validate the transaction datetime.

    :param transaction_datetime: Transaction datetime.
    :return: Validated transaction datetime (current time if not passed).
    """
    if not transaction_datetime:
        return datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    return transaction_datetime
