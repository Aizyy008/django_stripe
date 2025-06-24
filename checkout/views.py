from django.shortcuts import render, redirect
from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse, JsonResponse
import stripe

from .models import Product, PurchaseHistory

# Create your views here.
stripe.api_key = settings.STRIPE_SECRET_KEY

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


def ProductsListView(request):
    products = Product.objects.all()
    return render(request, 'products.html', {'products': products})


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
                    'unit_amount': int(product.price * 100),  # Ensure integer
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

        success_url=YOUR_DOMAIN + f'/stripe/payment-success/{productID}/',
        cancel_url=YOUR_DOMAIN + f'/stripe/pricing/{productID}/',
    )
    except Product.DoesNotExist:
        return render(request, '404.html', status=404)
    except Exception as e:
        print(f"Error creating checkout session: {e}")
        return render(request, 'error.html', {'error': str(e)})

    return redirect(checkout_session.url)



@csrf_exempt
def stripe_webhook(request):
    event = None
    payload = request.body
    sig_header = request.META.get('HTTP_STRIPE_SIGNATURE')

    try:
        event = stripe.Webhook.construct_event(
            payload, sig_header, settings.STRIPE_WEBHOOK_SECRET
        )
    except ValueError as e:
        # Invalid payload
        return HttpResponse(status=400)
    except stripe.error.SignatureVerificationError as e:
        # Invalid signature
        return HttpResponse(status=400)

    print("Event received:", event['type'])
    print("Payload: ", payload)


    # Handle the event
    if event['type'] == 'checkout.session.completed':
        session = event['data']['object']

        productID = session['metadata']['product_id']
        user_email = session['metadata']['user_email']

        # Here you can handle the successful payment, e.g., save to database
        print(f"Payment for product {productID} completed successfully for user {user_email}")

        get_product = Product.objects.get(id=productID)
        # Save to PurchaseHistory model
        PurchaseHistory.objects.create(
            purchaseID=session['id'],
            product=get_product,
            purchase_done=True,
            purchase_date=session['created']
        )

    elif event['type'] == 'checkout.session.async_payment_failed':
        session = event['data']['object']

        productID = session['metadata']['product_id']
        user_email = session['metadata']['user_email']

        # Here you can handle the unsuccessful payment, e.g., save to database
        print(f"Payment for product {productID} not completed for user {user_email}")

        get_product = Product.objects.get(id=productID)
        # Save to PurchaseHistory model
        PurchaseHistory.objects.create(
            purchaseID=session['id'],
            product=get_product,
            purchase_done=False,
            purchase_date=session['created']
        )

    else:
        print('Unhandled event type {}'.format(event['type']))

    return HttpResponse(status=200) # replaced return jsonify(success=True)