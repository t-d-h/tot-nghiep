# Generated by Django 5.0.2 on 2024-02-29 08:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('servers_management', '0004_servers_server_name'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='servers',
            name='requested_user',
        ),
        migrations.AlterField(
            model_name='servers',
            name='active_service',
            field=models.CharField(default='None', max_length=50),
        ),
        migrations.AlterField(
            model_name='servers',
            name='status',
            field=models.CharField(default='free', max_length=50),
        ),
    ]