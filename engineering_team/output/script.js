const account = new Account();

// Function to update the result output
function updateResultOutput(message) {
    const resultOutput = document.getElementById('result-output');
    resultOutput.textContent = message;
}

// Create account event listener
document.getElementById('create-account-form').addEventListener('submit', function(event) {
    event.preventDefault();
    const userId = document.getElementById('user_id').value;
    const initialDeposit = parseFloat(document.getElementById('initial_deposit').value);
    account.createAccount(userId, initialDeposit);
    updateResultOutput(`Account created for ${userId} with initial deposit of $${initialDeposit}`);
});

// Deposit funds event listener
document.getElementById('deposit-form').addEventListener('submit', function(event) {
    event.preventDefault();
    const depositAmount = parseFloat(document.getElementById('deposit_amount').value);
    account.deposit(depositAmount);
    updateResultOutput(`Deposited $${depositAmount}. New balance: $${account.getBalance()}`);
});

// Withdraw funds event listener
document.getElementById('withdraw-form').addEventListener('submit', function(event) {
    event.preventDefault();
    const withdrawAmount = parseFloat(document.getElementById('withdraw_amount').value);
    const success = account.withdraw(withdrawAmount);
    if (success) {
        updateResultOutput(`Withdrew $${withdrawAmount}. New balance: $${account.getBalance()}`);
    } else {
        updateResultOutput(`Withdrawal of $${withdrawAmount} failed. Insufficient funds.`);
    }
});

// Execute trade event listener
document.getElementById('trade-form').addEventListener('submit', function(event) {
    event.preventDefault();
    const symbol = document.getElementById('trade_symbol').value;
    const quantity = parseInt(document.getElementById('trade_quantity').value, 10);
    const transactionType = document.getElementById('transaction_type').value;
    const success = account.executeTrade(transactionType, symbol, quantity);
    if (success) {
        updateResultOutput(`${transactionType.toUpperCase()} ${quantity} shares of ${symbol}.`);
    } else {
        updateResultOutput(`Trade failed. Check balance or holdings.`);
    }
});

// View portfolio value event listener
document.getElementById('view-portfolio-value').addEventListener('click', function() {
    const portfolioValue = account.getPortfolioValue();
    updateResultOutput(`Total Portfolio Value: $${portfolioValue}`);
});

// View profit/loss event listener
document.getElementById('view-profit-loss').addEventListener('click', function() {
    const profitLoss = account.getProfitLoss();
    updateResultOutput(`Profit/Loss: $${profitLoss}`);
});

// View holdings event listener
document.getElementById('view-holdings').addEventListener('click', function() {
    const holdings = account.getHoldings();
    updateResultOutput(`Current Holdings: ${JSON.stringify(holdings)}`);
});

// View transactions event listener
document.getElementById('view-transactions').addEventListener('click', function() {
    const transactions = account.getTransactions();
    updateResultOutput(`Transaction History: ${JSON.stringify(transactions)}`);
});

// Example of get_share_price function
function get_share_price(symbol) {
    const prices = {
        'AAPL': 150,
        'TSLA': 900,
        'GOOGL': 2800
    };
    return prices[symbol] || null;
}

// Mocking account functions for testing
function Account() {
    this.balance = 0;
    this.holdings = {};
    this.transactions = [];
    this.initialDeposit = 0;

    this.createAccount = function(userId, initialDeposit) {
        this.initialDeposit = initialDeposit;
        this.balance = initialDeposit;
    };

    this.deposit = function(amount) {
        this.balance += amount;
    };

    this.withdraw = function(amount) {
        if (amount <= this.balance) {
            this.balance -= amount;
            return true;
        }
        return false;
    };

    this.executeTrade = function(type, symbol, quantity) {
        const price = get_share_price(symbol);
        const totalCost = price * quantity;
        if (type === 'buy') {
            if (totalCost <= this.balance) {
                this.balance -= totalCost;
                this.holdings[symbol] = (this.holdings[symbol] || 0) + quantity;
                this.transactions.push({type, symbol, quantity, price});
                return true;
            } 
        } else if (type === 'sell') {
            if ((this.holdings[symbol] || 0) >= quantity) {
                this.balance += totalCost;
                this.holdings[symbol] -= quantity;
                this.transactions.push({type, symbol, quantity, price});
                return true;
            }
        }
        return false;
    };

    this.getBalance = function() {
        return this.balance;
    };

    this.getPortfolioValue = function() {
        let totalValue = 0;
        for (let symbol in this.holdings) {
            const price = get_share_price(symbol);
            totalValue += this.holdings[symbol] * price;
        }
        return totalValue;
    };

    this.getProfitLoss = function() {
        const portfolioValue = this.getPortfolioValue();
        return (portfolioValue + this.balance) - this.initialDeposit;
    };

    this.getHoldings = function() {
        return this.holdings;
    };

    this.getTransactions = function() {
        return this.transactions;
    };
}