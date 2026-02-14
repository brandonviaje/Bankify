from account_reader import read_bank_accounts
from sessions import Session
from transaction_processor import TransactionProcessor

if __name__ == "__main__":
    file_path = "bank_accounts.txt"
    session = Session()
    accounts = read_bank_accounts(file_path)

    tp = TransactionProcessor(accounts)

    while True:
        if not session.session_active:
            print("\nPlease login to continue.")

        print("\nAvailable transaction codes:")
        print("login, logout, deposit, transfer, withdrawal, paybill, create, delete, disable, changeplan, exit\n")
        code = input("Enter transaction code: ").strip().lower()

        if code == "login":
            accounts = session.handle_login(file_path)

            # handle_login returns a new dict, so refresh tp
            tp.accounts = accounts

        elif code == "logout":
            if not session.session_active:
                print("You must login first.")
                continue

            session.handle_logout(accounts, "accounts_log.txt")
            # if logout should end the session entirely, uncomment:
            # break

        elif code == "exit":
            break

        else:
            if not session.session_active:
                print("You must login first.")
                continue

            if code == "deposit":
                tp.process_deposit(session.session_type, session.current_user)

            elif code == "transfer":
                tp.transfer(session.session_type, session.current_user)

            elif code == "withdrawal":
                tp.process_withdrawal(session.session_type, session.current_user)

            elif code == "paybill":
                tp.paybill(session.session_type, session.current_user)

            # privileged (admin-only)
            elif code == "create":
                tp.process_create(session.session_type)

            elif code == "delete":
                tp.process_delete(session.session_type)

            elif code == "disable":
                tp.process_disable(session.session_type)

            elif code == "changeplan":
                tp.process_changeplan(session.session_type)

            else:
                print("Invalid transaction code")
