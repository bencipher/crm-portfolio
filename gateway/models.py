from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()
# Create your models here.


class Jwt(models.Model):
    user = models.OneToOneField(
        User, related_name="logged_in_user", on_delete=models.CASCADE)
    access = models.TextField()
    refresh = models.TextField()
    date_created = models.DateTimeField(auto_now_add=True)
    date_updated = models.DateTimeField(auto_now=True)

    def __str__(self) -> str:
        return self.user.email + '\'s token'

    class Meta:
        verbose_name_plural = 'Jwt Tokens'
