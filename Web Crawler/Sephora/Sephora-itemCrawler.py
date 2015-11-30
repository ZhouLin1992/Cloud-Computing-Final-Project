from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from pyvirtualdisplay import Display
import unicodedata
import urllib.request
from bs4 import BeautifulSoup
import re, io, gzip, os, time

result_path = '/home/python/Desktop/Sephora'
base_url = 'www.sephora.com'

display = Display(visible=0, size=(800, 600)) # hide firefox browser
display.start()

rd = open (result_path + '/' + 'BrandList.txt', 'r') # read Brand address
rd_link = rd.readlines()
rd.close()

for i in range(0, 554):
    if (i % 2 == 0):
        # i = 96
        n = rd_link[i]
        name = n[:(len(n)-1)]
        dir_path = result_path + '/' + name
        if not os.path.isdir(dir_path):
            os.makedirs(dir_path) # create a directory for a brand
        l = rd_link[i + 1]
        address = l[:(len(l)-1)] + '?products=all&pageSize=-1'
        driver = webdriver.Firefox() # open firefox browser
        driver.get(address)
        # assert "Sephora" in driver.title
        elem = driver.page_source # fetch html
        driver.close()
        # unicodedata
        w = elem.encode('ascii', 'ignore')
        # parser
        parser = BeautifulSoup(w, 'lxml')
        # item name
        tag_div = parser.find_all('div')
        # item image
        tag_img = parser.find_all('img')
        # item price
        tag_price = parser.find_all('span')
        # item ratings
        tag_ratings = parser.find_all('div')
        # item info link
        tag_a = parser.find_all('a')
        # write item name into item_name.txt
        text_name = open (dir_path + '/item_name.txt', 'a')
        for line_div in tag_div:
            # print (line_div)
            if line_div.has_attr('class'):
                if line_div.has_attr('data-at'):
                    if line_div.has_attr('ng-bind-html'):
                        if (line_div.string != name):
                            text_name.write(line_div.string + '\n')
        text_name.close()
        # write item image link into item_image.txt
        text_image = open (dir_path + '/item_image.txt', 'a')
        for line_img in tag_img:
            if line_img.has_attr('class'):
                if line_img.has_attr('height'):
                    if line_img.has_attr('seph-lazy-src'):
                        if line_img.has_attr('src'):
                            if line_img.has_attr('width'):
                                text_image.write(base_url + line_img['seph-lazy-src'] + '\n')
        text_image.close()
        # write item price into item_price.txt
        text_price = open (dir_path + '/item_price.txt', 'a')
        for line_price in tag_price:
            if line_price.has_attr('class'):
                if line_price.has_attr('data-at'):
                    if (line_price.string != '0'):
                        if (line_price.string != 'How-To\'s'):
                            if (line_price.string != 'Quick Look'):
                                text_price.write(line_price.string + '\n')
        text_price.close()
        # write item ratings into item_ratings.txt
        text_ratings = open (dir_path + '/item_ratings.txt', 'a')
        for line_ratings in tag_ratings:
            if line_ratings.has_attr('ng-if'):
                if line_ratings.has_attr('seph-stars'):
                    if line_ratings.has_attr('class'):
                        text_ratings.write(line_ratings['seph-stars'] + '\n')
        text_ratings.close()
        # write item link into item_link.txt
        text_link = open (dir_path + '/item_link.txt', 'a')
        for line_a in tag_a:
            if line_a.has_attr('ng-repeat'):
                if line_a.has_attr('ng-if'):
                    if line_a.has_attr('href'):
                        if line_a.has_attr('data-at'):
                            if line_a.has_attr('data-product_id'):
                                if line_a.has_attr('class'):
                                    if line_a.has_attr('data-idx'):
                                        text_link.write(base_url + line_a['href'] + '\n')
        text_link.close()
