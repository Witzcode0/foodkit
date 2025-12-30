from django.urls import path
from apps.store.views import *

urlpatterns = [
    path("", index, name="index"),
    path("products/", products, name="products"),
    path("blogs/", blogs, name="blogs"),
    path("about/", about, name="about"),
    path("contact/", contact, name="contact"),
]