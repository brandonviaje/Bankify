from account_reader import read_bank_accounts

if __name__ == "__main__":
    file_path = "bank_accounts.txt"
    accounts = read_bank_accounts(file_path)

    print("Accounts:")
    for acc_num in accounts.keys():
        print(accounts[acc_num])
