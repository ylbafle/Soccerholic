from django.forms import ModelForm
from main.models import Product

class ProductForm(ModelForm):
    class Meta:
        model = Product      # isi dari form akan menjadi objek news   
        fields = ["name", "price", "description", "thumbnail", "category", "is_featured"]