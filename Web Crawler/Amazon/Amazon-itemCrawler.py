import urllib.request
from bs4 import BeautifulSoup
import re, io, gzip, os, time

result_path = '/home/python/Desktop/product/'
headers = {"Accept":"text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
		   "Accept-Encoding":"gzip",
		   "User-Agent":"Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/46.0.2490.71 Safari/537.36"
		  }
if not os.path.exists(result_path): #create/open "product" file
	os.makedirs(result_path)

base_url = 'http://www.amazon.com'
search_url = 'http://www.amazon.com/s/url=search-alias%3Dbeauty&field-keywords='

def fectch_html(url, retry=3): #unzip html
	attempts = 0
	while attempts < retry:
		try:
			req = urllib.request.Request(url, headers = headers)
			response = urllib.request.urlopen(req)
			# accept encoding is gzip, decode to get the actual html
			bi = io.BytesIO(response.read())
			gf = gzip.GzipFile(fileobj = bi, mode = 'rb')
			return gf.read()

		except Exception as e:
			print(str(e))	
			attempts += 1
			time.sleep(1)
	return ""


for keyword in ['cleanser', 'sun care', 'toner', 'makeup remover', 'moisturizer', \
				'night cream', 'BB cream', 'CC cream', 'eye cream', 'facial mask', \
				 'men face wash', 'exfoliator', 'night cream', 'cleaning oil', 'face mist']:
	product_dict = {}  #{skintype_tag:link}
	keyword_path = result_path + keyword 
	if not os.path.exists(keyword_path):
		os.makedirs(keyword_path)  #create/open a specific product file
	
	keyword_response = fectch_html(search_url + keyword, 3)
	#print (search_url + keyword)
	tag_parser = BeautifulSoup(keyword_response, 'lxml') #html parser
	for skintype_tag in ['Normal', 'Oily', 'Combination', 'Dry']:
		#text_file = open(keyword_path + '/' + skintype_tag + '.txt', 'w')
		text_file = open (keyword_path + '/' + keyword + '.txt', 'a')
		skintype_tag_span = tag_parser.find('span', text = skintype_tag) #find skintype_tag span
		if skintype_tag_span:
			s_tag = skintype_tag_span.string #get content of span
			tag_link = base_url + skintype_tag_span.parent['href'] #get link of skintype_tag
			# print(s_tag)
			# print(tag_link)
			product_dict.update({s_tag:tag_link})
			#print(product_dict)
			next_page = tag_link
			page = 1
			while(next_page != base_url):
				skintype_tag_html = fectch_html(next_page) #convert to html
				parser = BeautifulSoup(skintype_tag_html, 'lxml')
				result_list = parser.find_all('a')
				for link in result_list:
					if link.has_attr('title'):
						if link['title'] != 'Next Page':
							skin_type_text = open (keyword_path + '/' + skintype_tag + '.txt', 'a')
							skin_type_text.write(link['title'] + "\n")
							# print (link['title'])
							skin_type_text.write(link['href'] + "\n")
							# print (link['href'])
						else:
						 	next_page = base_url + link['href']
				print(keyword + " " + skintype_tag + " page " + str(page))
				page += 1
				if not parser.find(id="pagnNextLink"):
					break

	print (product_dict)
	text_file.write(str(product_dict))





	# 		tag_list.append(tag_parser.find('a', text = "skintype_tag"))
	# for link in tag_list:
	# 	print (link(['href']))

