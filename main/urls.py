from django.urls import path
from main.views import show_main, add_product, show_product, show_xml, show_json, show_xml_by_id, show_json_by_id
from main.views import register, login_user, logout_user
from main.views import edit_product, delete_product, add_product_ajax, login_ajax, register_ajax, delete_product_ajax, edit_product_ajax, proxy_image, create_news_flutter
app_name = 'main'

urlpatterns = [
    path('', show_main, name='show_main'),
    path('create-product/', add_product, name='add_product'),
    path('product/<str:id>', show_product, name="show_product"),
    path('xml/', show_xml, name='show_xml'),
    path('json/', show_json, name='show_json'),
    path('xml/<str:product_id>/', show_xml_by_id, name='show_xml_by_id'),
    path('json/<str:product_id>/', show_json_by_id, name='show_json_by_id'),
    path('register/', register, name='register'),
    path('login/', login_user, name='login'),
    path('logout/', logout_user, name='logout'),
    path('product/<uuid:id>/edit', edit_product, name='edit_product'),
    path('product/<uuid:id>/delete', delete_product, name='delete_product'),
    path('create-product-ajax', add_product_ajax, name='add_product_ajax'),
    path('login-ajax/', login_ajax, name='login_ajax'),
    path('register-ajax/', register_ajax, name='register_ajax'),
    path('delete_product_ajax/<uuid:id>/', delete_product_ajax, name='delete_product_ajax'),
    path('edit-product-ajax/<uuid:id>/', edit_product_ajax, name='edit_product_ajax'),
    path('proxy-image/', proxy_image, name='proxy_image'),
    path('create-flutter/', create_news_flutter, name='create_news_flutter'),
]

