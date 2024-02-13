

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
    page_title="Analyze Stocks - NSE ",
    page_icon="✅",
    layout="wide")

col1, col2, col3 = st.columns([1, 3, 1])

with col2:
    nse_df = pd.read_excel('nse_data.xlsx')
    nse_df = nse_df.head(500)
    
    nse_df['Symbol'] = [str(s) + '.NS' for s in nse_df['Symbol']]

    x = list(pd.unique(nse_df['Symbol'] ))
    x.remove('HDFC.NS')

    code = st.selectbox("Select the NSE Stock CODE :sunglasses:", x)
    st.write('You selected:', code)

    chosen_stocks = code




    st.title("Analysis Stocks - NSE ")

    st.header('Check the public sentiment before investing at your own risk', divider='rainbow')


    st.subheader('The date range should be at least 1 month')

    today = datetime.datetime.now()
    window_day = today - datetime.timedelta(days=30)
    c_start = datetime.datetime.now() - datetime.timedelta(days=730)
    c_end = datetime.datetime.today()

    d = st.date_input(
        "Select a Time Frame ( >= 30 days ) ",
        (window_day, today),
        c_start,
        c_end,
        format="DD.MM.YYYY",
    )

    
    try:
        if (d[0] and d[1]):
            s_date = d[0].strftime('%Y-%m-%d')
            e_date = d[1].strftime('%Y-%m-%d')

    #st.write(s_date , e_date)

            if (d[1] - d[0]) >= datetime.timedelta(days=30) :

                #st.write('7 days')

                with st.spinner('Analyzing data...'):
                    df = yf.download(
                        tickers = chosen_stocks,
                        start=s_date,
                        #end=date.today().replace(day=2),
                        end = e_date,
                        interval = "1d",
                        threads=True,
                        group_by = 'ticker'
                    )


                    nifty = yf.download(
                        tickers = '^NSEI',
                        start=s_date,
                        #end=date.today().replace(day=2),
                        end = e_date,
                        interval = "1d",
                        threads=True,
                        group_by = 'ticker'
                    )

                # Monthly shows data of last day of month
                    
                df = df[['Adj Close', 'Volume']]
                df.columns = ['Price', 'Vol']


                # resample 

                #df = df.resample('5d').mean()
                #nifty = nifty.resample('5d').mean()



                df['P5'] = df['Price'].shift(5)
                df['V5'] = df['Vol'].shift(5)

                df['PC'] = df['Price'] - df['P5']
                df['VC'] = df['Vol'] - df['V5']


                df['N50'] = nifty['Adj Close']

                df = df[df['Vol'] != 0]

                tab1, tab2, tab3= st.tabs(["📈 Chart", "📈 Vol Chart", "🗃 Data"])


                with tab1:

                    import plotly.graph_objects as go

                    fig = go.Figure()

                    fig.add_trace(
                        go.Scatter(
                            x=list(df.index),
                            y=df['Price'],
                            name = 'Price'
                        ))

                    fig.add_trace(
                        go.Bar(
                            x=list(df.index),
                            y=df['Vol']//(df['Vol'].max() / (df['Price'].max() -df['Price'].min())) + df['Price'].min()  ,
                            opacity=0.1,
                            name = 'Volume',
                            hoverinfo='none'
                        ))

                    fig.update_layout(yaxis={"range":[df['Price'].min(), df['Price'].max()]})



                    #fig.show()



                    
                    #fig.add_trace(
                    #    go.Scatter(
                    #        x=list(df.index),
                    #        y=df['Price'],
                    #        name = 'Price'
                    #    ))

                    #fig.add_trace(
                    #    go.Bar(
                    #        x=list(df.index),
                    #        y=df['Vol']//(df['Vol'].max() / df['Price'].max()) ,
                    #        opacity=0.1,
                    #        name = 'Volume'
                    #    ))

                    #fig = px.line(df.reset_index() , x='Date', y='Price', markers=True)
                    #fig.show()

                    #fig.update_layout(height=600)
                    #fig.update_traces( hovertemplate=None)
                    #fig.update_layout(hovermode="x")

                    st.plotly_chart(fig, use_container_width=True, theme= 'streamlit')

                with tab2:
                    fig = px.bar(df.reset_index(), x='Date', y='Vol')
                    st.plotly_chart(fig, use_container_width=True, theme= 'streamlit')

                with tab3:
                    pass





                


    except:
        pass

















