from django.db import models
import uuid
from django.core.validators import MinValueValidator

from user.models import User
from category.models import Category

# Create your models here.
class Transaction (models.Model):
    transaction_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    # user = models.ForeignKey(User, related_name='transaction_user', on_delete=models.CASCADE)
    
    title = models.CharField(max_length=256, null=False, blank=False)
    amount = models.DecimalField(max_digits=12, decimal_places=2, blank=False, null=False, validators=[MinValueValidator(0.00)])
    category = models.ForeignKey(Category, related_name='transaction_category', on_delete=models.CASCADE, null=False, blank=False)
    transaction_time = models.DateTimeField(null=False, blank=False)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return str(self.title) +"-"+ str(self.category.category_name) +"-"+ str(self.category.user.username) 
