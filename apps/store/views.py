from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.core.paginator import Paginator
from django.conf import settings
from django.core.mail import send_mail
from apps.master.helpers import is_valid_email, is_valid_mobile, is_valid_password, generate_otp
from apps.users.models import User, Inqueries
from apps.store.models import BlogCategory, Blogs, Product, Cart, Address, Order, OrderItem
from functools import wraps
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from decimal import Decimal
import json
from apps.store.forms import AddressForm

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
    if request.method == "POST":
        email_ = request.POST['email']

        if not is_valid_email(email_):
            print("-----1")
            messages.warning(request, "Your email address is invalid.")
            return redirect("forgot_password")

        # Email already exists check (FIXED)
        if not User.objects.filter(email=email_).exists():
            print("-----2")
            messages.info(request, "No account exists with this email.")
            return redirect("forgot_password")
        

        get_user = User.objects.get(email=email_)
        print("-----3", get_user)
        otp_ = generate_otp(length=4)
        print("-----4", otp_)
        subject = "Password Reset OTP"
        message = f"""
            Hello,

            We received a request to reset your password.

            Your One-Time Password (OTP) is: {otp_}

            This OTP is valid for 5 minutes.
            Please do not share this OTP with anyone.

            If you did not request this, please ignore this email.

            Thank you,
            Your App Team
        """
        send_mail(
            subject,
            message,
            settings.EMAIL_HOST_USER,
            [email_],
            fail_silently=False,
        )
        print("-----5", "email sent")
        get_user.otp = otp_
        get_user.save()
        print("-----6", "otp saved")
        messages.success(request, "OTP has been sent to your email.")
        return render(request, "store/forgot_password_otp_verify.html", {"email":email_})
    print("-----0", "page open")
    return render(request, "store/forgot_password.html")

def forgot_password_otp_verify(request):
    if request.method == "POST":
        email_ = request.POST['email']
        otp_ = request.POST['otp']
        new_password_ = request.POST['new_password']
        confirm_password_ = request.POST['confirm_password']

        get_user = User.objects.get(email=email_)

        if get_user.otp != otp_:
            messages.warning(request, "Invalid OTP!!!")
            return render(request, "store/forgot_password_otp_verify.html", {"email":email_})
        

        if new_password_ != confirm_password_:
            messages.warning(request, "New password and confirm password does not match.")
            return render(request, "store/forgot_password_otp_verify.html", {"email":email_})
        
        is_valid_password_, message = is_valid_password(new_password_)
        if not is_valid_password_:
            messages.warning(request, message)
            return render(request, "store/forgot_password_otp_verify.html", {"email":email_})
        
        get_user.password = new_password_
        get_user.save()
        messages.success(request, "Password has been successfull updated.")
        return redirect("signin")
    return render(request, "store/forgot_password_otp_verify.html")

def index(request):
    blogs = Blogs.objects.all().order_by("-created_at")[:3]
    products = Product.objects.all().order_by("-created_at")[:8]
    context = {
        'blogs': blogs,
        'products':products,
    }
    return render(request, "store/index.html", context)

def products(request):
    product_list = Product.objects.filter(is_active=True)
    paginator = Paginator(product_list, 12)

    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)

    return render(request, "store/products.html", {
        "products": page_obj
    })

def product_detail(request, product_id):
    product = Product.objects.get(id=product_id)
    return render(request, "store/product_detail.html", {"product":product})

def blogs(request):
    blog_list = Blogs.objects.all().order_by("-created_at")

    paginator = Paginator(blog_list, 6)  # 5 blogs per page
    page_number = request.GET.get('page')
    blogs = paginator.get_page(page_number)

    context = {
        'blogs': blogs
    }
    return render(request, "store/blogs.html", context)

def blog_detail(request, id):
    blog = get_object_or_404(Blogs, id=id)
    print(blog)
    return render(request, "store/blog_detail.html", {"blog": blog})

def about(request):
    return render(request, "store/about.html")

def contact(request):
    if request.method == "POST":
        fullname_ = request.POST['fullname']
        email_ = request.POST['email']
        message_ = request.POST['message']

        if not is_valid_email(email_):
            messages.warning(request, "Your email address is invalid.")
            return render(request, "store/contact.html")

        new_inquiry = Inqueries.objects.create(
            fullname= fullname_,
            email = email_,
            message = message_
        )
        new_inquiry.save()
        messages.success(request, "Your query submitted succefully.")
        return redirect("contact")
    return render(request, "store/contact.html")

