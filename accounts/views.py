from django.shortcuts import render, redirect, get_object_or_404
from .models import Product, Sale
from django.db.models import Sum

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
        product = get_object_or_404(Product, id=product_id)

        if product.stock >= quantity:

            total_price = product.price * quantity
            
            Sale.objects.create(
                customer_name=customer_name,
                product=product,
                quantity=quantity,
                total=total_price
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
