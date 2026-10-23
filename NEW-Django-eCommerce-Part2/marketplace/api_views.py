from rest_framework import viewsets, permissions
from .models import Store, Product, Review
from .serializers import StoreSerializer, ProductSerializer, ReviewSerializer


class IsVendorOrReadOnly(permissions.BasePermission):
    """
    Custom permission: Allows read-only access for anyone,
    but restricts write/create actions to authenticated vendors.
    """
    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return True
        return request.user.is_authenticated and getattr(
            request.user, 'is_vendor', False
            )


class StoreViewSet(viewsets.ModelViewSet):
    queryset = Store.objects.all()
    serializer_class = StoreSerializer
    permission_classes = [IsVendorOrReadOnly]

    def perform_create(self, serializer):
        # Automatically assign the logged-in user as the vendor when creating
        # a store
        serializer.save(vendor=self.request.user)


class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    permission_classes = [IsVendorOrReadOnly]


class ReviewViewSet(viewsets.ReadOnlyModelViewSet):
    """
    ReadOnlyModelViewSet allows users to retrieve/view reviews
    without allowing unauthorized modifications via the API.
    """
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer
    permission_classes = [permissions.AllowAny]
