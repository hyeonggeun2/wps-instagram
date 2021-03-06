# Generated by Django 2.2.9 on 2020-01-08 02:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('members', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='img_profile',
            field=models.ImageField(blank=True, upload_to='users_profile/', verbose_name='프로필이미지'),
        ),
        migrations.AddField(
            model_name='user',
            name='name',
            field=models.CharField(default='', max_length=30),
            preserve_default=False,
        ),
    ]
