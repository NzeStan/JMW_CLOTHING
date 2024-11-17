from django.urls import path
from . import views

app_name = "cart"

urlpatterns = [
    path("", views.cart_detail, name="cart_detail"),
    path("add/<str:model_name>/<uuid:item_id>/", views.cart_add, name="cart_add"),
    path(
        "remove/<str:model_name>/<uuid:item_id>/", views.cart_remove, name="cart_remove"
    ),
]


htmx_urlpatterns = []

urlpatterns += htmx_urlpatterns
