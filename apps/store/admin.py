from django.contrib import admin
from apps.store.models import BlogCategory, Blogs
# Register your models here.

admin.site.register(BlogCategory)
admin.site.register(Blogs)
