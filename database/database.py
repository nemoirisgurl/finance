import sqlite3
import tabulate
import matplotlib.pyplot as plt
import pandas as pd


DB_PATH = "database\\finances.db"
SQL_PATH = "schema\\schema.sql"


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
            plt.figure(figsize=(10, 5))
            plt.plot(df.index, df["net_balance"], marker="o", linestyle="--")
            plt.title("Net Balance History")
            plt.xlabel("Date")
            plt.ylabel("Net Balance")
            plt.axhline(0, color="red", linestyle="--")
            plt.grid()
            plt.show(block=True)
            plt.close()
        except sqlite3.OperationalError as e:
            print("There is no data available. Initializing database...")
            init_db()


def delete_transaction(transaction_id):
    with sqlite3.connect(DB_PATH) as con:
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
    with sqlite3.connect(DB_PATH) as con:
        try:
            con.execute("DELETE FROM transactions")
            con.commit()
            print("All transactions deleted successfully.")
        except sqlite3.OperationalError as e:
            print("There is no data available. Initializing database...")
            init_db()


if __name__ == "__main__":
    init_db()
