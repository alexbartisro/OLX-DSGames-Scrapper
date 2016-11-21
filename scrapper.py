from lxml import html
import time, requests, logging

page = requests.get('https://www.olx.ro/electronice-si-electrocasnice/jocuri-console/cluj-judet/q-ds/')
thefile = open('test.txt', 'w')

def scrap():
	try:
		tree = html.fromstring(page.content)
		post = tree.xpath('//*[@id="offers_table"]/tbody/tr/td/table/tbody/tr/td/a/img')
		for img in post:
			print(img.get('alt'), img.get('src'))
			#thefile.write("%s - %s\n" % img.get('alt'), img.get('src'))
	except Exception, e:
		print('Exception! Will continue execution.')
		logging.error('\r\nCould not scrap')
		logging.error('\r\n', e)


if __name__ == "__main__":
	while 1:
		scrap()
		time.sleep(3600)