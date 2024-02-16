# Generated by Django 4.2.4 on 2023-10-24 08:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('direct', '0004_remove_groupmessage_chat_remove_otomessage_chat_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='GroupCall',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('call_start_time', models.DateTimeField(auto_now_add=True)),
                ('call_duration_minutes', models.PositiveIntegerField(default=0)),
                ('is_video_call', models.BooleanField(default=False)),
            ],
        ),
        migrations.CreateModel(
            name='OTOCall',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('call_start_time', models.DateTimeField(auto_now_add=True)),
                ('call_duration_minutes', models.PositiveIntegerField(default=0)),
                ('is_video_call', models.BooleanField(default=False)),
            ],
        ),
        migrations.RemoveField(
            model_name='groupchat',
            name='call_duration_minutes',
        ),
        migrations.RemoveField(
            model_name='groupchat',
            name='call_start_time',
        ),
        migrations.RemoveField(
            model_name='groupchat',
            name='is_video_call',
        ),
        migrations.RemoveField(
            model_name='onetoonechat',
            name='call_duration_minutes',
        ),
        migrations.RemoveField(
            model_name='onetoonechat',
            name='call_start_time',
        ),
        migrations.RemoveField(
            model_name='onetoonechat',
            name='is_video_call',
        ),
    ]