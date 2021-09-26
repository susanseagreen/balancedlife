from .models import User
from django.shortcuts import render, redirect
from .forms import UserForm
from django.core.mail import send_mail
from django.contrib.auth.base_user import BaseUserManager
from django.contrib import messages
from django.template.loader import render_to_string
from django.utils.html import strip_tags


def register(request):
    if request.method == 'POST':
        user_form = UserForm(request.POST)
        if user_form.is_valid():
            instance_user = user_form.save(commit=False)
            user_code = BaseUserManager().make_random_password()
            instance_user.user_code = user_code
            instance_user.save()
            email_user(request, instance_user)

            subject = "New Member on your Recipes Shopping List heroku site!"
            message = f"Someone new has signed up with email {instance_user.email}"
            email_me(request, instance_user, subject, message)

            return render(request, 'registration/registered.html', {"email": instance_user.email})
        messages.success(request, user_form.errors.as_text())
    user_form = UserForm()
    return render(request, 'registration/register.html', {'form': user_form})


def email_user(request, instance):
    email = instance.email
    subject = "Recipes Shopping List"
    context = {
        "instance": instance,
        "path": request.build_absolute_uri('/')[:-1],
        "id": instance.id,
        "user_code": instance.user_code
    }
    html_message = render_to_string('emails/email_user.html', context=context)
    plain_message = strip_tags(html_message)
    send_mail(subject, plain_message, email, [email], html_message=html_message)


def email_me(request, instance_user, subject, message):
    my_email = 'sbelling8@gmail.com'
    context = {
        "path": request.build_absolute_uri('/')[:-1],
        "instance_user": instance_user
    }
    html_message = render_to_string('emails/email_me.html', context=context)
    plain_message = strip_tags(html_message)
    send_mail(subject, plain_message, my_email, [my_email], html_message=html_message)


def user_activate(request, user_id, user_code):
    user = User.objects.filter(id=user_id, user_code=user_code).first()
    email = 'holiday.planner.help@gmail.com'
    if user:
        user.is_active = True
        user.save()
        subject = "Your Account has been activated"
        message = f"Your 'Recipes Shopping List' Account has been activated"
        send_mail(subject, message, email, [user.email])
        messages.success(request, f'{user.username} has been successfully activated')
    else:
        messages.success(request, f"Something went wrong. Please contact {email} for assistance")

    return redirect('shopping_lists:create')


def superuser_activate(request, user_id, user_code):
    user = User.objects.filter(id=user_id, user_code=user_code).first()
    if user:
        user.is_superuser = True
        user.is_staff = True
        user.save()
        subject = "SUPERUSER: Member on your Recipes Shopping List heroku site!"
        message = f"{user.email} has activated their account"
        email_me(user.email, subject, message)
        messages.success(request, 'You have been successfully activated')
    else:
        email = 'holiday.planner.help@gmail.com'
        messages.success(request, f"Something went wrong. Please contact {email} for assistance")

    return redirect('home')


def resend_activation_email(request):
    if request.POST:
        user_email = request.POST.get('email')
        user = User.objects.filter(email=user_email).first()
        if user:
            email_user(request, user)
            messages.success(request, 'An email has been sent to your email address')
            messages.success(request, 'Please activate your account via the link in the email')
            return redirect('home')
        else:
            messages.success(request, f"Email not found")
            messages.success(request, f"You do not have an account registered under this email")
            return redirect('register')

    else:
        return render(request, 'registration/resend_email.html', {})
