
from dataclasses import dataclass


# Immutable transaction record
@dataclass(frozen=True)
class Transaction:
    transaction_id: int
    action: str
    amount: float
    resulting_balance: float


class Account:

    def __init__(self, account_number, balance=0):

        if not isinstance(account_number, str) or not account_number.strip():
            raise ValueError("Invalid account number")

        if isinstance(balance, bool) or not isinstance(balance, (int, float)):
            raise ValueError("Invalid balance")

        if balance < 0:
            raise ValueError("Balance cannot be negative")

        self.account_number = account_number
        self.__balance = balance
        self.__transactions = []

    @property
    def balance(self):
        return self.__balance

    @property
    def statement(self):
        return tuple(self.__transactions)

    def deposit(self, amount, transaction_id):

        self.__validate_amount(amount)

        self.__balance += amount

        self.__add_transaction(
            transaction_id, "Deposit", amount
        )

    def withdraw(self, amount, transaction_id):

        self.__validate_amount(amount)

        if amount > self.__balance:
            raise ValueError("Insufficient funds")

        self.__balance -= amount

        self.__add_transaction(
            transaction_id, "Withdrawal", amount
        )

    def __validate_amount(self, amount):

        if isinstance(amount, bool) or not isinstance(amount, (int, float)):
            raise ValueError("Amount must be numeric")

        if amount <= 0:
            raise ValueError("Amount must be positive")

    def __add_transaction(self, transaction_id, action, amount):

        record = Transaction(
            transaction_id,
            action,
            amount,
            self.__balance
        )

        self.__transactions.append(record)


class Bank:

    def __init__(self):

        self.__accounts = {}
        self.__next_transaction_id = 1

    def add_account(self, account):

        if not isinstance(account, Account):
            raise TypeError("Invalid account")

        if account.account_number in self.__accounts:
            raise ValueError("Account already exists")

        self.__accounts[account.account_number] = account

    def get_account(self, account_number):

        if account_number not in self.__accounts:
            raise ValueError("Account does not exist")

        return self.__accounts[account_number]

    def deposit(self, account_number, amount):

        account = self.get_account(account_number)

        account.deposit(amount, self.__next_transaction_id)
        self.__next_transaction_id += 1

    def withdraw(self, account_number, amount):

        account = self.get_account(account_number)

        account.withdraw(amount, self.__next_transaction_id)
        self.__next_transaction_id += 1

    def transfer(self, sender_number, receiver_number, amount):

        sender = self.get_account(sender_number)
        receiver = self.get_account(receiver_number)

        sender._Account__validate_amount(amount)

        if sender is receiver:
            raise ValueError("Cannot transfer to the same account")

        if amount > sender.balance:
            raise ValueError("Insufficient funds")

        # Both balances are updated after validation
        transaction_id = self.__next_transaction_id

        sender.withdraw(amount, transaction_id)
        receiver.deposit(amount, transaction_id)

        self.__next_transaction_id += 1

    def account_statement(self, account_number):

        account = self.get_account(account_number)

        return account.statement


# Create accounts
account_a = Account("A", 1000)
account_b = Account("B", 200)

# Create bank
bank = Bank()

bank.add_account(account_a)
bank.add_account(account_b)

# Transfer money
bank.transfer("A", "B", 350)

# Display balances
print("Account A:", account_a.balance)
print("Account B:", account_b.balance)

# Display statements
print("\nAccount A Statement:")
for transaction in bank.account_statement("A"):
    print(transaction)

print("\nAccount B Statement:")
for transaction in bank.account_statement("B"):
    print(transaction)
