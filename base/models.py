from django.db import models
from django.contrib.auth.models import User


class Notes(models.Model):
  note_title = models.CharField(max_length=50)
  content = models.TextField()
  user_id = models.ForeignKey(User,on_delete=models.CASCADE)
  doc = models.DateTimeField(auto_now_add=True)

