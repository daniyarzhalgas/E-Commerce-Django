from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator


class Category(models.Model):
    class CategoryType(models.TextChoices):
        ELECTRONICS = "electronics", "Electronics"
        CLOTHING = "clothing", "Clothing"
        TOYS = "toys", "Toys"

    name = models.CharField(max_length=50, choices=CategoryType.choices)

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
    image = models.ImageField(upload_to="products/", blank=True, null=True)
    is_active = models.BooleanField(default=True)
    discount_percent = models.DecimalField(
        max_digits=5,
        decimal_places=2,
        blank=True,
        null=True,
        validators=[MinValueValidator(0), MaxValueValidator(100)],
        help_text="Enter discount as percentage, e.g., 10 for 10%"
    )

    @property
    def discounted_price(self):
        if self.discount_percent:
            return self.price * (1 - self.discount_percent / 100)
        return self.price

    def __str__(self):
        return f"{self.name} - ${self.price}"
