from account_reader import read_bank_accounts
from sessions import Session

if __name__ == "__main__":
    file_path = "bank_accounts.txt"
    session = Session()

    # start event loop
    while True:
        code = input("Enter transaction code: ").strip().lower()

        # handle login/logout
        if code == "login":
            accounts = session.handle_login(file_path)
        elif code == "logout":
            # must be logged in first
            if not session.session_active:
                print("You must login first.")
                continue

            session.handle_logout(file_path)
            break  # end session
        else:
            # must be logged in first
            if not session.session_active:
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


#Perhaps new main that works with account stuff like deposit, create, delete, disable, changeplan, paybill, etc.
####################################
# main.py
# from sessions import Session
# from transaction_processor import TransactionProcessor
# from admin import Admin

# if __name__ == "__main__":
#     file_path = "bank_accounts.txt"
#     session = Session()
#     accounts = None

#     while True:
#         code = input("Enter transaction code: ").strip().lower()

#         if code == "login":
#             accounts = session.handle_login(file_path)
#             if accounts is None:
#                 continue

#         elif code == "logout":
#             if not session.session_active:
#                 print("You must login first.")
#                 continue
#             session.handle_logout(accounts, file_path)
#             break

#         else:
#             if not session.session_active:
#                 print("You must login first.")
#                 continue

#             tp = TransactionProcessor(accounts)
#             admin = Admin(accounts)

#             if code == "deposit":
#                 tp.process_deposit(session.session_type, session.current_user)

#             elif code == "create":
#                 admin.process_create(session.session_type)

#             elif code == "delete":
#                 admin.process_delete(session.session_type)

#             elif code == "disable":
#                 admin.process_disable(session.session_type)

#             else:
#                 print("Transaction not implemented in Phase 2.")
