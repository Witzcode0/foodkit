from django.shortcuts import render

# Create your views here.
def index(request):
    return render(request, "store/index.html")

def products(request):
    return render(request, "store/products.html")

def blogs(request):
    return render(request, "store/blogs.html")

def about(request):
    return render(request, "store/about.html")

def contact(request):
    return render(request, "store/contact.html")