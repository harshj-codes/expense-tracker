import os
from expenses import add_expense, view_expenses, show_summary, export_report, delete_expense
from config import CATEGORIES


def pick_category():
    print("\n📂 Select a category:")

    for i, category in enumerate(CATEGORIES, start=1):
        print(f"{i}. {category}")

    while True:
        try:
            choice = int(input("Choose a number: "))

            if choice < 1 or choice > len(CATEGORIES):
                print("⚠️ Invalid choice. Try again.")
                continue

            selected = CATEGORIES[choice - 1]

            # if user picks Other
            if selected == "Other":
                custom = input("Enter custom category name: ").strip()
                if custom:
                    return custom
                else:
                    print("⚠️ Category name cannot be empty. Try again.")
                    continue

            return selected

        except ValueError:
            print("⚠️ Please enter a number.")


def main():
    while True:
        os.system("cls" if os.name == "nt" else "clear")

        print("=" * 40)
        print("       💰 Expense Tracker")
        print("=" * 40)
        print("1. Add Expense")
        print("2. View All Expenses")
        print("3. Show Summary")
        print("4. Export Report")
        print("5. Delete Expense")
        print("6. Exit")
        print("=" * 40)

        try:
            choice = int(input("Choose an option: "))
        except ValueError:
            print("⚠️ Please enter a number.")
            input("\nPress Enter to continue...")
            continue

        if choice == 1:
            category = pick_category()

            while True:
                try:
                    amount = float(input("Enter amount (₹): "))
                    if amount <= 0:
                        print("⚠️ Amount must be greater than 0.")
                        continue
                    break
                except ValueError:
                    print("⚠️ Please enter a valid number.")

            description = input("Enter description: ").strip()
            if not description:
                description = "No description"

            add_expense(category, amount, description)
            input("\nPress Enter to continue...")

        elif choice == 2:
            view_expenses()
            input("\nPress Enter to continue...")

        elif choice == 3:
            show_summary()
            input("\nPress Enter to continue...")

        elif choice == 4:
            export_report()
            input("\nPress Enter to continue...")

        elif choice == 5:
            delete_expense()
            input("\nPress Enter to continue...")

        elif choice == 6:
            print("\n👋 Goodbye!")
            break

        else:
            print("⚠️ Invalid option. Choose between 1 and 6.")
            input("\nPress Enter to continue...")


if __name__ == "__main__":
    main()