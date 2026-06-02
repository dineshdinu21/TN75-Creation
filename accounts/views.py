from django.shortcuts import render, redirect, get_object_or_404
from .models import Product, Sale
from django.contrib.auth.models import User
from django.http import HttpResponse
from django.db.models import Sum,Q
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth import views as auth_views
# from .forms import RegisterForm

def create_admin_once(request):
    if not User.objects.filter(username='Dinu').exists():
        User.objects.create_superuser('Dinu', 'admin@test.com', 'Dinu1234')
        return HttpResponse("Admin created successfully!")
    return HttpResponse("This Admin already exists.")

# def register(request):
#     form = RegisterForm()
#     if request.method == 'POST':
#         form = RegisterForm(request.POST)
#         if form.is_valid():
#             user = form.save(commit=False)
#             user.is_approved = False
#             user.save()
#             return redirect('login')
#     return render(request,'register.html',{'form': form})

def homepage(request):
    products = Product.objects.all()
    sales = Sale.objects.all().order_by('-date')
    context = {
        'products': products,
        'sales': sales,
    }
    return render(request, 'homepage1.html', context)

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

# @login_required
def add_sale(request):
    # if not request.user.is_approved:
    #     return HttpResponse("You are not approved to add sales.")
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

def edit_status(request, sale_id):
    sale = get_object_or_404(Sale, id=sale_id)
    if sale.status == True:
        sale.status = False
    else:
        sale.status = True
    sale.save()
    return redirect('home')

def daily_sales_report(request):
    summary_list = Sale.objects.values('date__date').annotate(
        total_revenue=Sum('total'),
        total_qty=Sum('quantity'),
        unpaid_qty=Sum('quantity',filter=Q(status=False)),
        unpaid_total=Sum('total', filter=Q(status=False))
    ).order_by('-date__date')

    return render(request, 'daily_report.html', {'summary_list': summary_list})