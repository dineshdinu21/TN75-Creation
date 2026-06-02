from django.urls import path
from . import views
# from django.contrib.auth import views as auth_views

urlpatterns = [
    path('', views.homepage, name='home'),
    path('products/', views.add_product, name='products'),
    path('sales/', views.add_sale, name='sales'),
    path('products/list/', views.product_list, name='product_list'),
    path('tn75/admin-login/', views.create_admin_once, name='create_admin'),
    path('edit/status/<int:sale_id>/', views.edit_status, name='edit_status'),
    path('daily-report/', views.daily_sales_report, name='daily_report'),
    # path('register/', views.register, name='register'),
    # path('login/', auth_views.LoginView.as_view(template_name='login.html'), name='login'),
    # path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    
]