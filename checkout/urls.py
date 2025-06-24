from django.contrib import admin
from django.urls import path

from .views import *

urlpatterns = [
    path('products/', ProductsListView, name='products-list'),
    path('pricing/<int:productID>/', PricingView, name='pricing'),
    path('create-checkout-session/<int:productID>/', CreateCheckoutSessionView, name='create-checkout-session'),
    path('payment-success/<int:productID>/', PaymentSuccessView, name='payment-success'),
    path('payment-failed/<int:productID>/', PaymentFailedView, name='payment-failed'),
    path('checkout/<int:product_id>/', CreateCheckoutSessionView, name='checkout'),
    path('webhook/', stripe_webhook, name='stripe-webhook'),
]
