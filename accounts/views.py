from django.views.generic import TemplateView
from django.contrib.auth import get_user_model
from django.http import HttpResponse



# HTMX STUFFS
def check_email(request):
    email = request.POST.get("email")
    if get_user_model().objects.filter(email=email).exists():
        return HttpResponse('<div class="text-red-500">This email already exists</div>')
    else:
        return HttpResponse('<div class="text-green-500">This email is available</div>')

