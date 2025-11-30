import yfinance as yf
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from scipy.stats import median_abs_deviation
from sklearn.ensemble import IsolationForest

# Define the time range for analysis
start_year = 2025
end_year = 2025
start_month=2
end_month=8
method = 'isolation_forest'  # 'robust_z_score' or 'isolation_forest'

# # Specify the ticker (for example Bitcoin in USD)
# ticker = "BTC-USD"  #"EURUSD=X"

# # Fetch the data
# df = yf.download(ticker, 
#                  start="2021-01-01", 
#                  end="2025-11-13", 
#                  interval="1d",
#                 #  progress=False)

# Maybe save to CSV
# df.to_csv(ticker+'.csv')
file_path = "/Users/idan/Desktop/Dorit/Anomaly_detection/steps.csv"
# Read the CSV
df = pd.read_csv(file_path, encoding='latin1')


# explore and clean data  
df.info()
print(df.describe())
print(df.head())
print(df.isnull().sum())

def order_file(df):
        df['startDate'] = pd.to_datetime(df['startDate'], errors='coerce')
        df["Date"] = df['startDate'].dt.date
        df_filtered = df[
            (df['startDate'].dt.year >= start_year) &
            (df['startDate'].dt.year <= end_year) &
            (df['startDate'].dt.month >= start_month) &
            (df['startDate'].dt.month <= end_month)]

        daily_df = df_filtered.groupby("Date")['steps'].sum().reset_index()
        daily_df = daily_df.sort_values(by='Date', ascending=True) 
        return daily_df

# df['Date'] = pd.to_datetime(df['Date'],format="%d/%m/%Y")
# df = df.sort_values(by='Date', ascending=True)   # מהישן לחדש

df = order_file(df)

# Plotting the time series
df = df.set_index('Date')

df['steps'].plot(figsize=(12,5))
plt.xlabel("Date")
plt.ylabel("steps")
plt.show()


# Plotting the distribution of values
plt.figure(figsize=(12,5))
sns.kdeplot(df['steps'].dropna(), fill=True, color='orange')
plt.show()

# Z-score based anomaly detection using Median Absolute Deviation (MAD)
# it is more robust to outliers than mean and standard deviation
# but it not a good choice for trends datasets
def robust_z_score(series):
    mad = median_abs_deviation(df['steps'])
    median = np.median(df['steps'])

    print(median)
    print(mad)

    def compute_robust_z_score(x):
        return .6745*(x-median)/mad

    df['z-score'] = df['steps'].apply(compute_robust_z_score)
    print(df.head())

    df['baseline'] = 1

    df.loc[df['z-score'] >= 3.5, 'baseline'] = -1
    df.loc[df['z-score'] <=-3.5, 'baseline'] = -1
    return df

def isolation_forest_anomaly_detection(df):

    iso_forest = IsolationForest(contamination=0.01, random_state=42)
    df['anomaly_if'] = iso_forest.fit_predict(df[['steps']])
    df['baseline'] = 1
    df.loc[df['anomaly_if'] == -1, 'baseline'] = -1
    return df


# Evaluation
def check_anomalies(df, column='baseline'):
    if df['baseline'].value_counts().shape[0] < 2:
        print("No anomalies detected.")
        return
    else:
        anomaly_rate = (df['baseline'] == -1).mean()
        print("Anomaly Rate:", anomaly_rate)
        def plt_anomalies(df):
            plt.figure(figsize=(12,5))
            plt.plot(df.index, df['steps'], label='steps')
            plt.scatter(df[df['baseline']==-1].index,
                        df[df['baseline']==-1]['steps'],
                        marker='o',color= 'red', s=10, label='Anomaly')
            plt.legend()
            plt.show()
        plt_anomalies(df) 


def choose_method(method):
    if method == 'robust_z_score':
        robust_z_score(df)
    elif method == 'isolation_forest':
        isolation_forest_anomaly_detection(df)
    else:
        print("Unknown method")


choose_method(method)       
check_anomalies(df)
print("end")

