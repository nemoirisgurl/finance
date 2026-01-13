import sqlite3

DB_NAME = "finances.db"
SQL_FILE = "schema.sql"


def init_db(db_name=DB_NAME):
    with sqlite3.connect(db_name) as con:
        with open(SQL_FILE, "r") as f:
            sql_script = f.read()
        con.executescript(sql_script)
        print(f"Database '{db_name}' initialized successfully.")


def add_transaction(transaction_name, transaction_type, amount):
    with sqlite3.connect(DB_NAME) as con:
        con.execute(
            "INSERT INTO transactions (transaction_name, transaction_type, amount) VALUES (?, ?, ?)",
            (transaction_name, transaction_type, amount),
        )
        con.commit()
        print("Transaction added successfully.")


def view_transactions():
    with sqlite3.connect(DB_NAME) as con:
        cur = con.execute("SELECT * FROM transactions")
        transactions = cur.fetchall()
        for transaction in transactions:
            print(transaction)


def main():
    while True:
        print("\n--------Finance Manager--------")
        print("1. Initialize Database")
        print("2. Add Transaction")
        print("3. View Transactions")
        print("4. Exit")
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
                    add_transaction(transaction_name, transaction_type, amount)
                case 3:
                    view_transactions()
                case default:
                    break
        except ValueError:
            print("Invalid input. Please enter a number corresponding to the options.")


if __name__ == "__main__":
    main()
