from django.contrib.auth.models import User
from django.db import models

class Note(models.Model):
    title = models.CharField(max_length=255)
    content = models.TextField()
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

class SharedNote(models.Model):
    note = models.ForeignKey(Note, on_delete=models.CASCADE)
    shared_with = models.ManyToManyField(User)
    shared_at = models.DateTimeField(auto_now_add=True)

class NoteVersionHistory(models.Model):
    note = models.ForeignKey(Note, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    timestamp = models.DateTimeField(auto_now_add=True)
    changes = models.TextField()
