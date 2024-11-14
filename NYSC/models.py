from django.db import models
from django.urls import reverse
import uuid
from django.core.validators import MinValueValidator
from .constants import TYPE_CHOICES, PRODUCT_NAME


class Category(models.Model):
    name = models.CharField(max_length=200)
    slug = models.SlugField(max_length=200, unique=True)

    class Meta:
        ordering = ["name"]
        indexes = [
            models.Index(fields=["name"]),
        ]
        verbose_name = "category"
        verbose_name_plural = "categories"

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse("nysc:product_list_by_category", args=[self.slug])


class Product(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    category = models.ForeignKey(
        Category, related_name="products", on_delete=models.CASCADE
    )
    name = models.CharField(max_length=200, choices=PRODUCT_NAME)
    slug = models.SlugField(max_length=200)
    image = models.URLField(max_length=600)
    description = models.TextField(blank=True)
    price = models.DecimalField(
        max_digits=10, decimal_places=2, validators=[MinValueValidator(0.01)]
    )
    size = models.CharField(max_length=11)
    available = models.BooleanField(default=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    type = models.CharField(max_length=20, choices=TYPE_CHOICES)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse("nysc:product_detail", args=[self.id, self.slug])
