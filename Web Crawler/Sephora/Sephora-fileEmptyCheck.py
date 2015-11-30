import shutil
import os

# Check if item_name.txt is empty. if it is, delete its directory; otherwise, keep it.
main_path = '/home/python/Desktop/Sephora/'
Brand_Item_add = main_path + 'Brand-Item(no empty)'
fName = os.listdir(Brand_Item_add)
l = len(fName)
print (l)
for i in range(0, l):
    brandName_value = fName[i]
    f = Brand_Item_add + '/' + brandName_value
    if os.stat(f + '/' + 'item_name.txt').st_size == 0: # check whether file is empty
        shutil.rmtree(f) # delete file


# 1st: Remove duplicate lines in a file
dirName = os.listdir(Brand_Item_add)
l = len(dirName)
print (l)
result_path = '/home/python/Desktop/Sephora-Brand-Item(no duplicate)/'
input_path = '/home/python/Desktop/Sephora/Brand-Item(no empty)/'
for i in range(0, l):
    print (dirName[i])
    outputdir = result_path + dirName[i]
    if not os.path.isdir(outputdir):
            os.makedirs(outputdir) # create a directory for each brand
    inputdir = input_path + dirName[i] + '/'
    for lst in ['item_name.txt', 'item_image.txt', 'item_link.txt', 'item_price.txt', 'item_ratings.txt']:
        print (lst)
        outfilename = outputdir + '/' + lst
        infilename = inputdir + lst
        lines_seen = set() # holds lines already seen
        outfile = open (outfilename, "w")
        for line in open (infilename, "r"):
            if line not in lines_seen: # not a duplicate
                outfile.write(line)
                lines_seen.add(line)
        outfile.close()

# 2nd: copy back price.txt and ratings.txt
for i in range(0, l):
    outputdir = result_path + dirName[i] + '/'
    inputdir = input_path + dirName[i] + '/'
    for key in ['item_price.txt', 'item_ratings.txt']:
        src = inputdir + key
        dst = outputdir + key
        shutil.copyfile(src, dst) # copy
