from django.urls import path
from .views import HomePageView
from . import views

app_name = "pages"

urlpatterns = [
    path("", HomePageView.as_view(), name="home"),
]


htmx_urlpatterns = []

urlpatterns += htmx_urlpatterns
