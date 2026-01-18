import sqlite3
import re


DB_NAME = "finances.db"
SQL_FILE = "schema.sql"
DATE_REGEX = re.compile(r"^\d{4}-\d{2}-\d{2}$")  # YYYY-MM-DD format


def init_db(db_name=DB_NAME):
    with sqlite3.connect(db_name) as con:
        with open(SQL_FILE, "r") as f:
            sql_script = f.read()
        con.executescript(sql_script)
        print(f"Database '{db_name}' initialized successfully.")


def add_transaction(transaction_name, transaction_type, amount, transaction_date):
    with sqlite3.connect(DB_NAME) as con:
        try:
            if transaction_date and DATE_REGEX.match(transaction_date):
                con.execute(
                    "INSERT INTO transactions (transaction_name, transaction_type, amount, transaction_date) VALUES (?, ?, ?, ?)",
                    (transaction_name, transaction_type, amount, transaction_date),
                )
            else:
                con.execute(
                    "INSERT INTO transactions (transaction_name, transaction_type, amount) VALUES (?, ?, ?)",
                    (transaction_name, transaction_type, amount),
                )
            con.commit()
            print("Transaction added successfully.")
        except sqlite3.IntegrityError as e:
            print("Please choose a valid transaction type: 'income' or 'expense'.")


def view_transactions(transaction_type=None):
    with sqlite3.connect(DB_NAME) as con:
        try:
            if transaction_type in ("income", "expense"):
                cur = con.execute(
                    "SELECT * FROM transactions WHERE transaction_type = ?",
                    (transaction_type,),
                )
            else:
                cur = con.execute("SELECT * FROM transactions")
            transactions = cur.fetchall()
            if transactions:
                for row in transactions:
                    print(row)
            else:
                print("No transactions found.")
        except sqlite3.OperationalError as e:
            print("There is no data available. Initializing database...")
            init_db()


def calc_balance(start_date=None, end_date=None):
    with sqlite3.connect(DB_NAME) as con:
        try:
            if start_date and end_date:
                cur = con.execute(
                    "SELECT SUM(CASE WHEN transaction_type = 'income' THEN amount ELSE 0 END), SUM(CASE WHEN transaction_type = 'expense' THEN amount ELSE 0 END) FROM transactions WHERE transaction_date BETWEEN ? AND ?",
                    (start_date, end_date),
                )
            else:
                cur = con.execute(
                    "SELECT SUM(CASE WHEN transaction_type = 'income' THEN amount ELSE 0 END), SUM(CASE WHEN transaction_type = 'expense' THEN amount ELSE 0 END) FROM transactions"
                )
            result = cur.fetchone()
            total_income = result[0]
            total_expense = result[1]
            balance = total_income - total_expense
            print("\n--------Balance--------")
            if start_date:
                print(f"From: {start_date} To: {end_date}")
            print(f"Total Income: {total_income or 0}")
            print(f"Total Expense: {total_expense or 0}")
            print(f"Balance: {balance}")
        except sqlite3.OperationalError as e:
            print("There is no data available. Initializing database...")
            init_db()


def delete_transaction(transaction_id):
    with sqlite3.connect(DB_NAME) as con:
        try:
            if transaction_id:
                con.execute(
                    "DELETE FROM transactions WHERE id = ?",
                    (transaction_id,),
                )
                con.commit()
                print(f" Transaction with ID '{transaction_id}' deleted successfully.")
            else:
                print("Please provide a valid transaction ID to delete.")
        except sqlite3.OperationalError as e:
            print("There is no data available. Initializing database...")
            init_db()


def delete_all_transactions():
    with sqlite3.connect(DB_NAME) as con:
        try:
            con.execute("DELETE FROM transactions")
            con.commit()
            print("All transactions deleted successfully.")
        except sqlite3.OperationalError as e:
            print("There is no data available. Initializing database...")
            init_db()


def main():
    while True:
        print("\n--------Finance Manager--------")
        print("1. Initialize Database")
        print("2. Add Transaction")
        print("3. View Transactions")
        print("4. Delete Transaction")
        print("5. Delete All Transactions")
        print("6. Calculate Balance")
        print("7. Exit")
        try:
            match int(input("Choose an option: ")):
                case 1:
                    init_db()
                case 2:
                    transaction_name = input("Enter transaction name: ")
                    transaction_type = input(
                        "Enter transaction type (income/expense): "
                    )
                    amount = float(input("Enter amount: "))
                    transaction_date = input(
                        "Enter transaction date (YYYY-MM-DD) or leave blank for today: "
                    )
                    add_transaction(
                        transaction_name, transaction_type, amount, transaction_date
                    )
                case 3:
                    transaction_type = input(
                        "Enter transaction type (income/expense) or enter any key to view all: "
                    )
                    view_transactions(transaction_type)
                case 4:
                    transaction_id = input("Enter transaction ID to delete: ")
                    delete_transaction(transaction_id)
                case 5:
                    delete_all_transactions()
                case 6:
                    start_date = input(
                        "Enter start date (YYYY-MM-DD) or press enter to skip: "
                    )
                    end_date = input(
                        "Enter end date (YYYY-MM-DD) or press enter to skip: "
                    )
                    calc_balance(
                        start_date if DATE_REGEX.match(start_date) else None,
                        end_date if DATE_REGEX.match(end_date) else None,
                    )
                    print(start_date, end_date)
                case 7:
                    print("\nExiting the program.")
                    break
                case _:
                    print("Please choose a valid option.")
        except ValueError:
            print("Invalid input. Please enter a number corresponding to the options.")
        except KeyboardInterrupt:
            print("\nExiting the program.")
            break


if __name__ == "__main__":
    main()
