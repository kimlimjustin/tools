from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.urls import reverse
from django.db import IntegrityError
from index.models import User
from .models import Note
# Create your views here.

def index(request):
	notes = None
	totalnotes = None
	if request.user.is_authenticated:
		notes = Note.objects.filter(creator = request.user)
		totalnotes = notes.count()
	return render(request, "notes/index.html", {
		"notes": notes,
		"totalnotes": totalnotes
		})


def create(request):
	if request.method == "POST":
		title = request.POST["title"]
		note = request.POST['note']
		this_note = Note(title = title, creator = request.user, note = note)
		this_note.save()
		return HttpResponseRedirect(reverse('note', args = [this_note.id]))
	else:
		return render(request, "notes/create.html")

def note(request, id):
	note = Note.objects.filter(pk = id)
	if note.count() == 0 or not request.user.is_authenticated:
		return render(request, "notes/error.html")
	note = note[0]
	if note.creator != request.user:
		return render(request, "notes/error.html")
	if request.method == "POST":
		this_note = Note.objects.get(pk = id)
		this_note.title = request.POST["title"]
		this_note.note = request.POST["note"]
		this_note.save()
		return HttpResponseRedirect(reverse('index'))
	return render(request, "notes/note.html", {
		"note": note
		})