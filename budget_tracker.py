import sqlite3
from datetime import datetime

DB_NAME = 'budget.db'

def initialize_db():
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute('''
        CREATE TABLE IF NOT EXISTS transactions (
            id INTEGER PRIMARY KEY,
            type TEXT CHECK(type IN ('expense', 'income')) NOT NULL,
            category TEXT NOT NULL,
            amount REAL NOT NULL,
            date TEXT NOT NULL
        )
    ''')
    conn.commit()
    conn.close()

def add_transaction(transaction_type, category, amount):
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    date = datetime.now().strftime("%Y-%m-%d")
    c.execute('''
        INSERT INTO transactions (type, category, amount, date)
        VALUES (?, ?, ?, ?)
    ''', (transaction_type, category, amount, date))
    conn.commit()
    conn.close()

def calculate_budget():
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute('SELECT SUM(amount) FROM transactions WHERE type = "income"')
    total_income = c.fetchone()[0] or 0.0
    c.execute('SELECT SUM(amount) FROM transactions WHERE type = "expense"')
    total_expenses = c.fetchone()[0] or 0.0
    conn.close()
    return total_income, total_expenses, total_income - total_expenses

def expense_analysis():
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute('SELECT category, SUM(amount) FROM transactions WHERE type = "expense" GROUP BY category')
    expenses_by_category = c.fetchall()
    conn.close()
    return expenses_by_category

def list_transactions():
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute('SELECT * FROM transactions')
    transactions = c.fetchall()
    conn.close()
    return transactions

def main():
    initialize_db()
    while True:
        print("\nPersonal Budget Tracker")
        print("1. Add Expense")
        print("2. Add Income")
        print("3. Calculate Budget")
        print("4. Expense Analysis")
        print("5. List Transactions")
        print("6. Exit")
        choice = input("Choose an option: ")
        if choice == '1':
            category = input("Category: ")
            amount = float(input("Amount: "))
            add_transaction('expense', category, amount)
        elif choice == '2':
            category = input("Category: ")
            amount = float(input("Amount: "))
            add_transaction('income', category, amount)
        elif choice == '3':
            total_income, total_expenses, remaining_budget = calculate_budget()
            print(f"Total Income: {total_income}")
            print(f"Total Expenses: {total_expenses}")
            print(f"Remaining Budget: {remaining_budget}")
        elif choice == '4':
            expenses_by_category = expense_analysis()
            for category, amount in expenses_by_category:
                print(f"Category: {category}, Amount Spent: {amount}")
        elif choice == '5':
            transactions = list_transactions()
            for transaction in transactions:
                print(f"ID: {transaction[0]}, Type: {transaction[1]}, Category: {transaction[2]}, Amount: {transaction[3]}, Date: {transaction[4]}")
        elif choice == '6':
            break
        else:
            print("Invalid choice. Please try again.")

if __name__ == '__main__':
    main()
