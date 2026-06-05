import csv
import datetime
from config import CSV_FILE, CATEGORIES


#Reads all expenses from the CSV files and return them as a list of dictionaries.
#Converts amount of float for calculations. Skip corrupted rows silently.
#Returns an empty list if the file doesn't exist yet.
def load_expenses():
    expenses = []

    try:
        with open(CSV_FILE, "r", newline="") as file:
            reader = csv.DictReader(file)

            for row in reader:
                try:
                    row["amount"] = float(row["amount"])
                    expenses.append(row) 
                except (ValueError, KeyError): 
                    continue

    except FileNotFoundError:
        pass

    return expenses                


#Adds a new expense to the CSV file with today's date.
#Creates the file with headers if it doesn't exist yet.
def add_expense(category, amount, description):
    today = datetime.date.today().strftime("%d %B %Y")

    try:
        with open(CSV_FILE, "r") as f:
            file_exists = True
    except FileNotFoundError:
        file_exists = False

    with open(CSV_FILE, "a", newline="") as file:
        writer = csv.writer(file)

        if not file_exists:
            writer.writerow(["date", "category", "amount", "description"])

        writer.writerow([today, category, amount, description])

    print(f"\n✅ Expense added: {category} — ₹{amount} on {today}")


#Loads and prints all expenses as a numbered list.
#Shows date, category, amount, and description for each entry.
def view_expenses():
    expenses = load_expenses()

    if not expenses:
        print("\n⚠️ No expenses found.")
        return
    
    print("\n📋 All Expenses:")
    print("-" * 50)

    for i, expense in enumerate(expenses, start=1):
        print(f"{i}.[{expense['date']}] {expense['category']} - ₹{expense['amount']:.2f} | {expense['description']}")

    print("-" * 50) 


#Groups expenses by category and prints totals plus grand total. 
#Asks user to filter by current month or view all time.
def show_summary():
    expenses = load_expenses()

    if not expenses:
        print("\n⚠️ No expenses found.")
        return
    
    print("\n📊 Summary Options:")
    print("1. All time")
    print("2. This month")

    choice = input("Choose (1 or 2): ").strip()

    if choice == "2":
        current_month = datetime.date.today().month
        current_year = datetime.date.today().year
        expenses = [
            e for e in expenses
            if datetime.datetime.strptime(e["date"], "%d %B %Y").month == current_month
            and datetime.datetime.strptime(e["date"], "%d %B %Y").year == current_year
        ]

        if not expenses:
            print("\n⚠️ No expenses found in this month.")
            return
        
    summary = {}
    for expense in expenses:
        category = expense["category"]
        if category not in  summary:
            summary[category] = 0
        summary[category] += expense["amount"]

    print("\n📊 Expense Summary:")
    print("-" * 50)

    grand_total = 0
    for category, total in summary.items():
        print(f"{category}: ₹{total:.2f}") 
        grand_total += total

    print("-" * 50)
    print(f"Grand Total: ₹{grand_total:.2f}")


#Generates a summary report and saves it.
#Overwrites any previous report. 
def export_report():
    from config import REPORT_FILE
    expenses = load_expenses()

    if not expenses:
        print("\n⚠️ No expenses to export.")
        return
    
    print("\n📁 Export Options:")
    print("1. All time")
    print("2. This month")

    choice = input("Choose (1 or 2): ").strip()

    if choice == "2":
        current_month = datetime.date.today().month
        current_year = datetime.date.today().year
        expenses = [
            e for e in expenses
            if datetime.datetime.strptime(e["date"], "%d %B %Y").month == current_month
            and datetime.datetime.strptime(e["date"], "%d %B %Y").year == current_year
        ]

        if not expenses:
            print("\n⚠️ No expenses found for this month.")
            return
        
    summary = {}
    for expense in expenses:
        category = expense["category"]
        if category not in summary:
            summary[category] = 0
        summary[category] += expense["amount"]

    with open(REPORT_FILE, "w", encoding="utf-8") as file:
        file.write("Expense Report\n")
        file.write("=" * 50 + "\n")
                   
        grand_total = 0
        for category, total in summary.items():
            file.write(f"{category}: ₹{total:.2f}\n")
            grand_total += total

        file.write("=" * 50 + "\n")
        file.write(f"Grand Total: ₹{grand_total:.2f}\n")
        file.write(f"\nGenerated on: {datetime.date.today().strftime('%d %B %Y')}\n")

    print(f"\n✅ Report saved to {REPORT_FILE}")


#Delete a single expense by its number from the list.
#Rewrites the entire CSV file without the deleted row.
def delete_expense():
    expenses = load_expenses()

    if not expenses:
        print("\n⚠️ No expenses to delete.")
        return
    
    view_expenses()

    try:
        choice = int(input("\nEnter expense number to delete: "))

        if choice < 1 or choice > len(expenses):
            print("\n⚠️ Invalid number. Please try again.")
            return
        
        deleted = expenses.pop(choice - 1)
        
        with open(CSV_FILE, "w", newline="") as file:
            writer = csv.DictWriter(file, fieldnames=["date", "category", "amount", "description"])
            writer.writeheader()
            writer.writerows(expenses)

        print(f"\n✅ Deleted: {deleted['category']} — ₹{deleted['amount']:.2f} | {deleted['description']}")

    except ValueError:
        print("\n⚠️  Invalid input. Please enter a number.")