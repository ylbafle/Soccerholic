import uuid
from django.db import models
from django.contrib.auth.models import User

class Product(models.Model):
    CATEGORY_CHOICES = [
        ('ball', 'Ball'),
        ('jersey', 'Jersey'),
        ('keychains', 'Keychains'),
        ('shoe', 'Shoe')
    ]
    
    # menghubungkan satu product dengan satu user (many-to-one relationship)
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=255)                 # nama item
    price = models.IntegerField()                           # harga item
    description = models.TextField()                        # deskripsi item
    thumbnail = models.URLField(blank=True, null=True)      # gambar item
    category =  models.CharField(max_length=20, choices=CATEGORY_CHOICES, default='none')   # item category
    is_featured = models.BooleanField(default=False)        # status unggahan item
    stock = models.PositiveIntegerField(default=0)
