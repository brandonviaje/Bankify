import transactions

if __name__ == "__main__":
    file_path = "bank_accounts.txt"
    accounts = {}

    # start event loop
    while True:
        code = input("Enter transaction code: ").strip().lower()

        # handle login/logout
        if code == "login":
            accounts = transactions.handle_login(file_path)
        elif code == "logout":
            transactions.handle_logout(file_path)
            break  # end session
        else:
            # must be logged in first
            if not transactions.session_active:
                print("You must login first.")
                continue

            # add ur function here when u guys are done adding ur logic (make sure u write ur function in transactions.py)
            if code == "withdrawal":
                pass
            elif code == "deposit":
                pass
            elif code == "transfer":
                pass
            elif code == "paybill":
                pass
            elif code == "create":
                pass
            elif code == "delete":
                pass
            elif code == "disable":
                pass
            elif code == "changeplan":
                pass
            else:
                print("Invalid transaction code")
