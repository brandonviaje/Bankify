
# add ur function implementation here: i.e. handle_deposit etc.

def transfer():
    
    accounts = read_bank_accounts(file_path)

    if session_type == "admin":
        account_holder_name = input("Enter account holder name: ")

    account_number_from = input("Enter account number to transfer from: ")
    account_number_to = input("Enter account number to transfer to: ")
    amount = input("Enter amount to transfer: ")

    if account_number_from not in accounts:
        print("Source account not found.")
        return
    if account_number_to not in accounts:
        print("Destination account not found.")
        return
    
    try:
        if amount <= 0:
            print("Amount must be positive.")
            return
        if accounts[account_number_from].balance < amount or accounts[account_number_to].balance < amount:
            print("Insufficient funds.")
            return
        accounts[account_number_from].balance -= amount
        accounts[account_number_to].balance += amount
        print(f"Transferred {amount} from {account_number_from} to {account_number_to}.")

    except ValueError:
        print("Invalid amount. Please enter a numeric value.")
        return

    


