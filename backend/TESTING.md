# Testing Report


# Methods Tested
## process_transactions(accounts, transactions)

- Coverage Type: Decision and loop coverage
- Purpose: Iterates through all transactions and routes each to the correct handler function.
- Structure:
  - Loop: Iterates over every transaction in the list.
  - Decisions: Multiple if/elif/else statements determine the type of transaction, check account existence, and handle invalid codes.
  - Nested Decisions: Checks like if code != '05' and acc_num not in accounts and if code == '00': continue add complexity.

---
## process_changeplan(session_type, current_user)

- Coverage Type: Statement Coverage
- Purpose: Toggles the account plan between ‘SP’ (Student) and ‘MP’ (Non-Student)
- Structure:
  - Decision: Checks the current account plan:
  - If 'SP', changes it to 'NP'.
  - Else, changes it to 'SP'.
  - No loop: This method handles a single account at a time.


## Method Under Test (Statement Coverage)

## Method Under Test (Decision + Loop Coverage)

`process_transactions(accounts, transactions)`

This method processes a list of financial transactions using a loop and multiple decision branches based on transaction codes.

It includes:

- 1 loop → iterates through `transactions`
- multiple decision branches → based on transaction codes and account validation



---

# Test Case Table

| TC# | Description                 | Input                        | Expected Result            | Coverage                |
| --- | --------------------------- | ---------------------------- | -------------------------- | ----------------------- |
| TC1 | Empty transaction list      | []                           | No changes                 | Loop = 0                |
| TC2 | Single Deposit              | 1 txn (code='04', amount=50) | Balance increases          | Loop = 1                |
| TC3 | Skip code '00'              | code='00'                    | No change                  | Decision (skip branch)  |
| TC4 | Invalid account             | account='99999'              | Error logged, ignored      | Decision (false branch) |
| TC5 | Valid withdrawal            | code='01', amount=50         | Balance decreases          | Decision (true branch)  |
| TC6 | Insufficient withdrawal     | code='01', amount > balance  | No change                  | Decision (false branch) |
| TC7 | Create new account          | code='05', new account       | Account created            | Branch coverage         |
| TC8 | Invalid transaction code    | code='99'                    | Ignored                    | Default/else branch     |
| TC9 | Multiple mixed transactions | deposit + withdrawal combo   | Sequential correct updates | Loop + integration      |

---

# Loop Coverage Analysis

The loop `for txn in transactions:` is tested using:

- TC1 → 0 iterations (empty list)
- TC2 → 1 iteration (single transaction)
- TC9 / TC10 → multiple iterations

This ensures full loop coverage:

- loop not executed
- loop executed once
- loop executed multiple times

---

# Decision Coverage Summary

| Decision Point             | Covered By |
| -------------------------- | ---------- |
| Skip code "00"             | TC3        |
| Account exists check fails | TC4        |
| Deposit (04)               | TC2        |
| Withdrawal (01)            | TC5        |
| Insufficient funds         | TC6        |
| Create account (05)        | TC7        |
| Invalid code (else)        | TC8        |

---
# How to Run
Navigate to the Backend directory: 
cd bankend

Run the pytest:
Pytest -v

---

# Summary

This test suite achieves:

- Statement coverage (all lines executed)
- Decision coverage (all branches exercised)
- Loop coverage (0, 1, and multiple iterations)
- Error handling validation (invalid account and invalid code cases)
