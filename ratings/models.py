from django.db import models
from django.conf import settings
from products.models import Product


class Rating(models.Model):
    """
    The Rating model with releation to User and Product model..
    """
    RATE_CHOICES = (
        (5, u'\u2605'*5),
        (4, u'\u2605'*4),
        (3, u'\u2605'*3),
        (2, u'\u2605'*2),
        (1, u'\u2605'),
    )
    owner = models.ForeignKey(settings.AUTH_USER_MODEL,
                              on_delete=models.CASCADE)
    product = models.ForeignKey(
        Product, on_delete=models.CASCADE, related_name="product_rating"
    )
    score = models.PositiveSmallIntegerField(default=0, choices=RATE_CHOICES)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']
        unique_together = ['owner', 'product']

    def __str__(self):
        """
        Returns string represenation of rating's owner an rated product.
        """
        return f"{self.owner} {self.product}"
