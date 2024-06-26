# Generated by Django 4.2.4 on 2023-10-10 18:57

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='GMessage',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
            ],
        ),
        migrations.CreateModel(
            name='OTOMessage',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
            ],
        ),
        migrations.CreateModel(
            name='OneToOneChat',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('call_start_time', models.DateTimeField(auto_now_add=True)),
                ('call_duration_minutes', models.PositiveIntegerField(default=0)),
                ('is_video_call', models.BooleanField(default=False)),
                ('participants', models.ManyToManyField(to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='GroupChat',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('call_start_time', models.DateTimeField(auto_now_add=True)),
                ('call_duration_minutes', models.PositiveIntegerField(default=0)),
                ('is_video_call', models.BooleanField(default=False)),
                ('admin_users', models.ManyToManyField(blank=True, default=None, related_name='group_chats_admin', to=settings.AUTH_USER_MODEL)),
                ('participants', models.ManyToManyField(related_name='group_chats_participating', to=settings.AUTH_USER_MODEL)),
                ('root_user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='group_chats_created', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
