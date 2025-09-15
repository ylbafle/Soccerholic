import uuid
from django.db import models

class Product(models.Model):
    CATEGORY_CHOICES = [
        ('ball', 'Ball'),
        ('jersey', 'Jersey'),
        ('keychains', 'Keychains'),
        ('shoe', 'Shoe')
    ]

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=255)                 # nama item
    price = models.IntegerField()                           # harga item
    description = models.TextField()                        # deskripsi item
    thumbnail = models.URLField(blank=True, null=True)      # gambar item
    category =  models.CharField(max_length=20, choices=CATEGORY_CHOICES, default='none')   # item category
    is_featured = models.BooleanField(default=False)        # status unggahan item
    
    def __str__(self):
        return self.name  # still unsure