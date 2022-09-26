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
    # CURRENCY_CHOICES = (
    #     ('EUR', u'\u20ac'),
    #     ('USD', u'\u0024'),
    #     ('GBP', u'\u00a3'),
    #     ('PLN', 'z' + u'\u0142'),
    # )
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


# DJANGO-SIGNALS FUNCTIONS
# @receiver(pre_save, sender=Product)
# def reject_products(sender, instance, **kwargs):
#     """
#     Method raises Exception when saved product
#     exceeds the tenth allowed for the user.
#     """
#     if len(Product.objects.filter(owner=instance.owner)) >= 10:
#         raise APIException("Only 10 products allowed per user")


# @receiver(post_save, sender=Product)
# def create_image(sender, instance, created, **kwargs):
#     """
#     Method creates ProductImage instance with default image
#     when post_save signal is received on Product instance creation.
#     """
#     if created and not ProductImage.objects.filter(product=instance):
#         ProductImage.objects.create(product=instance, owner=instance.owner)


@receiver(pre_save, sender=ProductImage)
def reject_pictures(sender, instance, **kwargs):
    """
    Method raises Exception when saved picture
    exceeds the fifth allowed for the product.
    """
    if len(ProductImage.objects.filter(product=instance.product.id)) > 5:
        raise APIException("Only 5 pictures allowed for a product")


# @receiver(pre_save, sender=ProductImage)
# def delete_default(sender, instance, **kwargs):
#     """
#     Method deletes the default image only
#     when pre_save signal is received on ProductImage instance creation
#     and default image exists as an instance's product key.
#     """
#     default_image = "../default_gkffon"
#     # print("presave >>> ", ProductImage.objects.filter(
#     #     product=instance.product.id, image=default_image))
#     if ProductImage.objects.filter(product=instance.product.id, image=default_image):
#         ProductImage.objects.filter(
#             product=instance.product.id, image=default_image).delete()


# @receiver(post_delete, sender=ProductImage)
# def create_image(sender, instance, **kwargs):
#     """
#     Method creates ProductImage instance with default image
#     when post_delete signal is received on ProductImage instance.
#     Signal is executed if related product has no image's
#     and the instance is not the default_image (pre_save delete_default signal conflict).
#     """
#     default_image = "../default_gkffon"
#     # print("postdelete instance image >>> ", instance.image)
#     # print("default image >>> ", default_image)
#     # print("instance == default image >>> ", instance.image == default_image)
#     if not ProductImage.objects.filter(product=instance.product.id) and not instance.image == default_image:
#         ProductImage.objects.create(
#             product=instance.product, owner=instance.owner)
#         print("post delete default created")
