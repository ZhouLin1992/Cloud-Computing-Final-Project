import mysql.connector
from random import *
import random
import names
import string
import time
import gzip
from amazon.api import AmazonAPI
import os

# Amazon product API Key
AMAZON_ACCESS_KEY = 'AKIAIYXEGNFLL2JWDBDA'
AMAZON_SECRET_KEY = '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'
AMAZON_ASSOC_TAG = 'Benthos-20'
amazon = AmazonAPI(AMAZON_ACCESS_KEY, AMAZON_SECRET_KEY, AMAZON_ASSOC_TAG)

# unzip json file
def parse(path):
  g = gzip.open(path, 'r')
  for l in g:
    yield eval(l)

zl = mysql.connector.connect(user='zl', password='2290', host='127.0.0.1', database='Benthos')
cursor = zl.cursor()

# cursor.execute("DROP DATABASE IF EXISTS Benthos")
# cursor.execute("CREATE DATABASE Benthos")
cursor.execute("USE Benthos")

tables = []

# # drop existed productDB table
# cursor.execute("DROP TABLE IF EXISTS productDB")

#------------------create table------------------------
# create item table
tables.append(
  "CREATE TABLE `productTable` ("
  "  `productID` int(50) NOT NULL AUTO_INCREMENT,"
  "  `ASIN` varchar(100) NOT NULL,"
  "  `itemName` varchar(300) NOT NULL,"
  "  `itemImage` varchar(300) NOT NULL,"
  "  `itemPrice` float(10) NOT NULL,"
  "  `itemBrand` varchar(100) NOT NULL,"
  "  `description` text(2000) NOT NULL,"
  "  `itemRank` int(50) NOT NULL,"
  "  `itemRating` tinyint NOT NULL,"
  "  PRIMARY KEY (`productID`)"
  ") ENGINE=InnoDB")

# # create product table
# tables.append(
#   "CREATE TABLE `productDB` ("
#   "  `productID` int(10) NOT NULL AUTO_INCREMENT,"
#   "  `weatherCH` tinyint NOT NULL,"
#   "  `weatherDW` tinyint NOT NULL,"
#   "  `gender` int(2) NOT NULL,"
#   "  `age` tinyint NOT NULL,"
#   "  `stCombination` tinyint NOT NULL,"
#   "  `stNormal` tinyint NOT NULL,"
#   "  `stDry` tinyint NOT NULL,"
#   "  `stOily` tinyint NOT NULL,"
#   "  `productName` varchar(300),"
#   "  `productLink` varchar(300),"
#   "  PRIMARY KEY (`productID`)"
#   ") ENGINE=InnoDB")

# create user information table
tables.append(
  "CREATE TABLE `userTable` ("
  "  `userID` int(10) NOT NULL AUTO_INCREMENT,"
  "  `reviewerID` varchar(50) NOT NULL,"
  "  `reviewerName` varchar(50) NOT NULL,"
  "  `email` varchar(255) NOT NULL,"  
  "  `password` varchar(34) NOT NULL,"
  "  PRIMARY KEY (`userID`)"
  ") ENGINE=InnoDB")

# create review table
tables.append(
  "CREATE TABLE `reviewTable` ("
  "  `recordID` int NOT NULL AUTO_INCREMENT PRIMARY KEY,"
  "  `reviewerID` varchar(50) NOT NULL,"
  "  `ASIN` varchar(100) NOT NULL,"
  "  `reviewText` text(2000) NOT NULL,"
  "  `rating` int(10) NOT NULL,"
  "  `summary` varchar(1000) NOT NULL,"
  "  `reviewTime` varchar(1000) NOT NULL,"
  "  FOREIGN KEY (`reviewerID`) REFERENCES `userTable` (`reviewerID`) "
  "  ON DELETE CASCADE ON UPDATE CASCADE," 
  "  FOREIGN KEY (`ASIN`) REFERENCES `itemTable` (`ASIN`) "
  "  ON DELETE CASCADE ON UPDATE CASCADE"   
  ") ENGINE=InnoDB")

