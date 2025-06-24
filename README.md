# Stripe Payments Django Project

This project demonstrates Stripe payment integration in a Django application. Users can view products, select one, and complete a purchase using Stripe Checkout.

---

## Features

- Product listing and detail view
- Stripe Checkout integration
- Success and failure payment pages
- Environment-based configuration for sensitive keys

---

## Project Structure

```
stripe_payments/
├── checkout/
│   ├── migrations/
│   ├── templates/
│   │   └── pricing.html
│   ├── admin.py
│   ├── apps.py
│   ├── models.py
│   ├── urls.py
│   └── views.py
├── stripe_payments/
│   ├── __init__.py
│   ├── asgi.py
│   ├── settings.py
│   ├── urls.py
│   └── wsgi.py
├── templates/
│   ├── 404.html
│   └── error.html
├── db.sqlite3
├── .env
├── .gitignore
└── manage.py
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
```

Replace with your actual Stripe test keys.

### 5. Apply Migrations

```bash
python manage.py migrate
```

### 6. Create a Superuser (Optional, for Admin)

```bash
python manage.py createsuperuser
```

### 7. Add Products

You can add products via the Django admin or by creating them in the shell:

```bash
python manage.py shell
```
```python
from checkout.models import Product
Product.objects.create(name="Test Product", price=1000, description="A test product", image="https://via.placeholder.com/150")
exit()
```

### 8. Run the Development Server

```bash
python manage.py runserver
```

---

## Usage

- Visit `http://localhost:8000/pricing/<productID>/` to view a product and purchase it.
- On successful payment, you will be redirected to the payment success page.
- On failure or cancellation, you will see the payment failed page.

---

## File Overview

- **settings.py**: Loads Stripe keys from `.env` using `python-dotenv`.
- **checkout/views.py**: Handles product display, Stripe checkout session creation, and payment result pages.
- **templates/pricing.html**: Product detail and purchase page.
- **templates/404.html** and **templates/error.html**: Error handling templates.

---

## Notes

- Make sure your Stripe keys are kept secret and never committed to version control.
- This project is for demonstration and development purposes only. Do not use DEBUG=True in production.

---

## License

MIT License