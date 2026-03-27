import sys
import os
import pytest
from unittest.mock import patch
from backend_processor  import process_transactions


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

def test_empty_transactions():
    accounts = create_account()
    result = process_transactions(accounts, [])
    assert result == accounts

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

def test_multiple_transactions():
    accounts = create_account()
    transactions = [
        {'code': '04', 'account_number': '12345', 'amount': 50, 'name': '', 'misc': ''},
        {'code': '01', 'account_number': '12345', 'amount': 30, 'name': '', 'misc': ''}
    ]
    result = process_transactions(accounts, transactions)
    assert result['12345']['balance'] == 120