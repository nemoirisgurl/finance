import database.database as db
import helpers.helpers as hlp


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
                    db.init_db()
                case 2:
                    transaction_name = input("Enter transaction name: ")
                    transaction_type = input(
                        "Enter transaction type (income/expense): "
                    )
                    amount = float(input("Enter amount: "))
                    transaction_date = input(
                        "Enter transaction date (YYYY-MM-DD) or leave blank for today: "
                    )
                    if (
                        not hlp.is_valid_date(transaction_date)
                        and transaction_date != ""
                    ):
                        print("Invalid date.")
                        continue
                    db.add_transaction(
                        transaction_name,
                        transaction_type,
                        amount,
                        (transaction_date),
                    )
                case 3:
                    transaction_type = input(
                        "Enter transaction type (income/expense) or enter any key to view all: "
                    )
                    db.view_transactions(transaction_type)
                case 4:
                    transaction_id = input("Enter transaction ID to delete: ")
                    db.delete_transaction(transaction_id)
                case 5:
                    db.delete_all_transactions()
                case 6:
                    start_date = input(
                        "Enter start date (YYYY-MM-DD) or press enter to skip: "
                    )
                    end_date = input(
                        "Enter end date (YYYY-MM-DD) or press enter to skip: "
                    )
                    if (not hlp.is_valid_date(start_date) and start_date != "") or (
                        not hlp.is_valid_date(end_date) and end_date != ""
                    ):
                        print("Invalid date.")
                        continue
                    db.calc_balance(
                        start_date if hlp.is_valid_date(start_date) else None,
                        end_date if hlp.is_valid_date(end_date) else None,
                    )
                    # print(start_date, end_date)
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
