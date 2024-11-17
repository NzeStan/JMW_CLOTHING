from decimal import Decimal
from django.conf import settings
from django.apps import apps
import uuid
import logging
logger = logging.getLogger(__name__)


class Cart:

    def __init__(self, request):
        self.session = request.session
        cart = self.session.get(settings.CART_SESSION_ID)
        if not cart:
            cart = self.session[settings.CART_SESSION_ID] = {}
        self.cart = cart

    def __iter__(self):
        """
        Iterate over the items in the cart and get the products
        from the database.
        """
        product_ids_to_remove = []
        items_to_delete = []

        for item_id, item in self.cart.items():
            try:
                model_name = item.get("model")
                if not model_name:
                    items_to_delete.append(item_id)
                    continue

                Model = apps.get_model("NYSC", model_name)
                product_id = item.get("id")
                if not product_id:
                    items_to_delete.append(item_id)
                    continue

                try:
                    obj = Model.objects.get(id=uuid.UUID(product_id))
                    item_copy = item.copy()
                    item_copy["item"] = obj
                    item_copy["price"] = Decimal(item["price"])
                    item_copy["total_price"] = item_copy["price"] * item["quantity"]
                    yield item_copy
                except (ValueError, Model.DoesNotExist):
                    product_ids_to_remove.append(item_id)
                    continue

            except Exception as e:
                logger.error(f"Error processing cart item {item_id}: {str(e)}")
                items_to_delete.append(item_id)
                continue

        # Clean up both invalid items and corrupted items
        self._remove_invalid_items(product_ids_to_remove)
        if items_to_delete:
            for item_id in items_to_delete:
                del self.cart[item_id]
            self.save()

    def _remove_invalid_items(self, item_ids):
        """Remove invalid items from cart"""
        modified = False
        for item_id in item_ids:
            if item_id in self.cart:
                del self.cart[item_id]
                modified = True

        if modified:
            self.save()

    def cleanup(self):
        """
        Remove any cart items that reference non-existent products
        """
        product_ids_to_remove = []

        for item_id, item in self.cart.items():
            try:
                model_name = item["model"]
                Model = apps.get_model("NYSC", model_name)
                Model.objects.get(id=uuid.UUID(item["id"]))
            except (Model.DoesNotExist, apps.apps.LookupError):
                product_ids_to_remove.append(item_id)

        self._remove_invalid_items(product_ids_to_remove)

    def add(self, item, model_name, quantity=1, override_quantity=False):
        """
        Add an item to the cart or update its quantity.
        """
        try:
            item_id = f"{model_name.lower()}_{str(item.id)}"

            if item_id not in self.cart:
                self.cart[item_id] = {
                    "quantity": 0,
                    "price": str(item.price),
                    "model": model_name,
                    "id": str(item.id),
                }

            if override_quantity:
                self.cart[item_id]["quantity"] = quantity
            else:
                self.cart[item_id]["quantity"] += quantity

            self.save()
        except Exception as e:
            logger.error(f"Error adding item to cart: {str(e)}")

    def remove(self, item, model_name):
        """
        Remove an item from the cart.
        """
        try:
            item_id = f"{model_name.lower()}_{str(item.id)}"
            if item_id in self.cart:
                del self.cart[item_id]
                self.save()
        except Exception as e:
            logger.error(f"Error removing item from cart: {str(e)}")

    def get_total_price(self):
        try:
            return sum(
                Decimal(item["price"]) * item["quantity"]
                for item in self.cart.values()
                if "price" in item and "quantity" in item
            )
        except Exception as e:
            logger.error(f"Error calculating total price: {str(e)}")
            return Decimal("0")

    def clear(self):
        try:
            del self.session[settings.CART_SESSION_ID]
            self.save()
        except Exception as e:
            logger.error(f"Error clearing cart: {str(e)}")

    def __len__(self):
        """
        Count all items in the cart.
        """
        return sum(item["quantity"] for item in self.cart.values())

    def save(self):
        self.session.modified = True
