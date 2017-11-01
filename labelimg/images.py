from PIL import Image
import math
import os

depth=0
#building a file tree to hold <num_images> images
def buildFileTree(num_images):
	print ("Building file tree to support "+str(num_images)+" images...")
	num_leaves=num_images//1000
	global depth
	depth=int(math.log(num_leaves, 10))
	i=0
	for i in range(0, num_leaves):
		path='Images/'
		num=i
		j=0
		while j<depth:
			path=path+str(num%10)+'/'
			num=num//10
			j=j+1
			os.makedirs(path, exist_ok=True)
	print ("Tree Built")
	
#hashing integer <num> value into a file path	
def buildPath(num):
	hash_num=num
	path='Images/'
	i=0
	for i in range(0, depth):
		path=path+str(num%10)+'/'
		hash_num=hash_num//10
	return path+str(num)+'.jpg'	
	
def addJpeg(pil_image, id):
	path=buildPath(id)
	pil_image.save(path)
	
def getJpeg(num):
	path=buildPath(num)
	im=Image.open(path)
	return im
