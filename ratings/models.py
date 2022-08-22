from django.db import models
from django.conf import settings
# from django.core.validators import MaxValueValidator, MinValueValidator
from products.models import Product


class Rating(models.Model):
    RATE_CHOICES = (
        (5, "excellence"),
        (4, "very good"),
        (3, "good"),
        (2, "poor"),
        (1, "bad"),
    )
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    product = models.ForeignKey(
        Product, default=None, on_delete=models.CASCADE, related_name="product_rating"
    )
    score = models.PositiveSmallIntegerField(default=0, choices=RATE_CHOICES)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']
        unique_together = ['owner', 'product']

    def __str__(self):
        return f"{self.owner} {self.product}"