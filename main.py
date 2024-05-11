import work_with_db

import subprocess


def main():
    # Execute initial database setup script
    setup_script_path = "001__initial_db_setup.py"
    subprocess.run(["python", setup_script_path])
    # Example usage
    # Add banks
    banks_data = [("Bank A",), ("Bank B",), ("Bank C",)]
    work_with_db.add_bank(*banks_data)

    # Add users
    users_data = [("John Doe", "1990-01-01", "1"),
                  ("Alice Smith", "1985-05-15", "2"),
                  ("Bob Johnson", "1978-11-30", "3")]
    work_with_db.add_user(*users_data)

    # Add accounts
    accounts_data = [(1, "credit", "ID--j3-q-432547-u9", 1, "USD", 1500.0, "gold"),
                     (2, "debit", "ID--jh-q-432547-u4", 2, "EUR", 1000.0, "silver"),
                     (3, "credit", "ID--j3-q-43254-u10", 3, "GBP", 2000.0, "platinum")]
    work_with_db.add_account(*accounts_data)

    # Modify user
    work_with_db.modify_user(1, ("Jonathan Doe", "1990-01-01", "3"))

    # Delete bank
    work_with_db.delete_bank(3)

    # Modify account
    work_with_db.modify_account(1, (1, "credit", "ID--j3-q-43254-u11", 1, "USD", 2000.0, "active"))

    # Money transfer
    work_with_db.money_transfer(1, 2, 500.0)

    # Delete user
    work_with_db.delete_user(3)
    work_with_db.add_user(4, "Alex Von", "2000-10-06", "1")
    work_with_db.add_bank("Bank D")


if __name__ == "__main__":
    main()
