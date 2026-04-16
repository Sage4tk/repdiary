from django.db import models
import uuid
from django.contrib.auth.models import AbstractUser
# Create your models here.
class User(AbstractUser):
  id = models.UUIDField(
    primary_key=True,
    default=uuid.uuid4,
    editable=False
  )
  birth = models.DateField(null=True)