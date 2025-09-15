from django.shortcuts import render, redirect, get_object_or_404
from main.forms import ProductForm
from main.models import Product
from django.http import HttpResponse
from django.core import serializers

# Create your views here.
def show_main(request):
    # mengambil seluruh object Product yang tersimpan di database
    product_list = Product.objects.all()

    # context berisi data yang akan dikirimkan ke tampilan
    context = {
        'nama_aplikasi': 'Soccerholic',
        'nama': 'Cathlin Abigail',
        'kelas' : 'PBP A',
        'product_list': product_list
    }

    return render(request, "main.html", context)

# fungsi untuk generate form untuk menambahkan data produk
def add_product(request):
    form = ProductForm(request.POST or None)

    if form.is_valid() and request.method == "POST":
        form.save()
        return redirect('main:show_main')

    context = {'form': form}
    return render(request, "add_product.html", context)

def show_product(request, id):
    product = get_object_or_404(Product, pk=id)

    context = {
        'product': product
    }

    return render(request, "product_details.html", context)

def show_xml(request):
    product_list = Product.objects.all()
    xml_data = serializers.serialize("xml", product_list)
    return HttpResponse(xml_data, content_type="application/xml")

def show_json(request):
    product_list = Product.objects.all()
    json_data = serializers.serialize("json", product_list)
    return HttpResponse(json_data, content_type="application/json")

def show_xml_by_id(request, product_id):
   try:
       item = Product.objects.filter(pk=product_id)
       xml_data = serializers.serialize("xml", item)
       return HttpResponse(xml_data, content_type="application/xml")
   except Product.DoesNotExist:
       return HttpResponse(status=404)

def show_json_by_id(request, product_id):
   try:
       item = Product.objects.get(pk=product_id)
       json_data = serializers.serialize("json", [item])
       return HttpResponse(json_data, content_type="application/json")
   except Product.DoesNotExist:
       return HttpResponse(status=404)

# demo1
# def add_employee(request):
#    employee1 = Employee.objects.create(name = "cathlin", age = 19, persona = "-")

#    return render(request, "main.html", {"name": employee1.name, "age": employee1.age, "persona": employee1.persona})