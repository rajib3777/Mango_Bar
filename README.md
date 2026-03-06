# Mango Bar - E-commerce API (DRF)

A robust Django Rest Framework (DRF) backend for the Mango Bar e-commerce platform, designed to connect with a React frontend.

## Features
- **Custom User Model**: Admin, Seller, and Customer roles.
- **JWT Authentication**: Secure login, signup, and token refresh.
- **Product Management**: Category filtering and advanced search.
- **Cart System**: API-based cart management.
- **Orders & Payments**: Checkout flow with payment integration hooks.
- **Admin & Seller Panels**: Specialized API endpoints for management.
- **Cloudinary Integration**: Automatic image hosting and optimization.

## Tech Stack
- Python 3.x / Django 5.x
- Django Rest Framework (DRF)
- SimpleJWT (Auth)
- PostgreSQL (Neon)
- Cloudinary (Media)
- WhiteNoise (Static Files)
- Vercel (Deployment)

## Project Setup

1. **Clone the repository:**
   ```bash
   git clone https://github.com/rajib3777/Mango_Bar.git
   cd Mango_Bar
   ```

2. **Create and activate a virtual environment:**
   ```bash
   python -m venv venv
   # Windows:
   venv\Scripts\activate
   # Linux/Mac:
   source venv/bin/activate
   ```

3. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

4. **Environment Variables:**
   Create a `.env` file in the root directory:
   ```ini
   PGDATABASE=neondb
   PGUSER=neondb_owner
   PGPASSWORD=your_password
   PGHOST=your_host
   PGPORT=5432

   cloud_name=your_cloud_name
   api_key=your_api_key
   api_secret=your_api_secret
   ```

5. **Apply migrations:**
   ```bash
   python manage.py migrate
   ```

6. **Run the server:**
   ```bash
   python manage.py runserver
   ```

## API Endpoints

### Authentication
| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/accounts/register/` | User registration |
| POST | `/accounts/login/` | User login (returns JWT) |
| GET | `/accounts/profile/` | View current user profile |
| PUT | `/accounts/edit-profile/` | Update profile information |

### Products
| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/api/products/` | List all products |
| POST | `/api/products/` | Add new product (Seller only) |
| GET | `/api/products/<id>/` | Product details |
| GET | `/api/products/search/?q=<query>` | Search products |
| GET | `/api/categories/` | List all categories |

### Cart & Orders
| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/cart/cart/` | View user cart |
| POST | `/cart/cart-items/` | Add item to cart |
| POST | `/orders/api/buy-now/` | Place an order |
| GET | `/orders/api/orders/` | View order history |

### Admin/Seller Panel
| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/admin-panel/overview/` | Statistics overview |
| GET | `/admin-panel/dashboard/` | Dashboard metrics |

## License
MIT License

### Author
[MD. Rajibul Islam Shuvo](https://github.com/rajib3777/Mango_Bar)
