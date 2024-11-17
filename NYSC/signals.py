from django.db.models.signals import pre_delete
from django.dispatch import receiver
from .models import Product
from django.conf import settings


@receiver(pre_delete, sender=Product)
def remove_from_carts(sender, instance, **kwargs):
    """Remove product from all active carts when it's deleted"""
    from django.contrib.sessions.models import Session
    from django.contrib.sessions.backends.db import SessionStore

    # Get all active sessions
    for session in Session.objects.all():
        try:
            session_data = SessionStore(session_key=session.session_key)
            cart = session_data.get(settings.CART_SESSION_ID)

            if cart:
                # Create product identifier as used in cart
                item_id = f"product_{str(instance.id)}"
                if item_id in cart:
                    del cart[item_id]
                    session_data[settings.CART_SESSION_ID] = cart
                    session_data.save()
        except:
            continue
