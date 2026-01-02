from django.shortcuts import render, redirect
from django.contrib import messages
from apps.master.helpers import is_valid_email, is_valid_mobile, is_valid_password
from apps.users.models import User
# Create your views here.
def signin(request):
    return render(request, "store/signin.html")

def signup(request):
    if request.method == "POST":
        first_name_ = request.POST.get('first_name')
        last_name_ = request.POST.get('last_name')
        email_ = request.POST.get('email')
        mobile_ = request.POST.get('mobile')
        password_ = request.POST.get('password')
        confirm_password_ = request.POST.get('confirm_password')

        # Email format check
        if not is_valid_email(email_):
            messages.warning(request, "Your email address is invalid.")
            return render(request, "store/signup.html")

        # Email already exists check (FIXED)
        if User.objects.filter(email=email_).exists():
            messages.info(request, "This email already exists.")
            return render(request, "store/signup.html")

        # Mobile validation
        if not is_valid_mobile(mobile_):
            messages.warning(request, "Mobile number is invalid (format: +91 XXXXXXXXXX).")
            return render(request, "store/signup.html")

        # Password match check
        if password_ != confirm_password_:
            messages.warning(request, "Password and Confirm Password do not match.")
            return render(request, "store/signup.html")

        # Password validation
        is_valid_password_, message = is_valid_password(password_)
        if not is_valid_password_:
            messages.warning(request, message)
            return render(request, "store/signup.html")
        
        # new_user = User.objects.create(
        #     first_name = first_name_,
        #     last_name = last_name_,
        #     email = email_,
        #     mobile = mobile_,
        #     password = password_
        # )
        # new_user.save()
        messages.success(request, "Your registration has been succefully done.")
        return render(request, 'store/otp_verification.html', {"email": email_})
    return render(request, "store/signup.html")

def otp_verify(request):
    return render(request, 'store/otp_verification.html')

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