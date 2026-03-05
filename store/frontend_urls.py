# store/frontend_urls.py
from django.urls import path

from store import views
from .views import *

urlpatterns = [
    path("", products_page, name="products_page"),
    path("cart/", cart_page, name="cart_page"),
    path("product/<int:id>/", views.product_detail_page, name="product_detail"),
    path("checkout/", views.checkout_page, name="checkout"),
]
