from django.contrib.auth.models import AbstractUser
from django.db.models import ImageField, EmailField


class User(AbstractUser):
    email = EmailField(verbose_name="Email address", unique=True)
    image = ImageField(upload_to='user_images/', null=True, blank=True)
    
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    class Meta:
        verbose_name = "User"
        verbose_name_plural = "Users"

    def __str__(self) -> str:
        return self.email
