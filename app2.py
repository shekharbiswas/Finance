

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
    nse_df = nse_df.head(1000)
    
    nse_df['Symbol'] = [str(s) + '.NS' for s in nse_df['Symbol']]
    tickers = list(pd.unique(nse_df['Symbol']))

    st.title("Momentum Stocks - NSE ")

    st.header('Top stocks showing most momentum', divider='rainbow')


    st.subheader('The date range should be at least 1 week')

    today = datetime.datetime.now()
    window_day = today - datetime.timedelta(days=6)
    c_start = datetime.datetime.now() - datetime.timedelta(days=365)
    c_end = datetime.datetime.today()

    d = st.date_input(
        "Check Momentum stocks for a Time Frame ",
        (window_day, today),
        c_start,
        c_end,
        format="DD.MM.YYYY",
    )
    

    #st.write(d[0])
    #st.write(d[1])


    #s_date = datetime.datetime.now() - datetime.timedelta(days=365)
    
    s_date = d[0].strftime('%Y-%m-%d')
    e_date = d[1].strftime('%Y-%m-%d')

    #st.write(s_date , e_date)

    if (d[1] - d[0]) >= datetime.timedelta(days=4) :

        #st.write('7 days')

        

        with st.spinner('Loading data...'):
            data = yf.download(
                tickers = tickers,
                start=s_date,
                #end=date.today().replace(day=2),
                end = e_date,
                interval = "1d",
                group_by = 'ticker'
            )
        
        # Monthly shows data of last day of month

        data = data[[col for col in data.columns if col[1] == 'Adj Close' ]]
        #data = data.reset_index() 
        data.columns = data.columns.droplevel(1)
        data = data.T

        col_backup = data.columns

        data.columns = list(pd.Series(data.columns).apply(lambda x :  x.strftime('%Y-%m-%d')))

        drop_stocks = list(data.index[data.isna().sum(axis = 1) > 10])
        data = data.drop(index=drop_stocks)


        data['diff'] = round(100*(data[data.columns[-1]] / data[data.columns[0]] - 1))
        data = data.sort_values(by = 'diff', ascending= False)

        data = data.dropna()

        data = data.reset_index()

        


        data['diff'] = data['diff'].astype(int)
        
        data = data.head(10)
        data['index'] = data['index'].str.split('.', n = 1, expand=True)[0]

        data = data.rename(columns = {'diff' : '% Increase'})

        tab1, tab2 = st.tabs(["📈 Chart", "🗃 Data"])

        
        st.write("\n \n ")

        with tab1:

            fig = px.scatter(data, x=data.columns[-2], y='% Increase',
	             size="% Increase", size_max=60, text="index", color = '% Increase', log_x=True)

            fig.update_layout(height=700)
            fig.update_traces( hovertemplate=None)
            fig.update_layout(hovermode="x")

            st.plotly_chart(fig, use_container_width=True, theme= 'streamlit')

        with tab2:
            st.dataframe(data[['index', '% Increase']])












    




