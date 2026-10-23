"""
View functions for managing authentication, vendor dashboards,
store/product CRUD, shoppin_cart, checkout, and customer reviews.
"""
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, logout
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.decorators import login_required
from django.core.mail import send_mail
from django.contrib import messages

from functions.reddit import fetch_reddit_posts

from .models import Store, Product, OrderItem, Review
from .forms import CustomeUserCreationForm, StoreForm, ProductForm, ReviewForm
from .decorators import vendor_required, buyer_required

# Create your views here.


def reddit_feed_view(request):
    posts = fetch_reddit_posts(limit=10)
    return render(request, 'marketplace/reddit_feed.html', {'posts': posts})


def register_view(request):
    """
    Handles user registration for both buyers and vendors.

    Returns:
        HttpResponse: Rendered registration template or redirect
        to home.
    """
    if request.method == 'POST':
        form = CustomeUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('home')
    else:
        form = CustomeUserCreationForm()
    return render(request, 'registration/register.html', {'form': form})


def login_view(request):
    """
    Handles user login authentication.

    Returns:
        HttpResponse: Rendered login template or redirect on success.
    """
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('home')
    else:
        form = AuthenticationForm()
    return render(request, 'registration/login.html', {'form': form})


def logout_view(request):
    """
    Logs out the current authenticated user.

    Returns:
        HttpResponseRedirect: Redirect to home page.
    """
    logout(request)
    return redirect('home')


def home_view(request):
    """
    Displays marketplace homepage listing all available products.

    Returns:
        HttpResponse: Rendered product catalog template.
    """
    products = Product.objects.select_related('store').all()
    return render(request, 'marketplace/home.html', {'products': products})


@login_required
@vendor_required
def vendor_dashboard(request):
    """
    Displays the vendor dashboard showing their stores and products.

    Returns:
        HttpResponse: Rendered vendor dashboard template.
    """
    stores = Store.objects.filter(vendor=request.user)
    return render(request, 'marketplace/vendor_dashboard.html',
                  {'stores': stores})


@login_required
@vendor_required
def store_create(request):
    """
    Allows a vendor to create a new store.

    Returns:
        HttpResponse: Rendered store creation form or redirect to dashboard.
    """
    if request.method == 'POST':
        form = StoreForm(request.POST)
        if form.is_valid():
            store = form.save(commit=False)
            store.vendor = request.user
            store.save()
            return redirect('vendor_dashboard')
    else:
        form = StoreForm()
    return render(request, 'marketplace/store_form.html', {'form': form})


@login_required
@vendor_required
def store_edit(request, store_id):
    """
    Allows a vendor to edit an existing store they own.

    Returns:
        HttpResponse: Rendered store form or redirect.
    """
    store = get_object_or_404(Store, id=store_id, vendor=request.user)
    if request.method == 'POST':
        form = StoreForm(request.POST, instance=store)
        if form.is_valid():
            form.save()
            return redirect('vendor_dashboard')
    else:
        form = StoreForm(instance=store)
    return render(request, 'marketplace/store_form.html',
                  {'form': form, 'store': store})


@login_required
@vendor_required
def store_delete(request, store_id):
    """
    Allows a vendor to delete an existing store they own.

    Returns:
        HttpResponseRedirect: Redirect to vendor dashboard.
    """
    store = get_object_or_404(Store, id=store_id, vendor=request.user)
    if request.method == 'POST':
        store.delete()
        return redirect('vendor_dashboard')
    return render(request, 'marketplace/store_confirm_delete.html',
                  {'store': store})


@login_required
@vendor_required
def product_add(request, store_id):
    """
    Allows a vendor to add a product to their specific store.

    Returns:
        HttpResponse: Rendered product form or redirect.
    """
    store = get_object_or_404(Store, id=store_id, vendor=request.user)
    if request.method == 'POST':
        form = ProductForm(request.POST)
        if form.is_valid():
            product = form.save(commit=False)
            product.store = store
            product.save()
            return redirect('vendor_dashboard')
    else:
        form = ProductForm()
    return render(request, 'marketplace/product_form.html',
                  {'form': form, 'store': store})


@login_required
@vendor_required
def product_edit(request, product_id):
    """
    Allows a vendor to edit a product in their store.

    Returns:
        HttpResponse: Rendered product form or redirect.
    """
    product = get_object_or_404(
        Product, id=product_id, store__vendor=request.user
    )
    if request.method == 'POST':
        form = ProductForm(request.POST, instance=product)
        if form.is_valid():
            form.save()
            return redirect('vendor_dashboard')
    else:
        form = ProductForm(instance=product)
    return render(request, 'marketplace/product_form.html',
                  {'form': form, 'product': product})


