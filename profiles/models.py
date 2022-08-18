from django.db import models
from django.conf import settings
from django.db.models.signals import post_save, post_delete
from django.contrib.auth.models import AbstractUser
from phonenumber_field.modelfields import PhoneNumberField


class User(AbstractUser):
    email = models.EmailField(max_length=50, unique=True, blank=False)
    first_name = models.CharField(max_length=50, blank=False)
    last_name = models.CharField(max_length=50, blank=False)
    
class Profile(models.Model):
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
        return f"{self.owner.username}'s profile"

    # this solution saves email as username when user is saved
    # def save(self, *args, **kwargs): 
    #     self.username = self.email
    #     return super().save(*args, **kwargs)

def create_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(owner=instance)

def delete_profile(sender, instance, **kwargs):
    User.objects.get(pk=instance.owner.id).delete()

post_save.connect(create_profile, sender=settings.AUTH_USER_MODEL)
post_delete.connect(delete_profile, sender=Profile)