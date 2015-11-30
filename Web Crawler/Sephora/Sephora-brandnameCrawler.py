#!/usr/bin/python3

import urllib.request
from bs4 import BeautifulSoup
import re, io, gzip, os, time

result_path = '/home/python/Desktop/Sephora'
base_url = 'http://www.sephora.com'
lst_url = 'http://www.sephora.com/brand/list.jsp'
headers = {"Accept" : "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
           "Accept-Encoding" : "gzip, deflate, sdch",
           "Host" : "www.sephora.com",
           "Upgrade-Insecure-Requests" : "1",
           "User-Agent" : "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/46.0.2490.86 Safari/537.36"
            }

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

req = fectch_html(lst_url, 3)
soup = BeautifulSoup(req, 'lxml')
refine_lst = soup.find_all('a', {'class' : 'Nav-link'})
for link in refine_lst:
    print (link.contents)
    print (base_url + link['href'])

name = open (result_path + '/' + 'BrandName.txt', "r")
rd_name = name.readlines()
name.close()
link = open (result_path + '/' + 'BrandLink.txt', "r")
rd_link = link.readlines()
link.close()

text = open (result_path + '/' + 'BrandList' + '.txt', 'w')
for i in range(0, 277):
    name = rd_name[i]
    rename = name[2:(len(name)-3)]
    relink = rd_link[i]
    text.write(rename + '\n')
    text.write(relink)

# op_brandlist = open (result_path + '/' + 'BrandList' + '.txt', 'r')
# rd_brandlist = op_brandlist.readlines()
# op_brandlist.close()

# for i in range(0, 1):
#     link = rd_link[i]
#     print (link)
#     BrdAllAdd = link[:(len(link)-1)] + '?products=all'
#     print (BrdAllAdd)
#     BrdAllReq = fectch_html(BrdAllAdd, 3)
#     BrdAllSoup = BeautifulSoup(BrdAllReq, 'lxml')
#     # BrdAllFile = open (result_path + '/' + rd_name[i] + '.txt', 'a')
#     BrdAllResult = BrdAllSoup.find_all('a', {'ng-if': 'sku'})
#     print (BrdAllResult)
#     for line in BrdAllResult:
#         if line.has_attr('data-product_id'):
#             print (line['href'])


