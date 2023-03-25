import pymongo
import pandas as pd
import matplotlib.pyplot as plt

# Connect to MongoDB database
client = pymongo.MongoClient("mongodb://localhost:27017/")
db = client["fundtrail"]
collection = db["m2"]

# Get transaction data from MongoDB
transactions = pd.DataFrame(list(collection.find()))

# Calculate average transaction amount for each account
avg_amounts = transactions.groupby('Account No')['DEPOSIT AMT'].mean()

# Define threshold to classify accounts as low volume or high volume
threshold = 5000

# Classify accounts as low volume or high volume
low_volume = avg_amounts[avg_amounts <= threshold].index.tolist()
high_volume = avg_amounts[avg_amounts > threshold].index.tolist()

# Generate histogram to visualize the distribution of transaction amounts
plt.hist(transactions['BALANCE AMT'], bins=20)
plt.xlabel('Transaction Amount')
plt.ylabel('Frequency')
plt.title('Distribution of Transaction Amounts')
plt.show()

import pymongo
import pandas as pd

# Connect to MongoDB database
client = pymongo.MongoClient("mongodb://localhost:27017/")
db = client["fundtrail"]
collection = db["transactions"]

# Get transaction data from MongoDB
transactions = pd.DataFrame(list(collection.find()))

# Calculate mean and standard deviation of deposit and withdrawal amounts for each account
grouped = transactions.groupby('account_number')['amount'].agg(['mean', 'std'])

# Define threshold to classify accounts as high volume or low volume
threshold = 2

# Classify accounts as high volume or low volume
high_volume = grouped[(grouped['mean'] > threshold * grouped['std'])].index.tolist()
low_volume = grouped[(grouped['mean'] <= threshold * grouped['std'])].index.tolist()


import pymongo
import pandas as pd

# Connect to MongoDB database
client = pymongo.MongoClient("mongodb://localhost:27017/")
db = client["fundtrail"]
collection = db["transactions"]

# Get transaction data from MongoDB
transactions = pd.DataFrame(list(collection.find()))

# Calculate mean and standard deviation of deposit and withdrawal amounts for each account
grouped = transactions.groupby('account_number')['amount'].agg(['mean', 'std'])

# Define threshold to classify accounts as high volume or low volume
threshold = 2

# Classify accounts as high volume or low volume
high_volume = grouped[(grouped['mean'] > threshold * grouped['std'])].index.tolist()
low_volume = grouped[(grouped['mean'] <= threshold * grouped['std'])].index.tolist()

# Check for anomalies in transaction details
for account in high_volume:
    df = transactions[transactions['account_number'] == account]
    if (df['amount'] > 10000).any():
        print(f"Alert: High amount transaction detected for account {account}")

for account in low_volume:
    df = transactions[transactions['account_number'] == account]
    daily_amounts = df.groupby('transaction_date')['amount'].sum()
    if (daily_amounts > 5000).any():
        print(f"Alert: Unusual transaction amount detected for account {account}")