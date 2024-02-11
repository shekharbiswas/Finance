

import time  # to simulate a real time data, time loop
import yfinance as yf
import matplotlib.pyplot as plt
from matplotlib.pyplot import figure
import yahoo_fin.stock_info as si
import numpy as np  # np mean, np random
import pandas as pd  # read csv, df manipulation
import plotly.express as px  # interactive charts
import streamlit as st  # 🎈 data web app development
import datetime

st.set_page_config(
    page_title="Momentum Stocks - NSE ",
    page_icon="✅",
    layout="wide")

col1, col2, col3 = st.columns([1, 3, 1])

with col2:
    nse_df = pd.read_excel('nse_data.xlsx')
    nse_df = nse_df.head(100)
    
    nse_df['Symbol'] = [str(s) + '.NS' for s in nse_df['Symbol']]

    st.title("Momentum Stocks - NSE ")

    st.header('Top stocks showing most momentum', divider='rainbow')


    st.write('Select window of at least 1 week')

    today = datetime.datetime.now()
    window_day = today - datetime.timedelta(days=7)
    c_start = datetime.datetime.now() - datetime.timedelta(days=365)
    c_end = datetime.datetime.today()

    d = st.date_input(
        "Select your vacation for next year",
        (window_day, today),
        c_start,
        c_end,
        format="DD.MM.YYYY",
    )
    

    st.write(d)


    s_date = datetime.datetime.now() - datetime.timedelta(days=365)
    s_date = s_date.strftime('%Y-%m-%d')
    e_date = datetime.datetime.today().strftime('%Y-%m-%d')


    



