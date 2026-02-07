from account_reader import read_bank_accounts

session_active = False   # session state
session_type = None      # "standard" or "admin"
current_user = None      # account holder name 

def handle_login(file_path):
    global session_active, session_type, current_user

    # check if an account is already logged in
    if session_active:
        print("Already logged in.")
        return

    # get session type
    while True:
        session_type = input("Enter session type (standard/admin): ").strip().lower()
        if session_type in {"standard", "admin"}:
            break

        print("Invalid session type. Retry")

    # handle session types
    if session_type == "standard":
        current_user = input("Enter account holder name: ").strip()
    else:
        current_user = "ADMIN"

    accounts = read_bank_accounts(file_path)  # read bank acounts file
    session_active = True
    print(f"Logged in as {current_user} ({session_type})")
    return accounts

def handle_logout(accounts):
    pass

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

    


