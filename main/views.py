from django.shortcuts import render, redirect, get_object_or_404
from main.forms import ProductForm
from main.models import Product

# Create your views here.
def show_main(request):
    # mengambil seluruh object Product yang tersimpan di database
    product_list = Product.objects.all()

    # context berisi data yang akan dikirimkan ke tampilan
    context = {
        'nama_aplikasi': 'Soccerholic',
        'nama': 'Cathlin Abigail',
        'kelas' : 'PBP A'
    }

    return render(request, "main.html", context)

# fungsi untuk generate form untuk menambahkan data produk
def create_product(request):
    form = ProductForm(request.POST or None)

    if form.is_valid() and request.method == "POST":
        form.save()
        return redirect('main:show_main')

    context = {'form': form}
    return render(request, "create_product.html", context)

def show_product(request, id):
    product = get_object_or_404(Product, pk=id)

    context = {
        'product': product
    }

    return render(request, "product_detail.html", context)

# demo
# def add_employee(request):
#    employee1 = Employee.objects.create(name = "cathlin", age = 19, persona = "-")

#    return render(request, "main.html", {"name": employee1.name, "age": employee1.age, "persona": employee1.persona})