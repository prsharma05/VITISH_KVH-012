import pymongo
import matplotlib.pyplot as plt

# Establish a connection to the MongoDB database
client = pymongo.MongoClient("mongodb://localhost:5050/")
db = client["mydatabase"]
collection = db["mycollection"]

# Query the database to get the necessary information
accounts = {}
for transaction in collection.find():
    account_no = transaction["Account no"]
    transaction_type = transaction["TRANSACTION DETAILS"]
    withdrawal_amount = transaction["WITHDRAWAL AMT"]
    deposit_amount = transaction["DEPOSIT AMT"]
    balance_amount = transaction["BALANCE AMT"]
    if account_no not in accounts:
        accounts[account_no] = {"withdrawal_total": 0, "deposit_total": 0}
    if transaction_type == "withdrawal":
        accounts[account_no]["withdrawal_total"] += withdrawal_amount
    elif transaction_type == "deposit":
        accounts[account_no]["deposit_total"] += deposit_amount

# Classify the accounts based on their transaction volumes
mean_withdrawal = sum(account["withdrawal_total"]
                      for account in accounts.values()) / len(accounts)
mean_deposit = sum(account["deposit_total"]
                   for account in accounts.values()) / len(accounts)
for account_no, account in accounts.items():
    if account["withdrawal_total"] > mean_withdrawal and account["deposit_total"] > mean_deposit:
        print(f"Account {account_no} is a high-volume account")
    elif account["withdrawal_total"] < mean_withdrawal and account["deposit_total"] < mean_deposit:
        print(f"Account {account_no} is a low-volume account")
    else:
        print(f"Account {account_no} is a medium-volume account")

# Visualize the data using a line chart
for account_no, account in accounts.items():
    balance = [transaction["balance amount"]
               for transaction in collection.find({"Account no.": account_no})]
    dates = [transaction["Date"]
             for transaction in collection.find({"Account no.": account_no})]
    plt.plot(dates, balance, label=f"Account {account_no}")
plt.legend()
plt.xlabel("Date")
plt.ylabel("Balance")
plt.show()