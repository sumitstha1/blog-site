# Generated by Django 4.1.7 on 2023-03-04 09:05

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0008_client_profile_picture'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='client',
            name='otp',
        ),
    ]