import sys
from account_reader import read_bank_accounts
from sessions import Session
from transaction_processor import TransactionProcessor

"""
Bank ATM Front-End Main Program

This serves as the main entry point for the Bank system.
It initializes the bank account data, manages user sessions, and
routes user-entered transaction codes to the appropriate handlers.

The program:
- Loads bank account data from a file
- Manages login/logout sessions
- Accepts transaction commands from the user
- Delegates transaction processing to the TransactionProcessor
- Enforces session rules (e.g., login required for transactions)
- Supports regular user and admin operations

Transaction codes:
login, logout, deposit, transfer, withdrawal, paybill,
create, delete, disable, changeplan, exit
"""

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: python main.py <current_accounts_file> <transaction_output_file>")
        sys.exit(1)

    accounts_file = sys.argv[1]
    transaction_file = sys.argv[2]
    session = Session()

    accounts = read_bank_accounts(accounts_file)
    tp = TransactionProcessor(accounts, transaction_file)

    while True:
        if not session.session_active:
            print("\nPlease login to continue.")

        print("\nAvailable transaction codes:")
        print("login, logout, deposit, transfer, withdrawal, paybill, create, delete, disable, changeplan, exit\n")

        try:
            code = input("Enter transaction code: ").strip().lower()
        except EOFError:
            break 

        if code == "login":
            accounts = session.handle_login(accounts_file)
        # Only update if login succeeded
            if accounts is not None:
                tp.accounts = accounts
                tp.standard_withdraw_total = 0.0
                tp.standard_transfer_total = 0.0

        elif code == "logout":
            if not session.session_active:
                print("You must login first.")
                continue

            session.handle_logout(accounts, transaction_file)
            # if logout should end the session entirely, uncomment:
            break

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
                tp.process_delete(session.session_type, session.current_user)

            elif code == "disable":
                tp.process_disable(session.session_type, session.current_user)

            elif code == "changeplan":
                tp.process_changeplan(session.session_type, session.current_user)

            else:
                print("Invalid transaction code")
