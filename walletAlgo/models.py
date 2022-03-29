from email.headerregistry import Address
from django.db import models
from django.contrib.auth.models import AbstractUser
# Create your models here.


class user(AbstractUser):
    passfrase=models.TextField(max_length=500)
    Address=models.CharField(max_length=100)
    privateKey=models.CharField(max_length=100)