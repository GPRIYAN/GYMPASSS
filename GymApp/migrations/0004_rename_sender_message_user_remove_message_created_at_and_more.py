# Generated by Django 5.1.3 on 2024-12-09 08:19

import django.db.models.deletion
import django.utils.timezone
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('GymApp', '0003_alter_message_options_alter_room_options_and_more'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.RenameField(
            model_name='message',
            old_name='sender',
            new_name='user',
        ),
        migrations.RemoveField(
            model_name='message',
            name='created_at',
        ),
        migrations.RemoveField(
            model_name='message',
            name='exercise_animation_url',
        ),
        migrations.RemoveField(
            model_name='room',
            name='participants',
        ),
        migrations.AddField(
            model_name='message',
            name='timestamp',
            field=models.DateTimeField(default=django.utils.timezone.now),
        ),
        migrations.AlterField(
            model_name='room',
            name='trainer',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
    ]
