from django.db import models, connection
from django.conf import settings

#def drop_table(table_name):
#    cursor = connection.cursor()
#    sql = f"DROP TABLE {table_name};"
#    cursor.execute(sql)

class CreateBattery(models.Model):
    energy_capacity = models.IntegerField()
    soc_min = models.IntegerField()
    soc_max = models.IntegerField()
    base_cost = models.FloatField()
    energy_cost = models.FloatField()

    def __str__(self):
        return str(self.energy_capacity)

class AddBattery(models.Model):
    bat_name = models.CharField(max_length=10)
    zone = models.IntegerField()
    createbattery = models.ForeignKey(CreateBattery, on_delete=models.CASCADE)

    def __str__(self):
        return self.bat_name

class AddComponent(models.Model):
    bat_name = models.CharField(max_length=10)
    zone = models.IntegerField()
    createbattery = models.ForeignKey(CreateBattery, on_delete=models.CASCADE)

    def __str__(self):
        return self.bat_name
