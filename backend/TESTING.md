# Testing Documentation

# Methods Tested

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
    - skip transactions (`code == '00'`)
    - invalid account handling
    - account creation exception (`code == '05'` bypasses validation)

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

| TC#  | Description                  | Input                        | Expected Result                     | Coverage Type        |
|------|------------------------------|------------------------------|-------------------------------------|----------------------|
| TC1  | Empty transaction list       | `[]`                         | No changes                          | Loop = 0             |
| TC2  | Single deposit               | code='04', amount=50         | Balance increases                   | Loop = 1             |
| TC3  | Skip transaction             | code='00'                    | No change                           | Skip branch          |
| TC4  | Invalid account              | account='99999'              | Error logged, ignored               | Decision (True)      |
| TC5  | Valid withdrawal             | code='01', amount=50         | Balance decreases                   | Branch coverage      |
| TC6  | Insufficient funds           | code='01', amount > balance  | No change                           | Internal condition   |
| TC7  | Create new account           | code='05'                    | Account created                     | Branch coverage      |
| TC8  | Invalid transaction code     | code='99'                    | Ignored                             | Else branch          |
| TC9  | Multiple transactions        | mixed operations             | Sequential correct updates          | Loop (multiple)      |
| TC10 | Transfer transaction         | code='02'                    | Funds moved between accounts        | Branch coverage      |
| TC11 | Paybill transaction          | code='03'                    | Balance decreases                   | Branch coverage      |
| TC12 | Delete account               | code='06'                    | Account removed                     | Branch coverage      |
| TC13 | Disable account              | code='07'                    | Account status updated              | Branch coverage      |
| TC14 | Change plan                  | code='08'                    | Account plan updated                | Branch coverage      |

---

## **process_change_plan() Test Cases**

| TC# | Description                   | Input     | Expected Result | Coverage Type           |
|-----|------------------------------|-----------|-----------------|-------------------------|
| TC1 | Change SP → NP                | plan='SP' | plan='NP'       | If branch               |
| TC2 | Change NP → SP                | plan='NP' | plan='SP'       | Else branch             |
| TC3 | Invalid/unknown plan fallback | plan='XX' | plan='SP'       | Else branch (edge case) |

---

# Loop Coverage Analysis

The loop `for txn in transactions:` is tested using:

- **TC1** → 0 iterations (empty list)
- **TC2–TC8, TC10–TC14** → 1 iteration (single transaction)
- **TC9** → multiple iterations (mixed transactions)

### Result

Full loop coverage achieved:

- Loop not executed
- Loop executed once
- Loop executed multiple times

---

# Decision Coverage Summary

## process_transactions()

| Decision Point                          | Covered By |
|----------------------------------------|------------|
| Skip code `"00"`                       | TC3        |
| Invalid account check                  | TC4        |
| Withdrawal (`01`)                      | TC5, TC6   |
| Transfer (`02`)                        | TC10       |
| Paybill (`03`)                         | TC11       |
| Deposit (`04`)                         | TC2        |
| Create account (`05`)                  | TC7        |
| Delete account (`06`)                  | TC12       |
| Disable account (`07`)                 | TC13       |
| Change plan (`08`)                     | TC14       |
| Invalid code (`else`)                  | TC8        |

### Result

All decision branches in the transaction routing logic are executed at least once.

---

# Statement Coverage Summary

## process_change_plan()

| Statement / Decision Path     | Covered By |
|------------------------------|------------|
| Plan is `'SP'` (if branch)   | TC1        |
| Plan is not `'SP'` (else)    | TC2, TC3   |
| Assignment to `'NP'`         | TC1        |
| Assignment to `'SP'`         | TC2, TC3   |

---

# Final Coverage Conclusion

The test suite achieves:

- **100% decision (branch) coverage** for `process_transactions()`
- **100% loop coverage** (0, 1, and multiple iterations)
- **100% statement coverage** for `process_change_plan()`

All control flow paths, including edge cases and invalid inputs, are exercised. This satisfies the requirements for comprehensive **white-box testing**.

---

# How to Run

## 1. Install pytest (if not already installed)

Make sure pytest is installed in your environment before running the tests.

```bash
python -m pip install pytest
```

## 2. Run the test suite
```bash
cd backend
python -m pytest -v
```
