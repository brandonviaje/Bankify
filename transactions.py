from account_reader import read_bank_accounts

def transfer(accounts, session_type, current_user):
    
    if session_type == "admin":
        account_holder_name = input("Enter account holder name: ")

        if account_holder_name not in accounts:
            print("Account holder not found.")
            return

    account_number_from = input("Enter account number to transfer from: ")

    account_number_to = input("Enter account number to transfer to: ")
    try:
        amount = float(input("Enter amount to transfer: "))
    except ValueError:
        print("Invalid amount. Please enter a numeric value.")
        return

    if session_type != "admin" and account_number_from != current_user.account_number:
        print("You can only transfer from your own account.")
        return

    if account_number_to not in accounts:
        print("Destination account not found.")
        return
    
    try:
        if amount <= 0 or amount < 1000:
            print("Amount must be positive.")
            return
        if accounts[account_number_from].balance - amount < 0 or accounts[account_number_to].balance + amount < 0:
            print("Account balance cannot go below $0.")
            return
        
        accounts[account_number_from].balance -= amount
        accounts[account_number_to].balance += amount
        print(f"Transferred {amount} from {account_number_from} to {account_number_to}.")
        with open("transactions_file_log.txt", "a") as f:
            f.write(f"{account_number_from} to {account_number_to} with ${amount}\n")



    except ValueError:
        print("Invalid amount. Please enter a numeric value.")
        return

    


