from account_reader import read_bank_accounts
from sessions import Session
from transaction_processor import TransactionProcessor

if __name__ == "__main__":
    file_path = "bank_accounts.txt"
    session = Session()
    accounts = read_bank_accounts(file_path)

    tp = TransactionProcessor(accounts)  # create once, points to same dict

    while True:
        code = input("Enter transaction code: ").strip().lower()

        if code == "login":
            accounts = session.handle_login(file_path)
            tp.accounts = accounts  # IMPORTANT: refresh tp to use newly loaded accounts

        elif code == "logout":
            if not session.session_active:
                print("You must login first.")
                continue
            session.handle_logout(accounts, "accounts_log.txt")
        elif code == "exit":
            break # end session
        else:
            if not session.session_active:
                print("You must login first.")
                continue

            if code == "deposit":
                tp.process_deposit(session.session_type, session.current_user)

            elif code == "transfer":
                tp.transfer( session.session_type, session.current_user)

            elif code == "withdraw":
                tp.process_withdrawal(session.session_type, session.current_user)

            elif code == "paybill":
                tp.paybill(session.session_type, session.current_user)

            else:
                print("Invalid transaction code")

