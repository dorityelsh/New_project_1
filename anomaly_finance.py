import yfinance as yf
import pandas as pd
import matplotlib.pyplot as plt


# Specify the ticker (for example Bitcoin in USD)
ticker = "EURUSD=X"

# Fetch the data
df = yf.download(ticker, 
                 start="2017-01-01", 
                 end="2025-11-13", 
                 interval="1d",
                 progress=False)

# Maybe save to CSV
# df.to_csv("BTC_USD_history.csv")

# explore and clean data  
df.info()
print(df.describe())
print(df.head())

print(df.isnull().sum())


df['Close'].plot(figsize=(12,5))
plt.show()
