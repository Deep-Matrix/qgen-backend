from django.db import models
from django.contrib.auth.models import User
from djrichtextfield.models import RichTextField

class Notes(models.Model):
  note_title = RichTextField()
  content = RichTextField()
  user_id = models.ForeignKey(User,on_delete=models.CASCADE)
  doc = models.DateTimeField(auto_now_add=True)

