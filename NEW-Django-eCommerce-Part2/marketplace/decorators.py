"""
Custom decorators for role-based access control across views.
"""
from functools import wraps
from django.core.exceptions import PermissionDenied


def vendor_required(view_func):
    """
    Restrict view access strictly to authenticated vendor users.

    Returns:
        callable: Wrapped view function checking user vendor privileges.
    """
    @wraps(view_func)
    def _wrapped_view(request, *args, **kwargs):
        if request.user.is_authenticated and request.user.is_vendor:
            return view_func(request, *args, **kwargs)
        raise PermissionDenied("Access restricted to registered vendors.")

    return _wrapped_view


def buyer_required(view_func):
    """
    Restricts view access strictly to authenticated buyer accounts.

    Returns:
        callable: Wrapped view function checking user buyer privileges.
    """
    @wraps(view_func)
    def _wrapped_view(request, *args, **kwargs):
        if request.user.is_authenticated and request.user.is_buyer:
            return view_func(request, *args, **kwargs)
        raise PermissionDenied("Access restricted to registered buyers.")

    return _wrapped_view
