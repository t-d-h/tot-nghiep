# Generated by Django 5.0.2 on 2024-03-04 07:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('servers_management', '0006_servers_os'),
    ]

    operations = [
        migrations.CreateModel(
            name='Service_mapping',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('server_id', models.CharField(max_length=5)),
                ('service_id', models.CharField(max_length=5)),
            ],
            options={
                'db_table': 'mapping_table',
            },
        ),
    ]
