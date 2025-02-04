# Generated by Django 5.0.2 on 2024-03-07 15:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('servers_management', '0009_service_mapping2_alter_servers_os'),
    ]

    operations = [
        migrations.DeleteModel(
            name='Service_mapping',
        ),
        migrations.AddField(
            model_name='servers',
            name='cpu_graph',
            field=models.CharField(default='debian 12', max_length=500),
        ),
        migrations.AddField(
            model_name='servers',
            name='disk_graph',
            field=models.CharField(default='debian 12', max_length=500),
        ),
        migrations.AddField(
            model_name='servers',
            name='memory_graph',
            field=models.CharField(default='debian 12', max_length=500),
        ),
    ]
