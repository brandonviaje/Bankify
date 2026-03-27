# Testing Report – process_transactions()

## Method Under Test

`process_transactions(accounts, transactions)`

This method processes a list of financial transactions using a loop and multiple decision branches based on transaction codes.

It includes:

- 1 loop → iterates through `transactions`
- multiple decision branches → based on transaction codes and account validation

---

# Test Case Design Table (Decision + Loop Coverage)

| TC   | Description                   | Input Transaction(s)                                                   | Expected Result                     | Coverage           |
| ---- | ----------------------------- | ---------------------------------------------------------------------- | ----------------------------------- | ------------------ |
| TC1  | Empty transaction list        | `[]`                                                                   | No changes to accounts              | Loop = 0           |
| TC2  | Valid deposit (code 04)       | `[{'code':'04','account_number':'12345','amount':50}]`                 | Balance increases by 50             | Deposit branch     |
| TC3  | Skip code "00"                | `[{'code':'00','account_number':'12345','amount':50}]`                 | Transaction ignored, no change      | Skip branch        |
| TC4  | Invalid account number        | `[{'code':'04','account_number':'99999','amount':50}]`                 | Error logged, transaction skipped   | Account check fail |
| TC5  | Valid withdrawal              | `[{'code':'01','account_number':'12345','amount':50}]`                 | Balance decreases by 50             | Withdrawal branch  |
| TC6  | Withdrawal insufficient funds | `[{'code':'01','account_number':'12345','amount':200}]`                | No change to balance                | Insufficient funds |
| TC7  | Create account (code 05)      | `[{'code':'05','account_number':'00000','amount':200,'name':'Alice'}]` | New account created                 | Create branch      |
| TC8  | Invalid transaction code      | `[{'code':'99','account_number':'12345','amount':50}]`                 | Error logged, no changes            | Else branch        |
| TC9  | Multiple transactions         | `[deposit, withdrawal]`                                                | All transactions processed in order | Loop > 1 iteration |
| TC10 | Mixed valid + invalid cases   | `[valid txn, invalid account, invalid code]`                           | Valid processed, invalid skipped    | Full branch mix    |

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

# Summary

This test suite achieves:

- Statement coverage (all lines executed)
- Decision coverage (all branches exercised)
- Loop coverage (0, 1, and multiple iterations)
- Error handling validation (invalid account and invalid code cases)
