from django.shortcuts import render, redirect
from django.contrib import messages
from django.core.mail import send_mail
from apps.master.helpers import is_valid_email, is_valid_mobile, is_valid_password, generate_otp
from apps.users.models import User
from functools import wraps

# Create your views here.
def login_required(view_func):
    @wraps(view_func)
    def wrapper(request, *args, **kwargs):
        if request.session.get('user_id'):
            return view_func(request, *args, **kwargs)
        
        messages.warning(request, "Please log in to continue.")
        return redirect('signin')
    return wrapper

def signin(request):
    if request.method == "POST":
        email_ = request.POST.get('email')
        password_ = request.POST.get('password')
        if User.objects.filter(email=email_).exists():
            get_user = User.objects.get(email=email_)
            if password_ == get_user.password:
                if get_user.is_active:
                    request.session['user_id'] = str(get_user.id)
                    return redirect("index")
                else:
                    messages.warning(request, "Your account is not activated yet. Please contact the administrator for account activation. Email : admin@foodkit.com")
                    return redirect("signin")
            else:
                messages.warning(request, "Email or password does not match.")
                return redirect("signin")

        else:
            messages.warning(request, "Email or password does not match.")
            return redirect("signin")
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
        
        if User.objects.filter(mobile=mobile_).exists():
            messages.info(request, "This mobile already exists.")
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
        
        otp_ = generate_otp(length=4)
        
        new_user = User.objects.create(
            first_name = first_name_,
            last_name = last_name_,
            email = email_,
            mobile = mobile_,
            password = password_,
            otp=otp_
        )
        new_user.save()

        print(otp_)
        subject_ = "Verify Your Email Address | FOODKIT"
        message_ = f"""
        Hello, {first_name_} {last_name_}

        Thank you for creating an account with us.

        To complete your registration, please verify your email address by using the verification code below:

        Verification Code: {otp_}

        Please do not share this code with anyone.

        If you did not create this account, you can safely ignore this email.

        Best regards,
        FOODKIT Team
        info@foodkit.com
        """
        from_email_ = "brijesh.gondaliya07@gmail.com"
        recipient_list_ = [f"{email_}"]
        send_mail(subject=subject_, message=message_, from_email=from_email_, recipient_list=recipient_list_)

        messages.success(request, f"Please check your email [{email_}] to verify your account. Your registration has been completed successfully.")
        return render(request, 'store/otp_verification.html', {"email": email_})
    return render(request, "store/signup.html")

def otp_verify(request):
    if request.method == "POST":
        email_ = request.POST['email'] 
        otp_ = request.POST['otp'] 
        print(email_, otp_)
        if User.objects.filter(email=email_).exists():
            get_user = User.objects.get(email=email_)
            if otp_ == get_user.otp:
                get_user.is_active = True
                get_user.save()
                messages.success(request, "Your email has been verified successfully. Your account is now active.")
                return redirect("signin")
            else:
                messages.warning(request, "Invalid OTP.")
                return render(request, 'store/otp_verification.html')
        else:
            messages.warning(request, "Email dose not exist.")
            return render(request, 'store/otp_verification.html')

    return render(request, 'store/otp_verification.html')

def logout(request):
    del request.session["user_id"]
    messages.success(request, "Now, You are logged out.")
    return redirect("signin")

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

@login_required
def profile(request):
    return render(request, "store/profile.html")