🍋 Mango BAR – Advanced E-Commerce Management System

MangoDB is a full-featured e-commerce platform built with Django and Tailwind CSS, designed for seamless online shopping experiences. It includes three role-based dashboards (Admin, Seller, User), a powerful product management system, cart & order management, and a secure authentication system.

This project is developed with scalability, security, and a clean UI in mind — perfect for learning and real-world applications.

🚀 Features
🛒 User Features

Browse products by categories and search instantly

Add to Cart & Update Cart in real-time

Smooth Checkout Process

View & track order history

Secure profile management (edit profile, change password)

🏪 Seller Features

Add, update, and delete products

Manage inventory and pricing

View sales statistics

Order fulfillment & tracking

👨‍💼 Admin Features

Manage users (activate, deactivate accounts)

Manage sellers and approve products

View total orders, revenue, and statistics

Generate monthly profit/loss reports with graphs

🛠️ Tech Stack

Backend: Django (Python)

Frontend: Tailwind CSS, HTML, JavaScript

Database: SQLite / MySQL (configurable)

Authentication: Django's built-in auth system with email verification

Data Visualization: Chart.js / Django ORM queries

📂 Project Structure
MangoDB/
│
├── accounts/        # User, Seller, Admin authentication & profiles
├── products/        # Product listing & management
├── order/           # Cart, checkout & order tracking
├── dashboard/       # Role-based dashboards
├── templates/       # HTML templates
├── static/          # CSS, JS, images
└── manage.py

⚙️ Installation & Setup

Clone the repository

git clone https://github.com/yourusername/MangoDB.git
cd MangoDB


Create virtual environment & install dependencies

python -m venv env
source env/bin/activate  # Mac/Linux
env\Scripts\activate     # Windows

pip install -r requirements.txt


Run migrations

python manage.py makemigrations
python manage.py migrate


Create superuser

python manage.py createsuperuser


Start the server

python manage.py runserver

📊 Screenshots (Optional)

Add screenshots here for product pages, dashboards, and admin panel.

📌 Future Improvements

Payment gateway integration (Stripe/PayPal)

Wishlist feature

Product reviews & ratings

Mobile app integration (React Native / Flutter)

📜 License