@login_required
def add_to_cart(request, product_id):
    product = get_object_or_404(Product, id=product_id)

    user_id = request.session.get('user_id')

    if not user_id:
        return redirect("login")

    user = get_object_or_404(User, id=user_id)  # ✅ FIX

    cart_item, created = Cart.objects.get_or_create(
        user=user,
        product=product
    )
    if not created:
        cart_item.qty += 1
    else:
        cart_item.qty = 1

    cart_item.save()

    messages.success(request, f"{product.name} added to cart")
    return redirect("products")  # cart page URL name

@login_required
def cart(request):
    user_id = request.session.get('user_id')

    if not user_id:
        return redirect("login")

    user_ = get_object_or_404(User, id=user_id)
    cart_items = Cart.objects.filter(user=user_)
    total_amount = sum(item.total_price for item in cart_items)

    # Get all addresses of the user
    addresses = Address.objects.filter(user=user_).order_by('-is_primary')

    return render(request, "store/cart.html", {
        "cart_items": cart_items,
        "total_amount": total_amount,
        "addresses": addresses
    })


@login_required
def cart_increase(request, id):
    user_id = request.session.get('user_id')

    if not user_id:
        return redirect("login")

    user_ = get_object_or_404(User, id=user_id)
    cart_item = get_object_or_404(Cart, id=id, user=user_)
    cart_item.qty += 1
    cart_item.save()
    return redirect("cart")

@login_required
def cart_decrease(request, id):
    user_id = request.session.get('user_id')

    if not user_id:
        return redirect("login")

    user_ = get_object_or_404(User, id=user_id)
    cart_item = get_object_or_404(Cart, id=id, user=user_)

    if cart_item.qty > 1:
        cart_item.qty -= 1
        cart_item.save()
    else:
        cart_item.delete()  # auto remove if qty becomes 0

    return redirect("cart")

@login_required
def cart_remove(request, id):
    user_id = request.session.get('user_id')

    if not user_id:
        return redirect("login")

    user_ = get_object_or_404(User, id=user_id)
    cart_item = get_object_or_404(
        Cart,
        id=id,
        user=user_
    )
    cart_item.delete()
    return redirect("cart")

@login_required
def profile(request):
    user_id = request.session["user_id"]
    get_user = User.objects.get(id=user_id)
    addresses = Address.objects.filter(user=user_id).order_by("-is_primary", "-id")
    context = {
        'user':get_user,
        "addresses": addresses
    }
    return render(request, "store/profile.html", context)

@login_required
def update_image(request):
    user_id = request.session["user_id"]
    get_user = User.objects.get(id=user_id)
    if request.method == "POST":
        get_user.profile = request.FILES.get("profile")
        get_user.save()
        messages.success(request, "Profile picture updated successfully")
        return redirect("profile")
    context = {
        'user':get_user,
    }
    return render(request, "store/update_image.html", context)

@login_required
def add_address(request):
    user_id = request.session.get('user_id')

    if not user_id:
        return redirect("login")

    user_ = get_object_or_404(User, id=user_id)
    if request.method == "POST":
        form = AddressForm(request.POST)
        if form.is_valid():
            address = form.save(commit=False)
            address.user = user_
            address.save()
            return redirect("profile")
    else:
        form = AddressForm()

    return render(request, "store/address_form.html", {
        "form": form,
        "title": "Add Address"
    })


@login_required
def edit_address(request, id):
    user_id = request.session.get('user_id')

    if not user_id:
        return redirect("login")

    user_ = get_object_or_404(User, id=user_id)
    address = get_object_or_404(Address, id=id, user=user_)

    if request.method == "POST":
        form = AddressForm(request.POST, instance=address)
        if form.is_valid():
            form.save()
            return redirect("profile")
    else:
        form = AddressForm(instance=address)

    return render(request, "store/address_form.html", {
        "form": form,
        "title": "Edit Address"
    })


@login_required
def delete_address(request, id):
    user_id = request.session.get('user_id')

    if not user_id:
        return redirect("login")

    user_ = get_object_or_404(User, id=user_id)
    address = get_object_or_404(Address, id=id, user=user_)
    address.delete()
    return redirect("profile")

