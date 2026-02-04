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
