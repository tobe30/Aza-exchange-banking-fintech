from django.shortcuts import render

# Create your views here.

#email

def handling_404(request, exception):
    return render(request, 'core/404.html', {})

def new_useremail(request):
    return render(request, "email/register_email.html")

def trans_email(request):
    return render(request, "email/trans_email.html")

def index(request):
    return render(request, 'core/index.html')

def comingsoon(request):
    return render(request, 'core/coming-soon.html')

def aboutus(request):
    return render(request, 'core/about-us.html')