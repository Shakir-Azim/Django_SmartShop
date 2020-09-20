from django.shortcuts import render, redirect, HttpResponseRedirect
from django.http import HttpResponse
from .models import *
from django.contrib.auth.hashers import make_password, check_password
from django.views import View


# Create your views here.
class Index(View):

    def post(self, request):
        product_id = request.POST.get('product_id')
        remove = request.POST.get('remove')
        cart = request.session.get('cart')
        if cart:
            quantity = cart.get(product_id)
            if quantity:
                if remove:
                    if quantity == 1:
                        cart.pop(product_id)
                    else:
                        cart[product_id] = quantity - 1
                else:
                    cart[product_id] = quantity + 1
            else:
                cart[product_id] = 1
        else:
            cart = {}
            cart[product_id] = 1
        request.session['cart'] = cart
        print(request.session['cart'])
        return redirect('store:index')
         



    def get(self, request):
        cart = request.session.get('cart')
        if not cart:
            request.session['cart'] = {}


        products = None
        
        categories = Category.objects.all()
        cat_id = request.GET.get('category')
        if cat_id:
            products = Product.objects.filter(category=cat_id)
        else:
            products = Product.objects.all()

        context={'products':products, 'categories':categories}
        print('you are:', request.session.get('customer'))
        return render(request, 'store/index.html',context)




class Cart(View):
    def get(self, request):
        list_of_products_id_in_cart = list(request.session.get('cart').keys())
        products_in_cart = Product.objects.filter(id__in =list_of_products_id_in_cart)
        # print(products_in_cart)
        context = {'cart_products': products_in_cart}
        return render(request, 'store/cart.html',context)




class CheckOut(View):
    def post(self, request):
        address = request.POST.get('address')
        phone = request.POST.get('phone')
        customer = request.session.get('customer')
        cart = request.session.get('cart')
        list_of_products = list(cart.keys())
        products = Product.objects.filter(id__in =list_of_products)
        print(address, phone, customer,cart, products)

        for product in products:
            order = OrderPlaced(customer=Customer.objects.get(id=customer),
                          product=product,
                          price=product.price,
                          address=address,
                          phone=phone,
                          quantity=cart.get(str(product.id)))
            order.save()
        request.session['cart'] = {}

        return redirect('store:cart')




class Orders(View):
    def get(self, request):
        customer_id = request.session.get('customer')
        customer = Customer.objects.get(id = customer_id)
        orders = OrderPlaced.objects.filter(customer=customer).order_by('-date')
        # print(orders)
        context = {'orders':orders}
        return render(request, 'store/orders.html',context)




class Signup(View):
    def get(self, request):
        return render(request, 'store/signup.html')
    def post(self, request):
        first_name = request.POST.get('firstname')
        last_name = request.POST.get('lastname')
        phone = request.POST.get('phone')
        email = request.POST.get('email')
        password = request.POST.get('password')

        # validation---
        value = {
            'first_name': first_name,
            'last_name': last_name,
            'phone': phone,
            'email': email
        }

        customer = Customer(first_name=first_name,
                                last_name=last_name,
                                phone=phone,
                                email=email,
                                password=password)

        error_message = self.validateCustomer(customer)
        emailExist = Customer.objects.filter(email=email)
         # email verification---
        if emailExist:
            error_message = 'Email already exist'

        if not error_message:
            customer.password = make_password(customer.password)
            customer.save()
            return redirect('store:login')
        else:
            context = {
                'error': error_message,
                'values': value,
            }
            return render(request, 'store/signup.html', context)

    def validateCustomer(self, customer):
        error_message = None
        
        if (not customer.first_name):
            error_message = "First Name Required !!"
        elif len(customer.first_name) < 3:
            error_message = 'First Name must be 4 char long or more'
        elif not customer.last_name:
            error_message = 'Last Name Required'
        elif len(customer.last_name) < 3:
            error_message = 'Last Name must be 4 char long or more'
        elif not customer.phone:
            error_message = 'Phone Number required'
        elif len(customer.phone) < 10:
            error_message = 'Phone Number must be 10 char Long'
        elif len(customer.password) < 6:
            error_message = 'Password must be 6 char long'
        elif len(customer.email) < 5:
            error_message = 'Email must be 5 char long'
       

        return error_message




class Login(View):
    return_url = None
    def get(self, request):
        Login.return_url = request.GET.get('return_url')
        return render(request, 'store/login.html')

    def post(self, request):
        email = request.POST.get('email')
        password = request.POST.get('password')
        customer = Customer.objects.filter(email=email).first()
        
        
        error_message = None
        if customer:
            flag = check_password(password, customer.password)
            if flag:
                request.session['customer'] = customer.id
                request.session['customer_name'] = customer.first_name

                if Login.return_url:
                    return HttpResponseRedirect(Login.return_url)
                else:
                    Login.return_url = None
                    return redirect('store:index')
            else:
                error_message = 'Email or Password Invalid'
        else:
            error_message = 'Email or Password Invalid'
        return render(request, 'store/login.html', {'error':error_message})




def Logout(request):
    request.session.clear()
    return redirect('store:login')







