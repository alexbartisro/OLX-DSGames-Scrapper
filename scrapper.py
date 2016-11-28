from lxml import html
import time, requests, logging, pickle, os
from pushover import Client
from shutil import copyfile

logging.basicConfig(filename='scrapper.log',level=logging.DEBUG, format='%(asctime)s %(message)s')
url = 'https://www.olx.ro'
query = '/electronice-si-electrocasnice/jocuri-console/cluj-judet/q-ds/'

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

def compare(previousList, currentList):
	try:
		#return any(map(lambda v: v in list1, list2))
		for dict2 in currentList:
			for dict1 in previousList:
				if dict2["url"] != dict1["url"]:
					notify(dict2["name"], dict2["url"])
	except Exception as e:
		print e
		logging.error(e)

def notify(title, url):
	try:
		Client().send_message(url, title=title)
	except Exception as e:
		print e
		logging.error(e)

def run():
	previousList = read()
	currentList = scrap()
	if compare(previousList, currentList) is not True:
		logging.info('Lists are different')
	else:
		logging.info('Lists are identical')	
	write(currentList)

if __name__ == "__main__":
	while 1:
		run()
		time.sleep(3600)