# # create user behavior table
# tables.append(
#   "CREATE TABLE `userDB` ("
#   "  `recordID` int NOT NULL AUTO_INCREMENT PRIMARY KEY,"
#   "  `userID` int(10) NOT NULL," # userID is foreign key
#   "  `weatherCH` tinyint NOT NULL,"   #todo
#   "  `weatherDW` tinyint NOT NULL,"   #todo
#   "  `gender` int(2) NOT NULL,"
#   "  `age` tinyint NOT NULL,"
#   "  `stCombination` tinyint NOT NULL,"
#   "  `stNormal` tinyint NOT NULL,"
#   "  `stDry` tinyint NOT NULL,"
#   "  `stOily` tinyint NOT NULL,"
#   "  `productID` int(10) NOT NULL," #productID is foreign key
#   "  `ratings` tinyint NOT NULL,"
#   "  FOREIGN KEY (`userID`) REFERENCES `nameDB` (`userID`) "
#   "  ON DELETE CASCADE ON UPDATE CASCADE," 
#   "  FOREIGN KEY (`productID`) REFERENCES `productDB` (`productID`) "
#   "  ON DELETE CASCADE ON UPDATE CASCADE"   
#   ") ENGINE=InnoDB")

tables.append(
  "CREATE TABLE `similarityTable` ("
  "  `similarityID` int NOT NULL AUTO_INCREMENT PRIMARY KEY,"
  "  `ASIN1` varchar(100) NOT NULL,"
  "  `ASIN2` varchar(100) NOT NULL,"
  "  FOREIGN KEY (`ASIN1`) REFERENCES `itemTable` (`ASIN`) "
  "  ON DELETE CASCADE ON UPDATE CASCADE," 
  "  FOREIGN KEY (`ASIN2`) REFERENCES `itemTable` (`ASIN`) "
  "  ON DELETE CASCADE ON UPDATE CASCADE"   
  ") ENGINE=InnoDB")

for t in tables:
    try:
      cursor.execute(t)
    except mysql.connector.errors.ProgrammingError:
      # ignore
      pass

#--------------------insert data into table-------------------------

# Insert data into item table
add_itemTable = ("INSERT INTO productTable "
               "(ASIN, itemName, itemImage, itemPrice, \
                itemBrand, description, itemRank, itemRating) "
               "VALUES (%(ASIN)s, %(itemName)s, %(itemImage)s, \
                %(itemPrice)s, %(itemBrand)s, %(description)s, \
                %(itemRank)s, %(itemRating)s)")

input = "/home/zhoulin/Downloads/meta_Beauty.json.gz"
# use average result from MapReduce
path = '/home/zhoulin/AvgResult/part-r-00000'
r = open(path, 'r')
lns = r.readlines()
output = parse(input)
for line in output:
  ASIN_value = line['asin']
  product = amazon.lookup(ItemId = ASIN_value)
  tuple_price = product.price_and_currency
  itemPrice_value = tuple_price[0]
  if 'title' in line:
    itemName_value = line['title']
  else:
    itemName_value = 'null'
  if 'imUrl' in line:
    itemImage_value = line['imUrl']
  else:
    itemImage_value = ' '
  if 'description' in line:
    description_value = line['description']
  else:
    description_value = 'This item is off shelf.'
  if 'price' in line:
    itemPrice_value = line['price']
  else:
    itemPrice_value = 0.0
  if 'brand' in line:
    itemBrand_value = line['brand']
  else:
    itemBrand_value = 'null'
  if 'salesRank' in line:
    dic = line['salesRank']
    key = list(dic.values())
    itemRank_value = key[0]
    i += 1
  else:
    itemRank_value = 0
    pass
  for lines in lns:
    a = lines.split('\t')
    if a[0] == line['asin']:
      itemRating_value = int(float(a[1]))
    else:
      itemRating_value = 0
  # itemRating_value = random.randrange(0, 6)
  # itemRank_value = random.randrange(1, 1000000)

  data_itemTable = {
                  'ASIN': ASIN_value,
                  'itemName': itemName_value,
                  'itemImage': itemImage_value,
                  'itemPrice': itemPrice_value,
                  'itemBrand': itemBrand_value,
                  'description': description_value,
                  'itemRank': itemRank_value,
                  'itemRating': itemRating_value,
                  }
  cursor.execute(add_itemTable, data_itemTable)
  zl.commit()


