from django.shortcuts import render
from ftplib import FTP
import json
from django.http import JsonResponse


# Create your views here.
def index(request):
    return render(request, 'labelimg/label.html')


def getimg(request):
	ftp = FTP('128.46.75.58')     # connect to host, default port
	ftp.login()
	print('success')
	ftp.cwd('WD1')
	#ftp.retrlines('LIST')
	ftplist = ftp.nlst()
	ftp.cwd(ftplist[0])

	sub1 = ftp.nlst()
	ftp.cwd(sub1[0])

	a = ftp.nlst()

	out = []

	for element in a:
		element = 'ftp://128.46.75.58/WD1/' + ftplist[0] + '/' + sub1[0] + '/' + element
		out.append(element)

	j = json.dumps(out)
	#print(j)

	ftp.close()

	return JsonResponse({'list':j})