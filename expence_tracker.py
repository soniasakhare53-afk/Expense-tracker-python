import os
from datetime import datetime

FILE_NAME = "expenses.txt"
LOG_FILE = "error_log.txt"


def validate_date(date_str):
    try:
        datetime.strptime(date_str, "%Y-%m-%d")
        return True
    except ValueError:
        return False


def log_error(message):
    with open(LOG_FILE, "a") as file:
        file.write(f"{datetime.now()} - {message}\n")


#FILE HANDLING
def load_expenses():
    expenses = []
    if os.path.exists(FILE_NAME):
        with open(FILE_NAME, "r") as file:
            for line in file:
                try:
                    date, amount, category, note = line.strip().split(",")
                    expenses.append({
                        "date": date,
                        "amount": float(amount),
                        "category": category,
                        "note": note
                    })
                except ValueError:
                    log_error(f"Corrupted entry skipped: {line}")
    return expenses


def save_expenses(expenses):
    with open(FILE_NAME, "w") as file:
        for exp in expenses:
            file.write(f"{exp['date']},{exp['amount']},{exp['category']},{exp['note']}\n")



def add_expense(expenses):
    date = input("Enter date (YYYY-MM-DD) or press Enter for today: ").strip()
    if date == "":
        date = datetime.now().strftime("%Y-%m-%d")
    elif not validate_date(date):
        print("Invalid date format. Use YYYY-MM-DD.")
        return

    try:
        amount = float(input("Enter amount: "))
        category = input("Enter category (Food/Travel/etc): ").capitalize()
        note = input("Enter note: ")

        expenses.append({
            "date": date,
            "amount": amount,
            "category": category,
            "note": note
        })

        save_expenses(expenses)
        print("Expense added successfully!")

    except ValueError:
        print("Amount must be a number.")


def view_expenses(expenses):
    if not expenses:
        print("No expenses found.")
        return

    print("\n--- All Expenses ---")
    for i, exp in enumerate(expenses, start=1):
        print(f"{i}. {exp['date']} | {exp['category']} | ₹{exp['amount']} | {exp['note']}")


def category_summary(expenses):
    summary = {}
    for exp in expenses:
        summary[exp["category"]] = summary.get(exp["category"], 0) + exp["amount"]

    print("\n--- Category-wise Summary ---")
    for cat, amt in summary.items():
        print(f"{cat}: ₹{amt}")


def monthly_total(expenses):
    month = input("Enter month (MM): ")
    year = input("Enter year (YYYY): ")

    total = 0
    for exp in expenses:
        try:
            exp_year, exp_month, _ = exp["date"].split("-")
            if exp_month == month and exp_year == year:
                total += exp["amount"]
        except ValueError:
            log_error(f"Invalid date format found: {exp['date']}")

    print(f"Total expense for {month}-{year}: ₹{total}")


def budget_check(expenses):
    try:
        budget = float(input("Enter your monthly budget: "))
        month = input("Enter month (MM): ")
        year = input("Enter year (YYYY): ")

        total = 0
        for exp in expenses:
            try:
                exp_year, exp_month, _ = exp["date"].split("-")
                if exp_month == month and exp_year == year:
                    total += exp["amount"]
            except ValueError:
                continue

        print(f"Total spent: ₹{total}")
        if total > budget:
            print("Budget exceeded!")
        else:
            print("You are within budget.")

    except ValueError:
        print("Budget must be a number.")


def highest_spending_category(expenses):
    if not expenses:
        print("No data available.")
        return

    summary = {}
    for exp in expenses:
        summary[exp["category"]] = summary.get(exp["category"], 0) + exp["amount"]

    highest = max(summary, key=summary.get)
    print(f"Highest spending category: {highest} (₹{summary[highest]})")


def saving_suggestions(expenses):
    if not expenses:
        print("No data available.")
        return

    summary = {}
    for exp in expenses:
        summary[exp["category"]] = summary.get(exp["category"], 0) + exp["amount"]

    highest = max(summary, key=summary.get)
    print(f"\n Saving Tip: You spend most on {highest}. Try reducing expenses in this category.")


# UPDATE & DELETE
def update_expense(expenses):
    view_expenses(expenses)

    try:
        index = int(input("Enter expense number to update: ")) - 1
        if 0 <= index < len(expenses):
            exp = expenses[index]

            new_amount = input(f"New amount ({exp['amount']}): ")
            new_category = input(f"New category ({exp['category']}): ")
            new_note = input(f"New note ({exp['note']}): ")

            if new_amount:
                exp["amount"] = float(new_amount)
            if new_category:
                exp["category"] = new_category.capitalize()
            if new_note:
                exp["note"] = new_note

            save_expenses(expenses)
            print("Expense updated successfully!")
        else:
            print("Invalid expense number.")
    except ValueError:
        print("Invalid input.")


def delete_expense(expenses):
    view_expenses(expenses)

    try:
        index = int(input("Enter expense number to delete: ")) - 1
        if 0 <= index < len(expenses):
            deleted = expenses.pop(index)
            save_expenses(expenses)
            print(f"Deleted expense: {deleted}")
        else:
            print("Invalid expense number.")
    except ValueError:
        print("Invalid input.")


# MAIN MENU
def main():
    expenses = load_expenses()

    while True:
        print("\n====== Expense Tracker ======")
        print("1. Add Expense")
        print("2. View Expenses")
        print("3. Category Summary")
        print("4. Monthly Total")
        print("5. Budget Check")
        print("6. Highest Spending Category")
        print("7. Saving Suggestions")
        print("8. Update Expense")
        print("9. Delete Expense")
        print("10. Exit")

        choice = input("Choose an option: ")

        if choice == "1":
            add_expense(expenses)
        elif choice == "2":
            view_expenses(expenses)
        elif choice == "3":
            category_summary(expenses)
        elif choice == "4":
            monthly_total(expenses)
        elif choice == "5":
            budget_check(expenses)
        elif choice == "6":
            highest_spending_category(expenses)
        elif choice == "7":
            saving_suggestions(expenses)
        elif choice == "8":
            update_expense(expenses)
        elif choice == "9":
            delete_expense(expenses)
        elif choice == "10":
            print("Exiting Expense Tracker. Bye!")
            break
        else:
            print("Invalid choice. Try again.")


if __name__ == "__main__":
    main()