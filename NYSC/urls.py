from django.urls import path
from . import views

app_name = "nysc"

urlpatterns = [
    path("product_list/", views.ProductListView.as_view(), name="product_list"),
    path(
        "<slug:category_slug>/",
        views.ProductListView.as_view(),
        name="product_list_by_category",
    ),
    path(
        "product/<uuid:id>/<slug:slug>/",
        views.ProductDetailView.as_view(),
        name="product_detail",
    ),
]
htmx_urlpatterns = [
    
]

urlpatterns += htmx_urlpatterns
