# Generated by Django 4.2.2 on 2023-07-03 01:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('userInfo', '0006_userbar'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userbar',
            name='username',
            field=models.CharField(max_length=255),
        ),
    ]
