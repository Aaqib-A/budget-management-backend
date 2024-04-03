from django.db import models
import uuid
from django.contrib.auth.models import AbstractUser

from utils.constants import ROLES
# Create your models here.

class User(AbstractUser):
    user_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    role = models.CharField(max_length=16, choices=[(e.value, e.value) for e in ROLES])

    email = models.EmailField(unique=True)