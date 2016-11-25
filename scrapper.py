from lxml import html
import time, requests, logging, pickle, os
from pushover import Client
from shutil import copyfile

logging.basicConfig(filename='scrapper.log',level=logging.DEBUG, format='%(asctime)s %(message)s')
url = 'https://www.olx.ro'
query = '/electronice-si-electrocasnice/jocuri-console/q-ds/'

def scrap():
	try:
		page = requests.get(url + query)
		tree = html.fromstring(page.content)
		post = tree.xpath('//*[@id="offers_table"]/tbody/tr/td/table/tbody/tr/td/div/h3/a')
		savedList = []
		for link in post:
			dictionary = {}
			dictionary["name"] = link.xpath('strong')[0].text
			dictionary["url"] = str(link.get('href'))
			savedList.append(dictionary)
		logging.info('Page scrapped.')
		return savedList
	except Exception, e:
		print('Exception! Will continue execution. \nCould not scrap\n')
		print e
		logging.error(e)

def write(myList):
	with open('persisted.txt', 'wb') as f:
		pickle.dump(myList, f)
	logging.info('List persisted.')

def read():
	try:
		with open('persisted.txt', 'rb') as f:
			return pickle.load(f)
		logging.info('List loaded.')
	except Exception as e:
		print e
		logging.error(e)

def compare(list1, list2):
	try:
		return any(map(lambda v: v in list1, list2))
	except Exception as e:
		print e
		logging.error(e)

def notify():
	try:
		Client().send_message("Au aparut anunturi noi", title="OLX Updatat")
	except Exception as e:
		print e
		logging.error(e)

def run():
	previousList = read()
	currentList = scrap()
	if compare(previousList, currentList) is not False:
		logging.info('Lists are different')
		notify()
	else:
		logging.info('Lists are identical')	
	write(currentList)

if __name__ == "__main__":
	while 1:
		run()
		time.sleep(3600)
