from django.shortcuts import render, redirect
from .forms import *
from django.contrib.auth.models import User
from django.contrib.auth import login, authenticate, logout
from django.contrib import messages
from django.core.mail import send_mail,EmailMultiAlternatives # for emails
from django.template.loader import render_to_string
from django.utils.html import strip_tags


def home(reqeust):
    context = {}
    return render(reqeust, "SNweb/home.html",context)


def user_signup(request):
    if request.method == 'GET':
        form = SignUpForm()
        return render(request, 'registration/signup.html', {'form': form})

    if request.method == 'POST':
        form = SignUpForm(request.POST)

        if form.is_valid():
            email = form.cleaned_data['email']

            if User.objects.filter(email=email).exists():
                # Email already exists, show an error message
                form.add_error('email', 'This email is already used by another user ! Please add another one !')
                return render(request, 'registration/signup.html', {'form': form})

            # Email is unique, proceed with user registration
            user = form.save()

            my_subject = "👋🏻 Welcome to Simona's Nail Website !"
            my_recipient = form.cleaned_data['email']
            welcome_user =f"{user.username}"
            link_app = "http://127.0.0.1:8000/home"
            context = {
                "welcome_user": welcome_user,
                "link_app": link_app
            }
            html_message = render_to_string('registration/email_welcome_message.html',context=context)
            plain_message = strip_tags(html_message)
            email_message = EmailMultiAlternatives(
                subject = my_subject,
                body = plain_message,
                from_email = None,
                to = [my_recipient],
            )
            email_message.attach_alternative(html_message,"text/html")
            email_message.send()

            login(request, user)  # log-in the user after registration
            return redirect('home')
        else:
            print(form.errors)
            return render(request, 'registration/signup.html', {'form': form})


def user_login(request):
    if request.method == "GET":
        form = LogInForm()
        return render(request,template_name="registration/login.html",context={"form":form})
    elif request.method == "POST":
        form = LogInForm(request.POST)
        if form.is_valid():
            user_name = form.cleaned_data["user_name"]
            user_password = form.cleaned_data["user_password"]
            user = authenticate(request, username = user_name, password = user_password)
            if user:
                login(request,user)
                messages.success(request,"Ai fost autentificat !")
                return redirect('home')
        messages.error(request,"Autentificare nereusita !")
        return render(request,template_name="registration/login.html",context={"form":form})


def user_logout(request):
    logout(request)
    messages.success(request, "You have been logged out !")
    return redirect("login")



