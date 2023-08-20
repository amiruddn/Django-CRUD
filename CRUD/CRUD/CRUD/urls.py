from django.contrib import admin
from django.urls import path
from App import views

urlpatterns = [
    path('admin/', admin.site.urls),
    #home
    path('', views.home, name="home"),
    #add product
    path('add_product', views.add_product, name="add_product"),
    #view product
    path('product/<str:product_id>', views.product, name="product"),
    #edit product
    path('edit_product', views.edit_product, name="edit_product"),
    #delete product
    path('delete_product/<str:product_id>', views.delete_product, name="delete_product"),
]
