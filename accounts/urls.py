from django.urls import path
from . import views

urlpatterns = [
    path('', views.homepage, name='home'),
    path('products/', views.add_product, name='products'),
    path('sales/', views.add_sale, name='sales'),
]