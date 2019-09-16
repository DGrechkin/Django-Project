from django.db import models
from django.utils import timezone

# Create your models here.


class DonationType(models.Model):
    name = models.CharField(max_length=50)

    def get_name(self):
        return self.name

    def __str__(self):
        return str(self.name)


class Donation_List(models.Model):
    name = models.CharField(max_length=200)
    date = models.DateField(auto_now_add=True)
    amount = models.DecimalField(max_digits=13, decimal_places=2)
    donationType = models.CharField(max_length=100)

    def transaction(self):
        self.date = timezone.now()
        self.save()

    def __str__(self):
        return str(self.name)
