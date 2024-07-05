from django.shortcuts import render, redirect
from userauths.forms import UserRegisterForm
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from userauths.models import User
from django.core.mail import EmailMessage
from django.template.loader import render_to_string
from django.conf import settings


# Create your views here.

def registerview(request):
        if request.user.is_authenticated:
                messages.warning(request, f"Access Denied..")
              
                return redirect('core:index')
        
        if request.method == "POST":
            form = UserRegisterForm(request.POST or None)
            if form.is_valid():
                  #form.save()
                  new_user=form.save()
                  #on comment if want to use email
                  #html_template = 'email/register_email.html'
                  #html_message = render_to_string('email/register_email.html', {'form': form, 'request': request})
                  #html_message = render_to_string(html_template)
                  #subject = 'welcome to Aza'
                  #email_form = settings.EMAIL_HOST_USER
                  #recipient_list = [new_user.email]
                  #message = EmailMessage(subject, html_message,
                                  #email_form, recipient_list)
                  #message.content_subtype = 'html'
                  #message.send()
                  username = form.cleaned_data.get("username")
                  messages.success(request, f"Hey {username}, your account was created successfully")
                  new_user = authenticate(username=form.cleaned_data['email'], password=form.cleaned_data['password1'])
                  login(request, new_user)
                  return redirect('account:dashboard')
        else:
              form= UserRegisterForm()

        context ={
                "form":form,
        }
        return render(request, "userauths/register.html", context) 


def LoginView(request):
      if request.method == "POST":
            email = request.POST.get("email")
            password = request.POST.get("password")

            try:
                  user = User.objects.get(email=email)
                  user = authenticate(request, email=email, password=password)

                  if user is not None:
                        login(request, user)
                        messages.success(request, "You are logged in")
                        return redirect("account:dashboard")
                  else:
                        messages.warning(request,"username or password does not exsist")
                        return redirect("userauths:login")
            except:
                messages.warning(request, f"User with {email} does not exist")
      if request.user.is_authenticated:
            messages.warning(request, "You are already logged In")
            return redirect("account:account")
      return render(request, "userauths/login.html")

def logoutView(request):
      logout(request)
      messages.success(request, "You have been logged out")
      return redirect("userauths:login")