# Generated by Django 4.2.4 on 2024-01-02 17:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Accounts', '0004_alter_profile_profile_pic'),
    ]

    operations = [
        migrations.AddField(
            model_name='customuser',
            name='last_activity',
            field=models.DateTimeField(blank=True, null=True),
        ),
    ]