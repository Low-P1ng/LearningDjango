from django.db import models
from django.urls import reverse
from django.contrib.auth.models import User
from .managers import ItemManager
from django.utils import timezone

# Create your models here.
class Item(models.Model):
    
    class Meta:
        indexes=[
            models.Index(fields=['user_name', 'item_price']),
        ]
    
    def __str__(self):
        return self.item_name + ':' + str(self.item_price)
    
    def delete(self, ):
        self.is_deleted=True
        self.deleted_at=timezone.now()
        self.save()
    
    def get_absolute_url(self):
        return reverse('myapp:index')
    
    user_name = models.ForeignKey(User, on_delete=models.CASCADE, default=1)
    item_name = models.CharField(max_length=100, db_index=True)
    item_desc = models.CharField()
    item_price = models.DecimalField(max_digits=8, decimal_places=2, db_index=True)
    item_image = models.URLField(max_length=500, default='https://grandseasonscoquitlam.com/img/placeholders/comfort_food_placeholder.png?v=1')
    is_available = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    is_deleted = models.BooleanField(default=False) #soft delete flag
    deleted_at = models.DateTimeField(null=True, blank=True) #saves soft delete timestamps
    
    objects= ItemManager()
    all_objects= models.Manager()
        
