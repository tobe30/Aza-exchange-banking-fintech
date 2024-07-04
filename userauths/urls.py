from  django.urls import path

from userauths import views

app_name= "userauths"

urlpatterns=[
    path("sign-up/", views.registerview, name="register"),
    path("login/", views.LoginView, name="login"),
    path("sign-out/", views.logoutView, name="sign-out")


]