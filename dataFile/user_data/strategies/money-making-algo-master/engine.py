"""integrations from other applications"""
from app import app
from app.apihandlers import bitcoinity
from app import dbmanager

#python imports
import datetime
import json
import time
import sys

run = True

#initialize scrapers required for data scraping
s_bitcoinity = bitcoinity.BitcoinityScraper()

#Running timed draws of bid/ask spread
while run:
	data = s_bitcoinity.get_data()

	parsed_data = s_bitcoinity.parser_bidask(data)

	dbmanager.static_update_collection("bitcoinityAsk", parsed_data[0], 123)
	dbmanager.static_update_collection("bitcoinityBid", parsed_data[1], 123)
	user_choice = input("input s to stop:")
	if user_choice == "s":
		run = False