# Generated by Django 4.2.4 on 2023-10-25 18:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Accounts', '0002_alter_profile_blocked_friends_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='profile',
            name='profile_pic',
            field=models.ImageField(default='Default_pfp.jpg', upload_to='pics/pfp_image'),
        ),
    ]
