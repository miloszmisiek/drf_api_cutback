from django.db import models
from django.db.models import Q
from django.conf import settings
from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver
from djmoney.models.fields import MoneyField

class Product(models.Model):
    """
    Model for Product object in the database.
    """
    
    CATEGORIES = [
        (0, "Boards"),
        (1, "Kites"),
        (2, "Wetsuits"),
        (3, "Harnesses"),
        (4, "Others"),
    ]
    CURRENCY_CHOICES = (
        ('EUR', 'EUR'),
        ('USD', 'USD'),
        ('GBP', 'GBP'),
        ('PLN', 'PLN')
    )

    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    category = models.IntegerField(choices=CATEGORIES, blank=False)
    price = MoneyField(max_digits=10, decimal_places=2, null=True, 
                        currency_choices=CURRENCY_CHOICES, 
                        default_currency=None)
    title = models.CharField(max_length=50, blank=False)
    description = models.TextField(max_length=500)
    brand = models.CharField(max_length=50)
    inStock = models.BooleanField(blank=False, default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

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


# django-signals functions
@receiver(post_save, sender=Product)
def create_image(sender, instance, created, **kwargs):
    """
    Method creates ProductImage instance with default image 
    when post_save signal is received on Product instance creation.
    """
    if created and not ProductImage.objects.filter(product=instance):
        ProductImage.objects.create(product=instance)

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
