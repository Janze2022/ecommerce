from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', views.index, name='index'),
    path('category/<int:category_id>/', views.category_view, name='category_view'),
    path('search/', views.search_products, name='search_products'),  # Add this line for search

    path('add_product', views.add_product, name='add_product'),

    path('product_desc/<pk>', views.product_desc, name='product_desc'),

    path('add_to_cart/<pk>', views.add_to_cart, name='add_to_cart'),

    path('orderlist', views.orderlist, name='orderlist'),

    path('add_item/<int:pk>', views.add_item, name='add_item'),

    path('remove_item/<int:pk>', views.remove_item, name='remove_item'),

    path('checkout_page', views.checkout_page, name='checkout_page'),
    path('checkout/', views.checkout_view, name='checkout_view'),
    path('order-confirmation/<int:order_id>/', views.order_confirmation, name='order_confirmation'),  # Update URL pattern to capture order_id
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
