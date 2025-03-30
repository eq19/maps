## method for scraping bitcoinity
import requests
import json
import datetime
from app.apihandlers.classstructure import *

class BitcoinityScraper(Scraper):
	"""	Class for scraping Bitcoinity. Use its methods to draw data || Rihgt now just for public methods"""
	url = "https://data.bitcoinity.org/chart_data"
	
	data_type = "bidask_sum"
	currency = "USD"
	exchange = "bitfinex"
	compare = "no"
	bidask_percent = "1"
	bidask_unit = "curr"
	function = "none"
	timespan = "24h"
	groups_count = 10
	resolution = "minute"
	chart_type = "multi"
	smoothing = "linear"
	scale_type = "lin"

	def __init__(self):
		super(BitcoinityScraper, self).__init__()
		

	def get_params(self):
		#returns chart params in a dictionary format
		return {"data_type":self.data_type,"currency": self.currency,"exchange":self.exchange,
		"compare":self.compare,"bidask_percent":self.bidask_percent,"bidask_unit":self.bidask_unit,"function":self.function,"timespan":self.timespan,"groups_count":self.groups_count,"resolution":self.resolution,"chart_type":self.chart_type,"smoothing":self.smoothing,"scale_type":self.scale_type}

	def get_data(self):
		#returns chart data fetched through a post request
		response = requests.post(self.url, data=self.get_params())
		chartData = response.content
		# decodes receiving format to dictionary
		str_format = chartData.decode()
		json_acceptable_string = str_format.replace("'","\"")
		dict_format = json.loads(json_acceptable_string)
		return dict_format

	def example_params(self):
		return "tbd"


	#parser for the bidask data
	def parser_bidask(self, input_bidask):
		ask = input_bidask['data'][0]['values']
		bid = input_bidask['data'][1]['values']

		output_bid = []
		output_ask = []


		#turns array inputs into dictionaries
		for index, value in enumerate(ask):
		    
		    output_ask.append({str(value[0]):value[1]})

		for index, value in enumerate(bid):
		    
		    output_bid.append({str(value[0]):value[1]})

		return [output_ask,output_bid]



