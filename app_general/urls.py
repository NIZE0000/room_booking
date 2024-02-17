from django.urls import include, path

from app_general import views

urlpatterns = [
    path("", include("django.contrib.auth.urls")),
    path("", views.home, name="home"),
    path("about", views.about, name="about"),
    path("change-theme", views.change_theme, name="change_theme"),
]


handler500 = views.server_error
handler404 = views.page_not_found
handler403 = views.permission_denied
