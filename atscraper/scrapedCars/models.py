from django.db import models

# Create your models here.
class CarManufacturer(models.Model):
    car_manufacturer = models.CharField(max_length=100, null=True, blank=True)
    def __str__(self):
        return self.car_brand

class Car(models.Model):
    car_model = models.CharField(max_length=100, null=True, blank=True)
    car_link = models.CharField(max_length=100, null=True, blank=True)
    car_photo = models.CharField(max_length=300, null=True, blank=True)
    car_manufacturer = models.ForeignKey(
        CarManufacturer, on_delete=models.CASCADE)
    car_price = models.CharField(max_length=100, null=True, blank=True)
    car_color = models.CharField(max_length=100, null=True, blank=True)
    car_year = models.CharField(max_length=100, null=True, blank=True)
    car_type = models.CharField(max_length=100, null=True, blank=True)
    car_engine = models.CharField(max_length=100, null=True, blank=True)
    car_milage = models.CharField(max_length=100, null=True, blank=True)
    car_gearbox = models.CharField(max_length=100, null=True, blank=True)
    car_owners = models.CharField(max_length=100, null=True, blank=True)
    car_doors = models.CharField(max_length=100, null=True, blank=True)
    car_location = models.CharField(max_length=100, null=True, blank=True)
    car_nct = models.CharField(max_length=100, null=True, blank=True)
    def __str__(self):
        return str(self.id) + ' ' + str(self.car_manufacturer) + ' ' + str(self.car_model)
