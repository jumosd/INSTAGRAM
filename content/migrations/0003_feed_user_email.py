# Generated by Django 4.2 on 2023-05-24 00:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('content', '0002_rename_user_id_feed_user_nickname'),
    ]

    operations = [
        migrations.AddField(
            model_name='feed',
            name='user_email',
            field=models.CharField(blank=True, max_length=30),
        ),
    ]
