# Generated by Django 5.0.2 on 2024-02-29 10:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('servers_management', '0005_remove_servers_requested_user_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='servers',
            name='os',
            field=models.CharField(default='Debian 12', max_length=50),
        ),
    ]
