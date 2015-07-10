import math, operator, sys
import urllib2 #for web request for url
from PIL import Image
from PIL import ImageChops
from PIL import ImageOps


def rmsdiff(im1, im2):
    "Calculate the root-mean-square difference between two images"
    diff = ImageChops.difference(im1, im2)
    h = diff.histogram()
    sq = (value*((idx%256)**2) for idx, value in enumerate(h))
    sum_of_squares = sum(sq)
    avgx = float((im1.size[0] + im2.size[0])/2)
    avgy = float((im1.size[1] + im2.size[1])/2)
    rms = math.sqrt(sum_of_squares/float(avgx*avgy))
    return rms


def download(url):
	file_name = url.split('/')[-1]
	u = urllib2.urlopen(url)
	f = open(file_name, 'wb')
	meta = u.info()
	file_size = int(meta.getheaders("Content-Length")[0])
	print "Downloading: %s Bytes: %s" % (file_name, file_size)
	file_size_dl = 0
	block_sz = 4096
	while True:
    		buffer = u.read(block_sz)
    		if not buffer:
        		break
    		file_size_dl += len(buffer)
    		f.write(buffer)
    		status = "%6d K -  [%3.2f%%]" % (file_size_dl, file_size_dl * 100. / file_size)
    		status = status + chr(8)*(len(status)+1)
    		print "   downloaded:",status

	f.close()
	return file_name


possibile = [
	"90 degree rotated clock wise",
	"180 degree rotated",
	"90 degree rotated counter clock wise",
	"Scaled version",
	"Mirror image"
	]

def result(comp,x):
	rank = int (((1000 - comp)*100) / 1000)
	if(rank == 100):
		print "They are identical. Congrats.."
		print "Similarity : {}%".format(rank)
		exit(0)
	if(rank>=97):
		print possibile[x]
		print "Similarity : {}%".format(rank)
		exit(0)


print "Please provide same type of images Eg: both jpg,png\n"
url1 = raw_input('Enter URL of Image1 : ')
url2 = raw_input('Enter URL of Image2 : ')

image1 = download(url1)
image2 = download(url2)

im1 = Image.open(image1)
im2 = Image.open(image2)

# Rotation Checking
imx = im2
for x in range(0,3):
	imx = imx.rotate(90)
	comp = rmsdiff(im1,imx)
	result(comp,x)

#Scale Checking
imx = im2
x = (im1.size[0],im1.size[1])
imx = imx.resize(x, Image.ANTIALIAS)
comp = rmsdiff(im1,imx)
result(comp,3)

#Mirror image
imx = ImageOps.mirror(im2)
imx.save("mi.jpg")
comp = rmsdiff(im1,imx)
result(comp,4)

#When all check fails compute the similarity
comp = rmsdiff(im1,im2)
rank = int (((1000 - comp)*100) / 1000)
rank = abs(rank)

print "Similarity : {}%".format(rank)
count = int(10-(rank/10))
print "Not much similar"