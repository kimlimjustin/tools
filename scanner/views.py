from django.shortcuts import render

# Create your views here.
def scanner(request):
	return render(request, "scanner/index.html")