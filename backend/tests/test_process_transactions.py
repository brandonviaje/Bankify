"""
Test Suite: process_transactions
Author: Brandon Viaje and Jason Mong
This module contains unit tests for the `process_transactions` function,
which is responsible for handling multiple transaction types and updating
account states accordingly.

Purpose:
- Validate correct processing of transaction codes
- Ensure proper handling of valid and invalid operations
- Verify account balances and states are updated correctly

Dependencies:
- process_transactions function from backend_processor
"""
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
    

"""
TC10: Test transfer transaction (code 02).

Expectation:
- Amount should be transferred from source to destination account
"""
def test_transfer():
    accounts = create_account()
    
    # add destination account
    accounts['67890'] = {
        'account_number': '67890',
        'name': 'Jane',
        'status': 'A',
        'balance': 100,
        'total_transactions': 0,
        'plan': 'NP'
    }
    
    transactions = [{
        'code': '02',
        'account_number': '12345',
        'amount': 50,
        'name': '',
        'misc': '67890'
    }]

    result = process_transactions(accounts, transactions)

    assert result['12345']['balance'] == 50
    assert result['67890']['balance'] == 150


"""
TC11: Test paybill transaction (code 03).

Expectation:
- Balance should decrease by bill amount
"""
def test_paybill():
    accounts = create_account()

    transactions = [{
        'code': '03',
        'account_number': '12345',
        'amount': 40,
        'name': '',
        'misc': ''
    }]

    result = process_transactions(accounts, transactions)
    assert result['12345']['balance'] == 60


"""
TC12: Test delete account transaction (code 06).

Expectation:
- Account should be removed from system
"""
def test_delete_account():
    accounts = create_account()

    transactions = [{
        'code': '06',
        'account_number': '12345',
        'amount': 0,
        'name': 'John',
        'misc': ''
    }]

    result = process_transactions(accounts, transactions)
    assert '12345' not in result


"""
TC13: Test disable account transaction (code 07).

Expectation:
- Account status should change (e.g., to 'D')
"""
def test_disable_account():
    accounts = create_account()

    transactions = [{
        'code': '07',
        'account_number': '12345',
        'amount': 0,
        'name': '',
        'misc': ''
    }]

    result = process_transactions(accounts, transactions)
    assert result['12345']['status'] == 'D'


"""
TC14: Test change plan transaction (code 08).

Expectation:
- Account plan should be updated
"""
def test_change_plan():
    accounts = create_account()

    transactions = [{
        'code': '08',
        'account_number': '12345',
        'amount': 0,
        'name': '',
        'misc': ''
    }]

    result = process_transactions(accounts, transactions)
    
    assert result['12345']['plan'] != 'NP'
