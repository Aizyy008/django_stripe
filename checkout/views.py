from django.shortcuts import render, redirect
from django.conf import settings
from django.contrib.auth.decorators import login_required
import stripe

from .models import Product

# Create your views here.
stripe.api_key = settings.STRIPE_SECRET_KEY

@login_required
def CreateCheckoutSessionView(request, productID):
    product = Product.objects.get(id=productID)
    print('Product:', product)

    YOUR_DOMAIN = f"{request.scheme}://{request.get_host()}"
    
    # Note:
    # request.scheme gives the protocol (http or https)
    # request.get_host() gives the domain name and port (if any)
    # YOUR_DOMAIN will be something like 'http://localhost:8000' or 'https://yourdomain.com'

    try:
        checkout_session = stripe.checkout.Session.create(
        payment_method_types=['card'], 
        line_items=[
            {
                'price_data': {
                    'currency': 'usd',
                    'unit_amount': product.price * 100,
                    'product_data': {
                        'name': product.name,
                        'description': product.description,
                        'images': [f'{product.image}']
                    },
                },
                'quantity': 1,
            },
        ],
        metadata = {
            'product_id': productID,
            'user_email': request.user.email
        },
        
        mode='payment',

        success_url=YOUR_DOMAIN + f'/payment-success/{productID}',
        cancel_url=YOUR_DOMAIN + f'/pricing/{productID}',
    )
    except Product.DoesNotExist:
        return render(request, '404.html', status=404)
    except Exception as e:
        print(f"Error creating checkout session: {e}")
        return render(request, 'error.html', {'error': str(e)})

    return redirect(checkout_session.url)


def PaymentSuccessView(request, productID):
    product = Product.objects.get(id=productID)
    return render(request, 'payment-success.html', {'product': product})


def PaymentFailedView(request, productID):
    product = Product.objects.get(id=productID)
    return render(request, 'payment-failed.html', {'product': product})


def PricingView(request, productID):
    products = Product.objects.all()
    selected_product = None
    try:
        selected_product = Product.objects.get(id=productID)
    except Product.DoesNotExist:
        selected_product = None
    return render(request, 'pricing.html', {
        'products': products,
        'selected_product': selected_product,
        'productID': productID
    })