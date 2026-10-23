"""
URL routing configuration for the marketplace
application.

Maps URL endpoints to their corresponding view
functions for authentication, vendor dashboards,
store/product management, cart operations, reviews
and password reset flows.
"""

from rest_framework.routers import DefaultRouter
from .api_views import StoreViewSet, ProductViewSet, ReviewViewSet

from django.contrib.auth import views as auth_views
from django.urls import path, include
from . import views

router = DefaultRouter()
router.register(r'stores', StoreViewSet, basename='store')
router.register(r'products', ProductViewSet, basename='product')
router.register(r'reviews', ReviewViewSet, basename='review')

urlpatterns = [
    path('', views.home_view, name='home'),
    path('register/', views.register_view, name='register'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),

    # Vendor Dashboard & Store Management
    path('vendor/dashboard/', views.vendor_dashboard, name='vendor_dashboard'),
    path('vendor/stores/new/', views.store_create, name='store_create'),
    path(
        'vendor/stores/<int:store_id>/edit/',
        views.store_edit,
        name='store_edit'
    ),
    path(
        'vendor/stores/<int:store_id>/delete/',
        views.store_delete,
        name='store_delete'
    ),

    # Vendor Product Management
    path(
        'vendor/stores/<int:store_id>/products/new/',
        views.product_add,
        name='product_add'
    ),
    path(
        'vendor/products/<int:product_id>/edit/',
        views.product_edit,
        name='product_edit'
    ),
    path(
        'vendor/products/<int:product_id>/delete/',
        views.product_delete,
        name='product_delete'
    ),

    # Buyer Cart & Checkout
    path('cart/', views.view_cart, name='view_cart'),
    path(
        'cart/add/<int:product_id>/',
        views.add_to_cart,
        name='add_to_cart'
    ),
    path(
        'cart/update/<int:product_id>/',
        views.update_cart,
        name='update_cart'
    ),
    path(
        'cart/remove/<int:product_id>/',
        views.remove_from_cart,
        name='remove_from_cart'
    ),
    path('checkout/', views.checkout, name='checkout'),

    # Reviews
    path(
        'products/<int:product_id>/review/',
        views.add_review,
        name='add_review'
    ),
    path(
        'reviews/recent/',
        views.recent_reviews,
        name='recent_reviews'
    ),

    # Password Reset (Secure Expiring Token Flow via Django Built-in Views)
    path(
        'password-reset/',
        auth_views.PasswordResetView.as_view(
            template_name='registration/password_reset_form.html'
        ),
        name='password_reset'
    ),
    path(
        'password-reset/done/',
        auth_views.PasswordResetDoneView.as_view(
            template_name='registration/password_reset_done.html'
        ),
        name='password_reset_done'
    ),
    path(
        'reset/<uidb64>/<token>/',
        auth_views.PasswordResetConfirmView.as_view(
            template_name='registration/password_reset_confirm.html'
        ),
        name='password_reset_confirm'
    ),
    path(
        'reset/done/',
        auth_views.PasswordResetCompleteView.as_view(
            template_name='registration/password_reset_complete.html'
        ),
        name='password_reset_complete'
    ),
    path('reddit/', views.reddit_feed_view, name='reddit_feed'),

    # DRF API Endpoints under /api/
    path('api/', include(router.urls)),
]
