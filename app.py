

import time  # to simulate a real time data, time loop
import yfinance as yf
import matplotlib.pyplot as plt
from matplotlib.pyplot import figure
import yahoo_fin.stock_info as si
import numpy as np  # np mean, np random
import pandas as pd  # read csv, df manipulation
import plotly.express as px  # interactive charts
import streamlit as st  # 🎈 data web app development

st.set_page_config(
    page_title="Real-Time Stock Price",
    page_icon="✅",
    layout="wide",
)


info = pd.read_csv('nasdaq.csv')



# dashboard title
st.title("Real-Time Stock Price")

# top-level filters
code = st.selectbox("Select the Job", pd.unique(info["Symbol"]))

# creating a single-element container
placeholder = st.empty()

# dataframe filter
data = yf.download(code,'2023-01-01','2023-12-31')
data = data.reset_index()
df = data


# near real-time / live feed simulation
for seconds in range(200):

    df['5D'] = df['Adj Close'].shift(5)
    df['10D'] = df['Adj Close'].shift(10)    # chnage 10, 20 days
    df['change'] = round((df['Adj Close'].diff() / df['Adj Close'].abs().shift(1))*100,2)
    df['price_vol'] = (df['Adj Close']/ df['Volume'])*10**7*2
    #df = df.drop(columns = ['Open', 'High', 'Low', 'Close'])
    df['w_5'] = round((df['Adj Close']/ df['5D'] -1)*100,2)
    df['w_10'] = round((df['Adj Close']/ df['10D'] -1)*100,2)
    df['p_10'] = df['Adj Close'] - df['10D']
    df['p_10'] = df['p_10'].apply(lambda x: round(x,2 ))


    df['v5D'] = df['Volume'].shift(5)
    df['v10D'] = df['Volume'].shift(10) # 10 , 20 days
    df['v_5'] = round((df['Volume']/ df['v5D'] -1)*100,6)
    # momentum 10 day purpose
    df['v_10'] = round((df['Volume']/ df['v10D'] -1)*100,6)
    buy_ratings = list(range(0,-10,-1)) # rolling 10 and this is 2x



    df['change_pct_1'] = round((df['w_5'].diff() / df['w_5'].abs().shift())*100,2)
    df['vol_pct_1'] = round((df['Volume'].diff() / df['Volume'].abs().shift())*100,2)
    df['vol_pct_2'] = round((df['vol_pct_1'].diff() / df['vol_pct_1'].abs().shift())*100,2)
    df['vol_pct_2_'] = df['vol_pct_2'].diff().fillna(df['Volume'])
    asign = np.sign(df['vol_pct_2_'] )
    signchange = ((np.roll(asign, 1) - asign) != 0).astype(int)
    df['sign_change'] = signchange



    df = df[['Date','Adj Close', 'Volume', '5D', 'w_5', 'v5D', 'v_5', 'v_10', 'p_10', 'w_10']]

    try:
        df = df.drop(df[df.v_10 == np.inf].index[0]).reset_index(drop = True)
    except:
        pass

    figure(figsize=(18, 6), dpi=80)
    v_10_range = df['v_10'].max() - df['v_10'].min()
    p_10_range = df['p_10'].max() - df['p_10'].min()
    df['v_10'] = df['v_10']/ v_10_range
    df['p_10'] = df['p_10']/ p_10_range
    df.index = df.Date
    
    fig, ax = plt.subplots()
    
    ax.plot(df['Date'], df['p_10'])
    ax.plot(df['Date'], df['v_10'])

    ax.hlines(y=0, xmin=df['Date'][0], xmax=df['Date'][-1],linewidth=2, color='r')
    st.pyplot(fig)

    
    time.sleep(3)
