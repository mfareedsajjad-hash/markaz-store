# Markaz Clone — Complete E-commerce Platform

A full-featured **Python Flask** e-commerce website inspired by Markaz.app (Pakistan's shopping & dropshipping platform).

## Features

### Customer Side
- Beautiful responsive homepage (categories, featured, trending, deals, etc.)
- Product detail pages with related products
- Search functionality
- Category browsing
- User Registration & Login
- Shopping Cart (persistent with database)
- Checkout with Cash on Delivery
- Order history & order detail pages
- Stock management

### Admin Panel
- Dashboard with stats (products, orders, users, revenue)
- Add / Edit / Delete products
- Manage order statuses (Pending → Confirmed → Shipped → Delivered)
- Featured product toggle

## Tech Stack
- **Python 3** + **Flask**
- **SQLAlchemy** (SQLite database)
- **Flask-Login** (authentication)
- Bootstrap 5 + Font Awesome
- Unsplash product images

## Quick Start

```bash
# 1. Enter project folder
cd markaz_clone

# 2. Install dependencies
pip install -r requirements.txt

# 3. Run the app (database will auto-seed)
python app.py
```

Open browser: **http://127.0.0.1:5000**

## Demo Accounts

| Role     | Email              | Password  |
|----------|--------------------|-----------|
| Admin    | admin@markaz.pk    | admin123  |
| Customer | demo@markaz.pk     | demo123   |

## Project Structure

```
markaz_clone/
├── app.py              # Main application + all routes
├── models.py           # Database models (User, Product, Order...)
├── seed.py             # Sample data seeder
├── config.py           # Configuration
├── requirements.txt
├── markaz.db           # SQLite database (created on first run)
├── templates/
│   ├── base.html
│   ├── index.html
│   ├── product.html
│   ├── cart.html
│   ├── checkout.html
│   ├── orders.html
│   ├── order_detail.html
│   ├── category.html
│   ├── search.html
│   ├── auth/
│   │   ├── login.html
│   │   └── register.html
│   ├── admin/
│   │   ├── dashboard.html
│   │   ├── products.html
│   │   ├── product_form.html
│   │   └── orders.html
│   └── partials/
│       └── product_card.html
└── static/
```

## How to Use

1. **Browse** products on homepage
2. **Register / Login** to buy
3. **Add to Cart** → **Checkout** (Cash on Delivery)
4. **Admin** can login and manage products & orders

Built with ❤️ for Pakistan.
# markaz-store
