# -----------------------------------------
# Simple Banking System - Mini Project
# -----------------------------------------

# Predefined user accounts (you can extend this)
accounts = {
    "Tom": {"pin": "1234", "balance": 5000},
    "john": {"pin": "4321", "balance": 2500},
    "lijo": {"pin": "9999", "balance": 10000}
}

def login():
    username = input("Enter username: ")
    pin = input("Enter PIN: ")
    if username in accounts and accounts[username]["pin"] == pin:
        print("Login successful!")
        return username
    else:
        print("Invalid username or PIN. Try again.")
        return None

def deposit(username):
    amount = float(input("Enter amount to deposit: "))
    if amount <= 0:
        print("Deposit amount must be greater than zero.")
        return

    accounts[username]["balance"] += amount
    print(f"Deposit successful! Current balance: £{accounts[username]['balance']}")
def withdraw(username):
    amount = float(input("Enter amount to withdraw: "))
    if amount <= 0:
        print("Withdrawal amount must be greater than zero.")
        return

    if amount > accounts[username]["balance"]:
        print("Insufficient balance!")
        return
    accounts[username]["balance"] -= amount
    print(f"Withdrawal successful! Remaining balance: £{accounts[username]['balance']}")

def main():

    user = None
    while user is None:
        user = login()

    while True:
        print("1. Deposit Money")
        print("2. Withdraw Money")
        print("3. Check Balance")
        print("4. Logout")
        choice = input("Enter your choice: ")

        if choice == "1":
            deposit(user)
        elif choice == "2":
            withdraw(user)
        elif choice == "3":
            print(f"Your current balance: £{accounts[user]['balance']}")
        elif choice == "4":
            print("Logged out successfully. Goodbye!")
            break
        else:
            print("Invalid choice. Please try again.")

main()
