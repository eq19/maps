#class structures for the project
from abc import ABC, abstractmethod

class Scraper(ABC):
	"""Abstract Base Class for Scrapers. Requires three methods:
	get_params: returns a dictionary of the current params
	example_params: returns type and examples of the required params
	get_data: returns the data from the request. Ideally also describes the data received
	"""
	def __init__(self):
		super().__init__()
	

	@abstractmethod
	def get_params(self):
		"""get_params: returns a dictionary of the current params"""

	@abstractmethod
	def example_params(self): 
		"""example_params: returns type and examples of the required params"""

	@abstractmethod
	def get_data(self):
		"""get_data: returns the data from the request. Ideally also describes the data received"""
