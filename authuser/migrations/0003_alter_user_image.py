# Generated by Django 4.2.11 on 2024-06-08 05:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('authuser', '0002_user_image'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='image',
            field=models.ImageField(default='authuser/images/avator.png', upload_to='authuser/images/'),
        ),
    ]
