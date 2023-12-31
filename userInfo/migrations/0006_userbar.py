# Generated by Django 4.2.2 on 2023-07-03 01:03

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('userInfo', '0005_usersuggest'),
    ]

    operations = [
        migrations.CreateModel(
            name='UserBar',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('bars', models.BigIntegerField()),
                ('username', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='userInfo.userinfo')),
            ],
            options={
                'db_table': 'bars',
            },
        ),
    ]
