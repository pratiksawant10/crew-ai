class Account:

    def __init__(self, initial_deposit: float = 0.0) -> None:
        # Initializes account with initial deposit, balance, holdings, transactions
        self.balance = initial_deposit
        self.holdings = {}
        self.transactions = []
        self.initial_deposit = initial_deposit

    def deposit(self, amount: float) -> None:
        # Deposit amount and update balance
        self.balance += amount
        self.transactions.append(f"Deposit: ${amount}")

    def withdraw(self, amount: float) -> bool:
        # Withdraw amount if balance allows, update balance and record transaction
        if amount <= self.balance:
            self.balance -= amount
            self.transactions.append(f"Withdraw: ${amount}")
            return True
        return False

    def buy_shares(self, symbol: str, quantity: int) -> bool:
        # Purchase shares and update balance/holdings if funds available
        price = self.get_share_price(symbol)
        cost = price * quantity
        if cost <= self.balance:
            self.balance -= cost
            self.holdings[symbol] = self.holdings.get(symbol, 0) + quantity
            self.transactions.append(f"Buy: {quantity} {symbol} shares at ${price} each")
            return True
        return False

    def sell_shares(self, symbol: str, quantity: int) -> bool:
        # Sell shares from holdings if available, update balance/holdings
        if symbol in self.holdings and self.holdings[symbol] >= quantity:
            price = self.get_share_price(symbol)
            self.balance += price * quantity
            self.holdings[symbol] -= quantity
            self.transactions.append(f"Sell: {quantity} {symbol} shares at ${price} each")
            if self.holdings[symbol] == 0:
                del self.holdings[symbol]
            return True
        return False

    def get_portfolio_value(self) -> float:
        # Calculate the total value of the portfolio
        value = sum(self.get_share_price(symbol) * qty for symbol, qty in self.holdings.items())
        return value

    def get_profit_or_loss(self) -> float:
        # Calculate current profit or loss
        portfolio_value = self.get_portfolio_value()
        return self.balance + portfolio_value - self.initial_deposit

    def get_holdings(self) -> dict:
        # Return current holdings
        return self.holdings

    def get_transaction_history(self) -> list:
        # Return the transaction history
        return self.transactions

    @staticmethod
    def get_share_price(symbol: str) -> float:
        # Return fixed price for given stock symbol
        prices = {
            'AAPL': 150.0,
            'TSLA': 700.0,
            'GOOGL': 2800.0
        }
        return prices.get(symbol, 0.0)

# Test the module with example usage
account = Account(initial_deposit=1000)
account.deposit(500)
account.buy_shares('AAPL', 10)
account.sell_shares('AAPL', 5)
account.withdraw(200)
portfolio_value = account.get_portfolio_value()
profit_or_loss = account.get_profit_or_loss()
holdings = account.get_holdings()
transaction_history = account.get_transaction_history()

print("Portfolio Value:", portfolio_value)
print("Profit or Loss:", profit_or_loss)
print("Holdings:", holdings)
print("Transaction History:", transaction_history)