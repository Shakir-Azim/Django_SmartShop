from django.urls import path
from . import views
from .views import Login, Signup, Index, Cart, CheckOut, Orders
from .middlewares.auth import  auth_middleware

app_name = 'store'
urlpatterns = [
    path('', Index.as_view(), name='index'),
    path('signup/', Signup.as_view(), name='signup'),
    path('login/', Login.as_view(), name='login'),
    path('cart/', auth_middleware(Cart.as_view()), name='cart'),
    path('logout/', views.Logout, name='logout'),
    path('check-out', CheckOut.as_view(), name='checkout'),
    path('orders/', auth_middleware(Orders.as_view()), name='orders'),
    
]