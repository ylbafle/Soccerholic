import uuid
from django.db import models
from django.contrib.auth.models import User

class Book(models.Model):
    id = models.UUIDField(default = uuid.uuid4, primary_key=True)
    title = models.CharField(max_length=255)

class Author(models.Model):
    bio = models.TextField()
    books = models.ManyToManyField(Book)
    user = models.OneToOneField(User)