from django.db import models
from django.contrib.auth.models import AbstractUser
# from phonenumber_field.modelfields import PhoneNumberField


class User(AbstractUser):
    email = models.EmailField(max_length=50, unique=True, blank=False, null=False)
    
    
class Profile(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    image = models.ImageField(
        upload_to='images/', default='../default_profile_glasses_r9uhlr'
    )
    # phone_number = PhoneNumberField()

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.username}'s profile"

    # this solution saves email as username when user is saved
    # def save(self, *args, **kwargs): 
    #     self.username = self.email
    #     return super().save(*args, **kwargs)


