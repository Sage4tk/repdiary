from django.db import models
from apps.user.models import User
import uuid

# Create your models here.
class Session(models.Model):
  id = models.UUIDField(
    primary_key=True,
    default=uuid.uuid4,
    editable=False
  )
  user = models.ForeignKey(User, on_delete=models.CASCADE)
  date = models.DateTimeField()
  created_at = models.DateTimeField(auto_now_add=True)
  

class Exercise(models.Model):
  id = models.UUIDField(
    primary_key=True,
    default=uuid.uuid4,
    editable=False
  )
  session = models.ForeignKey(Session, on_delete=models.CASCADE, related_name='exercises')
  exercise = models.CharField(max_length=255)
  reps = models.IntegerField(null=True)
  sets = models.IntegerField(null=True)
  length = models.IntegerField(null=True)
  notes = models.CharField(null=True)