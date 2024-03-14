import streamlit as st
import pandas as pd
import numpy as np
import yfinance as yf
from pandas_datareader import data as pdr
import plotly.graph_objs as go
from plotly.subplots import make_subplots
import plotly.express as px
import matplotlib.pyplot as plt
import mplfinance as mpf
import matplotlib.dates as mdates
from streamlit_extras.metric_cards import style_metric_cards 
import requests_cache

import datetime
from datetime import datetime, timedelta


	## TO DO options container

st.set_page_config(layout="wide")



st.markdown("<h1 style='text-align: center; color: white;'>Dynamic Stock Performance Tracking Dashboard</h1>", unsafe_allow_html=True)
st.subheader('', divider = 'rainbow')
# Setting Cache

session = requests_cache.CachedSession('yfinance.cache')
session.headers['User-agent'] = 'my-program/1.0'

def load_data():
	yf.pdr_override()
	df = pdr.get_data_yahoo(ticker, start = start_date , end = end_date, session= session, interval=radio_choice)
	return df


		# Initialize session state variables
if 'start_date' not in st.session_state:
	st.session_state.start_date = None
if 'end_date' not in st.session_state:
	st.session_state.end_date = None



try:
  # error handling if ticker is blank or non exist
	with st.container(): # First container, stock name and time frame
		stock_name, space = st.columns((1,9))
	
		with stock_name:
			ticker = st.text_input(':blue[Enter Stock Ticker]', placeholder= 'example: AAPL', value = '')
	
	
			# back-programming
			stock_data = yf.Ticker(ticker, session = session)
			current_price = round(stock_data.fast_info['lastPrice'],2)
			yesterday_close = round(stock_data.history(period='2d')['Close'][0],2)

			#dividends
			dividends_df = pd.DataFrame(yf.Ticker(ticker).dividends)
			div_fig = px.line(dividends_df['Dividends'],title = f'{ticker} Dividends Cash Amount', template='simple_white')

			#earnings data frame , No null values
			earnings_df = pd.DataFrame(stock_data.earnings_dates)
			earnings_df = earnings_df.dropna()
			earnings_df['Change'] = earnings_df['Surprise(%)'].apply(lambda x: '🟢' if x > 0 else '🔴')

			#Cash Flow
			cashflow_df = pd.DataFrame(stock_data.cash_flow)




	
			#1 day
			price_diff = round(stock_data.fast_info['lastPrice'] - yesterday_close,4)
			price_diff_precent = abs(round((current_price/yesterday_close-1)*100,4)) # 1 day precent
	
			#1 month
			month_price = stock_data.history(period='1mo')['Close'][0]
			month_diff = round(stock_data.fast_info['lastPrice'] - month_price,4)
			month_diff_precent = round((current_price/month_price-1)*100,4)
	
			# ytd
			price_ytd = round(stock_data.history(period='ytd')['Close'][0],3)
			price_ytd_diff =  round(current_price - price_ytd, 4)
			price_ytd_diff_precent = round((current_price/price_ytd-1)*100,4)
	
			# 52 week range
			week52high = round(stock_data.history(period='1y')['High'].max(),2)
			week52low = round(stock_data.history(period='1y')['Low'].min(),2)
			week52text = str(week52low) + " -" + str(week52high)

			# Radio button selector state

	
			# Average Volume
			stock_avg_vol = stock_data.info['averageVolume']
	
			# Beta
			try:
				stock_beta = stock_data.info['beta']
			except:
				stock_beta = 'Not Available'
	
			# dividend yield
			try:
				dividendyield = str(round(stock_data.info['dividendYield']*100,4)) + "%"
			except:
				dividendyield = 'Not Available'


			#General Info Data

		
			try:
				company_name = stock_data.info['shortName']
			except:
				company_name = 'Not Available'

			
			try:
				industry = stock_data.info['industry']
			except:
				industry = 'Not Available'

			try:
				sector = stock_data.info['sector']
			except:
				sector = 'Not Available'

			try:
				website = stock_data.info['website']
			except:
				website = 'Not Available'

			try:
				num_employees = stock_data.info['fullTimeEmployees']
			except:
				num_employees = 'Not Available'

			try:
				country = stock_data.info['country']
			except:
				country = 'Not Available'

			try:
				num_analysts_rec = str(stock_data.info['numberOfAnalystOpinions'])
			except:
				num_analysts_rec = 'Not Available'

			general_data = {
    		'Attribute': ['Company Name', 'Industry', 'Sector', 'Country',"Number of Employees", 'Website', 'Num Analysts opinions'],
    		'Value': [company_name, sector, industry, country, num_employees, website, num_analysts_rec]}
	
	
	
			
			
	
	
			# plus or minus logic # 
			# if == plus >>> abs , else , no abs
	
	
			if current_price > yesterday_close:
				plusminus = "+"
				# 1 day
				price_diff = round(stock_data.fast_info['lastPrice'] - yesterday_close,4)
				price_diff_precent = abs(round((current_price/yesterday_close-1)*100,4))
	
			else:
				plusminus = "" # minus
	
				# 1 day
				price_diff_precent = round((current_price/yesterday_close-1)*100,4)
	
	
	
	
			if current_price > month_price:
				mplusminus = "+"
				#1 month
				month_diff = round(stock_data.fast_info['lastPrice'] - month_price,4)
				month_diff_precent = abs(round((current_price/month_price-1)*100,4))
	
			else:
				mplusminus = "" # minus
	
				# 1 month
				month_diff_precent = round((current_price/month_price-1)*100,4)
	
	
			if current_price > price_ytd:
	
				ytdplusminus = "+"
	
				price_ytd_diff =  abs(round(current_price - price_ytd, 4))
				price_ytd_diff_precent = abs(round((current_price/price_ytd-1)*100,4))
	
	
	
			else:
				ytdplusminus = ""
				price_ytd_diff =  round(current_price - price_ytd, 4)
				price_ytd_diff_precent = round((current_price/price_ytd-1)*100,4)
	
	

	
	

	st.subheader("") # space


	with st.container(): # 4 metrics: price, and price change 1D, 1M, YTD
		price_current, price_day_change, price_month_change, price_ytd = st.columns(4)
	
		with price_current:
			st.metric(label = 'Current Price', value = current_price, delta = "" )   ### DONE
	
		with price_day_change:
			st.metric(label = '1 Day Change', value = plusminus + str(price_diff), delta = str(price_diff_precent)+"%") # string concatination    ### DONE
	
		with price_month_change:
			st.metric(label = '1 Month Change', value = mplusminus + str(month_diff), delta = str(month_diff_precent) + "%") # DONE
	
		with price_ytd:
			st.metric(label = 'YTD Change', value = ytdplusminus + str(price_ytd_diff), delta = ytdplusminus + str(price_ytd_diff_precent) + "%") #DONE
	
	st.subheader("") # Virtual space
	
	with st.container(): # 4 second metrics: 52 week change, dividend yield, beta, average vol
	
		weekchange52, divyield, beta, avgvol = st.columns(4)
	
		with weekchange52: 
			st.metric(label = '52 week range', value = week52text, delta = "") # DONE
	
		with divyield:
			st.metric(label = 'Dividend Yield', value =dividendyield)
	
		with beta:
			st.metric(label = 'Beta', value = stock_beta)
	
		with avgvol:
			st.metric(label='Average Volume', value= stock_avg_vol)


	style_metric_cards(background_color = '#22242b' ,border_radius_px = 50,border_color = '#291757' , border_left_color = '#351d70')
	


	with st.container():

	 # options container
	
		st.subheader("") # space



		

		option = st.radio(
			":blue[Select]",
			["Chart", "General Info", 'Financials', 'Cash Flow', 'Dividends'])

		st.write('<style>div.row-widget.stRadio > div{flex-direction:row;}</style>', unsafe_allow_html=True) # horizontal radio hack

		if option == 'Cash Flow':

			st.dataframe(cashflow_df,
				use_container_width=True)

		if option == 'General Info':

			col1, col2 = st.columns(2)
			with col1:

				st.subheader('General Info')
				st.dataframe(general_data,
						use_container_width=True,
						hide_index=True
					 	)

			with col2:
				st.subheader('Earnings')
				st.dataframe(earnings_df,
					use_container_width=True)

		if option == 'Dividends':
			try:

				if len(yf.Ticker(ticker).dividends) > 0:
					st.plotly_chart(div_fig, use_container_width=True)

				else:
					st.write(f'Dividend chart is not available for {ticker}')


			except:
				st.write(f'Dividend chart is not available for {ticker}')

		if option == "Financials":

			with st.container():

				st.dataframe(stock_data.financials, use_container_width=True)


		if option == 'Chart':

			start, end, indicatorscol, timeframe = st.columns((0.5,0.5,0.8,3))

			with start:
				try:
					start_date = st.date_input(':blue[From]',
					value=datetime.today()- timedelta(days=365) , # 1 year from today()
					help = 'The start date of the chart',
					format="YYYY-MM-DD"
					)

				
					


					


				except:

					st.write('Something went wrong')

			with end:
				try:

					end_date= st.date_input(':blue[To]',
				 	value=datetime.today(),
				 	help = 'The end date of the chart',
				 	format="YYYY-MM-DD")

				except:

					st.write('Something went wrong')

			with timeframe:


				timeframe_radio_selector= st.radio(":blue[Candles Time Frame]",  ## Time Frame Radio 
					["Daily", "Weekly", "Monthly", "Quarterly"]
					)

				
				if timeframe_radio_selector == "Daily":

					radio_choice = '1d'

				elif timeframe_radio_selector == 'Weekly':
					radio_choice = '1wk'

				elif timeframe_radio_selector == 'Monthly':
					radio_choice = '1mo'

				elif timeframe_radio_selector == 'Quarterly':
					radio_choice = '3mo'

			with indicatorscol:
				indicators = st.multiselect(':blue[Indicators]',
				['20 MA', '50 MA', '100 MA','200 MA' , 'RSI'])








	
			df = load_data()
			df['20MA'] = df.Close.rolling(20).mean()
			df['50MA'] = df.Close.rolling(50).mean()
			df['100MA'] = df.Close.rolling(100).mean()
			df['200MA'] = df.Close.rolling(200).mean()





			# Create candlestick trace
			candlestick = go.Candlestick(
    			x=df.index, # dates
    			open=df['Open'],
    			high=df['High'],
   				low=df['Low'],
    			close=df['Close'],
    			#increasing_fillcolor='green',
    			#decreasing_fillcolor='red',
				)

			# Create layout
			layout = go.Layout(
    			title=f'{ticker} Stock Chart',
    			xaxis_title='Date',
    			yaxis_title='Price',
   				xaxis_rangeslider_visible=False, #idk its weird stuff. keep this false.
    			plot_bgcolor='rgba(0, 0, 0, 0)',  # Fully transparent background
      	paper_bgcolor='rgba(0, 0, 0, 0)',  # Fully transparent paper (outside plot area)
    			dragmode='zoom',
    			font=dict(
    				color='black',
    				size= 32)	
				)

			# Create figure and plot
			fig = go.Figure(data=[candlestick],
			layout=layout
			)



			
			fig.update_layout(
				title_font=dict(size=24)
			)

			for indicator in indicators:

				if indicator == "20 MA":
					fig.add_trace(go.Scatter(x=df.index, y = df['20MA'], mode = 'lines', name = '20MA'))

				elif indicator == "50 MA":
					fig.add_trace(go.Scatter(x=df.index, y = df['50MA'], mode = 'lines', name = '50MA'))

				elif indicator == "100 MA":
					fig.add_trace(go.Scatter(x=df.index, y = df['100MA'], mode = 'lines', name = '100MA'))

				elif indicator == "200 MA":
					fig.add_trace(go.Scatter(x=df.index, y = df['200MA'], mode = 'lines', name = '200MA'))

						

					






			if option == 'Chart':

				with st.container():
						st.plotly_chart(fig,
						use_container_width=True)

					
except:
	st.write('')


# Footer

footer="""<style>
a:link, a:visited {
  color: blue;
  background-color: transparent;
  text-decoration: underline;
}

a:hover, a:active {
  color: red;
  background-color: transparent;
  text-decoration: underline;
}

.footer {
  position: fixed;
  left: 0;
  bottom: 0;
  width: 100%;
  background-color: #22242b;
  color: white;
  text-align: center;
}
</style>

<div class="footer">
  <p style="font-size: 4px"> </p>
  <p style="font-size: 16px">
    Copyright © 2024 Itzhak Davidi <br>
    This project is for educational purposes only and should not be used for commercial purposes or distributed without permission.
  </p>
</div>
"""

st.markdown(footer, unsafe_allow_html=True)
