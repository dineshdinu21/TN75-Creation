from django.shortcuts import render, redirect, get_object_or_404
from .models import Product, Sale
from django.db.models import Sum
from django.contrib.auth.models import User
from django.http import HttpResponse

def create_admin_once(request):
    if not User.objects.filter(username='Dinu').exists():
        User.objects.create_superuser('Dinu', 'admin@test.com', 'Dinu1234')
        return HttpResponse("Admin created successfully!")
    return HttpResponse("This Admin already exists.")

def homepage(request):
    products = Product.objects.all()
    sales = Sale.objects.all().order_by('-date')
    context = {
        'products': products,
        'sales': sales,
    }
    return render(request, 'homepage.html', context)

def add_product(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        price = request.POST.get('price')
        stock = request.POST.get('stock')

        Product.objects.create(
            name=name,
            price=price,
            stock=stock
        )
        return redirect('home') 

    return render(request, 'products.html')

def add_sale(request):
    products = Product.objects.all()

    if request.method == 'POST':
        product_id = request.POST.get('product')
        quantity = int(request.POST.get('quantity'))
        customer_name = request.POST.get('customer_name')
        customer_price= request.POST.get('price')
        status = request.POST.get('status') == 'True'
        product = get_object_or_404(Product, id=product_id)

        if product.stock >= quantity:
            if customer_price:
                final_price = int(customer_price)
            else:
                final_price = product.price

            total_price = final_price * quantity
            
            Sale.objects.create(
                customer_name=customer_name,
                product=product,
                price=final_price,
                quantity=quantity,
                total=total_price,
                status=status
            )

            product.stock -= quantity
            product.save()

            return redirect('home')
        else:
            return render(request, 'sales.html', {
                'products': products, 
                'error': 'Pothumaana stock illai!'
            })

    return render(request, 'sales.html', {'products': products})


def product_list(request):
    products = Product.objects.all()
    return render(request, 'product_list.html', {'products': products})

