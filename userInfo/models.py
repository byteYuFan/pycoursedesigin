from django.db import models


class UserInfo(models.Model):
    user_id = models.AutoField(primary_key=True)
    username = models.CharField(max_length=255)
    password = models.CharField(max_length=255)
    email = models.EmailField()
    flag = models.BooleanField(default=False)
    time = models.DateTimeField(null=True)


class UserSuggest(models.Model):
    username = models.CharField(max_length=255)
    email = models.CharField(max_length=255)
    subject = models.CharField(max_length=255)
    text = models.TextField()

    def __str__(self):
        return self.subject


class UserBar(models.Model):
    username = models.CharField(max_length=255)
    bar = models.BigIntegerField()
    # 添加其他字段...

    class Meta:
        db_table = 'bars'
