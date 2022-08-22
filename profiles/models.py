from django.db import models
from django.conf import settings
from django.contrib.auth.models import AbstractUser
from phonenumber_field.modelfields import PhoneNumberField
from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver


class User(AbstractUser):
    """
    Custom User model inherits from Abstrac User model.
    """
    email = models.EmailField(max_length=50, unique=True, blank=False)
    first_name = models.CharField(max_length=50, blank=False)
    last_name = models.CharField(max_length=50, blank=False)

    def __str__(self):
        """
        Returns string representation of owner's username.
        """
        return self.username
    
class Profile(models.Model):
    """
    The Profile model with One to One realtionship to User model.
    """
    owner = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    image = models.ImageField(
        upload_to='images/', default='../default_profile_glasses_r9uhlr'
    )
    phone_number = PhoneNumberField()

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        """
        Returns string representation of profile's owner.
        """
        return f"{self.owner.username}'s profile"

    # this solution saves email as username when user is saved
    # def save(self, *args, **kwargs): 
    #     self.username = self.email
    #     return super().save(*args, **kwargs)

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