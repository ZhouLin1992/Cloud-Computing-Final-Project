from amazon.api import AmazonAPI

AMAZON_ACCESS_KEY = 'AKIAIYXEGNFLL2JWDBDA'
AMAZON_SECRET_KEY = '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'
AMAZON_ASSOC_TAG = 'Benthos-20'
amazon = AmazonAPI(AMAZON_ACCESS_KEY, AMAZON_SECRET_KEY, AMAZON_ASSOC_TAG)
ASIN_1 = 'B004WAGFQC'
ASIN_2 = 'B006HKR50A'
product_1 = amazon.lookup(ItemId=ASIN_1)
product_2 = amazon.lookup(ItemId=ASIN_2)
price_1 = product_1.price_and_currency
price_2 = product_2.price_and_currency
link_1 = product_1.large_image_url
link_2 = product_2.large_image_url
print(product_1.title)
print(link_2)
print(link_1)
# print(type(price))
# print(type(price[0]))
# print(product.title)