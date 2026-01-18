 # Project 1: Expense Tracker (Text-based)

expenses = []

def add_expense():
    name = input("Enter item name: ")
    amount = float(input("Enter amount: "))
    expenses.append({'item': name, 'amount': amount})

def view_expenses():
    for e in expenses:
        print(f"{e['item']} - ₹{e['amount']}")

def total_expenses():
    total = sum(e['amount'] for e in expenses)
    print("Total Expenses: ₹", total)

while True:
    print("\n1.Add\n2. View\n3. Total\n4. Exit")
    choice = input("Enter choice: ")
    if choice == '1':
        add_expense()
    elif choice == '2':
        view_expenses()
    elif choice == '3':
        total_expenses()
    elif choice == '4':
        break
    else:
        print("Invalid choice")
