from cProfile import Profile
from pyexpat.errors import messages
from django.contrib.auth.decorators import login_required
from django.core.mail import EmailMessage
from django.http import HttpRequest, HttpResponse, HttpResponseBadRequest, HttpResponseRedirect
from django.shortcuts import render, redirect, get_object_or_404
from django.template.loader import render_to_string
from django.urls import reverse
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode

from app_users.forms import ExtendedProfileForm, RegisterForm, UserProfileForm, EditProfileForm
from app_users.models import CustomUser
from app_users.utils.activation_token_generator import activation_token_generator
from django.core.mail import send_mail


def register(request: HttpRequest):
    # POST
    if request.method == "POST":
        form = RegisterForm(request.POST)
        if form.is_valid():
            # Register and wait for activation
            user: CustomUser = form.save(commit=False)
            user.is_active = False
            user.save()

            # Build email body
            context = {
                "protocol": request.scheme,
                "host": request.get_host(),
                "uidb64": urlsafe_base64_encode(force_bytes(user.id)),
                "token": activation_token_generator.make_token(user),
            }

            print(context['host'])
            email_body = render_to_string(
                "app_users/activate_email.html", context=context
            )

            # Send email
            email = EmailMessage(
                to=[user.email],
                subject="Activate Booking account ",
                body=email_body,
            )
            email.send()

            # Change redirect to register thank you
            return HttpResponseRedirect(reverse("register_thankyou"))
    else:
        form = RegisterForm()

    # GET
    context = {"form": form}
    return render(request, "app_users/register.html", context)


def register_thankyou(request: HttpRequest):
    return render(request, "app_users/register_thankyou.html")


def activate(request: HttpRequest, uidb64: str, token: str):
    title = "Activate account เรียบร้อย"
    content = "คุณสามารถเข้าสู่ระบบได้เลย"
    id = urlsafe_base64_decode(uidb64).decode()
    try:
        user = CustomUser.objects.get(id=id)
        if not activation_token_generator.check_token(user, token):
            raise Exception("Check token false")
        user.is_active = True
        user.save()
    except:
        print("Activate ไม่ผ่าน")
        title = "Activate account ไม่ผ่าน"
        content = "เป็นไปได้ว่าลิ้งค์ไม่ถูกต้อง หรือหมดอายุไปแล้ว"

    context = {"title": title, "content": content}
    return render(request, "app_users/activate.html", context)


@login_required
def dashboard(request: HttpRequest):
    return render(request, "app_users/dashboard.html")


@login_required
def profile(request: HttpRequest):
    user = request.user

    # POST
    if request.method == "POST":
        form = UserProfileForm(request.POST, instance=user)
        is_new_profile = False
        try:
            # Will be updated profile
            extended_form = ExtendedProfileForm(request.POST, instance=user.profile)
        except:
            # Will be created profile
            is_new_profile = True
            extended_form = ExtendedProfileForm(request.POST)

        if form.is_valid() and extended_form.is_valid():
            form.save()
            if is_new_profile:
                # Create profile
                profile = extended_form.save(commit=False)
                profile.user = user
                profile.save()
            else:
                # Update profile
                extended_form.save()
            response = HttpResponseRedirect(reverse("profile"))
            response.set_cookie("is_saved", "1")
            return response
    else:
        form = UserProfileForm(instance=user)
        try:
            extended_form = ExtendedProfileForm(instance=user.profile)
        except:
            extended_form = ExtendedProfileForm()

    # GET
    is_saved = request.COOKIES.get("is_saved") == "1"
    flash_message = "บันทึกเรียบร้อย" if is_saved else None
    context = {
        "form": form,
        "extended_form": extended_form,
        "flash_message": flash_message,
    }
    response = render(request, "app_users/profile.html", context)
    if is_saved:
        response.delete_cookie("is_saved")
    return response

@login_required
def user_list(request):
    users = CustomUser.objects.all()
    return render(request, 'admin_dashboard/user_list.html', {'users': users})


@login_required
def edit_user(request):
    user = request.user 
    if request.method == 'POST':
        form = UserProfileForm(request.POST, instance=user)
        if form.is_valid():
            form.save()
            messages.success(request, 'Profile updated successfully!')
            return redirect('user/list')  
    else:
        form = UserProfileForm(instance=user)  

    return render(request, 'edit_user.html', {'form': form})

@login_required
def edit_profile(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        if email:
            user = get_object_or_404(CustomUser, email=email)
            form = EditProfileForm(request.POST, instance=user)
            if form.is_valid():
                form.save()
                return redirect('/users/list')  # Redirect to user list page after successful edit
        else:
            return HttpResponseBadRequest("Invalid request: email field is required")
    else:
        email = request.GET.get('email')
        user = get_object_or_404(CustomUser, email=email)
        form = EditProfileForm(instance=user)
    return render(request, 'admin_dashboard/edit_profile.html', {'form': form, 'email': email})


@login_required
def delete_user(request):
    if request.method == 'POST':
        email = request.POST.get('email')  # Retrieve the email from POST data
        if email:
            try:
                user = get_object_or_404(CustomUser, email=email)
                user.delete()
                return redirect('/users/list')
            except CustomUser.DoesNotExist:
                return HttpResponseBadRequest("User does not exist")
        else:
            return HttpResponseBadRequest("Invalid request: email field is required")
    else:
        return HttpResponseBadRequest("Invalid request: POST method required")