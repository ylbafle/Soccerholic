from django.forms import ModelForm
from main.models import Product
# from django import forms
from django.utils.html import strip_tags

class ProductForm(ModelForm):
    class Meta:
        model = Product      # isi dari form akan menjadi objek produk
        fields = ["name", "stock", "price", "description", "thumbnail", "category", "is_featured"]

    def clean_name(self):
        name = self.cleaned_data["name"]
        return strip_tags(name)

    def clean_description(self):
        description = self.cleaned_data["description"]
        return strip_tags(description)
    
# demo 3
# class CarForm(forms.Form):
#     name = forms.CharField(max_length=255)
#     brand = forms.CharField(max_length=255)
#     stock = forms.IntegerField()