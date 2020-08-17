from django.urls import path
from . import views

urlpatterns = [
	path('', views.index, name="notes"),
	path("create", views.create, name="create"),
	path("note/<int:id>", views.note, name="note")
]