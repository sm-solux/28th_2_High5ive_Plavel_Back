from django.db import models
from django.conf import settings
from sign.models import CustomUser

User = CustomUser

# Create your models here.
class MyPage(models.Model):
    my_user = models.ForeignKey(User, null=True, on_delete=models.CASCADE)
