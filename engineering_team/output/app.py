# app.py
import gradio as gr
from accounts import Account

# Initialize a new account with an initial deposit
account = Account(initial_deposit=1000)

def create_account(initial_deposit):
    global account
    account = Account(initial_deposit=initial_deposit)
    return f"Account created with initial deposit: ${initial_deposit}"

def deposit(amount):
    account.deposit(amount)
    return f"Deposited: ${amount}"

def withdraw(amount):
    if account.withdraw(amount):
        return f"Withdrawn: ${amount}"
    else:
        return "Insufficient funds"

def buy_shares(symbol, quantity):
    if account.buy_shares(symbol, quantity):
        return f"Bought {quantity} shares of {symbol}"
    else:
        return "Not enough funds to buy shares"

def sell_shares(symbol, quantity):
    if account.sell_shares(symbol, quantity):
        return f"Sold {quantity} shares of {symbol}"
    else:
        return "Not enough shares to sell"

def report_portfolio_value():
    value = account.get_portfolio_value()
    return f"Total Portfolio Value: ${value}"

def report_profit_or_loss():
    profit_or_loss = account.get_profit_or_loss()
    return f"Profit/Loss: ${profit_or_loss}"

def report_holdings():
    holdings = account.get_holdings()
    return f"Current Holdings: {holdings}"

def report_transactions():
    transactions = account.get_transaction_history()
    return f"Transaction History: {transactions}"

with gr.Blocks() as interface:
    gr.Markdown("# Trading Simulation Platform")
    
    with gr.Tab("Account Management"):
        initial_deposit = gr.Number(label="Initial Deposit", value=0)
        gr.Button("Create Account").click(create_account, [initial_deposit], gr.Textbox(label="Output"))
        
        deposit_amount = gr.Number(label="Deposit Amount")
        gr.Button("Deposit").click(deposit, [deposit_amount], gr.Textbox(label="Output"))
        
        withdraw_amount = gr.Number(label="Withdraw Amount")
        gr.Button("Withdraw").click(withdraw, [withdraw_amount], gr.Textbox(label="Output"))

    with gr.Tab("Trade Shares"):
        stock_symbol = gr.Textbox(label="Stock Symbol")
        quantity = gr.Number(label="Quantity")

        gr.Button("Buy Shares").click(buy_shares, [stock_symbol, quantity], gr.Textbox(label="Output"))
        gr.Button("Sell Shares").click(sell_shares, [stock_symbol, quantity], gr.Textbox(label="Output"))

    with gr.Tab("Reports"):
        gr.Button("Portfolio Value").click(report_portfolio_value, [], gr.Textbox(label="Output"))
        gr.Button("Profit or Loss").click(report_profit_or_loss, [], gr.Textbox(label="Output"))
        gr.Button("Holdings").click(report_holdings, [], gr.Textbox(label="Output"))
        gr.Button("Transactions").click(report_transactions, [], gr.Textbox(label="Output"))

interface.launch()