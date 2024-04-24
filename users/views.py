from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.conf import settings
from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404
from django.core.mail import send_mail
import string
import random
from django.template.loader import render_to_string
from django.core.mail import EmailMessage
from django.contrib.sites.shortcuts import get_current_site
from django.utils.encoding import force_bytes, force_str
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from .tokens import account_activation_token
from django.http import Http404
from django.contrib.auth.decorators import login_required
from .forms import ProfileForm
from courses.models import Enrolement


def send_account_verification_email(request, user):
    current_site = get_current_site(request)
    mail_subject = 'Tutornet Account activation link'
    message = render_to_string('users/activation_email.html', {
        'user': user,
        'domain': current_site.domain,
        'uid': urlsafe_base64_encode(force_bytes(user.pk)),
        'token': account_activation_token.make_token(user),
    })
    to_email = user.email
    email = EmailMessage(
        mail_subject, message, to=[to_email]
    )
    email.send()


def send_password_reset_email(request, user):
    current_site = get_current_site(request)
    mail_subject = 'Tutornet Password Reset link'
    message = render_to_string('users/password_reset_email.html', {
        'user': user,
        'domain': current_site.domain,
        'uid': urlsafe_base64_encode(force_bytes(user.pk)),
        'token': account_activation_token.make_token(user),
    })
    to_email = user.email
    email = EmailMessage(
        mail_subject, message, to=[to_email]
    )
    email.send()


def login_user(request):
    get_data = request.GET
    
    next = get_data.get('next', None)

    if next == None:
        next = request.session.get('next_page', None)

    if next is not None:
        request.session['next_page'] = next
   
    if request.user.is_authenticated:
        return redirect(next if next is not None else 'home_page')

    if request.method == "GET":
        return render(request, 'users/login.html')

    
  

    data = request.POST
    email = data['email']
    password = data['password']

    user = authenticate(email=email, password=password)

    if user is not None:
        if user.is_active:
            login(request, user)
            return redirect(next) if next != None else redirect('home_page')
        else:
            return redirect('not_verified_page')

    else:
        messages.add_message(request, messages.ERROR,
                             'Invalid username or password.')
        return render(request, 'users/login.html')


def register(request):
    next = request.GET.get('next', None)

    if next == None:
        next = request.session.get('next_page', None)
    if next is not None:
        request.session['next_page'] = next

    if request.user.is_authenticated:
        return redirect(next if next is not None else "home_page")



    if request.method == "GET":
        return render(request, 'users/register.html')

    if request.method == "POST":
        if request.user.is_authenticated:
            return redirect('home_page')
        

        data = request.POST

        first_name = data.get('first_name', None)
        last_name = data.get('last_name', None)
        email = data.get('email', None)
        phone_number = data.get('phone', None)
        gender = data.get('gender', None)
        account_type = data.get('account_type', None)
        password = data.get('password', None)

        # check if all the fields are provided
        if first_name == "" or last_name == "" or email == "" or password == "" or phone_number == "":
            messages.add_message(request, messages.ERROR,
                                 'All the fields must be provided')
            return render(request, 'users/register.html')

        User = get_user_model()
        try:
            # try finding user with the given email
            usr = User.objects.get(email=email)
            messages.add_message(
                request, messages.ERROR, 'An account with the provided email address is already registered')
            return render(request, 'users/register.html')
        except User.DoesNotExist:
            pass

        user = User(
            first_name=first_name,
            last_name=last_name,
            email=email,
            mobile_number=phone_number,
            gender=gender,
            is_active=True,
            tutor=False,
        )
        user.set_password(password)
        #  save user
        user.save()

        # send verification email
        send_account_verification_email(request, user)

        if user is not None:
            login(request, user)
            messages.add_message(
                request,
                messages.SUCCESS,
                'User created successfully, activate your account with the link sent to your email'
            )
            return redirect('not_verified_page')
        else:
            messages.add_message(
                request,
                messages.ERROR,
                'User Registration Failed, please check your inputs and try again'
            )
            return render(request, 'users/register.html')


def not_verified(request):
    return render(request, 'users/not_activated.html')


def verify_account(request, id, token):
    User = get_user_model()
    try:
        uid = force_str(urlsafe_base64_decode(id))
        user = User.objects.get(pk=uid)
    except (TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None
    if user is not None and account_activation_token.check_token(user, token):
        user.is_active = True
        user.save()
        messages.add_message(request, messages.SUCCESS,
                             'Your account is now activated')
        return redirect('profile_page')
    else:
        return render(request, 'base/404.html')


def forget_password(request):

    if request.method == "POST":
        email = request.POST.get('email', None)
        if email is not None:
            User = get_user_model()
            try:
                usr = User.objects.get(email=email)
                send_password_reset_email(request, usr)
                return render(request, 'users/email_reset_code_sent.html')

            except User.DoesNotExist:
                messages.add_message(
                    request, messages.ERROR, "No user with given email is found")

    return render(request, 'users/forget_password.html')


def new_password(request, id, token):
    # get user by verifying given id and token
    User = get_user_model()
    try:
        uid = force_str(urlsafe_base64_decode(id))
        user = User.objects.get(pk=uid)
    except (TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None
    if user is not None and account_activation_token.check_token(user, token):
        # if user is found,
        if request.method == "GET":
            # if the request is get, meaning from the email, render set new password form
            return render(request, 'users/set_new_password.html', context={"id": id, "token": token})

        # if request is post, meaning from set password form,
        if request.method == "POST":
            password = request.POST.get("password", None)
            # check if password is provided
            if password is not None:
                try:
                    # try settinf a new password for the user and then redirect to profile page
                    user.set_password(password)
                    user.save()
                    messages.add_message(request, messages.SUCCESS,
                                         'Your account is now activated')
                    return redirect('login_page')
                except:
                    # if setting password failed, set an error message and redirect to set password page
                    messages.add_message(request, messages.ERROR,
                                         'Invalid password, please try again')
                    return render(request, 'users/set_new_password.html', context={"id": id, "token": token})
            else:
                # if not password is provided from the form, set error and redirect back to set password page
                messages.add_message(request, messages.ERROR,
                                     'Invalid password, please try again')
                return render(request, 'users/set_new_password.html', context={"id": id, "token": token})
    else:
        # if the id and/or token provided are wrong, redirect to invali_code page.
        return render(request, 'users/invalid_code.html')


@login_required(login_url='login_page')
def profile(request):

    enrolements = request.user.enrolements.filter(status=1)

    context = {
        "enrolements": enrolements
    }

    return render(request, 'users/profile.html', context=context)


@login_required(login_url='login_page')
def edit_profile(request):
    if request.method == "POST":
        user = request.user
        form = ProfileForm(instance=user, data=request.POST,
                           files=request.FILES)
        if form.is_valid():
            form.save()
            return redirect('profile_page')
        else:
            for error in form.errors:
                messages.add_message(request, messages.ERROR, str(error))
            return render(request, 'users/edit_profile.html')

    return render(request, 'users/edit_profile.html')


def logout_user(request):
    if request.user is not None:
        logout(request)
    return redirect('home_page')
