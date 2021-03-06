from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.db import models, connection
from django.conf import settings

#def drop_table(table_name):
#    cursor = connection.cursor()
#    sql = f"DROP TABLE {table_name};"
#    cursor.execute(sql)

class CreateSystem(models.Model):
    system_name = models.CharField(max_length=32)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.system_name

class AddComponent(models.Model):
    system_name = models.ForeignKey(CreateSystem, on_delete=models.CASCADE)
    comp_name = models.CharField(max_length=10)
    comp_type = models.CharField(max_length=10)
    comp_num = models.IntegerField()
    zone = models.IntegerField()

    def __str__(self):
        return self.comp_name

class CreateDemand(models.Model):
    demand = models.FileField(upload_to='documents/')
    uploaded_at = models.DateTimeField(auto_now_add=True)
    component = models.OneToOneField(AddComponent, on_delete=models.CASCADE, primary_key=True)

class CreateBattery(models.Model):
    energy_capacity = models.IntegerField()
    soc_min = models.IntegerField()
    soc_max = models.IntegerField()
    base_cost = models.FloatField()
    energy_cost = models.FloatField()
    component = models.OneToOneField(AddComponent, on_delete=models.CASCADE)
    def __str__(self):
        return str(self.component)

class CreateSolar(models.Model):
    system_capacity = models.IntegerField()
    base_cost = models.FloatField()
    perw_cost = models.FloatField()
    component = models.OneToOneField(AddComponent, on_delete=models.CASCADE, primary_key=True)
    def __str__(self):
        return str(self.component)

class CreateConverter(models.Model):
    power = models.IntegerField()
    base_cost = models.FloatField()
    power_cost = models.FloatField()
    component = models.OneToOneField(AddComponent, on_delete=models.CASCADE, primary_key=True)
    def __str__(self):
        return str(self.power)

class CreateGenerator(models.Model):
    power = models.IntegerField()
    base_cost = models.FloatField()
    fuel_cost = models.FloatField()
    component = models.OneToOneField(AddComponent, on_delete=models.CASCADE, primary_key=True)
    def __str__(self):
        return str(self.power)

class CreateGrid(models.Model):
    energy_cost = models.FloatField()
    nm_allowed = models.BooleanField(default=False)
    component = models.OneToOneField(AddComponent, on_delete=models.CASCADE, primary_key=True)
    def __str__(self):
        return str(self.energy_cost)

class CreateController(models.Model):
    component = models.OneToOneField(AddComponent, on_delete=models.CASCADE, primary_key=True)

    def __str__(self):
        return str(self.system_capacity)

class AddToController(models.Model):
    component = models.OneToOneField(AddComponent, on_delete=models.CASCADE, primary_key=True)
    controller = models.OneToOneField(CreateController, on_delete=models.CASCADE)
    mode = models.CharField(max_length=2, choices=(('ss', 'Solar Support'), ('ab', 'Arbitrage'), ('ps', 'Peak Shaving')))

class ComponentOutputs(models.Model):
    component = models.OneToOneField(AddComponent, on_delete=models.CASCADE, primary_key=True)
    output = models.TextField()
