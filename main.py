import random

import work_with_db
from functions_task5 import *

import subprocess
from faker import Faker
import csv


# Function to create a CSV file with user data
def create_users_csv(file_path, num_users=100):
    fake = Faker()
    with open(file_path, 'w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(['Full Name', 'Birth Day', 'Accounts'])
        for _ in range(num_users):
            full_name = fake.name()
            while len(full_name.split()) != 2:
                full_name = fake.name()
            birth_day = fake.date_of_birth(minimum_age=18, maximum_age=90).strftime('%Y-%m-%d')
            accounts = fake.random_int(min=1, max=5)  # Generate random number of accounts per user
            writer.writerow([full_name, birth_day, accounts])


def create_accounts_csv(file_path, num_accounts=500, num_users=100, num_banks=10):
    fake = Faker()

    # Define account types, currencies, and statuses
    account_types = ['debit', 'credit']
    currencies = ['USD', 'EUR', 'GBP']
    statuses = ['gold', 'silver', 'platinum']

    with open(file_path, 'w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(['User ID', 'Account Type', 'Account Number', 'Bank ID', 'Currency', 'Amount', 'Status'])

        for account_id in range(1, num_accounts + 1):
            user_id = random.randint(1, num_users)
            account_type = random.choice(account_types)
            account_number = f'ID--j{random.randint(1, 9)}-q-{random.randint(1, 9)}{random.randint(1, 9)}' \
                             f'{random.randint(1, 9)}{random.randint(1, 9)}{random.randint(1, 9)}' \
                             f'-u{random.randint(10, 99)}'
            bank_id = random.randint(1, num_banks)
            currency = random.choice(currencies)
            amount = round(random.uniform(-1000, 10000), 2)  # Random amount between 100 and 10000
            status = random.choice(statuses)

            writer.writerow([user_id, account_type, account_number, bank_id, currency, amount, status])


def create_banks_csv(file_path, num_banks=10):
    with open(file_path, 'w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(['name'])
        for i in range(num_banks):
            writer.writerow([f'bank {i}'])


def main():
    # Execute initial database setup script
    # setup_script_path = "001__initial_db_setup.py"
    # subprocess.run(["python", setup_script_path])
    # create_users_csv('users.csv')
    # create_banks_csv('banks.csv')
    # create_accounts_csv('accounts.csv')
    # # work_with_db.add_users_from_csv('users.csv')
    # work_with_db.add_banks_from_csv('banks.csv')
    # work_with_db.add_accounts_from_csv('accounts.csv')

    work_with_db.money_transfer(1, 2, 50, '2024-02-12')

    # Test all the functions
    print("Random User Discounts:", random_user_discount([1, 2, 3, 4, 5]))
    print("Users with Debts:", users_with_debts())
    print("Bank with Biggest Capital:", bank_with_biggest_capital())
    print("Bank Serving Oldest Client:", bank_serving_oldest_client())
    print("Bank with Highest Outbound Users:", bank_with_highest_outbound_users())
    print(delete_incomplete_users_and_accounts())
    print("User Transactions Last 3 Months:", user_transactions_last_3_months(1))


if __name__ == "__main__":
    main()
