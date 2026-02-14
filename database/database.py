import sqlite3
import tabulate
import matplotlib.pyplot as plt
import pandas as pd
from datetime import date
import os

CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
ROOT_DIR = os.path.dirname(CURRENT_DIR)
DB_PATH = os.path.join(CURRENT_DIR, "finances.db")
SQL_PATH = os.path.join(ROOT_DIR, "schema", "schema.sql")


def init_db(DB_PATH=DB_PATH):
    with sqlite3.connect(DB_PATH) as con:
        with open(SQL_PATH, "r") as f:
            sql_script = f.read()
        con.executescript(sql_script)
        print(f"Database '{DB_PATH}' initialized successfully.")


def add_transaction(transaction_name, transaction_type, amount, transaction_date):
    with sqlite3.connect(DB_PATH) as con:
        try:
            if transaction_date:
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


def update_transactions(
    transaction_id, transaction_name, transaction_type, amount, transaction_date
):
    with sqlite3.connect(DB_PATH) as con:
        try:
            con.execute(
                "UPDATE transactions SET transaction_name = ?, transaction_type = ?, amount = ?, transaction_date = ? WHERE id = ?",
                (
                    transaction_name,
                    transaction_type,
                    amount,
                    (
                        transaction_date
                        if transaction_date != ""
                        else date.today().strftime("%Y-%m-%d")
                    ),
                    transaction_id,
                ),
            )
            con.commit()
            print("Transaction updated successfully.")
        except sqlite3.IntegrityError as e:
            print("Please choose a valid transaction type: 'income' or 'expense'.")


def view_transactions(transaction_type=None):
    with sqlite3.connect(DB_PATH) as con:
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
                headers = [
                    "ID",
                    "Transaction Name",
                    "Transaction Type",
                    "Amount",
                    "Transaction Date",
                ]
                print(tabulate.tabulate(transactions, headers, tablefmt="grid"))
            else:
                print("No transactions found.")
        except sqlite3.OperationalError as e:
            print("There is no data available. Initializing database...")
            init_db()


def view_max_min_transactions():
    with sqlite3.connect(DB_PATH) as con:
        try:
            income_cur = con.execute(
                "SELECT MAX(amount), MIN(amount) FROM transactions WHERE transaction_type = 'income'"
            )
            income_result = income_cur.fetchone()
            expense_cur = con.execute(
                "SELECT MAX(amount), MIN(amount) FROM transactions WHERE transaction_type = 'expense'"
            )
            expense_result = expense_cur.fetchone()
            print("Income:")
            print(f"  Max: {income_result[0]}, Min: {income_result[1]}")
            print("Expense:")
            print(f"  Max: {expense_result[0]}, Min: {expense_result[1]}")
        except sqlite3.OperationalError as e:
            print("There is no data available. Initializing database...")
            init_db()


def calc_balance(start_date=None, end_date=None):
    with sqlite3.connect(DB_PATH) as con:
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
            total_income = result[0] or 0.0
            total_expense = result[1] or 0.0
            balance = total_income - total_expense
            print("\n--------Balance--------")
            if start_date:
                print(f"From: {start_date} To: {end_date}")
            print(f"Total Income: {total_income}")
            print(f"Total Expense: {total_expense}")
            print(f"Balance: {balance}")
        except sqlite3.OperationalError as e:
            print("There is no data available. Initializing database...")
            init_db()


def plot_balance(start_date=None, end_date=None):
    with sqlite3.connect(DB_PATH) as con:
        try:
            if start_date and end_date:
                cur = con.execute(
                    "SELECT transaction_date, SUM(CASE WHEN transaction_type = 'income' THEN amount ELSE -amount END) FROM transactions WHERE transaction_date BETWEEN ? AND ? GROUP BY transaction_date ORDER BY transaction_date",
                    (start_date, end_date),
                )
            else:
                cur = con.execute(
                    "SELECT transaction_date, SUM(CASE WHEN transaction_type = 'income' THEN amount ELSE -amount END) FROM transactions GROUP BY transaction_date ORDER BY transaction_date"
                )
            data = cur.fetchall()
            print(data)
            if not data:
                print("No data available to plot.")
                return
            df = pd.DataFrame(data, columns=["transaction_date", "balance"])
            df["transaction_date"] = pd.to_datetime(df["transaction_date"])
            df.set_index("transaction_date", inplace=True)
            df["net_balance"] = df["balance"].cumsum()
            f, ax = plt.subplots(figsize=(10, 5))
            ax.plot(df.index, df["net_balance"], marker="o", linestyle="--")
            ax.set_title("Net Balance History")
            ax.set_xlabel("Date")
            ax.set_ylabel("Net Balance")
            ax.axhline(0, color="red", linestyle="--")
            ax.grid()
            return f
        except sqlite3.OperationalError as e:
            print("There is no data available. Initializing database...")
            init_db()


def plot_interest(data):
    years = [entry["year"] for entry in data]
    principals = [entry["principal"] for entry in data]
    print(tabulate.tabulate(data, headers="keys", tablefmt="grid"))

    plt.figure(figsize=(10, 5))
    plt.plot(years, principals, marker="o", linestyle="--")
    plt.title("Investment Growth Over Time")
    plt.xlabel("Years")
    plt.ylabel("Total Amount")
    plt.grid()
    plt.show(block=True)
    plt.close()


def delete_transaction(transaction_id):
    with sqlite3.connect(DB_PATH) as con:
        try:
            cur = con.execute(
                "DELETE FROM transactions WHERE id = ?",
                (transaction_id,),
            )
            con.commit()
            if cur.rowcount > 0:
                print(f" Transaction with ID '{transaction_id}' deleted successfully.")
            else:
                print("Please provide a valid transaction ID to delete.")
        except sqlite3.OperationalError as e:
            print("There is no data available. Initializing database...")
            init_db()


def delete_all_transactions(choice="y"):
    with sqlite3.connect(DB_PATH) as con:
        try:
            signal = (
                choice
                or input(
                    "Are you sure you actually want to delete all transactions? (y/n): "
                ).lower()
            )
            if signal != "y":
                print("Operation cancelled.")
                return
            con.execute("DELETE FROM transactions")
            con.commit()
            print("All transactions deleted successfully.")
        except sqlite3.OperationalError as e:
            print("There is no data available. Initializing database...")
            init_db()


if __name__ == "__main__":
    init_db()
