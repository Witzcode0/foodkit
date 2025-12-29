from django.urls import path
from apps.store.views import *

urlpatterns = [
    path("", index, name="index")
]