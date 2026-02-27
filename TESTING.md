#  Testing the Program

##  Run All Tests

To execute the full test suite, run:

```bash
bash run_tests.sh
```

This will:
- Run the program against all test cases
- Generate transaction files
- Simulate the full terminal session (user interaction flow)
- Generate an `output/` directory containing:
  - Produced `.atf` transaction files  
  - Captured terminal logs (`.out`)
---

## About Terminal Logs

The terminal logs represent the **full ATM simulation**, including prompts and system responses.
The terminal logs **do NOT capture user input**. They only capture what the program **prints to terminal**.

Example output:

```
Please login to continue.

Available transaction codes:
login, logout, deposit, transfer, withdrawal, paybill, create, delete, disable, changeplan, exit

Enter transaction code: You must login first.

Please login to continue.

Available transaction codes:
login, logout, deposit, transfer, withdrawal, paybill, create, delete, disable, changeplan, exit

Enter transaction code: [DEBUG] txn line length=41 expected=40 :: '00                      00000 00000.00   '
```

The validation script compares this entire output exactly to the expected output including:
- Prompts  
- Error messages  
- Debug messages  
- Spacing  
- Line breaks  

---

## Validate the Transaction File Output

To compare the generated transaction file with the expected output:

```bash
bash validate_transaction_file.sh
```

This checks:
- The produced `.atf` file  
- Against the expected transaction file  
- Reports any differences  

---

## Validate the Terminal Logs

To compare the actual console simulation with the expected log:

```bash
bash validate_terminal_logs.sh
```

This checks:
- Printed terminal output against the expected terminal log  
- Reports mismatches 

---

## Bank Transaction Test Table

| Test ID | Feature / Transaction | Requirement Tested |
|---------|--------------------|------------------|
| FE_01  | Login       | Rejects transactions before login |
| FE_02  | Login       | Reject login if already logged in |
| FE_03  | Login       | Accept admin login mode |
| FE_04  | Login       | Accept standard login |
| FE_05  | Logout      | Reject logout if no session is active |
| FE_06  | Logout      | Write the transaction file and reject further transactions after logout |
| FE_07  | Withdrawal  | Successful withdrawal within the session limit and account balance |
| FE_08  | Withdrawal  | Reject withdrawal exceeding $500 in standard mode |
| FE_09  | Withdrawal  | Reject a withdrawal that causes a negative balance |
| FE_10  | Withdrawal  | Reject withdrawal from an account not owned by the user |
| FE_11  | Transfer    | Successful transfer between two valid accounts (under session limit and balance limits) |
| FE_12  | Transfer    | Reject transfer exceeding $1000 in standard mode |
| FE_13  | Transfer    | Reject transfer if the source or destination account is invalid |
| FE_14  | Transfer    | Reject the transfer that would cause a negative balance |
| FE_15  | Pay Bill    | Successful payment to the company on the allowed list |
| FE_16  | Pay Bill    | Reject a payment to a company not on the allowed list |
| FE_17  | Pay Bill    | Reject payment that exceeds $2000 in standard mode |
| FE_18  | Pay Bill    | Reject payment that would cause a negative balance |
| FE_19  | Pay Bill    | Reject payment from an account not owned by the user |
| FE_20  | Deposit     | Successful deposit to a valid account |
| FE_21  | Deposit     | Reject the deposit to an account not owned by the logged-in user |
| FE_22  | Deposit     | Ensure deposited funds are not available for further transactions in the same session |
| FE_23  | Create      | Admin successfully creates a new account with a valid name, balance, and unique account number |
| FE_24  | Create      | Reject creation due to an invalid name, an invalid balance, or a duplicate account number |
| FE_25  | Create      | Reject the attempt to create an account in the standard session |
| FE_26  | Delete      | Admin deletes the existing account. No further transactions on that account |
| FE_27  | Delete      | Reject deletion if invalid name and account number |
| FE_28  | Delete      | Reject the delete attempt if in standard mode |
| FE_29  | Disable     | Admin disables the active account. No further transactions |
| FE_30  | Disable     | Reject if the account name /number is invalid |
| FE_31  | Disable     | Reject disabled attempt if in standard mode |
| FE_32  | Change Plan | Admin changes payment plan from SP → NP for a valid account |
| FE_33  | Change Plan | Reject change if the account name or account number is invalid |
| FE_34  | Change Plan | Reject attempt in standard mode |

## Recommended Workflow

```bash
bash run_tests.sh
bash validate_transaction_file.sh
bash validate_terminal_logs.sh
```
