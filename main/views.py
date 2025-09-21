from django.shortcuts import render, redirect, get_object_or_404
from main.forms import CarForm, ProductForm
from main.models import Car, Product
from django.http import HttpResponse
from django.core import serializers
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required   # membatasi pengguna yang bisa membuka sutatu halaman
import datetime
from django.http import HttpResponseRedirect
from django.urls import reverse

# Create your views here.
@login_required(login_url='/login')   # jika user belum login maka tidak bisa lihat show_main dan akan diarahkan ke halaman login
def show_main(request):
    filter_type = request.GET.get("filter", "all")  # default 'all'

    # mengambil object Product, all -> menampilkan semua produk, filter -> hanya menampilkan produk dari user yang sedang login
    if filter_type == "all":
        product_list = Product.objects.all()
    else:
        product_list = Product.objects.filter(user=request.user)   

    # context berisi data yang akan dikirimkan ke tampilan
    context = {
        'nama_aplikasi': 'Soccerholic',
        'nama': 'Cathlin Abigail',
        'kelas' : 'PBP A',
        'product_list': product_list,
        'last_login': request.COOKIES.get('last_login', 'Never'), # nilai default jika cookie last_login tidak ada adalah Never
    }

    return render(request, "main.html", context)

def create_car(request):
    if form.is_valid() and request.method == "POST":
        form = CarForm()
        car = Car.objects.create(name=form.cleaned_data["name"], brand=form.cleaned_data["brand"], stock=form.cleaned_data["stock"])
        return render(request, "main.html")
    else:
        form = CarForm()
        return render(request, "create_car.html", {"form" : form})


# fungsi untuk generate form untuk menambahkan data produk
def add_product(request):
    form = ProductForm(request.POST or None)

    if form.is_valid() and request.method == "POST":
        product_entry = form.save(commit = False)   # commit = False memungkinkan kita untuk modifikasi objek sebelum disimpan
        product_entry.user = request.user           # field user diisi dengan nilai request user -> connect setiap product dengan user yang sedang login
        product_entry.save()
        return redirect('main:show_main')

    context = {'form': form}
    return render(request, "add_product.html", context)

@login_required(login_url='/login')   
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
   
def register(request):
    # membuat akun user baru
    form = UserCreationForm()

    if request.method == "POST":
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save() # menyimpan data form ke database
            messages.success(request, 'Your account has been successfully created!')
            return redirect('main:login')   # redirect setelah berhasil register (ke halaman login)
    context = {'form':form}
    return render(request, 'register.html', context)

def login_user(request):
    # kalau user submit form login (setelah isi data di form)
    if request.method == 'POST':
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)                                         # user login dengan sistem django, simpan data di session
            response = HttpResponseRedirect(reverse("main:show_main"))   # ke halaman utama setelah berhasil login
            # untuk mendaftar cookie last_login dan  menyimpan timestamp terakhir kali pengguna login
            response.set_cookie('last_login', str(datetime.datetime.now()))
            return response 

    # untuk menampilkan halaman form kosong -> tampilan halaman kosong (template yang digunakan login.html)
    else:
        form = AuthenticationForm(request)
    context = {'form': form}
    return render(request, 'login.html', context)

def logout_user(request):
    logout(request)                 # method untuk menghapus sesi pengguna yang saat ini sedang login
    response = HttpResponseRedirect(reverse('main:login'))
    response.delete_cookie('last_login')    # menghapus cookie last_login dari daftar cookies di response
    return response

# demo1
# def add_employee(request):
#    employee1 = Employee.objects.create(name = "cathlin", age = 19, persona = "-")

#    return render(request, "main.html", {"name": employee1.name, "age": employee1.age, "persona": employee1.persona})