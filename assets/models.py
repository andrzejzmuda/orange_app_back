from django.db import models
from django import template


register = template.Library()


class Manufacturer(models.Model):
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = 'Manufacturer'


class Department(models.Model):
    name = models.CharField(max_length=255)
    detailedName = models.CharField(max_length=255, null=True, blank=True)

    def __str__(self):
        return self.name, self.detailedName

    class Meta:
        verbose_name_plural = 'Department'


class Status(models.Model):
    status = models.CharField(max_length=255)

    def __str__(self):
        return self.status

    class Meta:
        verbose_name_plural = 'Status'


class Asset(models.Model):
    assetNr = models.CharField(max_length=255)
    eqNr = models.CharField(max_length=255)
    serialNumber = models.CharField(max_length=255)
    manufacturer = models.ForeignKey(Manufacturer, on_delete=models.SET_NULL, null=True, blank=True)
    description = models.CharField(max_length=255)

    def __str__(self):
        return self.assetNr, self.eqNr, self.serialNumber, self.manufacturer, self.description

    class Meta:
        verbose_name_plural = 'Asset'


class History(models.Model):
    asset = models.ForeignKey(Asset, on_delete=models.CASCADE)
    department = models.ForeignKey(Department, on_delete=models.SET_NULL, null=True, blank=True)
    status = models.ForeignKey(Status, on_delete=models.SET_NULL, null=True, blank=True)
    entryDate = models.DateTimeField(auto_now_add=True)
    owner = models.CharField(max_length=255, null=True, blank=True)
    inventoried = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return self.asset, self.department, self.status, self.entryDate, self.owner, self.inventoried

    class Meta:
        verbose_name_plural = 'History'
