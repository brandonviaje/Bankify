import sys
import os
import pytest
from unittest.mock import patch
from backend_processor import process_transactions


"""
Helper function to create a sample account dictionary used across all unit tests.

Returns:   dict: A single test account with initial balance and metadata
"""
def create_account():
    return {
        '12345': {
            'account_number': '12345',
            'name': 'John',
            'status': 'A',
            'balance': 100,
            'total_transactions': 0,
            'plan': 'NP'
        }
    }

"""
TC1: Test system behavior with no transactions.

Expectation:
- Accounts should remain unchanged
- No processing should occur
"""
def test_empty_transactions():
    accounts = create_account()
    result = process_transactions(accounts, [])
    assert result == accounts

"""
TC2: Test single deposit transaction (code 04).

Expectation:
- Balance should increase by deposit amount
"""
def test_single_deposit():
    accounts = create_account()
    transactions = [{
        'code': '04',
        'account_number': '12345',
        'amount': 50,
        'name': '',
        'misc': ''
    }]
    result = process_transactions(accounts, transactions)
    assert result['12345']['balance'] == 150

"""
TC3: Test transaction with code '00' (skip operation).

Expectation:
- Transaction should be ignored
- Balance should remain unchanged
"""
def test_skip_code_00():
    accounts = create_account()
    transactions = [{
        'code': '00',
        'account_number': '12345',
        'amount': 50,
        'name': '',
        'misc': ''
    }]
    result = process_transactions(accounts, transactions)
    assert result['12345']['balance'] == 100

"""
TC4: Test transaction with non-existent account number.

Expectation:
- Transaction should be ignored
- No new account should be created
"""
def test_invalid_account():
    accounts = create_account()
    transactions = [{
        'code': '04',
        'account_number': '99999',
        'amount': 50,
        'name': '',
        'misc': ''
    }]
    result = process_transactions(accounts, transactions)
    assert '99999' not in result

"""
TC5: Test valid withdrawal transaction (code 01).

Expectation:
- Balance should decrease by withdrawal amount
"""
def test_withdrawal_valid():
    accounts = create_account()
    transactions = [{
        'code': '01',
        'account_number': '12345',
        'amount': 50,
        'name': '',
        'misc': ''
    }]
    result = process_transactions(accounts, transactions)
    assert result['12345']['balance'] == 50

"""
TC6: Test withdrawal with insufficient funds.

Expectation:
- Withdrawal should be rejected
- Balance should remain unchanged
"""
def test_withdrawal_insufficient():
    accounts = create_account()
    transactions = [{
        'code': '01',
        'account_number': '12345',
        'amount': 200,
        'name': '',
        'misc': ''
    }]
    result = process_transactions(accounts, transactions)
    assert result['12345']['balance'] == 100

"""
TC7: Test account creation transaction (code 05).

Expectation:
- A new account should be added
- Total number of accounts should increase
"""
def test_create_account():
    accounts = create_account()
    transactions = [{
        'code': '05',
        'account_number': '00000',
        'amount': 200,
        'name': 'Alice',
        'misc': ''
    }]
    result = process_transactions(accounts, transactions)
    assert len(result) == 2

"""
TC8: Test handling of invalid transaction code.

Expectation:
- Transaction should be ignored
- No changes to account balance
"""
def test_invalid_code():
    accounts = create_account()
    transactions = [{
        'code': '99',
        'account_number': '12345',
        'amount': 50,
        'name': '',
        'misc': ''
    }]
    result = process_transactions(accounts, transactions)
    assert result['12345']['balance'] == 100

"""
TC9: Test multiple sequential transactions.

Expectation:
- Transactions should be processed in order
- Final balance should reflect all valid operations
"""
def test_multiple_transactions():
    accounts = create_account()
    transactions = [
        {'code': '04', 'account_number': '12345', 'amount': 50, 'name': '', 'misc': ''},
        {'code': '01', 'account_number': '12345', 'amount': 30, 'name': '', 'misc': ''}
    ]
    result = process_transactions(accounts, transactions)
    assert result['12345']['balance'] == 120
    