from rest_framework.exceptions import APIException
from django_countries.fields import CountryField
from django.db.models.functions import Coalesce
from django.db import models
from django.conf import settings
from django.db.models.signals import post_save, pre_save, post_delete
from django.dispatch import receiver
from djmoney.models.fields import MoneyField


class ProductRatingManager(models.Manager):
    """
    Custom model manager allowing for avg_score
    and all_scores to be avaialble globally.
    """

    def get_queryset(self):
        """
        Returns queryset annotated with avg_score and all_scores fields.
        """
        # query = Product.objects.values('price')
        # print(query)
        return super(ProductRatingManager, self).get_queryset().annotate(
            avg_score=Coalesce(models.Avg(
                ('product_rating__score')), models.Value(0.0)),
            all_scores=models.Count('product_rating__score'),
        )


class Product(models.Model):
    """
    Model for Product object in the database.
    """
    CATEGORIES = (
        (0, "Boards"),
        (1, "Kites"),
        (2, "Wetsuits"),
        (3, "Harnesses"),
        (4, "Others"),
    )
    owner = models.ForeignKey(settings.AUTH_USER_MODEL,
                              on_delete=models.CASCADE)
    category = models.IntegerField(choices=CATEGORIES, blank=False)
    price = MoneyField(max_digits=10, decimal_places=2, blank=False,
                       default_currency='EUR')
    title = models.CharField(max_length=30, blank=False)
    description = models.TextField(max_length=500)
    brand = models.CharField(max_length=15)
    in_stock = models.BooleanField(blank=False, default=False)
    street = models.CharField(max_length=50)
    city = models.CharField(max_length=20)
    country = CountryField(blank_label='(select country)')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    # get access to avg_score and all_scores fields
    objects = ProductRatingManager()

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        """
        String representation of Product object.
        """
        return self.title


class ProductImage(models.Model):
    """
    Model for Product image object in the database.
    """
    owner = models.ForeignKey(settings.AUTH_USER_MODEL,
                              on_delete=models.CASCADE)
    product = models.ForeignKey(
        Product, default=None,
        on_delete=models.CASCADE,
        related_name="product_images"
    )
    image = models.ImageField(
        upload_to='images/', default='../default_gkffon'
    )

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        """
        String representation of Product's image object.
        """
        return self.image.url




@receiver(pre_save, sender=ProductImage)
def reject_pictures(sender, instance, **kwargs):
    """
    Method raises Exception when saved picture
    exceeds the fifth allowed for the product.
    """
    if len(ProductImage.objects.filter(product=instance.product.id)) > 5:
        raise APIException("Only 5 pictures allowed for a product")

