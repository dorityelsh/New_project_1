import yfinance as yf
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from scipy.stats import median_abs_deviation
from sklearn.ensemble import IsolationForest


# # Specify the ticker (for example Bitcoin in USD)
# ticker = "BTC-USD"  #"EURUSD=X"
method = 'isolation_forest'  # 'robust_z_score' or 'isolation_forest'
# # Fetch the data
# df = yf.download(ticker, 
#                  start="2021-01-01", 
#                  end="2025-11-13", 
#                  interval="1d",
#                 #  progress=False)

# Maybe save to CSV
# df.to_csv(ticker+'.csv')
file_path = "/Users/idan/Desktop/Dorit/Datasets/sea_level_3.csv"
# Read the CSV
df = pd.read_csv(file_path, encoding='latin1')


# explore and clean data  
df.info()
print(df.describe())
print(df.head())
print(df.isnull().sum())

df['Date'] = pd.to_datetime(df['Date'],format="%d/%m/%Y")
df = df.sort_values(by='Date', ascending=True)   # מהישן לחדש


# Plotting the time series
df = df.set_index('Date')

df['Level'].plot(figsize=(12,5))
plt.xlabel("Date")
plt.ylabel("Level")
plt.show()


# Plotting the distribution of values
plt.figure(figsize=(12,5))
sns.kdeplot(df['Level'].dropna(), fill=True, color='orange')
plt.show()

# Z-score based anomaly detection using Median Absolute Deviation (MAD)
# it is more robust to outliers than mean and standard deviation
# but it not a good choice for trends datasets
def robust_z_score(series):
    mad = median_abs_deviation(df['Level'])
    median = np.median(df['Level'])

    print(median)
    print(mad)

    def compute_robust_z_score(x):
        return .6745*(x-median)/mad

    df['z-score'] = df['Level'].apply(compute_robust_z_score)
    print(df.head())

    df['baseline'] = 1

    df.loc[df['z-score'] >= 3.5, 'baseline'] = -1
    df.loc[df['z-score'] <=-3.5, 'baseline'] = -1
    return df

def isolation_forest_anomaly_detection(df):

    iso_forest = IsolationForest(contamination=0.01, random_state=42)
    df['anomaly_if'] = iso_forest.fit_predict(df[['Level']])
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
            plt.plot(df.index, df['Level'], label='Level')
            plt.scatter(df[df['baseline']==-1].index,
                        df[df['baseline']==-1]['Level'],
                        marker='o',color= 'red', s=10, label='Anomaly')
            plt.legend()
            plt.show()
        plt_anomalies(df) 


def choose_method(method='isolation_forest'):
    if method == 'robust_z_score':
        robust_z_score(df)
    elif method == 'isolation_forest':
        isolation_forest_anomaly_detection(df)
    else:
        print("Unknown method")


choose_method('isolation_forest')       
check_anomalies(df)
print("end")

