from django.urls import path
from . import views


app_name = "accounts"

urlpatterns = []


htmx_urlpatterns = [
    path("check_email/", views.check_email, name="check-email"),
]

urlpatterns += htmx_urlpatterns
