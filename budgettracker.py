import json
import matplotlib.pyplot as plt
from datetime import datetime

BUDGET_FILE = "budget.json"

def format_inr(amount):
    return f"₹{amount:,.2f}"

def load_budget():
    try:
        with open(BUDGET_FILE, "r") as f:
            return json.load(f)
    except FileNotFoundError:
        return {"income": 0, "expenses": []}

def save_budget(budget):
    with open(BUDGET_FILE, "w") as f:
        json.dump(budget, f, indent=2)

def display_budget(budget):
    print("\n===== BUDGET TRACKER =====")
    print(f"Income: {format_inr(budget['income'])}")
    if not budget['expenses']:
        print("No expenses recorded.")
    else:
        print("Expenses:")
        for expense in budget['expenses']:
            print(f"- {expense['category']}: {format_inr(expense['amount'])} ({expense['date']})")
    balance = budget['income'] - sum(expense['amount'] for expense in budget['expenses'])
    print(f"Remaining Budget: {format_inr(balance)}\n")

def add_income(budget):
    try:
        amount = float(input("Enter income amount: ₹"))
        budget['income'] += amount
        print("Income added successfully.")
    except ValueError:
        print("Invalid input. Please enter a valid number.")

def add_expense(budget):
    category = input("Enter expense category: ")
    name = input("Enter expense name: ")
    try:
        amount = float(input("Enter expense amount: ₹"))
        date_str = input("Enter expense date (DD/MM/YYYY): ")
        date = datetime.strptime(date_str, "%d/%m/%Y").strftime("%d/%m/%Y")
        budget['expenses'].append({"category": category, "name": name, "amount": amount, "date": date})
        print("Expense added successfully.")
    except ValueError:
        print("Invalid input. Please enter a valid number.")

def analyze_expenses(budget):
    if not budget['expenses']:
        print("No expenses recorded.")
        return
    categories = set(expense['category'] for expense in budget['expenses'])
    print("Expense Analysis:")
    for category in categories:
        category_total = sum(expense['amount'] for expense in budget['expenses'] if expense['category'] == category)
        print(f"- {category}: {format_inr(category_total)}")

def plot_spending_trends(budget):
    if not budget['expenses']:
        print("No expenses recorded for spending trends.")
        return
    categories = set(expense['category'] for expense in budget['expenses'])
    dates = sorted(set(expense['date'] for expense in budget['expenses']))
    for category in categories:
        amounts = [sum(expense['amount'] for expense in budget['expenses'] if expense['category'] == category and expense['date'] == date) for date in dates]
        plt.plot(dates, amounts, label=category)
    plt.xlabel('Date')
    plt.ylabel('Total Amount Spent (INR)')
    plt.title('Spending Trends Over Time')
    plt.legend()
    plt.show()

def main():
    budget = load_budget()
    while True:
        print("1. Add Income")
        print("2. Add Expense")
        print("3. View Budget")
        print("4. Expense Analysis")
        print("5. Spending Trends")
        print("6. Exit")
        choice = input("Enter your choice (1-6): ")
        if choice == "1":
            add_income(budget)
        elif choice == "2":
            add_expense(budget)
        elif choice == "3":
            display_budget(budget)
        elif choice == "4":
            analyze_expenses(budget)
        elif choice == "5":
            plot_spending_trends(budget)
        elif choice == "6":
            save_budget(budget)
            print("Exiting Budget Tracker. Goodbye!")
            break
        else:
            print("Invalid choice. Please enter a number between 1 and 6.")

if __name__ == "__main__":
    main()
