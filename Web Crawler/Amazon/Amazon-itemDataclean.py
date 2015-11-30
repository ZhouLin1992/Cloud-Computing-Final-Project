path = '/home/python/Desktop/product-old-2/'
for productType in ['cleanser', 'eye cream', 'CC cream', 'moisturizer', 'night cream', 'sun care', 'toner']:
	for skinType in ['Combination', 'Dry', 'Oily', 'Normal']:
		address = path + productType + '/' + skinType + '.txt'
		f = open(address, "r")
		lines = f.readlines()
		print (lines)
		f.close()
		f = open(address,"w")
		for line in lines:
			if (not line.startswith('/s/')):
				if (line not in ["Image View\n", "Previous Page\n"]):
					print (line)
					f.write(line)
		# if (line not in ["Image View\n", "Previous Page\n"] or not line.startswith('/s/')):
		# 	print (line)
		# 	f.write(line)

		f.close()
