from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
import base64

# Create your views here.

def encrypt(password):
	first = base64.b64encode(password.encode("utf-8"))
	result = ''
	for i in first:
		result += chr(i - (i % len(password) // i))
	return result

def index(request):
	if request.method == "POST":
		password = request.POST["password"]
		result = encrypt(password)
		return render(request, "password/index.html", {
			"result": result,
			"origin": password
			})
	return render(request, "password/index.html")