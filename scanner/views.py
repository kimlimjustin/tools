from django.shortcuts import render
from django.conf import settings
from django.core.files.storage import FileSystemStorage
from django.http import HttpResponseRedirect
from django.urls import reverse
import cv2
import numpy as np
from . import mapper
# Create your views here.
def scanner(request):
	if request.method == "POST" and request.FILES["myfile"]:
		myfile = request.FILES['myfile']
		fs = FileSystemStorage()
		filename = fs.save(myfile.name, myfile)
		uploaded_file_url = fs.url(filename)
		location = fs.path(filename)
		return render(request, "scanner/index.html", {
			"uploaded_file_url": uploaded_file_url,
			"location": location
			})
	return render(request, "scanner/index.html")

def scan(request):
	if request.method == "POST":
		image = request.POST["image"]
		image=cv2.imread(image)
		image=cv2.resize(image,(1300,800))
		orig=image.copy()
		gray=cv2.cvtColor(image,cv2.COLOR_BGR2GRAY)
		blurred = cv2.GaussianBlur(gray, (5,5), 0)
		edged=cv2.Canny(blurred,30,50)
		contours,hierarchy=cv2.findContours(edged,cv2.RETR_LIST,cv2.CHAIN_APPROX_SIMPLE) 
		contours=sorted(contours,key=cv2.contourArea,reverse=True)
		for c in contours:
			p = cv2.arcLength(c, True)
			approx=cv2.approxPolyDP(c,0.02*p,True)
			if len(approx == 4):
				target = approx
				break
		print(target)
		approx = mapper.mapp(target)
		pts=np.float32([[0,0],[800,0],[800,800],[0,800]])
		op=cv2.getPerspectiveTransform(approx,pts)
		dst=cv2.warpPerspective(orig,op,(800,800))
		#cv2.imshow("Scanned",dst)
		cv2.imwrite("scanner//static//output.jpg", dst)
		return render(request, "scanner/output.html")
	else:
		return HttpResponseRedirect(reverse("scanner"))