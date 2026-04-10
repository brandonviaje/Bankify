# Phase 6: Integration & Delivery – Bankify

This document explains how we integrated the **Bankify** front‑end and back‑end systems for Phase 6.  We created two shell scripts — `daily.sh` and `weekly.sh` — to automate multi‑session processing and simulate a full week of banking activity.

## Overview of Phase 6

Prior phases focused on implementing and testing the front‑end ATM (`main.py`) and the back‑end batch processor (`backend/backend_main.py`) separately.  In Phase 6, our goal was to connect these components so that a day’s worth of customer sessions could be processed automatically and the results could be carried forward across days.  The two key deliverables are:

- **Daily script** (`daily.sh`) — runs the front‑end for one or more session files, merges the resulting transaction logs, then runs the back‑end to apply all transactions and produce updated account files.
- **Weekly script** (`weekly.sh`) — invokes the daily script seven times in sequence, using the prior day’s output as the next day’s input.  It exercises a variety of operations over the week (deposits, withdrawals, transfers, bill payments, account management and error conditions).

## The Daily Script

The daily script accepts three types of arguments:

1. A **current accounts file** — the state of accounts at the start of the day (e.g. `bank_accounts.txt`).
2. A **master accounts file** — the long‑term ledger used by the back‑end (e.g. `backend/old_master_accounts.txt`).
3. One or more **session files** — each is a text file of commands that simulate a complete ATM session (e.g. `inputs/FE_04.txt`).

### What it does

For each session file, `daily.sh`:

1. **Copies the starting current accounts file** into a temporary working directory.  All sessions share the same starting state.
2. **Runs the front‑end ATM** (`main.py`), piping the session file into standard input.  The front‑end writes its transaction log to a `.atf` file.
3. After all sessions, **merges the `.atf` files** into a single `merged_transactions.txt`.
4. **Prepares the back‑end inputs** by copying the master accounts file and the merged transaction file into the names the back‑end expects (`old_master_accounts.txt` and `merged_transactions.txt`).
5. **Runs the back‑end** (`backend/backend_main.py`) to apply all transactions in order.  This produces two new files:
   - `new_master_accounts.txt` — the updated master ledger.
   - `new_current_accounts.txt` — the updated current accounts file, ready for the next day.

### Running the daily script

To process a single day’s sessions, run `daily.sh` from the project root (`cd Bankify`) (using a Unix‑like shell such as Git Bash or WSL on Windows):

```bash
bash daily.sh bank_accounts.txt backend/old_master_accounts.txt inputs/FE_04.txt inputs/FE_20.txt
```
In this example, the script processes two sessions (FE_04 and FE_20) against bank_accounts.txt and writes updated account files. You can pass any number of session files.

## The Weekly Script

The weekly script automates a full week’s processing by calling `daily.sh` seven times. After each run, it saves the results into files like `accounts_day1_current.txt` and `accounts_day1_master.txt`, then uses those files as the starting points for the next day. This simulates how account balances and statuses evolve over several days.

### Session schedule

We selected session files to exercise the major features and some common error conditions:
| Day | Sessions (description)                                                |
| --- | --------------------------------------------------------------------- |
| 1   | `FE_04.txt`, `FE_20.txt` – valid login/deposit                        |
| 2   | `FE_07.txt`, `FE_08.txt` – valid withdrawal and over‑limit withdrawal |
| 3   | `FE_11.txt`, `FE_12.txt` – valid transfer and over‑limit transfer     |
| 4   | `FE_15.txt`, `FE_16.txt` – valid paybill and invalid paybill          |
| 5   | `FE_23.txt`, `FE_26.txt` – account creation and deletion              |
| 6   | `FE_29.txt`, `FE_32.txt` – disable account and change plan            |
| 7   | `FE_21.txt` – deposit into an account the user doesn’t own (error)    |

You can modify the `DAY1`, `DAY2`, … `DAY7` arrays in `weekly.sh` to use different combinations of session files.

## Running the weekly script

Execute the weekly script from the project root (`cd Bankify`):

```bash
bash weekly.sh
```

The script will print progress messages for each day and produce new account files:
- `accounts_dayN_current.txt` and `accounts_dayN_master.txt` for each day (1 ≤ N ≤ 7).
- Final `new_master_accounts.txt` and `new_current_accounts.txt` reflecting the cumulative result of the week.

## Generated Files and Git

The scripts generate several files that represent daily and final account states. These should not be committed to version control. We updated the repository’s .gitignore to exclude these auto‑generated files:
`new_current_accounts.txt`
`new_master_accounts.txt`
`accounts_day*.txt`
`.daily_tmp/`

This prevents noise in the repository when you or teammates run the scripts locally. Only the source scripts (`daily.sh` and `weekly.sh`) and relevant configuration files need to be tracked.

## Customising and Extending
- Change the session schedule: Edit the arrays at the top of `weekly.sh` to run different sessions or more than two sessions per day.
- Create your own sessions: Session files live in the `inputs/` directory. Each file contains the commands a user would enter during an ATM session. To test new behaviours, add new files there and include them in the daily or weekly script arguments.
- Resetting account state: The starting files `bank_accounts.txt` and `backend/old_master_accounts.txt` represent day‑zero accounts. If you need to rerun the scripts from scratch, restore these files to their original versions.

## Summary

Phase 6 brings together the front‑end ATM interface and the back‑end batch processor. By automating session processing (`daily.sh`) and simulating consecutive days (`weekly.sh`), we can verify that all transaction types are handled correctly and that the system maintains consistent state across days. The scripts also make it easy to test additional scenarios simply by adding session files and adjusting the weekly schedule.