# # Partly insert randomly-generated data into product table
# add_productDB = ("INSERT INTO productDB "
#                "(weatherCH, weatherDW, gender, age, \
#                	stCombination, stNormal, stDry, stOily, \
#                 productName, productLink) "
#                "VALUES (%(weatherCH)s, %(weatherDW)s, \
#                	%(gender)s, %(age)s, %(stCombination)s, \
#                	%(stNormal)s, %(stDry)s, %(stOily)s, \
#                 %(productName)s, %(productLink)s)")

# path = '/home/python/Desktop/product-old-2/'
# for productType in ['cleanser', 'eye cream', 'CC cream', \
#                     'moisturizer', 'night cream', 'sun care', \
#                     'toner']:
#     for skinType in ['Combination', 'Dry', 'Oily', 'Normal']:
#         address = path + productType + '/' + skinType + '.txt'
#         f = open(address, "r")
#         lines = f.readlines()
#         f.close()
#         num = 0
#         for line in lines:
#             if (not line.startswith('http://')):
#                 productName_value = line
#                 num += 1
#             else:
#                 productLink_value = line
#                 num += 1
#             if (num % 2 == 0):
#                 weatherCH_value = random.randrange(3)
#                 weatherDW_value = random.randrange(3)
#                 gender_value = 0
#                 age_value = random.randrange(6)
#                 stCombination_value = random.randrange(5)
#                 stNormal_value = random.randrange(5)
#                 stDry_value = random.randrange(5)
#                 stOily_value = random.randrange(5)
#                 data_product = {
#                   'weatherCH': weatherCH_value,
#                   'weatherDW': weatherDW_value,
#                   'gender': gender_value,
#                   'age': age_value,
#                   'stCombination': stCombination_value,
#                   'stNormal': stNormal_value,
#                   'stDry': stDry_value,
#                   'stOily': stOily_value,
#                   'productName': productName_value,
#                   'productLink': productLink_value,
#                   }
#                 cursor.execute(add_productDB, data_product)
#                 zl.commit()

##----------random name & email & password generator-------------------

# random email generator
domains = [ "hotmail.com", "gmail.com", "aol.com", \
            "mail.com" , "mail.kz", "yahoo.com"]
letters = [ "a", "b", "c", "d","e", "f", "g", "h", \
            "i", "j", "k", "l", "m", "n", "o", "p", \
            "q", "r", "s", "t", "u", "v", "w", "x", "y", "z"]

def get_one_random_domain(domains):
        return domains[random.randint( 0, len(domains)-1)]

def get_one_random_name(letters):
    email_name = ""
    for i in range(7):
        email_name = email_name + letters[random.randint(0,11)]
    return email_name

def generate_random_emails():
    one_name = str(get_one_random_name(letters))
    one_domain = str(get_one_random_domain(domains))         
    email_address = one_name + "@" + one_domain
    return email_address

#print (generate_random_emails())

# random password generator
def password_generator():
    characters = string.ascii_letters + string.punctuation + string.digits
    password =  "".join(choice(characters) for x in range(randint(8, 16)))
    return password

# Insert data into user table
add_userTable = ("INSERT INTO userTable "
           "(reviewerID, reviewerName, email, password) "
           "VALUES (%(reviewerID)s, %(reviewerName)s, \
            %(email)s, %(password)s)")

infile = "/home/zhoulin/Downloads/reviews_Beauty.json.gz"
outfile = parse(infile)
ID_seen = set()
i = 0
for line in outfile:
  if line['reviewerID'] not in ID_seen:
    reviewerID_value = line['reviewerID']
    ID_seen.add(line['reviewerID'])
    if 'reviewerName' in line:
      reviewerName_value = line['reviewerName']
    else:
      i += 1
      reviewerName_value = 'Anonymous' + str(i)
    email_value = generate_random_emails()
    password_value = password_generator()
    data_userTable = {
                    'reviewerID': reviewerID_value,
                    'reviewerName': reviewerName_value,
                    'email': email_value,
                    'password': password_value,
                    }
    cursor.execute(add_userTable, data_userTable)
    zl.commit()

