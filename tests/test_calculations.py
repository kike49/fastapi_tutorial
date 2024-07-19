from app.calculations import InsufficientFunds, add, BankAccount
import pytest

@pytest.fixture
def zero_bank_account():
    return BankAccount()

@pytest.fixture
def balance_bank_account():
    return BankAccount(50)

@pytest.mark.parametrize("num1, num2, result",[(3, 2, 5), (7, 1, 8), (12, 4, 16)])
def test_add(num1, num2, result):
    assert add(num1, num2) == result

def test_bank_inital_amount(balance_bank_account):
    assert balance_bank_account.balance == 50

def test_balance_default(zero_bank_account):
    assert zero_bank_account.balance == 0

def test_withdraw(balance_bank_account):
    balance_bank_account.withdraw(20)
    assert balance_bank_account.balance == 30

def test_deposit(balance_bank_account):
    balance_bank_account.deposit(30)
    assert balance_bank_account.balance == 80

def test_interest(balance_bank_account):
    balance_bank_account.collect_interest()
    assert round(balance_bank_account.balance, 2) == 55

@pytest.mark.parametrize("deposited, withdrawal, balance", [(300, 200, 100), (70, 10, 60), (12, 4, 8)])
def test_bank_transactions(zero_bank_account, deposited, withdrawal, balance):
    zero_bank_account.deposit(deposited)
    zero_bank_account.withdraw(withdrawal)
    assert zero_bank_account.balance == balance

def insufficient_funds(balance_bank_account):
    with pytest.raises(InsufficientFunds):
        balance_bank_account.withdraw(100)

