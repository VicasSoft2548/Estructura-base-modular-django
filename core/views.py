# Create your views here.
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import LoginView
from django.shortcuts import render


class CustomLoginView(LoginView):
    template_name = "core/login.html"
    redirect_authenticated_user = True


@login_required
def dashboard(request):
    return render(request, "core/dashboard.html")