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
