#tradeblock chart scraper
import requests
import datetime
from app.apihandlers.classstructure import *

class TradeblockScraper(Scraper):
	"""Tradeblock Scraper scrapes information from tradeblock through their get responses. This currently only works for their chart data"""
	# Example get request
	#"https://tradeblock.com/api/markets/ohlcv/bfnx/eth-usd/?start=1509528977000&end=1512768977000&period=1h"

	page_to_draw = "ohlcv"
	# bfnx, stmp
	exchange = "bfnx"
	#examples include xbt-usd
	curr_pair = "eth-usd"
	#start time and end time in "Unix" datetime format (/1000 from Javascript)
	start_time = datetime.datetime.fromtimestamp(1509528977)
	end_time = datetime.datetime.fromtimestamp(1512768977)
	period = "1h"

	def __init__(self):
		super(TradeblockScraper, self).__init__()
		print("Params: ",self.get_params())
	
	def get_params(self):
		#returns params in a dictionary format
		return {"page_to_draw":self.page_to_draw,"exchange":self.exchange,"curr_pair":self.curr_pair,"start_time": self.start_time, "end_time":self.end_time}

	def get_data(self):
		#fetches data from tradeblock thorugh get request
		get_request = 'https://tradeblock.com/api/markets/{}/{}/{}/?start={}&end={}&period={}'.format(self.page_to_draw, self.exchange, self.curr_pair, self.start_time.timestamp()*1000, self.end_time.timestamp()*1000,self.period)
		response = requests.get(get_request)
		return response.content

	def example_params(self):
		return "tbd"