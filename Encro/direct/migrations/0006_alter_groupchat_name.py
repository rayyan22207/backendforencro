# Generated by Django 4.2.4 on 2023-10-31 16:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('direct', '0005_groupcall_otocall_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='groupchat',
            name='name',
            field=models.CharField(max_length=255),
        ),
    ]