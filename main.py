import sys
from account_reader import read_bank_accounts
from sessions import Session
from transaction_processor import TransactionProcessor
from transaction_processor import write_txn_line 
from transaction_processor import custom_input

"""
Bank ATM Front-End Main Program

This serves as the main entry point for the Bank system.
It initializes the bank account data, manages user sessions, and
routes user-entered transaction codes to the appropriate handlers.
"""

def main():
    if len(sys.argv) != 3:
        print("Usage: python main.py <current_accounts_file> <transaction_output_file>")
        sys.exit(1)

    accounts_file = sys.argv[1]
    transaction_file = sys.argv[2]

    # init session and load accounts
    session = Session()
    accounts = read_bank_accounts(accounts_file)
    tp = TransactionProcessor(accounts, transaction_file)

    # ensure transaction file exists
    with open(transaction_file, "a"):
        pass
    
    # main bank loop
    while True:
        if not session.session_active:
            print("\nPlease login to continue.")

        print("\nAvailable transaction codes:")
        print("login, logout, deposit, transfer, withdrawal, paybill, create, delete, disable, changeplan, exit\n")

        try:
            code = custom_input("Enter transaction code: ").strip().lower()
        except EOFError:
            print("\nExiting program.")
            break

        # LOGIN
        if code == "login":
            new_accounts = session.handle_login(accounts_file)
            if new_accounts is not None:  # Login succeeded
                tp.accounts = new_accounts
                tp.standard_withdraw_total = 0.0
                tp.standard_transfer_total = 0.0
                tp.standard_paybill_total = 0.0

        # LOGOUT
        elif code == "logout":
            if not session.session_active:
                print("You must login first.")
                continue

            session.handle_logout(accounts, transaction_file)
            break  # End program after logout

        # EXIT
        elif code == "exit":
            # if logged in, logout first
            if session.session_active:
                session.handle_logout(accounts, transaction_file)
            break

        # BANKING TRANSACTIONS
        else:
            if not session.session_active:
                print("You must login first.")
                continue

            if code == "deposit":
                if tp.process_deposit(session.session_type, session.current_user):
                    session.mark_transaction()

            elif code == "transfer":
                if tp.transfer(session.session_type, session.current_user):
                    session.mark_transaction()

            elif code == "withdrawal":
                if tp.process_withdrawal(session.session_type, session.current_user):
                    session.mark_transaction()

            elif code == "paybill":
                if tp.paybill(session.session_type, session.current_user):
                    session.mark_transaction()

            # ADMIN-ONLY operations
            elif code == "create":
                if tp.process_create(session.session_type):
                    session.mark_transaction()

            elif code == "delete":
                if tp.process_delete(session.session_type, session.current_user):
                    session.mark_transaction()

            elif code == "disable":
                if tp.process_disable(session.session_type, session.current_user):
                    session.mark_transaction()

            elif code == "changeplan":
                if tp.process_changeplan(session.session_type, session.current_user):
                    session.mark_transaction()

            else:
                print("Invalid transaction code")

    # if transacton wasn't executed, add a placeholder in the .atf file
    if not session.transactions_done:
        try:
            write_txn_line(
                transaction_file,
                code="00",
                name="",
                acct="00000",
                amount=0.0,
                misc=""
            )
        except Exception as e:
            print(f"Error writing placeholder transaction: {e}")

if __name__ == "__main__":
    main()
