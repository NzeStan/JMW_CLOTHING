from django.shortcuts import render, redirect, get_object_or_404
from django.views.decorators.http import require_POST
from NYSC.models import Product
from .cart import Cart
from django.apps import apps
from .forms import CartAddProductForm
from django.conf import settings
import logging
logger = logging.getLogger(__name__)


@require_POST
def cart_add(request, model_name, item_id):
    cart = Cart(request)
    Model = apps.get_model("NYSC", model_name)
    item = get_object_or_404(Model, id=item_id)
    form = CartAddProductForm(request.POST)

    if form.is_valid():
        cd = form.cleaned_data
        cart.add(
            item=item,
            model_name=model_name,
            quantity=cd["quantity"],
            override_quantity=cd["override"],
        )
    return redirect("cart:cart_detail")


@require_POST
def cart_remove(request, model_name, item_id):
    cart = Cart(request)
    Model = apps.get_model("NYSC", model_name)
    item = get_object_or_404(Model, id=item_id)
    cart.remove(item, model_name)
    return redirect("cart:cart_detail")


def cart_detail(request):
    try:
        cart = Cart(request)
        # Clean up any invalid items before displaying
        cart.cleanup()

        items = []
        for item in cart:
            item["update_quantity_form"] = CartAddProductForm(
                initial={"quantity": item["quantity"], "override": True}
            )
            items.append(item)
        return render(request, "cart/cart_detail.html", {"cart": cart})
    except Exception as e:
        logger.error(f"Error in cart_detail view: {str(e)}")
        # Clear the problematic cart
        request.session[settings.CART_SESSION_ID] = {}
        return redirect("nysc:product_list")
