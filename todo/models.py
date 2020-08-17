from django.db import models
from index.models import User
# Create your models here.
class Todo(models.Model):
	todo = models.CharField(max_length = 3000)
	deadline = models.CharField(max_length = 12)
	owner = models.ForeignKey(User, on_delete = models.CASCADE, related_name = 'owner')
