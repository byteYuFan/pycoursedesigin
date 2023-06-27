from django.db import models


# Create your models here.

class UserInfo(models.Model):
    user_id = models.AutoField(primary_key=True)
    username = models.CharField(max_length=255,unique=True)
    password = models.CharField(max_length=255)
    email = models.EmailField(unique=True)
    flag = models.BooleanField(default=False)
    time = models.DateTimeField(null=True)

    def __str__(self):
        return self.username
