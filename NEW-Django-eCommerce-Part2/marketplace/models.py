"""
Database models for the marketplace application.

Defines the custom User, model, Store, Product, Order,
OrderItem and Review models.
"""
from django.contrib.auth.models import AbstractUser
from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator

# Create your models here.


class User(AbstractUser):
    """
    Custom User model extending Django's AbstractUser.

    Attributes:
        is_vendor (bool): Flag indicating if the user is a vendor.
        is_buyer (bool): Flag indicating if the user is a buyer.
    """
    is_vendor = models.BooleanField(default=False)
    is_buyer = models.BooleanField(default=False)


class Store(models.Model):
    """
    Represents a store owned by a vendor.
    """
    vendor = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="stores"
    )
    name = models.CharField(max_length=255, unique=True)
    description = models.TextField()

    def __str__(self):
        """Returns the store name string representation."""
        return self.name


class Product(models.Model):
    """
    Represents an item sold within a vendor store.
    """
    store = models.ForeignKey(
        Store,
        on_delete=models.CASCADE,
        related_name='products'
    )
    name = models.CharField(max_length=200)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    stock = models.PositiveIntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        """Returns the product name string representation."""
        return self.name


class Order(models.Model):
    """
    Represents a completed customer pruchase.
    """
    buyer = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="orders"
    )
    created_at = models.DateTimeField(auto_now_add=True)


class OrderItem(models.Model):
    """
    Represents an individual line items inside an order.
    """
    order = models.ForeignKey(
        Order,
        on_delete=models.CASCADE,
        related_name="items"
    )
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)


class Review(models.Model):
    """
    Represents customer product reviews.
    """
    product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE,
        related_name="reviews"
    )
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    rating = models.IntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(5)],
        help_text="Rating from 1 (poor) to 5 (excellent)"
    )
    text = models.TextField()
    is_verified = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        """Returns a formatted review summary string."""
        status = "Verified" if self.is_verified else "Unverified"
        return f"Review by {self.user.username} ({status})"