# for nameDB_i in range(0,5000):   # number of users
#     firstname_value = names.get_first_name(gender = 'female')
#     lastname_value = names.get_last_name()
#     email_value = generate_random_emails()
#     password_value = password_generator()
#     data_name = {
#                 'firstname': firstname_value,
#                 'lastname': lastname_value,
#                 'email': email_value,
#                 'password': password_value, 
#                 }
#     cursor.execute(add_name, data_name)
#     zl.commit()

# Insert data into review table
add_reviewTable = ("INSERT INTO reviewTable "
               "(reviewerID, ASIN, reviewText, rating, \
                summary, reviewTime) "
               "VALUES (%(reviewerID)s, %(ASIN)s, %(reviewText)s, \
                %(rating)s, %(summary)s, %(reviewTime)s)")

for ln in outfile:
  reviewerID_value = ln['reviewerID']
  ASIN_value = ln['asin']
  reviewText_value = ln['reviewText']
  rating_value = int(ln['overall'])
  summary_value = ln['summary']
  reviewTime_value = ln['reviewTime']
  data_reviewTable = {
                      'reviewerID': reviewerID_value,
                      'ASIN': ASIN_value,
                      'reviewText': reviewText_value,
                      'rating': rating_value,
                      'summary': summary_value,
                      'reviewTime': reviewTime_value,
                    }
  cursor.execute(add_reviewTable, data_reviewTable)
  zl.commit()


# # Insert data into user table
# add_userDB = ("INSERT INTO userDB "
#                "(userID, weatherCH, weatherDW, gender, age, \
#                 stCombination, stNormal, stDry, stOily, \
#                 productID, ratings) "
#                "VALUES (%(userID)s, %(weatherCH)s, %(weatherDW)s, \
#                 %(gender)s, %(age)s, %(stCombination)s, \
#                 %(stNormal)s, %(stDry)s, %(stOily)s, \
#                 %(productID)s, %(ratings)s)")

# user_num = 1 
# while (user_num <= 2000):
#     i = 1
#     userID_value = user_num
#     weatherCH_value = random.randrange(3)
#     weatherDW_value = random.randrange(3)
#     gender_value = 0  # female
#     age_value = random.randrange(6)
#     stCombination_value = random.randrange(5)   # todo skintype can not be repeated
#     stNormal_value = random.randrange(5)
#     stDry_value = random.randrange(5)
#     stOily_value = random.randrange(5)   
#     while (i <= 20):      #times of repeating for each user (products of each user) 
#         # a specific user rated several products
#         random.seed(time.clock()) # random seed is current process time
#         productID_value = random.randrange(12221)  #todo not repeat for a specific product
#         ratings_value = random.randrange(5)
#         data_userDB = {
#           'userID': userID_value,
#           'weatherCH': weatherCH_value,
#           'weatherDW': weatherDW_value,
#           'gender': gender_value,
#           'age': age_value,
#           'stCombination': stCombination_value,
#           'stNormal': stNormal_value,
#           'stDry': stDry_value,
#           'stOily': stOily_value,
#           'productID':productID_value,
#           'ratings': ratings_value,
#           }
#         cursor.execute(add_userDB, data_userDB)
#         zl.commit()
#         i += 1
#     user_num += 1

# insert data into similarity table
# add_similarityTable = ("INSERT INTO similarityTable "
#                "(ASIN1, ASIN2) "
#                "VALUES (%(ASIN1)s, %(ASIN2)s)")

path = '/home/zhoulin/Desktop/Benthos/similarityTable/similarity.txt'
read_file = open(path, 'r')
l = read_file.readlines()
for lines in l:
  parts = lines.split('\t')
  ASIN1_value = parts[0]
  ASIN2_value = parts[1]
  data_similarityTable = {
                          'ASIN1': ASIN1_value,
                          'ASIN2': ASIN2_value,        
                          }
  cursor.execute(add_similarityTable, data_similarityTable)
  zl.commit()

cursor.close()
zl.close()