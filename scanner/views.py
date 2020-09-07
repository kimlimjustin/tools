from django.shortcuts import render
from django.conf import settings
from django.core.files.storage import FileSystemStorage
from django.http import HttpResponseRedirect
from django.urls import reverse
# Create your views here.
def scanner(request):
	if request.method == "POST" and request.FILES["myfile"]:
		myfile = request.FILES['myfile']
		fs = FileSystemStorage()
		filename = fs.save(myfile.name, myfile)
		uploaded_file_url = fs.url(filename)
		return render(request, "scanner/index.html", {
			"uploaded_file_url": uploaded_file_url
			})
	return render(request, "scanner/index.html")

def scan(request):
	if request.method == "POST":
		image = request.POST["image"]
		print(image)
	else:
		return HttpResponseRedirect(reverse("scanner"))