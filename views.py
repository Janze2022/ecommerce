from core.forms import *
from core.models import *
from core.models import Category, Product
from core.forms import CheckoutForm
from core.forms import *
from core.models import *
from django.utils import timezone
from django.shortcuts import get_object_or_404, render, redirect
from django.contrib.auth.decorators import login_required
from .models import CheckoutAddress, Order, OrderItem


def order_confirmation(request, order_id):
    """View for the order confirmation page."""
    # Get the order using the order_id
    order = get_object_or_404(Order, pk=order_id)
    return render(request, 'core/order_confirmation.html', {'order': order})


@login_required
def checkout_view(request):
    # Check if user already has a checkout address
    if CheckoutAddress.objects.filter(user=request.user).exists():
        return render(request, 'core/checkout.html', {'payment_allow': 'allow'})

    if request.method == 'POST':
        form = CheckoutForm(request.POST)
        if form.is_valid():
            street_address = form.cleaned_data.get('street_address')
            apartment_address = form.cleaned_data.get('apartment_address')
            country = form.cleaned_data.get('country')
            zip_code = form.cleaned_data.get('zip_code')

            try:
                # Save the checkout address
                checkout_address = CheckoutAddress(
                    user=request.user,
                    street_address=street_address,
                    apartment_address=apartment_address,
                    country=country,
                    zip_code=zip_code,
                )
                checkout_address.save()

                # After saving address, create an order
                order = Order.objects.create(
                    user=request.user,
                    ordered_date=timezone.now(),
                    status='pending'  # You can set the status to pending or any other relevant status
                )

                # Add all cart items to the order
                order_items = OrderItem.objects.filter(user=request.user, ordered=False)
                for order_item in order_items:
                    order.items.add(order_item)
                    order_item.ordered = True
                    order_item.save()

                order.save()
                messages.success(request, "Order placed successfully!")

                # Redirect to the order confirmation page with the order_id
                return redirect('order_confirmation', order_id=order.id)

            except Exception as e:
                messages.warning(request, f"Error saving checkout address or placing the order: {str(e)}")
                return redirect('checkout_view')
        else:
            messages.warning(request, "Please fix the errors in the form.")
            return render(request, 'core/checkout.html', {'form': form})
    else:
        form = CheckoutForm()
        return render(request, 'core/checkout.html', {'form': form})


def category_view(request, category_id):
    category = get_object_or_404(Category, pk=category_id)
    products = Product.objects.filter(category=category)
    return render(request, 'core/category.html', {'category': category, 'products': products})



@login_required
def orderlist(request):
    order = Order.objects.filter(user=request.user, ordered=False).first()
    if order:
        return render(request, 'core/orderlist.html', {'order': order})
    else:
        return render(request, 'core/orderlist.html', {'message': "Your cart is empty."})

def order_confirmation(request):
    """View for the order confirmation page."""
    # This could render a template showing the confirmation details or a success message
    return render(request, 'core/order_confirmation.html')

@login_required
def checkout_view(request):
    # Check if user already has a checkout address
    if CheckoutAddress.objects.filter(user=request.user).exists():
        return render(request, 'core/checkout.html', {'payment_allow': 'allow'})

    if request.method == 'POST':
        form = CheckoutForm(request.POST)
        if form.is_valid():
            street_address = form.cleaned_data.get('street_address')
            apartment_address = form.cleaned_data.get('apartment_address')
            country = form.cleaned_data.get('country')
            zip_code = form.cleaned_data.get('zip_code')

            try:
                # Save the checkout address
                checkout_address = CheckoutAddress(
                    user=request.user,
                    street_address=street_address,
                    apartment_address=apartment_address,
                    country=country,
                    zip_code=zip_code,
                )
                checkout_address.save()

                # After saving address, create an order
                order = Order.objects.create(
                    user=request.user,
                    ordered_date=timezone.now(),
                    status='pending'  # You can set the status to pending or any other relevant status
                )

                # Add all cart items to the order
                order_items = OrderItem.objects.filter(user=request.user, ordered=False)
                for order_item in order_items:
                    order.items.add(order_item)
                    order_item.ordered = True
                    order_item.save()

                order.save()
                messages.success(request, "Order placed successfully!")
                return redirect('orderlist')  # Redirect to order list or confirmation page

            except Exception as e:
                messages.warning(request, f"Error saving checkout address or placing the order: {str(e)}")
                return redirect('checkout_view')
        else:
            messages.warning(request, "Please fix the errors in the form.")
            return render(request, 'core/checkout.html', {'form': form})
    else:
        form = CheckoutForm()
        return render(request, 'core/checkout.html', {'form': form})

