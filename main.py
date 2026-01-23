import database.database as db
import helpers.helpers as hlp


def main():
    while True:
        print("\n--------Finance Manager--------")
        print("1. Initialize Database")
        print("2. Add Transaction")
        print("3. Update Transactions")
        print("4. View Transactions")
        print("5. Delete Transaction")
        print("6. Delete All Transactions")
        print("7. Calculate Balance")
        print("8. Plot Balance")
        print("9. Exit")
        print("11. Calculate Interest")
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
                    transaction_id = int(input("Enter transaction ID to update: "))
                    transaction_name = input("Enter new transaction name: ")
                    transaction_type = input(
                        "Enter new transaction type (income/expense): "
                    )
                    amount = float(input("Enter new amount: "))
                    transaction_date = input(
                        "Enter new transaction date (YYYY-MM-DD) or leave blank for today: "
                    )
                    if (
                        not hlp.is_valid_date(transaction_date)
                        and transaction_date != ""
                    ):
                        print("Invalid date.")
                        continue
                    db.update_transactions(
                        transaction_id,
                        transaction_name,
                        transaction_type,
                        amount,
                        (transaction_date),
                    )
                case 4:
                    transaction_type = input(
                        "Enter transaction type (income/expense) or enter any key to view all: "
                    )
                    db.view_transactions(transaction_type)
                case 5:
                    transaction_id = int(input("Enter transaction ID to delete: "))
                    db.delete_transaction(transaction_id)
                case 6:
                    db.delete_all_transactions()
                case 7:
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
                case 8:
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
                    db.plot_balance(
                        start_date if hlp.is_valid_date(start_date) else None,
                        end_date if hlp.is_valid_date(end_date) else None,
                    )
                case 9:
                    print("\nExiting the program.")
                    break
                case 11:
                    principal = float(input("Enter the principal amount: "))
                    rate = float(input("Enter the annual interest rate (in %): "))
                    years = int(input("Enter the number of years: "))
                    monthly_contribution = float(
                        input("Enter the monthly contribution amount (default is 0): ")
                        or 0
                    )
                    compounds_per_year = int(
                        input(
                            "Enter the number of times interest is compounded per year (default is 12): "
                        )
                        or 1
                    )
                    interest_data = hlp.calc_interest(
                        principal,
                        rate,
                        years,
                        monthly_contribution,
                        compounds_per_year,
                    )
                    db.plot_interest(interest_data)
                case _:
                    print("Please choose a valid option.")
        except ValueError:
            print("Invalid input. Please enter a number corresponding to the options.")
        except KeyboardInterrupt:
            print("\nReturning to main menu.")
            continue


if __name__ == "__main__":
    main()
