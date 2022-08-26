from rest_framework.exceptions import APIException
from django_countries.fields import CountryField
from django.db import models
from django.conf import settings
from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver
from djmoney.models.fields import MoneyField


class ProductRatingManager(models.Manager):
    def get_queryset(self):
        return super(ProductRatingManager, self).get_queryset().annotate(
            avg_score=models.Avg('product_rating__score'),
            all_scores=models.Count('product_rating__score')
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
    CURRENCY_CHOICES = (
        ('EUR', 'EUR'),
        ('USD', 'USD'),
        ('GBP', 'GBP'),
        ('PLN', 'PLN')
    )
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    category = models.IntegerField(choices=CATEGORIES, blank=False)
    price = MoneyField(max_digits=10, decimal_places=2, blank=False,
                        default=0, currency_choices=CURRENCY_CHOICES, 
                        default_currency=CURRENCY_CHOICES[0][0])
    title = models.CharField(max_length=50, blank=False)
    description = models.TextField(max_length=500)
    brand = models.CharField(max_length=50)
    inStock = models.BooleanField(blank=False, default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    # get access to avg_score and all_scores fields
    objects = ProductRatingManager()

    def __str__(self):
        """
        String representation of Product object.
        """
        return self.title


class ProductImage(models.Model):
    """
    Model for Product image object in the database.
    """
    product = models.ForeignKey(
        Product, default=None, on_delete=models.CASCADE, related_name="product_images"
    )
    image = models.ImageField(
        upload_to='images/', default='../default-image_aqtoyb'
    )

    def __str__(self):
        """
        String representation of Product's image object.
        """
        return self.image.url

class Location(models.Model):
    """
    A model which holds information about a particular location
    """
    address = models.CharField(max_length=100)
    city = models.CharField(max_length=50)
    country = CountryField(blank_label='(select country)')
    product = models.ForeignKey(
        Product, default=None, on_delete=models.CASCADE, related_name="product_location"
    )

    def __str__(self):
        """
        String representation of Product's image object.
        """
        return f"{self.product}'s location"


# DJANGO-SIGNALS FUNCTIONS
@receiver(pre_save, sender=Product)
def reject_products(sender, instance, **kwargs):
    """
    Method raises Exception when saved picture exceeds the fifth allowed for the product.
    """
    if len(Product.objects.filter(owner=instance.owner)) >= 10:
        raise APIException("Only 10 products allowed per user")


@receiver(post_save, sender=Product)
def create_image(sender, instance, created, **kwargs):
    """
    Method creates ProductImage instance with default image 
    when post_save signal is received on Product instance creation.
    """
    if created and not ProductImage.objects.filter(product=instance):
        ProductImage.objects.create(product=instance)

@receiver(pre_save, sender=ProductImage)
def reject_pictures(sender, instance, **kwargs):
    """
    Method raises Exception when saved picture exceeds the fifth allowed for the product.
    """
    if len(ProductImage.objects.filter(product=instance.product.id)) >= 5:
        raise APIException("Only 5 pictures allowed for a product")

@receiver(pre_save, sender=ProductImage)
def delete_default(sender, instance, **kwargs):
    """
    Method deletes the default image only 
    when pre_save signal is received on ProductImage instance creation
    and default image exists as an instance's product key.
    """
    default_image = "../default-image_aqtoyb"
    ProductImage.objects.filter(
        product=instance.product.id,
        image=default_image
    ).delete() if ProductImage.objects.filter(
        product=instance.product.id,
        image=default_image
    ) else None
