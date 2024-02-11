

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
    page_title="Build your MF Portfolio",
    page_icon="✅",
    layout="wide")

col1, col2, col3 = st.columns([1, 3, 1])

with col2:
    nse_df = pd.read_excel('nse_data.xlsx')
    nse_df = nse_df.head(50)
    
    nse_df['Symbol'] = [str(s) + '.NS' for s in nse_df['Symbol']]

    nse_df = nse_df.sort_values(by = 'Symbol')

    #info['Symbol'] = info['Symbol'] + '.NS'



# dashboard title
    st.title("Build your MF Portfolio")

# top-level filters
    x = pd.unique(nse_df["Symbol"])
    #x.sort()

    st.header('Choose 3 or more stocks to build your portfolio', divider='rainbow')

    chosen_stocks = []

    DEFAULT = '< PICK A VALUE >'

    #code1 = st.selectbox("Select the NSE Stock CODE :sunglasses:", x, key = 'code1' )
    #code2 = st.selectbox("Select the NSE Stock CODE :sunglasses:", x, key = 'code2' )
    #code3 = st.selectbox("Select the NSE Stock CODE :sunglasses:", x, key = 'code3' )
    #code4 = st.selectbox("Select the NSE Stock CODE :sunglasses:", x, key = 'code4')
    #code5 = st.selectbox("Select the NSE Stock CODE :sunglasses:", x, key = 'code5')
    codes = st.multiselect("Select the NSE Stock CODE :sunglasses:", x)
    #st.write('You selected:', list(codes))

    chosen_stocks = list(codes)

    s_date = datetime.datetime.now() - datetime.timedelta(days=365)
    s_date = s_date.strftime('%Y-%m-%d')
    e_date = datetime.datetime.today().strftime('%Y-%m-%d')

    #if ((code1 != DEFAULT) and (code2 != DEFAULT) and (code3 != DEFAULT) and (code4 != DEFAULT) and (code5 != DEFAULT)):
    #    pass
        

    #chosen_stocks = [str(code1), str(code2), str(code3), str(code4), str(code5)]

    #chosen_stocks = ['SBIN.NS', 'SIEMENS.NS', 'GODREJCP.NS', 'BAJFINANCE.NS', 'KOTAKBANK.NS']
    #st.write(chosen_stocks)

    if len(chosen_stocks) >= 3:
    #tickers = list(nse_df['Symbol'])[0:50]
        data = yf.download(
                #tickers = tickers,
                tickers= chosen_stocks,
                start=s_date,
                #end=date.today().replace(day=2),
                end = e_date,
                interval = "1d",
                group_by = 'ticker'
            )

        # Monthly shows data of last day of month
        # 

        data = data[[col for col in data.columns if col[1] == 'Adj Close' ]]
        #data = data.reset_index() 
        #st.dataframe(data)
        data.columns = data.columns.droplevel(1)
        data = data.T

        col_backup = data.columns

        data.columns = list(pd.Series(data.columns).apply(lambda x :  x.strftime('%Y-%m-%d')))

        ########## Mapping ###################
        #  120 : 10Y
        #    3 : 3M
        #    6 : 6 M
        #
        #   etc.
        #
        ##
        # drop stocks with lot of NAs

        drop_stocks = list(data.index[data.isna().sum(axis = 1) > 10])
        data = data.drop(index=drop_stocks)
        #data

        cdf = data.loc[chosen_stocks, :]

        # copy to show the table of chosen stocks

        chosen = cdf.copy()

        cdf = pd.DataFrame(cdf.mean(axis = 0))



        nifty = yf.download(
                tickers = '^NSEI',
                start=s_date,
                #end=date.today().replace(day=2),
                end = e_date,
                interval = "1d",
                group_by = 'ticker'
            )

        nifty = nifty['Adj Close']
        nifty = pd.DataFrame(nifty)
        nifty = nifty.reset_index()
        nifty['Date'] = nifty['Date'].apply(lambda x :  x.strftime('%Y-%m-%d'))
        nifty.columns = ['Date', 'NIFTY']
        #cdf['nifty'] = list(nifty)

        cdf = cdf.reset_index()
        cdf.columns = ['Date', 'Alpha']

        cdf = pd.merge(cdf, nifty)

        cdf['Alpha'] = round((100 / cdf['Alpha'][0])* cdf['Alpha'],1)
        cdf['NIFTY'] = round((100 / cdf['NIFTY'][0])* cdf['NIFTY'], 1)

        cdf = pd.melt(cdf, id_vars=['Date'], value_vars=['Alpha', 'NIFTY'])

        cdf.columns = ['Date', 'INDEX', 'PRICE']

        chosen = nse_df.loc[nse_df['Symbol'].isin(list(chosen.index)),'Company Name'].reset_index(drop = True)
        #st.header(' ## Chosen Stocks ' )
        st.table(chosen)


        fig = px.line(cdf, x="Date", y="PRICE", title='Alpha vs Nifty', color = 'INDEX',  color_discrete_sequence=['gray', 'blue'])
        #fig.show()  
        fig.update_layout(height=500)
        
        st.plotly_chart(fig, use_container_width=True, theme="streamlit")

    else:
        pass










