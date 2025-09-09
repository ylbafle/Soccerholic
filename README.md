Tautan PWS: https://cathlin-abigail-soccerholic.pbp.cs.ui.ac.id/

1. Penjelasan bagaimana saya mengimplementasikan checklist per checklist:
    a. Membuat proyek Django baru
        Proyek Django (soccerholic) saya berada pada direktori utama (Soccerholic). Sebelumnya, dilakukan instalasi dependencies (requirements.txt) yang berisi modul-modul yang diperlukan untuk menjalankan konsep MVT dan membuat proyek kali ini. Setelah berhasil mengunduh modul pada dependencies, proyek Django dibuat dengan command django-admin startproject soccerholic . yang akan membuat folder 'soccerholic' yang berisi file project Django secara otomatis (settings, manage, dll). Kemudian, dilanjutkan dengan konfigurasi environment variables dan proyek.
    b. Membuat aplikasi dengan nama main pada proyek Django
        Direktori aplikasi pada direktori utama berfungsi untuk menangani suatu bagian atau fitur tertentu dari proyek. Aplikasi baru, yaitu main, dibuat dengan menjalankan command python manage.py startapp main. Command ini akan membuat suatu folder main secara otomatis pada direktori utama (Soccerholic) yang berisi file penting sebagai struktur aplikasi untuk implementasi MVT, seperti models.py, view.py, templates, dan lainnya. Hal ini karena aplikasi memiliki model, tampilan, template, dan URL yang terkait dengannya.
        Direktori aplikasi bersifat independen dan memungkinkan bagi Django untuk memiliki banyak aplikasi yang saling terhubung dalam satu proyek.
    c. Melakukan routing agar dapat menjalankan main
        Routing dapat dilakukan setelah kita membuat template (main.html) dan menghubungkannya pada view (views.py). Routing akan memetakan URL yang diakses oleh pengguna ke view tertentu dalam aplikasi.
        Untuk melakukan routing, saya membuat berkas urls.py di dalam direktori main yang akan berisi konfigurasi routing untuk aplikasi main itu sendiri. Di dalam urls.py, fungsi path() digunakan untuk mendefinisikan URL. Kemudian, import show_main dari main.views bermaksud agar show_main dari views.py pada main dipanggil ketika URL yang direquest pengguna sesuai dengan pola yang ditentukan. Hal ini karena show_main yang tahu apa yang harus ditampilan pada browser. 
    d. Membuat model pada aplikasi main (Product)
        Model bertugas untuk mengatur dan mengelola data pada aplikasi atau sebagai representasi tabel pada database. Membuat model dilakukan dengan mengubah berkas models.py dalam aplikasi main sesuai ketentuan pada checklist keempat, yaitu membuat atribut nama, price, description, category, thumbnail, dan is_featured.
        Setelah melakukan perubahan pada model, saya menjalankan makemigrations (command python manage.py makemigrations) dan migrate (command python manage.py migrate) untuk memastikan perubahan ditangkap oleh Django.
    e. Membuat fungsi pada views.py untuk dikembalikan ke dalam template HTML (main.html)
        views.py dibuat agar data pada Product atau models dapat ditampilkan ke pengguna melalui halaman HTML.
        Pertama, saya memastikan pada berkas views.py terdapat from django.shortcuts import render karena fungsi render yang akan merender tampilan HTML. Kemudian, saya menambahkan fungsi show_main yang akan menerima parameter request untuk mengatur permintaan HTTP dan mengembalikan tampilan yang sesuai (diambil dari main.html atau template). 
        Pada fungsi show_main terdapat context, yaitu sebuah dictionary yang berisi data untuk dikirimkan ke tampilan, yaitu NPM, nama, dan nama toko. 
    f. Deployment ke PWS
        Setelah login SSO, saya create new project dengan project name 'soccerholic'. Setelah menyimpan credentials yang saya peroleh, saya mengedit raw editor dan menyesuaikan isinya dengan isi dile .env.prod. Setelah itu saya menuju settings.py pada direktori proyek, dan menambahkan URL deployment PWS pada list ALLOWED_HOSTS. Setelah melakukan git add, commit, and push, saya menjalankan project command yang ada di halaman PWS. Setelah memasukan credentials, saya dapat melihat status deployment saya, yaitu Running. Sebagai langkah akhir, saya melakukan git push pws master.

2. Bagan request client ke web aplikasi berbasis Django
    Gambar bagan: ![alt text](routing.jpg)
    a. Client request -> browser mengirim request ke server Django. 
    b. Django akan melakukan pengecekan pola URL melalui berkas urls.py (pada direktori soccerholic). 
    c. Jika URL sesuai, Django akan meneruskan request ke urls.py pada direktori main dan memanggil fungsi show_main dari views.py. Jika tidak sesuai, Django akan mengembalikan 404 Not Found.
    c. Kemudian, views.py yang terdapat fungsi show_main akan memanggil main.html atau template. 
    d. main.html akan menerima context dari views.py dan mengganti placeholder {{  }} dengan value yang sesuai dan menghasilkan HTML final yang akan dirender dan dikirim kembali ke browser. 
    e. Browser menampilkan halaman ke pengguna.

3. Peran settings.py pada proyek Django
    settings.py berperan penting dalam setiap proyek Django. Hal ini karena settings.py menjadi pusat pengaturan untuk proyek yang menghubungkan kode aplikasi dengan database dan server. Sebagai pusat konfigurasi, settings.py juga mengatur bagaimana aplikasi dijalankan melalui pengaturan penting, seperti aplikasi apa saja yang terdaftar (INSTALLED_APPS), akses (ALLOWED_HOSTS), pengaturan database (pada proyek ini saya menggunakan PostgreSQL seperti arahan tutorial), dan lainnya.

4. Cara kerja migrasi database di Django
    Migrasi database memastikan database dan model pada kode (models.py) sinkron. Setelah kita melakukan perubahan pada models.py, kita makemigration (command python manage.py makemigrations) untuk memastikan perubahan tercatat oleh Django (makemigration hanya mencatat). Kemudian, dilakukan migrate (command python manage.py migrate) untuk menjalankan file migrasi yang telah dicatat ke database.

5. Menurut saya, alasan Django dijadikan permulaan pembelajaran pengembangan perangkat lunak salah satunya karena Django menggunakan Python yang merupakan bahasa pemrograman yang ramah pemula. Karena belum pernah mempelajari framework lain, untuk hal teknis lainnya belum saya ketahui. Namun, setelah mempelajari Django, framework ini memiliki desain yang terstruktur terutama karena konsep MVT (Model, View, dan Template).

6. Tidak ada, asisten dosen sangat membantu dalam mengerjalan tutorial 1.
