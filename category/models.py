from django.db import models
import uuid

from user.models import User
from utils.constants import CATEGORY_TYPE

# Create your models here.
class Category(models.Model):
    category_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(User, related_name='category_user', on_delete=models.CASCADE)

    category_name = models.CharField(max_length=256, null=False, blank=False)
    category_type = models.CharField(max_length=8, choices=[(e.value, e.value) for e in CATEGORY_TYPE], default=CATEGORY_TYPE.EXPENSE.value)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = (('user', 'category_name'))

    def __str__(self):
        return str(self.user.username) + "-"+ str(self.category_name)
