import json
from django.shortcuts import render, redirect, get_object_or_404
from main.forms import ProductForm
from main.models import Product
from django.http import HttpResponse
from django.core import serializers
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required   # membatasi pengguna yang bisa membuka sutatu halaman
import datetime
from django.http import HttpResponseRedirect, JsonResponse
from django.urls import reverse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST
from django.utils.html import strip_tags
from django.contrib.auth.models import User
import requests
import json
from django.http import JsonResponse

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
        'nama': request.user.username,
        'kelas' : 'PBP A',
        'product_list': product_list,
        'last_login': request.COOKIES.get('last_login', 'Never'), # nilai default jika cookie last_login tidak ada adalah Never
    }

    return render(request, "main.html", context)

# decorator memastikan view ini hanya bisa diakses via metode POST.
@require_POST
def add_product_ajax(request):
    # Memeriksa apakah user sudah login. Jika belum, kirim response error.
    if not request.user.is_authenticated:
        return JsonResponse({"status": "fail", "message": "User not logged in"}, status=401)

    # ambil data dari request.POST
    name = strip_tags(request.POST.get("name")) 
    description = strip_tags(request.POST.get("description"))
    price = request.POST.get("price")
    stock = request.POST.get("stock") 
    category = request.POST.get("category")
    thumbnail = request.POST.get("thumbnail")
    is_featured = request.POST.get("is_featured") == 'on'
    user = request.user

    # buat objek Product baru
    new_product = Product(
        name=name, 
        price=price,
        stock=stock,
        description=description,
        category=category,
        thumbnail=thumbnail,
        is_featured=is_featured,
        user=user
    )
    new_product.save()

    return JsonResponse({"status": "success", "message": "Product added successfully"}, status=201)

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

@login_required()   
def show_product(request, id):
    product = get_object_or_404(Product, pk=id)

    context = {
        'product': product
    }

    return render(request, "product_details.html", context)

@require_POST
def login_ajax(request):
    # ambil data JSON yang dikirim dari frontend
    data = json.loads(request.body)
    username = data.get("username")
    password = data.get("password")

    # authenticate user
    user = authenticate(request, username=username, password=password)

    if user is not None:
        # jika autentikasi berhasil, user bisa login
        login(request, user)
        # kirim response sukses dalam format JSON
        return JsonResponse({
            "status": "success",
            "message": "Login successful!"
        })
    else:
        # kirim response error kalau gagal
        return JsonResponse({
            "status": "fail",
            "message": "Invalid username or password."
        }, status=401) # status 401 berarti "unauthorized"
    
def edit_product(request, id):
    product = get_object_or_404(Product, pk=id)
    form = ProductForm(request.POST or None, instance=product)

    if form.is_valid() and request.method == 'POST':
        form.save()
        return redirect('main:show_main')

    context = {
        'form': form
    }

    return render(request, "edit_product.html", context)

@require_POST
@login_required
def edit_product_ajax(request, id):
    product = get_object_or_404(Product, pk=id)

    if request.user != product.user:
        return JsonResponse({"status": "fail", "message": "You are not authorized to edit this product."}, status=403)

    form = ProductForm(request.POST, instance=product)

    if form.is_valid():
        form.save()
        return JsonResponse({"status": "success", "message": "Product updated successfully."})
    else:
        return JsonResponse({"status": "fail", "errors": form.errors}, status=400)

def delete_product(request, id):
    product = get_object_or_404(Product, pk=id)
    product.delete()
    return HttpResponseRedirect(reverse('main:show_main'))

def show_xml(request):
    product_list = Product.objects.all()
    xml_data = serializers.serialize("xml", product_list)
    return HttpResponse(xml_data, content_type="application/xml")

def show_json(request):
    product_list = Product.objects.all()
    data = [
        {
            'id': str(product.id),
            'name': product.name,
            'price': product.price,
            'description': product.description,
            'category': product.category,
            'thumbnail': product.thumbnail,
            'stock': product.stock,
            'is_featured': product.is_featured,
            'user_id': product.user_id,
            'user_username': product.user.username if product.user else None,
        }
        for product in product_list
    ]

    return JsonResponse(data, safe=False)   #  mengirimkan data dalam format JSON ke client, safe=False karena data yang dikirin berupa list, bukan dictionary

