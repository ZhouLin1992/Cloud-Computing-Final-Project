import os
import gzip

def parse(path):
	f = gzip.open(path, 'r')
	for line in f:
		yield eval(line)

dir_path = '/home/zhoulin/Desktop/Benthos/reviewInfo/'
if not os.path.isdir(dir_path):
	os.makedirs(dir_path)
input = '/home/zhoulin/Downloads/reviews_Beauty.json.gz'

r = 0 # reviewerID: 2023082
a = 0 # asin: 2023082
n = 0 # reviewerName: 2010957
t = 0 # reviewText: 2023082
o = 0 # overall: 2023082
s = 0 # summary: 2023082
time = 0 # reviewTime: 2023082

rd = parse(input)
for line in rd:
	if 'reviewerID' in line:
		r += 1
	if 'asin' in line:
		a += 1
	if 'reviewerName' in line:
		n += 1
		print(type(line['reviewerName']))
	if 'reviewText' in line:
		t += 1
	if 'overall' in line:
		o += 1
		print(type(line['overall']))
	if 'summary' in line:
		s += 1
	if 'reviewTime' in line:
		time += 1

print (r)
print (a)
print (n)
print (t)
print (o)
print (s)
print (time)