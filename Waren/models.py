from django.db import models

# Create your models here.
class WarenKategorien(models.Model):
    Waren_Kategorien_Name = models.CharField(max_length=50)
    Waren_Kategorien_Bild = models.ImageField(upload_to="img")

class WarenInfo(models.Model):
    Ware_Name = models.CharField(max_length=150)
    Ware_Preis = models.FloatField(default=0)
    Ware_Info = models.CharField(max_length=8000)
    Ware_Bild = models.ImageField(upload_to="Waren")
    Ware_Kategorien = models.ForeignKey("WarenKategorien",on_delete=models.CASCADE)