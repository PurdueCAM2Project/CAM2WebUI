from django.shortcuts import render
from ftplib import FTP
import json
from django.http import JsonResponse


# Create your views here.
def index(request):
    return render(request, 'labelimg/label.html')


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

	if (sd == len(sub1)):
		sd = 0
		fd = fd + 1
		ftp.cwd('..')
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