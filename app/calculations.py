def add(num1: int, num2: int) -> int:
    return num1 + num2

class InsufficientFunds(Exception):
    pass

class BankAccount():
    def __init__(self, start_balance=0) -> None:
        self.balance = start_balance
    
    def deposit(self, amount: int) -> None:
        self.balance += amount

    def withdraw(self, amount: int) -> None:
        if amount > self.balance:
            raise Exception("Insuficient money to wirthdraw)")
        self.balance -= amount
    
    def collect_interest(self) -> None:
        self.balance *= 1.1