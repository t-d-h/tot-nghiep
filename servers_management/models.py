from django.db import models
import django_tables2 as tables
from django_tables2 import TemplateColumn
import random


class Services(models.Model):
   id = models.AutoField(primary_key=True)
   used_server = models.CharField(max_length = 50)
   owner = models.CharField(max_length = 50)
   service_name = models.CharField(max_length = 50)
   class Meta:
      db_table = "services"

class Servers(models.Model):
   id = models.AutoField(primary_key=True)
   server_name = models.CharField(max_length = 50, default='0000000')
   cpu_model = models.CharField(max_length = 50, default='0000000')
   memory = models.CharField(max_length = 50, default='0000000')
   active_service = models.CharField(max_length = 1000, default='None')
   disk = models.CharField(max_length = 50, default='0000000')
   status = models.CharField(max_length = 50, default='free')
   os = models.CharField(max_length = 50, default='debian 12')

   cpu_graph = models.CharField(max_length = 500, default='No graph added')
   memory_graph = models.CharField(max_length = 500, default='No graph added')
   disk_graph = models.CharField(max_length = 500, default='No graph added')
   
   class Meta:
      db_table = "servers"

class Service_mapping2(models.Model): #id cua ban
   id = models.IntegerField(primary_key=True)
   server_id = models.CharField(max_length = 5)
   class Meta:
      db_table = "mapping_table2"


# tables
class ServiceTable(tables.Table):
   edit_button =  tables.TemplateColumn('<a href="{% url "service_detail" record.id %}" class="btn btn-primary">Edit</a>', verbose_name='', )
   class Meta:
      model = Services
      template_name = "django_tables2/bootstrap.html"
      fields = ['id', 'service_name', 'owner', 'used_server']


class ServerTable(tables.Table):
   edit_button =  tables.TemplateColumn('<a href="{% url "server_detail" record.id %}" class="btn btn-primary">Edit</a>', verbose_name='', )
   monitor_button =  tables.TemplateColumn('<a href="{% url "server_monitor" record.id %}" class="btn btn-success"> Monitor </a>', verbose_name='', )
   class Meta:
      model = Servers
      template_name = "django_tables2/bootstrap.html"
      fields = ['id', 'server_name', 'os', 'cpu_model', 'memory', 'disk', 'active_service', 'status']