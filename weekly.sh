#!/bin/bash
# Weekly batch script for Bankify
#
# This script runs the daily batch script seven times, simulating seven
# consecutive days of banking operations. Each day starts with the
# current accounts file produced by the previous day and processes
# a selected set of transaction sessions. The resulting new current
# accounts file becomes the starting point for the next day.

set -e

# Absolute path to project root (directory of this script)
ROOT_DIR="$(cd "$(dirname "$0")" && pwd)"

# Ensure daily.sh is executable
chmod +x "$ROOT_DIR/daily.sh"

# Initial current and master accounts files for day 1
CURRENT_FILE="$ROOT_DIR/bank_accounts.txt"
MASTER_FILE="$ROOT_DIR/backend/old_master_accounts.txt"

# Define sessions for each day. These are chosen to exercise a variety of
# operations across the week including deposits, withdrawals, transfers,
# bill payments, account administration, and error conditions. Feel free to
# adjust these lists or add additional sessions as needed.

# Day 1: Successful login/deposit sessions
DAY1=(
    "$ROOT_DIR/inputs/FE_04.txt"  # valid login and deposit
    "$ROOT_DIR/inputs/FE_20.txt"  # valid deposit
)

# Day 2: Withdrawal and withdrawal-over-limit sessions
DAY2=(
    "$ROOT_DIR/inputs/FE_07.txt"  # valid withdrawal
    "$ROOT_DIR/inputs/FE_08.txt"  # withdrawal exceeding limit (error)
)

# Day 3: Transfer and transfer-over-limit sessions
DAY3=(
    "$ROOT_DIR/inputs/FE_11.txt"  # valid transfer
    "$ROOT_DIR/inputs/FE_12.txt"  # transfer exceeding limit (error)
)

# Day 4: Bill payment and invalid bill payment sessions
DAY4=(
    "$ROOT_DIR/inputs/FE_15.txt"  # valid paybill
    "$ROOT_DIR/inputs/FE_16.txt"  # invalid paybill
)

# Day 5: Account creation and deletion sessions
DAY5=(
    "$ROOT_DIR/inputs/FE_23.txt"  # create account
    "$ROOT_DIR/inputs/FE_26.txt"  # delete account
)

# Day 6: Account disabling and plan change sessions
DAY6=(
    "$ROOT_DIR/inputs/FE_29.txt"  # disable account
    "$ROOT_DIR/inputs/FE_32.txt"  # change account plan
)

# Day 7: Deposit to a non-owned account (error scenario)
DAY7=(
    "$ROOT_DIR/inputs/FE_21.txt"  # deposit into account the user does not own
)

for DAY in {1..7}; do
    echo "\n=== Running day $DAY ==="
    SESSIONS_VAR="DAY${DAY}[@]"
    SESSIONS=("${!SESSIONS_VAR}")
    "$ROOT_DIR/daily.sh" "$CURRENT_FILE" "$MASTER_FILE" "${SESSIONS[@]}"
    DAY_CUR_FILE="$ROOT_DIR/accounts_day${DAY}_current.txt"
    DAY_MAS_FILE="$ROOT_DIR/accounts_day${DAY}_master.txt"
    cp "$ROOT_DIR/new_current_accounts.txt" "$DAY_CUR_FILE"
    cp "$ROOT_DIR/new_master_accounts.txt" "$DAY_MAS_FILE"
    echo "Saved new accounts for day $DAY: $DAY_CUR_FILE (current), $DAY_MAS_FILE (master)"
    CURRENT_FILE="$DAY_CUR_FILE"
    MASTER_FILE="$DAY_MAS_FILE"
done

echo "\nWeekly processing complete. Final accounts files:"
echo "  Current: $CURRENT_FILE"
echo "  Master: $MASTER_FILE"
