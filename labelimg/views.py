from django.shortcuts import render
from ftplib import FTP
import json
from django.http import JsonResponse

import images
import imagedb
import os
from PIL import Image
import imagehash
from imagedb import Dataset
import getpass
import time


# Create your views here.
def labelimgindex(request):
    return render(request, 'labelimg/label.html')

def getdbimg(request):
	imagedb.connectDatabase("password")

	images.buildFileTree(10000)

	ids=os.listdir('web_ui_test')
	folder='web_ui_test/'
	imagest= [folder + image for image in ids]

	print("Adding 10 images to database and file system from folder 'web_ui_test'")
	i=0
	while i<10:
		imagedb.addImage(imagest[i], 'test1', {})
		i+=1

	dataset=Dataset('test1')
	while dataset.hasNext():
		data=dataset.getNext()
		hash=imagehash.average_hash(data[0])
		dbhash=data[1]['imagehash']
		if(str(hash)!=dbhash):
			message="\nIMAGES DO NOT MATCH!"
		else:
			message=" -Confirmed"
		print("Stored hash: "+str(hash)+" Database hash: "+str(dbhash)+message)



def getimg(request):
	fd = int(request.GET.get('dir'))
	sd = int(request.GET.get('subdir'))
	ftp = FTP('128.46.75.58')     # connect to host, default port
	ftp.login()
	print('success')
	ftp.cwd('WD1')
	#ftp.retrlines('LIST')
	ftplist = ftp.nlst()
	ftp.cwd(ftplist[fd])
	sub1 = ftp.nlst()

	#Unformatted directory has bug, todo

	if (sd == len(sub1)):
		sd = 0
		fd = fd + 1
		ftp.cwd('..')
		ftplist = ftp.nlst()
		ftp.cwd(ftplist[fd])
		sub1 = ftp.nlst()

	ftp.cwd(sub1[sd])
	a = ftp.nlst()

	out = []

	for element in a:
		element = 'ftp://128.46.75.58/WD1/' + ftplist[fd] + '/' + sub1[sd] + '/' + element
		out.append(element)

	j = json.dumps(out)
	#print(j)

	ftp.close()

	return JsonResponse({'list':j, 'fd': fd, 'sd': sd})
