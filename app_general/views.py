from datetime import datetime, timedelta

from django.http import HttpRequest
from django.http.response import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse

def home(request: HttpRequest):
    return render(request, "app_general/home.html")


def about(request: HttpRequest):
    return render(request, "app_general/about.html")


def change_theme(request: HttpRequest):
    referer = request.headers.get("referer")
    if referer is not None:
        response = HttpResponseRedirect(referer)
    else:
        response = HttpResponseRedirect(reverse("home"))

    # Theme
    theme = request.GET.get("theme")
    if theme == "dark":
        expired_date = datetime.now() + timedelta(days=365)
        response.set_cookie("theme", "dark", expires=expired_date, samesite="Lax")
    else:
        response.delete_cookie("theme")

    return response


def server_error(request):
    return render(request, 'app_general/500.html')

def page_not_found(request, exception):
    return render(request, 'app_general/404.html')

def permission_denied(request, exception):
    return render(request, 'app_general/403.html')
