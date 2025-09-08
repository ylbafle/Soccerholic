from django.shortcuts import render

# Create your views here.
def show_main(request):
    # context berisi data yang akan dikirimkan ke tampilan
    context = {
        'nama_aplikasi': 'Soccerholic',
        'nama': 'Cathlin Abigail',
        'kelas' : 'PBP A'
    }

    return render(request, "main.html", context)