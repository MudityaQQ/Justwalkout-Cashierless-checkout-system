from django.contrib import admin
from django.urls import path
from store.views import *
from store.views import Cart


urlpatterns = [
    # productInfo
    path('store/',storeIndex,name = 'storeIndex'),
    path('userWelcomePage/',userWelcomePage,name = 'userWelcomePage'),
    path('checkIn/',checkIn,name = 'checkIn'),
    path('cart',Cart.as_view(),name = 'cart'),
    path('checkout',CheckOut.as_view(),name = 'checkout'),
    path('welcome/<face_id>/',welcome,name='welcome'),
    path('productInfo/',productInfo,name = 'productInfo'),
]
