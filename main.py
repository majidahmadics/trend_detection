# Import Dependencies
import yfinance as yf
import pandas as pd
import datetime as dt
import streamlit as st
import plotly.graph_objects as go

# Streamlit app
st.title('Stock Analysis')

# Get ticker input from user
ticker = st.text_input('Enter stock ticker:', 'AAPL')

# get today date using date time module
end_date = dt.date.today()

# Download historical data for the given ticker
data = yf.download(ticker, start='2020-01-01', end=end_date)

# Check if data is downloaded
if not data.empty:
    # Reset index to make 'Date' a column
    data.reset_index(inplace=True)

    # Select relevant columns
    data = data[['Date', 'Close']]

    # Sort by Date just in case
    data.sort_values('Date', inplace=True)

    # Set Date as the index
    data.set_index('Date', inplace=True)

    # Calculate the moving average
    data['Moving_Average'] = data['Close'].rolling(window=30).mean()

    # Drop missing values
    data.dropna(inplace=True)

    # Define Trend Prediction function
    def trend_prediction(data, days=7):
        n = 0
        for i in range(days):
            if data['Close'].iloc[-(i+1)] > data['Moving_Average'].iloc[-(i+1)]:
                n += 1
        if n > days // 2:
            return 'Increasing'
        else:
            return 'Decreasing'

    # Predict trend
    trend = trend_prediction(data)

    # Plot data using Plotly
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=data.index, y=data['Close'], mode='lines', name='Close Price'))
    fig.add_trace(go.Scatter(x=data.index, y=data['Moving_Average'], mode='lines', name='Moving Average'))

    # Customize the layout
    fig.update_layout(
        title=f'Stock Price and Moving Average for {ticker}',
        xaxis_title='Date',
        yaxis_title='Price',
        legend_title='Legend'
    )

    # Display the plot in Streamlit
    st.plotly_chart(fig)

    # Display trend prediction
    if trend == 'Increasing':
        st.success('The trend is increasing. It might be a good time to buy.')
    else:
        st.warning('The trend is decreasing. It might not be a good time to buy.')

else:
    st.error('Failed to fetch data for the provided ticker.')