def show_xml_by_id(request, product_id):
   try:
       item = Product.objects.filter(pk=product_id)
       xml_data = serializers.serialize("xml", item)
       return HttpResponse(xml_data, content_type="application/xml")
   except Product.DoesNotExist:
       return HttpResponse(status=404)

def show_json_by_id(request, product_id):
    try:
        product = Product.objects.select_related('user').get(pk=product_id)
        data = {
            'id': str(product.id),
            'name': product.name,
            'price': product.price,
            'description': product.description,
            'category': product.category,
            'thumbnail': product.thumbnail,
            'stock': product.stock,
            'is_featured': product.is_featured,
            'user_id': product.user_id,'user_username': product.user.username if product.user else 'Toko No Name'
        }
        return JsonResponse(data)
    except Product.DoesNotExist:
       return JsonResponse({'detail': 'Not found'}, status=404)

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

@require_POST
def register_ajax(request):
    # ambil data mentah format json dari body request
    data = json.loads(request.body)
    # ekstrak setiap field dari data json
    username = data.get('username')
    password = data.get('password1')
    password2 = data.get('password2')

    # validasi di sisi server: pastikan kedua password cocok
    if password != password2:
        return JsonResponse({'status': 'fail', 'message': 'passwords do not match.'}, status=400)

    # cek apakah username sudah terdaftar di database
    if User.objects.filter(username=username).exists():
        return JsonResponse({'status': 'fail', 'message': 'username already taken.'}, status=400)

    # jika semua validasi lolos, proses pembuatan user baru
    try:
        # buat user baru dengan username dan password yang diberikan
        new_user = User.objects.create_user(username=username, password=password)
        # setelah user berhasil dibuat, langsung loginkan mereka ke dalam sesi
        login(request, new_user)
        # kirim response json yang menandakan registrasi berhasil
        return JsonResponse({'status': 'success', 'message': 'registration successful!'})
    except Exception as e:
        # tangani jika ada error lain yang tak terduga saat membuat user
        return JsonResponse({'status': 'fail', 'message': str(e)}, status=400)

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

@require_POST
def delete_product_ajax(request, id):
    try:
        product = Product.objects.get(pk=id)
        # pastikan hanya pemilik produk yang bisa delete
        if request.user == product.user:
            product.delete()
            return JsonResponse({"status": "success", "message": "Product deleted successfully."})
        else:
            return JsonResponse({"status": "fail", "message": "You are not authorized to delete this product."}, status=403)
    except Product.DoesNotExist:
        return JsonResponse({"status": "fail", "message": "Product not found."}, status=404)

def proxy_image(request):
    image_url = request.GET.get('url')
    if not image_url:
        return HttpResponse('No URL provided', status=400)
    
    try:
        # Fetch image from external source
        response = requests.get(image_url, timeout=10)
        response.raise_for_status()
        
        # Return the image with proper content type
        return HttpResponse(
            response.content,
            content_type=response.headers.get('Content-Type', 'image/jpeg')
        )
    except requests.RequestException as e:
        return HttpResponse(f'Error fetching image: {str(e)}', status=500)
    
@csrf_exempt
def create_news_flutter(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        name = strip_tags(data.get("name", ""))  # Strip HTML tags
        description = strip_tags(data.get("description", ""))  # Strip HTML tags
        stock = data.get("stock", 0)
        price = data.get("price", 0)
        category = data.get("category", "")
        thumbnail = data.get("thumbnail", "")
        is_featured = data.get("is_featured", False)
        user = request.user
        
        new_product = Product(
            name=name, 
            description=description,
            stock=stock,
            price=price,
            category=category,
            thumbnail=thumbnail,
            is_featured=is_featured,
            user=user
        )
        new_product.save()
        
        return JsonResponse({"status": "success"}, status=200)
    else:
        return JsonResponse({"status": "error"}, status=401)
    
# demo1
# def add_employee(request):
#    employee1 = Employee.objects.create(name = "cathlin", age = 19, persona = "-")

#    return render(request, "main.html", {"name": employee1.name, "age": employee1.age, "persona": employee1.persona})

# demo tugas 3
# def create_car(request):
#     if form.is_valid() and request.method == "POST":
#         form = CarForm()
#         car = Car.objects.create(name=form.cleaned_data["name"], brand=form.cleaned_data["brand"], stock=form.cleaned_data["stock"])
#         return render(request, "main.html")
#     else:
#         form = CarForm()
#         return render(request, "create_car.html", {"form" : form})

