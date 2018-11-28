from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.db import models, connection
from django.conf import settings

#def drop_table(table_name):
#    cursor = connection.cursor()
#    sql = f"DROP TABLE {table_name};"
#    cursor.execute(sql)

class CreateDemand(models.Model):
    demand = models.FloatField()

class CreateBattery(models.Model):
    energy_capacity = models.IntegerField()
    soc_min = models.IntegerField()
    soc_max = models.IntegerField()
    base_cost = models.FloatField()
    energy_cost = models.FloatField()

    def __str__(self):
        return str(self.energy_capacity)

class CreateSolar(models.Model):
    system_capacity = models.IntegerField()
    base_cost = models.FloatField()
    perw_cost = models.FloatField()

    def __str__(self):
        return str(self.system_capacity)

class CreateConverter(models.Model):
    system_capacity = models.IntegerField()
    base_cost = models.FloatField()
    perw_cost = models.FloatField()

    def __str__(self):
        return str(self.system_capacity)

class CreateGenerator(models.Model):
    system_capacity = models.IntegerField()
    base_cost = models.FloatField()
    perw_cost = models.FloatField()

    def __str__(self):
        return str(self.system_capacity)

class CreateGrid(models.Model):
    system_capacity = models.IntegerField()
    base_cost = models.FloatField()
    perw_cost = models.FloatField()

    def __str__(self):
        return str(self.system_capacity)

class CreateController(models.Model):
    system_capacity = models.IntegerField()
    base_cost = models.FloatField()
    perw_cost = models.FloatField()

    def __str__(self):
        return str(self.system_capacity)

class AddBattery(models.Model):
    bat_name = models.CharField(max_length=10)
    zone = models.IntegerField()
    createbattery = models.ForeignKey(CreateBattery, on_delete=models.CASCADE)
    
    def __str__(self):
        return self.bat_name

class AddComponent(models.Model):
    comp_name = models.CharField(max_length=10)
    comp_type = models.CharField(max_length=10)
    zone = models.IntegerField()
    object_id = models.PositiveIntegerField()
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    createcomponent = GenericForeignKey('content_type', 'object_id')

    def __str__(self):
        return self.comp_name
