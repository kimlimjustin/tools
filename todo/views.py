from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from .models import Todo
from django.urls import reverse
# Create your views here.
def todo(request):
	if request.method == "POST":
		todo = request.POST["todo"]
		deadline = request.POST["deadline"]
		temp = Todo(todo = todo, deadline = deadline, owner = request.user)
		temp.save()
	todo = None
	if request.user.is_authenticated:
		todo = Todo.objects.filter(owner = request.user)
	return render(request, "todo/todo.html", {
		"todo": todo
		})

def delete_todo(request, id):
	if not request.user.is_authenticated:
		return HttpResponseRedirect(reverse('index'))
	todo = Todo.objects.filter(id = id, owner = request.user)
	if todo.count() == 0:
		return render(request, "notes/error.html", {
			"404": True
			})
	else:
		todo = todo[0]
		todo.delete()
		todolist = Todo.objects.filter(owner = request.user)
		return HttpResponseRedirect(reverse('todo'))