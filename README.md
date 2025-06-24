# Stripe Payments Django Project

This project demonstrates Stripe payment integration in a Django application. Users can view products, select one, and complete a purchase using Stripe Checkout. It also includes webhook handling for payment events using Stripe and ngrok.

---

## Features

- Product listing and detail view
- Stripe Checkout integration
- Success and failure payment pages
- Stripe webhook integration for payment events
- Environment-based configuration for sensitive keys

---

## Project Structure

```
stripe_payments/
├── checkout/
│   ├── migrations/
│   ├── __init__.py
│   ├── admin.py
│   ├── apps.py
│   ├── models.py
│   ├── tests.py
│   ├── urls.py
│   └── views.py
│
├── stripe_payments/
│   ├── __init__.py
│   ├── asgi.py
│   ├── settings.py
│   ├── urls.py
│   └── wsgi.py
│
├── templates/
│   ├── 404.html
│   ├── error.html
│   ├── payment-failed.html
│   ├── payment-success.html
│   ├── pricing.html
│   ├── products.html
│   └── product.html
│
├── .env
├── .gitignore
├── db.sqlite3
├── manage.py
├── README.md
└── requirements.txt
```

---

## Setup Instructions

### 1. Clone the Repository

```bash
git clone <your-repo-url>
cd stripe_payments
```

### 2. Create and Activate a Virtual Environment

```bash
python3 -m venv venv
source venv/bin/activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

If `requirements.txt` does not exist, install manually:

```bash
pip install django python-dotenv stripe
```

### 4. Configure Environment Variables

Create a `.env` file in the project root:

```
STRIPE_PUBLISH_KEY=your_stripe_publishable_key
STRIPE_SECRET_KEY=your_stripe_secret_key
STRIPE_WEBHOOK_SECRET=your_stripe_webhook_secret
```

Replace with your actual Stripe test keys and webhook secret.

---

## Stripe Webhook Integration

### 1. Start Your Django Server

By default, Django runs on port 8000:

```bash
python manage.py runserver
```

### 2. Expose Your Local Server Using ngrok

Open a new terminal and run:

```bash
ngrok http 8000
```

Copy the HTTPS URL provided by ngrok (e.g., `https://xxxx-xxxx.ngrok-free.app`).

### 3. Set Up the Webhook in Stripe Dashboard

- Go to [Stripe Dashboard > Developers > Webhooks](https://dashboard.stripe.com/test/webhooks)
- Click **"Add endpoint"**
- Set the endpoint URL to:  
  ```
  https://xxxx-xxxx.ngrok-free.app/stripe/webhook/
  ```
- Select events to listen for (e.g., `checkout.session.completed`, `checkout.session.async_payment_failed`)
- After creation, copy the **Signing secret** and add it to your `.env` as `STRIPE_WEBHOOK_SECRET`.

### 4. Webhook Endpoint in Django

Your webhook endpoint is handled in `checkout/views.py`:

```python
@csrf_exempt
def stripe_webhook(request):
    # ... code to verify and process Stripe events ...
```

The URL is:
```
/stripe/webhook/
```
So the full URL (for Stripe and ngrok) is:
```
https://xxxx-xxxx.ngrok-free.app/stripe/webhook/
```

---

## Usage

- Visit `http://localhost:8000/stripe/products/` to view all products.
- Visit `http://localhost:8000/stripe/pricing/<productID>/` to view and purchase a product.
- On successful payment, you will be redirected to the payment success page.
- On failure or cancellation, you will see the payment failed page.
- Stripe will POST payment events to your webhook endpoint, which will be processed by your Django backend.

---

## File Overview

- **settings.py**: Loads Stripe keys and webhook secret from `.env` using `python-dotenv`.
- **checkout/views.py**: Handles product display, Stripe checkout session creation, payment result pages, and webhook processing.
- **templates/**: Contains all HTML templates for products, pricing, payment results, and errors.

---

## Notes

- Make sure your Stripe keys and webhook secret are kept secret and never committed to version control.
- This project is for demonstration and development purposes only. Do not use DEBUG=True in production.
- When using ngrok, you must update the webhook endpoint in Stripe every time you restart ngrok (as the URL changes).

---

## License

MIT License