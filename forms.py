from django import forms
from .models import Product, Category, SaleIn, CheckoutAddress
from django_countries.fields import CountryField
from django_countries.widgets import CountrySelectWidget


class CheckoutForm(forms.Form):
    first_name = forms.CharField(max_length=100)
    last_name = forms.CharField(max_length=100)
    city = forms.CharField(max_length=100)
    postal_code = forms.CharField(max_length=20)
    country = CountryField().formfield(widget=CountrySelectWidget())
    email = forms.EmailField()

    # Making address field optional
    street_address = forms.CharField(max_length=200, required=False)
    apartment_address = forms.CharField(max_length=200, required=False)


class CheckoutAddressForm(forms.ModelForm):
    class Meta:
        model = CheckoutAddress
        fields = ['street_address', 'apartment_address', 'country', 'zip_code']
        widgets = {
            'street_address': forms.TextInput(attrs={'class': 'form-control'}),
            'apartment_address': forms.TextInput(attrs={'class': 'form-control'}),
            'country': CountrySelectWidget(attrs={'class': 'form-control'}),
            'zip_code': forms.TextInput(attrs={'class': 'form-control'}),
        }

    def clean(self):
        cleaned_data = super().clean()
        # Add additional validation here if necessary
        return cleaned_data


class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ['name', 'category', 'sale_in', 'desc', 'price', 'product_available_count', 'product_image']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'category': forms.Select(attrs={'class': 'form-control'}),
            'sale_in': forms.Select(attrs={'class': 'form-control'}),
            'desc': forms.Textarea(attrs={'class': 'form-control', 'rows': '3'}),
            'price': forms.NumberInput(attrs={'class': 'form-control'}),
            'product_available_count': forms.NumberInput(attrs={'class': 'form-control'}),
            'product_image': forms.FileInput(attrs={'class': 'form-control'}),
        }

    def __init__(self, *args, **kwargs):
        super(ProductForm, self).__init__(*args, **kwargs)

        # Optional: You can set an empty label for select fields
        self.fields['category'].empty_label = "Select Category"
        self.fields['sale_in'].empty_label = "Select Sale Unit"

        # Optionally, set required=True for product image
        self.fields['product_image'].required = True
