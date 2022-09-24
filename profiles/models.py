from django.db import models
from django.conf import settings
from django.contrib.auth.models import AbstractUser
from phonenumber_field.modelfields import PhoneNumberField
from allauth.account.models import EmailAddress
from allauth.account.utils import *
from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from allauth.account.signals import email_confirmed, email_changed, email_added


class ProfileRatingManager(models.Manager):
    """
    Custom model manager allowing for avg_score
    and all_scores to be avaialble globally.
    """

    def get_queryset(self):
        """
        Returns queryset annotated with avg_score and all_scores fields.
        """
        return super(ProfileRatingManager, self).get_queryset().annotate(
            avg_score=models.Avg('owner__product__product_rating__score'),
            all_scores=models.Count('owner__product__product_rating__score')
        )


class User(AbstractUser):
    """
    Custom User model inherits from Abstrac User model.
    """
    email = models.EmailField(max_length=50, unique=True, blank=False)
    first_name = models.CharField(max_length=50, blank=True)
    last_name = models.CharField(max_length=50, blank=True)
    email_verified = models.BooleanField(default=False)

    def __str__(self):
        """
        Returns string representation of owner's username.
        """
        return self.username

    # def add_email_address(self, request, new_email):
    #     # Add a new email address for the user, and send email confirmation.
    #     # Old email will remain the primary until the new one is confirmed.
    #     return EmailAddress.objects.add_email(request, self.user, new_email, confirm=True)


class Profile(models.Model):
    """
    The Profile model with One to One realtionship to User model.
    """
    owner = models.OneToOneField(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    image = models.ImageField(
        upload_to='images/', default='../default_profile_glasses_r9uhlr'
    )
    phone_number = PhoneNumberField()

    objects = ProfileRatingManager()

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        """
        Returns string representation of profile's owner.
        """
        return f"{self.owner.username}'s profile"


@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_profile(sender, instance, created, **kwargs):
    """
    Method creates Profile for the new User instance.
    """
    if created:
        Profile.objects.create(owner=instance)


@receiver(post_delete, sender=Profile)
def delete_profile(sender, instance, **kwargs):
    """
    Method deletes user on Profile deletion.
    """
    User.objects.get(pk=instance.owner.id).delete()


@receiver(email_confirmed)
def email_confirmed_(request, email_address, **kwargs):
    """
    Signal tracks user's email confirmation and sets email_verified
    to True if confirmed.
    """
    user = email_address.user
    print(user)
    user.email_verified = True
    user.save()
