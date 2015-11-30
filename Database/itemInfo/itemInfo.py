import os
import gzip
from amazon.api import AmazonAPI

# Amazon products API keys
AMAZON_ACCESS_KEY = 'AKIAIYXEGNFLL2JWDBDA'
AMAZON_SECRET_KEY = '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'
AMAZON_ASSOC_TAG = 'Benthos-20'
amazon = AmazonAPI(AMAZON_ACCESS_KEY, AMAZON_SECRET_KEY, AMAZON_ASSOC_TAG)

def parse(path):
	f = gzip.open(path, 'r')
	for line in f:
		yield eval(line)

dir_path = '/home/zhoulin/Desktop/Benthos/itemInfo/'
if not os.path.isdir(dir_path):
	os.makedirs(dir_path)
input = '/home/zhoulin/Downloads/meta_Beauty.json.gz'

# products sum: 259204
rd = parse(input)
n = 0 # itemName: 258760
i = 0 # itemImage: 259116
d = 0 # description: 234497
p = 0 # price: 189930
b = 0 # brand: 128166
a = 0 # ASIN: 259204
r = 0 # salesrank: 254016
t = 0 # tag:

tag_seen = set()
tag_list = []
for line in rd:
	ASIN = line['asin']
	# use amazon API
	product = amazon.lookup(ItemId=ASIN)
	with open(dir_path + 'tag.txt', 'a') as w:
		if 'title' in line:
			itemName = line['title']
			print(type(itemName))
		else:
			itemName = 'null'
		if 'imUrl' in line:
			itemImage = line['imUrl']
			print(type(itemImage))
		else:
			itemImage = ' '
		if 'description' in line:
			description = line['description']
			print(type(description))
		else:
			description = 'This item is off shelf.'
		if 'price' in line:
			itemPrice = line['price']
			print(type(itemPrice))
		else:
			itemPrice = '0.0'
		if 'brand' in line:
			itemBrand = line['brand']
			print(itemBrand)
		else:
			itemBrand = 'null'
		if 'salesRank' in line:
			dictionary = line['salesRank']
			key = list(dictionary.values())
			# print(type(key[0]))
			r += 1
		if 'categories' in line:
			l = line['categories']
			l2 = l[0]
			for i in range(0, len(l2)):
				if l2[i] not in tag_seen:
					tag_seen.add(l2[i])
					tag_list.append(l2[i])
					t += 1
					w.write(l2[i] + '\n')
for i in range(0, len(tag_list)):
	print(tag_list[i])		
w.close()
		


		
		


