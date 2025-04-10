from django.db import models
from django.core.validators import MinValueValidator


class Category(models.Model):
    name = models.CharField(
        max_length=50,
        help_text="Category name"
    )

    def __str__(self):
        return self.name


class Product(models.Model):
    name = models.CharField(
        max_length=50,
        help_text="Product name"
    )
    price = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        validators=[MinValueValidator(0.00)],
        help_text="Price of the product"
    )
    description = models.TextField(
        help_text="Product description"
    )
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    link = models.URLField(blank=True, null=True)
    image = models.ImageField(upload_to="products/", blank=True, null=True)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.name} - ${self.price}"
