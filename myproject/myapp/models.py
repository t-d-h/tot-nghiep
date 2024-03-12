from django.db import models

class Service(models.Model):

   id = models.IntegerField(primary_key=True)
   used_server = models.CharField(max_length = 50)
   owner = models.CharField(max_length = 50)
   service_name = models.CharField(max_length = 50)
   class Meta:
      db_table = "services"

class Servers(models.Model):

   id = models.IntegerField(primary_key=True)
   cpu_model = models.CharField(max_length = 50, default='0000000')
   memory = models.CharField(max_length = 50, default='0000000')
   active_service = models.CharField(max_length = 50, default='0000000')
   disk = models.CharField(max_length = 50, default='0000000')
   status = models.CharField(max_length = 50, default='0000000')
   requested_user = models.CharField(max_length = 50, default='0000000')
   class Meta:
      db_table = "servers"
