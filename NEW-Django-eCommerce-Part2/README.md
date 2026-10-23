----------------------------------------
# Multi-Vendor eCommerce Web Application
----------------------------------------

An advanced, production-ready multi-vendor eCommerce platform built with
Django and backed by a MariaDB database. Part 2 extends the platform
with a fully functional RESTful API via Django REST Framework (DRF),
a live Reddit community integration feed, modular app-level template
organization, and secure token-based authentication.

-------------------------------------------------
# Key Features & Requirements Fulfilled
-------------------------------------------------
 
1. Custom Role-Based Authentication:
   - Distinct user roles for Buyers and Vendors upon registration.
   - Role-specific permissions restrict product creation and store management strictly to vendors, while allowing buyers to browse, cart, checkout, and review.
 
2. Session-Based Shopping Cart:
   - Fully persistent, lightweight shopping cart stored within Django sessions (request.session['cart']), allowing users to manage items seamlessly without database clutter prior to checkout.
 
3. Automated Checkout & Email Invoicing:
   - Secure checkout processing that atomically creates orders, clears the session cart, itemizes purchased products, and dispatches a comprehensive invoice directly to the buyer's email address.
 
4. Verified & Unverified Product Reviews:
   - Universal review submission allowing any registered user to leave feedback.
   - Automated backend validation queries past order history to dynamically flag reviews as Verified Purchase or Unverified Review.
 
5. Secure Password Recovery & Expiring Tokens:
   - Built-in Django cryptographic token generation (`PasswordResetView`) that dispatches secure recovery links with strict expiration timeouts (defaulting to a secure 3-day window) to prevent token replay attacks.
 
6. MariaDB Backend & Migrations:
   - Configured with `django.db.backends.mysql` utilizing 64-bit integer fields (`BigAutoField`) to ensure full structural integrity and prevent MariaDB foreign key (`Errno 150`) constraints during migration.

7. RESTful API (Django REST Framework):
    - Full CRUD operations ('GET', 'POST', 'PUT', 'DELETE') for 'Store', 'Product',
    and 'Review' resources using DRF ViewSets and Routers.
    - Custom 'IsVendorOrReadOnly' permission classes combined with Token
    Authentication for secure remote resource management.

8. Third-Party Reddit API Integration:
    - Custom helper function ('functions/reddit.py') querying 'r/django/new.json'
    with a mandatory custom 'User-Agent' header to securely fetch and render live
    community discussions.

9. Modular App-Level Architecture (Seperation of Concerns):
    - Marketplace-specific templates strictly organized inside 'marketplace/
    templates/marketplace/' following Django best practices, while shared global
    templates ('base.html' and 'registration/') remain at the project root level.

---------------
# Tech Stack
---------------
- Backend: Python, Django, Django REST Framework (DRF)
- Database: MariaDB / MySQL
- Frontend: Bootstrap 5, HTML5, CSS3, Django Template Engine
- Third-Party Integration: Python 'requests' library (Reddit JSON API)
- Authentication: Django Auth Framework, Cryptographic Tokens, & DRF Authentication.

---------------
# Prerequisites
---------------
Make sure you have the following installed on your system:
- Python (version 3.14.4)
- MariaDB / MySQL server

----------------------------------
# Installation & Local Setup Guide
----------------------------------

Follow these steps to set up and run the project locally on your machine:

1. Clone or Extract the Project
    - Clone the project from your GitHub profile and enter the project folder
    ```bash
    
    git clone https://github.com/mcusick001/Django-eCommerce-Application-Part-2
    
    cd NEW-Django-eCommerce-Part2
    ```

2. Set Up a Virtual Environment & Install Dependencies
    ```bash
    
    python -m venv venv

    venv\Scripts\Activate.ps1

    pip install -r requirements.txt
    ```

3. Configure the Environmental Variables
    - Windows (Command Prompt):
    ```cmd

    copy .env.example .env
    ```
    - Open the newly created .env file in your code editor and update
      the database username, password, and secret key to match your
      local environment.
      
4. Log into your MariaDB shell and create the database:
    ```bash

    mysql -u root -p
    ```
    - Once logged in, run the following SQL commands to create the
      database and user:
    ```sql

    CREATE DATABASE ecommerce_db;
    CREATE USER 'shop_user'@'localhost' IDENTIFIED BY 'password123';
    GRANT ALL PRIVILEGES ON ecommerce_db.* TO 'shop_user'@'localhost';
    FLUSH PRIVILEGES;
    EXIT;
    ``` 

5. Run Database Migrations
    - Apply the Django schema to your MariaDB instance:
    ```bash:

    python manage.py makemigrations
    python manage.py migrate
    ```

6. Create an Administrator (Superuser) Account
    ```bash:

    python manage.py createsuperuser
    ```
    - Follow the prompts to enter username, email, and password.

7. Run the deployment server
    ```bash:

    python manage.py runserver
    ```
    - Open your brower and navigate to 'http://127.0.0.1:8000/'
    to use the application!
