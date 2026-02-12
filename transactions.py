from account_reader import read_bank_accounts
from accounts import BankAccount

def transfer(accounts, session_type, current_user):
    
    if session_type == "admin":
        account_holder_name = input("Enter account holder name: ")

        if account_holder_name not in accounts:
            print("Account holder not found.")
            return

    account_number_from = input("Enter account number to transfer from: ")

    if account_number_from not in accounts:
        print("Source account not found.")
        return


    account_from = accounts[account_number_from]

    account_number_to = input("Enter account number to transfer to: ")

    if account_number_to not in accounts:
        print("Destination account not found.")
        return


    account_to = accounts[account_number_to]

    try:
        amount = float(input("Enter amount to transfer: "))
    except ValueError:
        print("Invalid amount. Please enter a numeric value.")
        return
    


    if session_type != "admin" and account_from.name != current_user:
        print("You can only transfer from your own account.")
        return
    
    try:
        if amount <= 0 or amount >= 1000:
            print("Amount must be positive and less than or equal to $1000.")
            return
        if account_from.balance - amount < 0 or account_to.balance + amount < 0:
            print("Account balance cannot go below $0.")
            return
        
        account_from.balance -= amount
        account_to.balance += amount
        print(f"Transferred {amount} from {account_number_from} to {account_number_to}.")
        with open("transactions_file_log.txt", "a") as f:
            f.write(f"{account_number_from} to {account_number_to} with ${amount}\n")



    except ValueError:
        print("Invalid amount. Please enter a numeric value.")
        return

    


