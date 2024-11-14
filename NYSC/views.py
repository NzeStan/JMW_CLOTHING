from django.views.generic import ListView
from django.views.generic import DetailView
from django.shortcuts import get_object_or_404
from .models import Category, Product
from cart.forms import CartAddProductForm


class ProductListView(ListView):
    model = Product
    template_name = "nysc/product/list.html"
    context_object_name = "products"

    def get_queryset(self):
        queryset = Product.objects.filter(available=True)
        self.category = None

        if self.kwargs.get("category_slug"):
            self.category = get_object_or_404(
                Category, slug=self.kwargs["category_slug"]
            )
            queryset = queryset.filter(category=self.category)

        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["categories"] = Category.objects.all()
        context["category"] = self.category
        return context


class ProductDetailView(DetailView):
    model = Product
    template_name = "nysc/product/detail.html"
    context_object_name = "product"

    def get_object(self):
        return get_object_or_404(
            Product, id=self.kwargs["id"], slug=self.kwargs["slug"], available=True
        )

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["cart_product_form"] = CartAddProductForm()
        return context
