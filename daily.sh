#!/bin/bash
# Daily batch script for Bankify
#
# Usage:
#   ./daily.sh <current_accounts_file> <master_accounts_file> <session1> [<session2> ...]
#
# This script runs the front‑end ATM for each supplied session file using the
# provided current accounts file, merges the resulting transaction files
# into a single merged transaction file, and then runs the back‑end to
# produce new master and current accounts files. The new files are
# written to the current directory as `new_master_accounts.txt` and
# `new_current_accounts.txt`.

set -e

if [ "$#" -lt 3 ]; then
    echo "Usage: $0 <current_accounts_file> <master_accounts_file> <session1> [<session2> ...]"
    exit 1
fi

# Absolute path to project root (directory of this script)
ROOT_DIR="$(cd "$(dirname "$0")" && pwd)"

CURRENT_ACCOUNTS="$1"
MASTER_ACCOUNTS="$2"
shift 2
SESSIONS=("$@")

# Temporary working directory for current run
TMP_DIR="$ROOT_DIR/.daily_tmp"
rm -rf "$TMP_DIR"
mkdir -p "$TMP_DIR"

# Copy the starting current accounts file into tmp as the reference for all sessions
cp "$CURRENT_ACCOUNTS" "$TMP_DIR/current_accounts.txt"

SESSION_OUTPUTS=()

# Run each session through the front end
for idx in "${!SESSIONS[@]}"; do
    SESSION_FILE="${SESSIONS[$idx]}"
    OUT_FILE="$TMP_DIR/session$((idx+1)).atf"
    SESSION_OUTPUTS+=("$OUT_FILE")

    echo "Running session $SESSION_FILE ..."
    python3 "$ROOT_DIR/main.py" "$TMP_DIR/current_accounts.txt" "$OUT_FILE" < "$SESSION_FILE"
done

# Merge all session outputs into a single merged transactions file
MERGED_FILE="$TMP_DIR/merged_transactions.txt"
cat "${SESSION_OUTPUTS[@]}" > "$MERGED_FILE"

echo "Merged ${#SESSION_OUTPUTS[@]} transaction files into $MERGED_FILE"

# Prepare back‑end inputs
cp "$MASTER_ACCOUNTS" "$ROOT_DIR/old_master_accounts.txt"
cp "$MERGED_FILE" "$ROOT_DIR/merged_transactions.txt"

# Run the back end
echo "Running back end ..."
python3 "$ROOT_DIR/backend/backend_main.py"

echo "Daily processing complete. New accounts files created:"
echo "  new_master_accounts.txt"
echo "  new_current_accounts.txt"
