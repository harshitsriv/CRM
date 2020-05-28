from django.shortcuts import render, redirect, reverse
from django.http import HttpResponse
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from .decorators import unauthenticated_user, allowed_users, admin_only
from django.contrib.auth.models import Group

from .models import *
from .forms import *
# Create your views here.
ALLOWED_ROLES = ['admin']

@login_required(login_url='login')
@admin_only
def home(request):
    orders = Order.objects.all()
    customers = Customer.objects.all()

    total_orders = orders.count()
    orders_del = orders.filter(status="Delivered").count()
    orders_pen = orders.filter(status="Pending").count()

    context = {
        "orders":orders,
        "customers":customers,
        "total_orders":total_orders,
        "orders_del":orders_del,
        "orders_pen":orders_pen,
    }

    return render(request, 'accounts/dashboard.html',context=context)

@login_required(login_url='login')
@allowed_users(allowed_roles= ALLOWED_ROLES)
def products(request):
    products = Product.objects.all()
    return render(request, 'accounts/products.html', {'products':products})

@login_required(login_url='login')
@allowed_users(allowed_roles= ALLOWED_ROLES)
def customers(request, cust_id):
    customer = Customer.objects.get(id = cust_id)
    cust_orders = customer.order_set.all()
    order_count = cust_orders.count()

    context_customer = {
        "customer":customer,
        "cust_orders":cust_orders,
        "order_count":order_count,
    }
    return render(request, 'accounts/customers.html', context = context_customer)

@login_required(login_url='login')
@allowed_users(allowed_roles= ALLOWED_ROLES)
def createOrder(request):
    form = OrderForm

    if request.method == "POST":
        #print(request.POST)
        form = OrderForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('/')

    context ={'form': form}
    return render(request, 'accounts/order_form.html', context)

@login_required(login_url='login')
@allowed_users(allowed_roles= ALLOWED_ROLES)
def updateOrder(request, pk):
    
    order = Order.objects.get(id=pk )
    form = OrderForm(instance=order)

    if request.method == "POST":
        #print(request.POST)
        form = OrderForm(request.POST, instance=order)
        if form.is_valid():
            form.save()
            return redirect('/')

    context ={'form': form}
    return render(request, 'accounts/order_form.html', context)

@login_required(login_url='login')
@allowed_users(allowed_roles= ALLOWED_ROLES)
def deleteOrder(request, pk):

    order = Order.objects.get(id=pk)

    if request.method == "POST":
        order.delete()
        return redirect('/')

    context= {'item':order}
    return render(request, 'accounts/delete_order.html', context)

@login_required(login_url='login')
@allowed_users(allowed_roles= ALLOWED_ROLES)
def updateCustomer(request, cust_pk):
    customer = Customer.objects.get(id = cust_pk)
    form = CustomerForm(instance = customer)

    if request.method== "POST":
        form = CustomerForm(request.POST, instance=customer)
        if form.is_valid():
            form.save()
            return redirect('/customers/'+str(customer.id)+'/')

    context = {'form':form}

    return render(request, 'accounts/customer_form.html', context)

@unauthenticated_user
def loginPage(request):

    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request , username=username , password = password)

        if user is not None:
            print("user validated")
            login(request , user)
            return redirect('/')
        else:
            messages.info(request, "Username or password in incorrect")
            return redirect(reverse('login'))

    context = {}
    return render(request, 'accounts/login.html', context)

@unauthenticated_user
def registerPage(request):
    form = CreateUserForm()

    if request.method == "POST":
        form = CreateUserForm(request.POST)
        print(request.POST)

        if form.is_valid():
            user = form.save()
            username = form.cleaned_data.get('username')
            #on creating new user, post_save signal runs created in signals.py
            messages.success(request , "Account created for username " + username)
            return redirect('login')
        else:
            print("invalid data")


    context = {'form':form}
    return render(request, 'accounts/register.html', context)

def logoutUser(request):
    logout(request)
    return redirect('login')

@login_required(login_url = 'login')
@allowed_users(allowed_roles= ['customer'])
def userView(request):
    orders = request.user.customer.order_set.all()

    total_orders = orders.count()
    orders_del = orders.filter(status="Delivered").count()
    orders_pen = orders.filter(status="Pending").count()

    context = {
        "orders":orders,
        "total_orders":total_orders,
        "orders_del":orders_del,
        "orders_pen":orders_pen,
    }

    return render(request, 'accounts/user.html',context)

@login_required(login_url = 'login')
@allowed_users(allowed_roles = ['customer'])
def accountSetting(request):
    form = CustomerForm(instance = request.user.customer)

    if request.method== "POST":
        form = CustomerForm(request.POST, request.FILES, instance = request.user.customer)
        if form.is_valid():
            form.save()


    context= {'form':form}
    return render(request, 'accounts/acc_setting.html', context)