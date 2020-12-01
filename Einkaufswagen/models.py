from django.db import models

# Create your models here.
class BestellungInfo(models.Model):
    Zustand = (
        (1, "Noch nicht bezahlen"),
        (2, "Noch nicht geliefert"),
        (3, "Geliefert"),
        (4, "Zugestellt"),
    )

    Bestellung_Nummer = models.CharField(max_length=100)
    # Addresse
    Bestellung_Add = models.CharField(max_length=200)
    # Empfaenger
    Bestellung_Empf = models.CharField(max_length=100)
    Bestellung_Tel = models.CharField(max_length=100)
    Bestellung_transkost = models.FloatField(default=3.99)
    Bestellung_Anmerkung = models.CharField(max_length=1000)
    Bestellung_Zustand = models.IntegerField(default=1, choices=Zustand)



class BestellungDetails(models.Model):
#    Ware_Kate = models.ForeignKey('Waren.WarenKategorien', on_delete=models.CASCADE)
    Ware_Kate = models.ForeignKey('Waren.WarenInfo', on_delete=models.CASCADE)
    Ware_Meng = models.IntegerField()
    Ware_Bestellung = models.ForeignKey("BestellungInfo", on_delete=models.CASCADE)
