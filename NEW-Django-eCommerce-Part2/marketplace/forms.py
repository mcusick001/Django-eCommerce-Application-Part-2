"""
Forms for user registration, stores, products, and reviews
in the marketplace app.
"""

from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import User, Store, Product, Review


class CustomeUserCreationForm(UserCreationForm):
    """
    Extended user creation form allowing selection of buyer or vendor role.
    """

    role = forms.ChoiceField(
        choices=[('buyer', 'Buyer'), ('vendor', 'Vendor')],
        required=True,
        widget=forms.Select(attrs={'class': 'form-select'})
    )

    class Meta(UserCreationForm.Meta):
        model = User
        fields = UserCreationForm.Meta.fields + ('email', 'role')

    def clean_email(self):
        email = self.cleaned_data.get('email')

        if email and User.objects.filter(email=email).exists():
            raise forms.ValidationError(
                "An account with this email address already exists."
                )

        return email

    def save(self, commit=True):
        """
        Saves the user and assigns vendor or buyer flags
        based on selected role.

        Returns:
            User: The created user instance.
        """
        user = super().save(commit=False)
        role = self.cleaned_data.get('role')
        if role == 'vendor':
            user.is_vendor = True
            user.is_buyer = False
        else:
            user.is_buyer = True
            user.is_vendor = False
        if commit:
            user.save()
        return user


class StoreForm(forms.ModelForm):
    """
    Form for creating and updating vendor stores.
    """

    class Meta:
        model = Store
        fields = ['name', 'description']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'description': forms.Textarea(
                attrs={'class': 'form-control', 'rows': 4}
            ),
        }


class ProductForm(forms.ModelForm):
    """
    Form for adding and updating products within a store.
    """

    class Meta:
        model = Product
        fields = ['name', 'description', 'price', 'stock']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'description': forms.Textarea(
                attrs={'class': 'form-control', 'rows': 3}
            ),
            'price': forms.NumberInput(attrs={'class': 'form-control'}),
            'stock': forms.NumberInput(
                attrs={'class': 'form-control', 'min': 0}
            )
        }


class ReviewForm(forms.ModelForm):
    """
    Form for submitting customer product reviews.
    """

    class Meta:
        model = Review
        fields = ['rating', 'text']
        widgets = {
            'rating': forms.NumberInput(
                attrs={'class': 'form-control', 'min': 1, 'max': 5}
            ),
            'text': forms.Textarea(
                attrs={'class': 'form-control', 'rows': 3}
            ),
        }