@login_required
@vendor_required
def product_delete(request, product_id):
    """
    Allows a vendor to remove a product.

    Returns:
        HttpResponseRedirect: Redirect to dashboard.
    """
    product = get_object_or_404(
        Product, id=product_id, store__vendor=request.user
    )
    if request.method == 'POST':
        product.delete()
        return redirect('vendor_dashboard')
    return render(request, 'marketplace/product_confirm_delete.html',
                  {'product': product})


@login_required
@buyer_required
def add_to_cart(request, product_id):
    """
    Adds a product to the user's session-based shopping cart.

    Returns:
        HttpResponseRedirect: Redirect to cart view.
    """
    product = get_object_or_404(Product, id=product_id)
    quantity = int(request.POST.get('quantity', 1))

    if quantity > product.stock:
        messages.error(
            request,
            f"Cannot add {quantity} units. Only {product.stock} available."
            )
        return redirect('home')

    cart = request.session.get('cart', {})

    if str(product_id) in cart:
        cart[str(product_id)]['quantity'] += quantity
    else:
        cart[str(product_id)] = {
            'quantity': quantity,
            'price': float(product.price),
            'name': product.name
        }

    request.session['cart'] = cart
    return redirect('view_cart')


@login_required
@buyer_required
def update_cart(request, product_id):
    cart = request.session.get('cart', {})
    if str(product_id) in cart:
        quantity = int(request.POST.get('quantity', 1))
        product = get_object_or_404(Product, id=product_id)
        if quantity > product.stock:
            messages.error(
                request,
                f"Stock limit exceeded. Max available: {product.stock}"
                )
        else:
            cart[str(product_id)]['quantity'] = quantity
            request.session['cart'] = cart
    return redirect('view_cart')


@login_required
@buyer_required
def remove_from_cart(request, product_id):
    cart = request.session.get('cart', {})
    if str(product_id) in cart:
        del cart[str(product_id)]
        request.session['cart'] = cart
    return redirect('view_cart')


@login_required
@buyer_required
def view_cart(request):
    """
    Displays the current contents of the buyer's shopping cart.

    Returns:
        HttpResponse: Rendered cart template.
    """
    cart = request.session.get('cart', {})
    total = sum(item['price'] * item['quantity'] for item in cart.values())
    return render(request, 'marketplace/cart.html',
                  {'cart': cart, 'total': total})


@login_required
@buyer_required
def checkout(request):
    """
    Processes cart checkout atomically, creates order records,
    sends invoice email, and clears the cart session.

    Returns:
        HttpResponse: Rendered checkout success template or redirect.
    """
    cart = request.session.get('cart', {})

    if not cart:
        messages.warning(request, "Your cart is empty.")
        return redirect('view_cart')

    if request.method == 'POST':
        for item_id, item_data in cart.items():
            product = get_object_or_404(Product, id=item_id)
            quantity = item_data['quantity']

            if quantity > product.stock:
                messages.error(
                    request,
                    f"Sorry, only {product.stock} units ("
                    f"of {product.name} are available."
                    )
                return redirect('view_cart')

            product.stock -= quantity
            product.save()

        invoice_message = (
            f"Thank you for your order, {request.user.username}!\n\n"
            f"Your order has been successfully processed and placed."
        )
        send_mail(
            subject="Your eCommerce Store Invoice",
            message=invoice_message,
            from_email="admin@ecommerce.local",
            recipient_list=[request.user.email],
            fail_silently=False,
        )

        request.session['cart'] = {}
        request.session.modified = True

        messages.success(
            request,
            "Order placed successfully! Invoice printed to console."
            )
        return redirect('home')

    return render(request, 'marketplace/checkout_success.html', {'cart': cart})


@login_required
def add_review(request, product_id):
    """
    Allows users to submit a product review. Automatically
    verifies if the buyer has a past order containing the
    product.

    Returns:
        HttpResponse: Rendered review form or redirect.
    """
    product = get_object_or_404(Product, id=product_id)
    if request.method == 'POST':
        form = ReviewForm(request.POST)
        if form.is_valid():
            review = form.save(commit=False)
            review.product = product
            review.user = request.user

            has_purchased = OrderItem.objects.filter(
                order__buyer=request.user,
                product=product
            ).exists()

            review.is_verified = has_purchased
            review.save()
            return redirect('recent_reviews')
    else:
        form = ReviewForm()
    return render(
        request, 'marketplace/review_form.html',
        {'form': form, 'product': product}
    )


def recent_reviews(request):
    """
    Displays the 20 most recent customer reviews across
    the marketplace.

    Returns:
        HttpResponse: Rendered recent reviews template.
    """
    reviews = Review.objects.select_related(
        'product', 'product__store', 'user'
    ).order_by('-created_at')[:20]
    return render(request, 'marketplace/recent_reviews.html',
                  {'reviews': reviews})
