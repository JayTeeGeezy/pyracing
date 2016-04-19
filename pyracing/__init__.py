from .common import Entity
from .meet import Meet
from .race import Race


def initialize(database, scraper):
	"""Initialize package dependencies

	database must be an object representing a database connection that conforms to the pymongo API, supporting code such as the following:
	documents = database[collection_name].find(filter)

	scraper must be an object that conforms to the pypunters.Scraper API, supporting code such as the following:
	meets = scraper.scrape_meets(date)
	"""

	Entity.database = database
	Entity.scraper = scraper