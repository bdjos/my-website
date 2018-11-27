from django.db import models, connection
from django.conf import settings

#def drop_table(table_name):
#    cursor = connection.cursor()
#    sql = f"DROP TABLE {table_name};"
#    cursor.execute(sql)

class CreateBatteryComponent(models.Model):
    bat_name = models.CharField(max_length=10)
    zone = models.IntegerField()
    

class CreateBatteryDetails(models.Model):
    energy_capacity = models.IntegerField()
    soc_min = models.IntegerField()
    soc_max = models.IntegerField()
    base_cost = models.FloatField()
    energy_cost = models.FloatField()
    link = models.ForeignKey(CreateBatteryDetails)


    def add_component(self):
        self.save()

    def __str__(self):
        return self.bat_name

    class Meta:
        managed = True
