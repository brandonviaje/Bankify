# Testing Report

# Methods Tested

---

## **process_transactions(accounts, transactions)**

### Coverage Type

- Decision Coverage
- Loop Coverage

### Purpose

Iterates through all transactions and routes each one to the correct handler function based on transaction codes and account validation.

### Structure

- **Loop**
  - Iterates over each transaction in `transactions`
- **Decision Logic**
  - Uses `if / elif / else` to determine transaction type
  - Validates account existence
  - Handles invalid transaction codes
- **Nested Conditions**
  - Includes checks such as:
    - invalid account handling
    - skip transactions (`code == '00'`)
    - account creation (`code == '05'`)

---

## **process_change_plan(accounts, acc_num, txn_context)**

### Coverage Type

- Statement Coverage

### Purpose

Toggles an account plan between:

- `'SP'` (Student Plan)
- `'NP'` (Non-Student Plan)

### Structure

- **Decision Only (No Loop)**
  - If plan is `'SP'` → change to `'NP'`
  - Else → change to `'SP'`

---

# Test Case Tables

---

## **process_transactions() Test Cases**

| TC# | Description              | Input                       | Expected Result            | Coverage Type      |
| --- | ------------------------ | --------------------------- | -------------------------- | ------------------ |
| TC1 | Empty transaction list   | `[]`                        | No changes                 | Loop = 0           |
| TC2 | Single deposit           | code='04', amount=50        | Balance increases          | Loop = 1           |
| TC3 | Skip transaction         | code='00'                   | No change                  | Skip branch        |
| TC4 | Invalid account          | account='99999'             | Error logged, ignored      | False branch       |
| TC5 | Valid withdrawal         | code='01', amount=50        | Balance decreases          | True branch        |
| TC6 | Insufficient funds       | code='01', amount > balance | No change                  | Condition failure  |
| TC7 | Create new account       | code='05'                   | Account created            | Branch coverage    |
| TC8 | Invalid transaction code | code='99'                   | Ignored                    | Else branch        |
| TC9 | Multiple transactions    | mixed operations            | Sequential correct updates | Loop + integration |

---

## **process_change_plan() Test Cases**

| TC# | Description                   | Input     | Expected Result | Coverage Type           |
| --- | ----------------------------- | --------- | --------------- | ----------------------- |
| TC1 | Change SP → NP                | plan='SP' | plan='NP'       | If branch               |
| TC2 | Change NP → SP                | plan='NP' | plan='SP'       | Else branch             |
| TC3 | Invalid/unknown plan fallback | plan='XX' | plan='SP'       | Edge case (else branch) |

---

# Loop Coverage Analysis

The loop `for txn in transactions:` is tested using:

- **TC1** → 0 iterations (empty list)
- **TC2** → 1 iteration (single transaction)
- **TC9** → multiple iterations (mixed transactions)

### Result

Full loop coverage achieved:

- Loop not executed
- Loop executed once
- Loop executed multiple times

---

# Decision Coverage Summary

## process_transactions()

| Decision Point        | Covered By |
| --------------------- | ---------- |
| Skip code `"00"`      | TC3        |
| Invalid account       | TC4        |
| Deposit (`04`)        | TC2        |
| Withdrawal (`01`)     | TC5        |
| Insufficient funds    | TC6        |
| Create account (`05`) | TC7        |
| Invalid code (else)   | TC8        |

---

# Statement Coverage Summary

## process_change_plan()

| Statement / Decision Path     | Covered By |
| ----------------------------- | ---------- |
| Plan is `'SP'` (if branch)    | TC1        |
| Plan is not `'SP'` (else)     | TC2, TC3   |
| Assignment to `'NP'`          | TC1        |
| Assignment to `'SP'`          | TC2, TC3   |

# How to Run

```bash
cd backend
python -m pytest -v
```