def checkout_address(request):
    if request.method == 'POST':
        form = CheckoutAddressForm(request.POST)
        if form.is_valid():
            # Save the form but don't commit to the database yet
            checkout_address = form.save(commit=False)
            checkout_address.user = request.user  # Associate with the logged-in user
            checkout_address.save()  # Save the address
            messages.success(request, "Address saved successfully!")
            return redirect('checkout')  # Redirect to checkout page or another page
        else:
            # Handle form errors
            print(form.errors)
            messages.error(request, "There was an error with your form.")
    else:
        form = CheckoutAddressForm()

    return render(request, 'checkout_address.html', {'form': form})

def category_view(request, category_id):
    category = get_object_or_404(Category, pk=category_id)
    products = Product.objects.filter(category=category)
    return render(request, 'core/category.html', {'category': category, 'products': products})

from django.shortcuts import render, redirect
from .forms import CheckoutAddressForm
from django.contrib import messages

def checkout(request):
    if request.method == 'POST':
        form = CheckoutAddressForm(request.POST)
        if form.is_valid():
            # Save the form but don't commit to the database yet
            checkout_address = form.save(commit=False)
            checkout_address.user = request.user  # Associate the address with the logged-in user
            checkout_address.save()  # Save the address
            messages.success(request, "Address saved successfully!")
            return redirect('checkout')  # Redirect to checkout or another page
        else:
            # Handle form errors
            print(form.errors)
            messages.error(request, "There was an error with your form.")
    else:
        form = CheckoutAddressForm()

    return render(request, 'checkout.html', {'form': form})


# Create your views here.
def search_products(request):
    query = request.GET.get('query', '')  # Get the search query from the form
    products = Product.objects.filter(name__icontains=query)  # Filter products based on the query
    return render(request, 'core/search_results.html', {'products': products, 'query': query})

@login_required
def checkout_page(request):
    # Check if user already has a checkout address
    if CheckoutAddress.objects.filter(user=request.user).exists():
        return render(request, 'core/checkout.html', {'payment_allow': 'allow'})

    if request.method == 'POST':
        form = CheckoutForm(request.POST)
        if form.is_valid():
            street_address = form.cleaned_data.get('street_address')
            apartment_address = form.cleaned_data.get('apartment_address')
            country = form.cleaned_data.get('country')
            zip_code = form.cleaned_data.get('zip_code')

            try:
                # Save the checkout address
                checkout_address = CheckoutAddress(
                    user=request.user,
                    street_address=street_address,
                    apartment_address=apartment_address,
                    country=country,
                    zip_code=zip_code,
                )
                checkout_address.save()
                return render(request, 'core/checkout.html', {'payment_allow': 'allow'})
            except Exception as e:
                messages.warning(request, f"Error saving checkout address: {str(e)}")
                return redirect('checkout_page')

        else:
            messages.warning(request, "Please fix the errors in the form.")
            return render(request, 'core/checkout.html', {'form': form})
    else:
        form = CheckoutForm()
        return render(request, 'core/checkout.html', {'form': form})


def index(request):
    # List all products
    products = Product.objects.all()
    return render(request, 'core/index.html', {'products': products})


@login_required
def add_product(request):
    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, "Product Added Successfully")
            return redirect('/')
        else:
            messages.warning(request, "There was an error with your form.")
    else:
        form = ProductForm()

    return render(request, 'core/add_product.html', {'form': form})


def product_desc(request, pk):
    product = get_object_or_404(Product, pk=pk)
    return render(request, 'core/product_desc.html', {'product': product})


