from django.db import models
from django.conf import settings
from django.db.models.signals import post_save
from djmoney.models.fields import MoneyField

class Product(models.Model):
    
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
        return self.title


class ProductImage(models.Model):
    product = models.ForeignKey(
        Product, default=None, on_delete=models.CASCADE, related_name="product_images"
    )
    image = models.ImageField(
        upload_to='images/', default='../default-image_aqtoyb'
    )

    def __str__(self):
        return self.image.url

def create_image(sender, instance, created, **kwargs):
    print(ProductImage.objects.filter(product=instance))
    if created and not ProductImage.objects.filter(product=instance):
        ProductImage.objects.create(product=instance)

post_save.connect(create_image, sender=Product)