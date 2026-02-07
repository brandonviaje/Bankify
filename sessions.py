from account_reader import read_bank_accounts

class Session:
    def __init__(self):
        self.session_active = False   # session state
        self.session_type = None      # "standard" or "admin"
        self.current_user = None      # account holder name

    def handle_login(self,file_path):

        # check if an account is already logged in
        if self.session_active:
            print("Already logged in.")
            return

        # get session type
        while True:
            self.session_type = input("Enter session type (standard/admin): ").strip().lower()
            if self.session_type in {"standard", "admin"}:
                break

            print("Invalid session type. Retry")

        # handle session types
        if self.session_type == "standard":
            self.current_user = input("Enter account holder name: ").strip()
        else:
            self.current_user = "ADMIN"

        accounts = read_bank_accounts(file_path)  # read bank acounts file
        self.session_active = True
        print(f"Logged in as {self.current_user} ({self.session_type})")
        return accounts

    def handle_logout(self,accounts):
        pass



#Perhaps new session that works with account stuff like deposit, create, delete, disable, changeplan, paybill, etc.
############################
# sessions.py
# from account_reader import read_bank_accounts
# from account_writer import write_bank_accounts

# class Session:
#     def __init__(self):
#         self.session_active = False
#         self.session_type = None
#         self.current_user = None

#     def handle_login(self, file_path):
#         if self.session_active:
#             print("Already logged in.")
#             return None

#         while True:
#             self.session_type = input("Enter session type (standard/admin): ").strip().lower()
#             if self.session_type in {"standard", "admin"}:
#                 break
#             print("Invalid session type. Retry")

#         if self.session_type == "standard":
#             self.current_user = input("Enter account holder name: ").strip()
#         else:
#             self.current_user = "ADMIN"

#         accounts = read_bank_accounts(file_path)
#         self.session_active = True
#         print(f"Logged in as {self.current_user} ({self.session_type})")
#         return accounts

#     def handle_logout(self, accounts, file_path):
#         # save accounts back to file
#         write_bank_accounts(file_path, accounts)

#         # reset session state
#         self.session_active = False
#         self.session_type = None
#         self.current_user = None

#         print("Logged out. Accounts saved.")

