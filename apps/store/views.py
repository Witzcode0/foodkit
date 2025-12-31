from django.shortcuts import render

# Create your views here.
def signin(request):
    return render(request, "store/signin.html")

def signup(request):
    if request.method == "POST":
        first_name_ = request.POST['first_name']
        last_name_ = request.POST['last_name']
        email_ = request.POST['email']
        mobile_ = request.POST['mobile']
        password_ = request.POST['password']
        confirm_password_ = request.POST['confirm_password']

        print(first_name_, last_name_, email_, mobile_, password_, confirm_password_)
    return render(request, "store/signup.html")

def forgot_password(request):
    return render(request, "store/forgot_password.html")

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