@login_required
def add_to_cart(request, pk):
    product = get_object_or_404(Product, pk=pk)

    if product.product_available_count < 1:
        messages.info(request, "Sorry, this product is out of stock.")
        return redirect("orderlist")

    # Create or get the order item for the user, including the sale_in field
    order_item, created = OrderItem.objects.get_or_create(
        product=product,
        user=request.user,
        ordered=False,
        sale_in=product.sale_in  # Add sale_in field here
    )

    # Get the order for the user or create one
    order_qs = Order.objects.filter(user=request.user, ordered=False)

    if order_qs.exists():
        order = order_qs[0]
        if order.items.filter(product__pk=pk).exists():
            if order_item.quantity < product.product_available_count:
                order_item.quantity += 1
                order_item.save()
                product.product_available_count -= 1
                product.save()
                messages.info(request, "Item quantity updated in cart.")
            else:
                messages.info(request, "Sorry, not enough stock.")
        else:
            order.items.add(order_item)
            product.product_available_count -= 1
            product.save()
            messages.info(request, "Item added to cart.")
    else:
        ordered_date = timezone.now()
        order = Order.objects.create(user=request.user, ordered_date=ordered_date)
        order.items.add(order_item)
        product.product_available_count -= 1
        product.save()
        messages.info(request, "Item added to cart.")

    return redirect("product_desc", pk=pk)


@login_required
def orderlist(request):
    order = Order.objects.filter(user=request.user, ordered=False).first()
    if order:
        return render(request, 'core/orderlist.html', {'order': order})
    else:
        return render(request, 'core/orderlist.html', {'message': "Your cart is empty."})


@login_required
def add_item(request, pk):
    product = get_object_or_404(Product, pk=pk)

    # Create or get the order item for the user
    order_item, created = OrderItem.objects.get_or_create(
        product=product,
        user=request.user,
        ordered=False,
    )

    # Get the order for the user or create one
    order_qs = Order.objects.filter(user=request.user, ordered=False)
    if order_qs.exists():
        order = order_qs[0]
        if order.items.filter(product__pk=pk).exists():
            if order_item.quantity < product.product_available_count:
                order_item.quantity += 1
                order_item.save()
                product.product_available_count -= 1
                product.save()
                messages.info(request, "Item quantity updated in cart.")
            else:
                messages.info(request, "Sorry, not enough stock.")
            return redirect("orderlist")
        else:
            order.items.add(order_item)
            messages.info(request, "Item added to cart.")
            return redirect("orderlist")
    else:
        ordered_date = timezone.now()
        order = Order.objects.create(user=request.user, ordered_date=ordered_date)
        order.items.add(order_item)
        messages.info(request, "Item added to cart.")
        return redirect("orderlist")


@login_required
def remove_item(request, pk):
    item = get_object_or_404(Product, pk=pk)
    order_qs = Order.objects.filter(user=request.user, ordered=False)

    if order_qs.exists():
        order = order_qs[0]
        if order.items.filter(product__pk=pk).exists():
            order_item = OrderItem.objects.get(
                product=item,
                user=request.user,
                ordered=False,
            )
            if order_item.quantity > 1:
                order_item.quantity -= 1
                order_item.save()
                item.product_available_count += 1
                item.save()
                messages.info(request, "Item quantity updated successfully.")
            else:
                order_item.delete()
                item.product_available_count += 1
                item.save()
                messages.info(request, "Item removed from cart.")
        else:
            messages.info(request, "This item is not in your cart.")
    else:
        messages.info(request, "You do not have any order.")

    return redirect("orderlist")


@login_required
def profile(request):
    try:
        customer = Customer.objects.get(user=request.user)
    except Customer.DoesNotExist:
        customer = Customer.objects.create(user=request.user)

    # Handle optional fields like phone and profile picture
    phone = getattr(customer, 'phone', 'Not provided')
    profile_pic_url = getattr(customer, 'profile_pic', None)

    return render(request, 'accounts/profile.html', {
        'customer': customer,
        'phone': phone,
        'profile_pic_url': profile_pic_url,
    })
