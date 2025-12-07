# Mango Bar - E commerce DRF project

<<<<<<< HEAD
features:

- Customer user Model with Admin / Seller / Customer Roles
- JWT authentication(login,Signup,Refreshtoken)
- product management(admin + seller only)
- catergory filterinfg + product search
- cart system with quantity update with product search
- orders module with checkout flow
- payment integration hook 
- admin panel + customer views
- drf browsable api_support

----------

Tech Stack :

- python 3.x
- django 5.x
- django rest framework
- jwt auth
- postgresql(neon)
- cloudinary
- whitenoise
- vercel deployment 

----------
-------
-----
## Project Set up

1. **Clone the repository:**
   ```bash
   git clone https://github.com/yourusername/phimart.git
   cd phimart
   ```

2. **Create and activate a virtual environment:**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows use `venv\Scripts\activate`
   ```

3. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

4. **Apply migrations:**
   ```bash
   python manage.py migrate
   ```

5. **Create a superuser:**
   ```bash
   python manage.py createsuperuser
   ```

6. **Run the development server:**
   ```bash
   python manage.py runserver
   ```    |


## Project Structure

### Mango Bar /
        accounts/
            __pycache__/
            migrations/
            templatetags/
            __init__.py
            admin.py
            apps.py
            decorators.py
            forms.py
            models.py
            serializers.py
            signals.py
            tests.py
            utils.py
            urls.py
            views.py
            api_views.py

        admin_panel/
            __pycache__/
            migrations/
            templatetags/
            __init__.py
            admin.py
            apps.py
            forms.py
            models.py
            serializers.py
            tests.py
            urls.py
            views.py

        cart/
            __pycache__/
            migrations/
            templatetags/
            __init__.py
            admin.py
            apps.py
            forms.py
            models.py
            serializers.py
            tests.py
            urls.py
            views.py
            api_views.py

        fixtures/
            images/
            mango_data.json

        mango_bar/
            __pycache__/
            __init__.py
            asgi.py
            wasgi.py
            urls.py
            settings.py

        media/
            images/
            products/
                main_images/

        orders/
            __pycache__/
            migrations/
            __init__.py
            admin.py
            apps.py
            forms.py
            models.py
            serializers.py
            tests.py
            urls.py
            views.py
            api_views.py
            extra_api.py

        payments/
            __pycache__/
            migrations/
            __init__.py
            admin.py
            apps.py
            sslcommerz.py
            models.py
            tests.py
            urls.py
            views.py
        products/
            __pycache__/
            migrations/
            __init__.py
            admin.py
            apps.py
            forms.py
            models.py
            serializers.py
            tests.py
            urls.py
            views.py
            api_views.py
            permissions.py
        static/
            css/
            images/
            js/
        .gitignore
        manage.py
        Readme.md
        requirements.txt
        vercel.json

    

## Api_keys
```ini
POST : [register](https://mango-bar.vercel.app/accounts/register/)

POST : [login](https://mango-bar.vercel.app/accounts/login/)

GET : [varify_email](https://mango-bar.vercel.app/accounts/verify-email/..../....../)

POST : [profile_view](https://mango-bar.vercel.app/accounts/profile/)

PUT : [edit_profile](https://mango-bar.vercel.app/accounts/edit-profile/)

PATCH : [change_password](https://mango-bar.vercel.app/accounts/change-password/)

GET : [product_list](https://mango-bar.vercel.app/api/products/)


PUT : [product_detail](https://mango-bar.vercel.app/api/products/<id>)

GET : [delete](https://mango-bar.vercel.app/products/api/<id>)

POST : [add_product](https://mango-bar.vercel.app/api/products/)

GET : [List_Search](https://mango-bar.vercel.app/products/api/search/?q=himsagar)

GET : [category](https://mango-bar.vercel.app/products/api/categories/)

GET : [cart](https://mango-bar.vercel.app/cart/cart-items/)

POST : [add to cart](https://mango-bar.vercel.app/cart/cart-items/)

PUT : [update_cart](https://mango-bar.vercel.app/cart/cart-items/<id>)

DELETE : [update_cart](https://mango-bar.vercel.app/cart/cart-items/<id>)

POST : [buy_now](https://mango-bar.vercel.app/orders/api/buy-now/)

PATCH : [update_status : admin_only](https://mango-bar.vercel.app/orders/api/orders/1/status/)

GET : [buy_now](https://mango-bar.vercel.app/orders/api/orders/)


GET : [status](https://mango-bar.vercel.app/orders/api/orders/5/status)


GET : [overview](https://mango-bar.vercel.app/admin-panel/overview/)


GET : [admin_dashboard](https://mango-bar.vercel.app/admin-panel/dashboard/)


GET : [mango_list](https://mango-bar.vercel.app/admin-panel/mangos/)


GET : [order_list](https://mango-bar.vercel.app/admin-panel/orders/)



```

## Environment Variables
Create a `.env` file in the root directory and add the following:
```ini
PGDATABASE=neondb
PGUSER=neondb_owner
PGPASSWORD=npg_gZ4PwGla1TRp
PGHOST=ep-still-sunset-adc78zsk-pooler.c-2.us-east-1.aws.neon.tech
PGPORT=5432


cloud_name=dbkgljhps
api_key=225277644954318
api_secret=UWn4fo3LSO4nZcf3UjXgh9o5A70

accounts :

    admin : rajib.somadhansoft@gmail.com
    password : rajib11001

    customer : rajibulislam3777@gmail.com
    password : rajib11001

    seller : rajibulislam256670@gmail.com
    password : rajib11001

```

## License
This project is licensed under the MIT License.




        
### Author
[MD.Rajibul Islam Shuvo]
(https://github.com/rajib3777/Mango_Bar)
=======
##ABOUT

>>>>>>> ce51f3f2d4d0f4657e8bafa166695c3aca19621a