@csrf_exempt
@login_required
def place_order(request):
    user_id = request.session.get('user_id')

    if not user_id:
        return redirect("login")

    user_ = get_object_or_404(User, id=user_id)

    if request.method == "POST":
        data = json.loads(request.body)

        item_ids = data.get("item_ids", [])
        frontend_subtotal = Decimal(str(data.get("subtotal", 0)))
        frontend_shipping = Decimal(str(data.get("shipping", 0)))
        frontend_total = Decimal(str(data.get("total_amount", 0)))
        selected_address_id = data.get("address_id")  # NEW: address sent from frontend

        if not item_ids:
            return JsonResponse({"error": "No items selected"}, status=400)

        cart_items = Cart.objects.filter(
            id__in=item_ids,
            user=user_
        ).select_related("product")

        if not cart_items.exists():
            return JsonResponse({"error": "Invalid cart items"}, status=400)

        # 🔐 Recalculate totals on server
        subtotal = Decimal("0")
        for item in cart_items:
            subtotal += Decimal(item.product.price) * item.qty

        shipping = Decimal("100") if subtotal < 1000 else Decimal("0")
        total_amount = subtotal + shipping

        # Optional: compare frontend vs backend totals
        if subtotal != frontend_subtotal or shipping != frontend_shipping or total_amount != frontend_total:
            return JsonResponse({"error": "Totals mismatch"}, status=400)

        # Get the address: either selected or primary
        if selected_address_id:
            address = get_object_or_404(Address, id=selected_address_id, user=user_)
        else:
            address = Address.objects.filter(user=user_, is_primary=True).first()
            if not address:
                return JsonResponse({"error": "No address available"}, status=400)

        # Create Order
        order = Order.objects.create(
            user=user_,
            subtotal=subtotal,
            shipping=shipping,
            total_amount=total_amount,
            address=address  # Add the address to order
        )

        # Create OrderItems
        for item in cart_items:
            OrderItem.objects.create(
                order=order,
                product=item.product,
                qty=item.qty,
                price=item.product.price,
                total_price=item.product.price * item.qty,
            )

        # Remove ordered items from cart
        cart_items.delete()

        return JsonResponse({
            "success": True,
            "order_id": order.id
        })

    return JsonResponse({"error": "Invalid request"}, status=405)

@login_required
def my_orders(request):
    user_id = request.session.get('user_id')

    if not user_id:
        return redirect("login")

    user_ = get_object_or_404(User, id=user_id)
    orders = Order.objects.filter(user=user_).order_by("-created_at")
    return render(request, "store/my_orders.html", {
        "orders": orders
    })

@login_required
def order_detail(request, order_id):
    user_id = request.session.get('user_id')

    if not user_id:
        return redirect("login")

    user_ = get_object_or_404(User, id=user_id)
    order = get_object_or_404(Order, id=order_id, user=user_)
    return render(request, "store/order_detail.html", {
        "order": order
    })

def send_order_success_email(user, order):
    subject = f"Order Confirmed – #{order.id}"

    message = f"""
    Hi {user.first_name} {user.last_name},

    Thank you for your order!

    Order ID: {order.id}
    Total Amount: ₹ {order.total_amount}

    Your order has been successfully placed and is being processed.

    Thank you for shopping with Foodkit
    """

    send_mail(
        subject,
        message,
        settings.EMAIL_HOST_USER,
        [user.email],
        fail_silently=False,
    )
    
@login_required
def order_success(request, order_id):
    user_id = request.session.get('user_id')

    if not user_id:
        return redirect("login")

    user_ = get_object_or_404(User, id=user_id)

    order = get_object_or_404(Order, id=order_id, user=user_)

    if not request.session.get(f"order_email_sent_{order.id}"):
        send_order_success_email(user_, order)
        request.session[f"order_email_sent_{order.id}"] = True

    return render(request, "store/order_success.html", {
        "order": order
    })

@login_required
def cancel_order(request, order_id):
    user_id = request.session.get('user_id')

    if not user_id:
        return redirect("login")

    user_ = get_object_or_404(User, id=user_id)
    order = get_object_or_404(Order, id=order_id, user=user_)

    if order.status == "CANCELLED":
        messages.warning(request, "This order is already cancelled.")
        return redirect("order_detail", order_id=order.id)

    if order.delivery_status in ["SHIPPED", "OUT_FOR_DELIVERY", "DELIVERED"]:
        messages.error(request, "This order cannot be cancelled as it is already shipped.")
        return redirect("order_detail", order_id=order.id)

    order.status = "CANCELLED"
    order.delivery_status = "CANCELLED"
    order.is_paid = False
    order.save()

    messages.success(request, "Your order has been cancelled successfully.")
    return redirect("order_detail", order_id=order.id)