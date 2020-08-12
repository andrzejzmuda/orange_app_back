from django.db import models
from django import template


register = template.Library()


class Manufacturer(models.Model):
    name = models.CharField(max_length=255)

    class Meta:
        verbose_name_plural = 'Manufacturer'

    def __str__(self):
        return self.name


class Department(models.Model):
    name = models.CharField(max_length=255)
    detailedName = models.CharField(max_length=255, null=True, blank=True)

    class Meta:
        verbose_name_plural = 'Department'

    def __str__(self):
        return '%s %s' % (self.name, self.detailedName)


class Status(models.Model):
    status = models.CharField(max_length=255)

    class Meta:
        verbose_name_plural = 'Status'

    def __str__(self):
        return self.status


class Asset(models.Model):
    assetNr = models.CharField(max_length=255)
    eqNr = models.CharField(max_length=255)
    serialNumber = models.CharField(max_length=255)
    manufacturer = models.ForeignKey(Manufacturer, on_delete=models.SET_NULL, null=True, blank=True)
    description = models.CharField(max_length=255)

    class Meta:
        verbose_name_plural = 'Asset'

    def __str__(self):
        return '%s %s' % (self.assetNr, self.eqNr)


class History(models.Model):
    asset = models.ForeignKey(Asset, on_delete=models.CASCADE)
    department = models.ForeignKey(Department, on_delete=models.SET_NULL, null=True, blank=True)
    status = models.ForeignKey(Status, on_delete=models.SET_NULL, null=True, blank=True)
    entryDate = models.DateTimeField(auto_now_add=True)
    owner = models.CharField(max_length=255, null=True, blank=True)
    inventoried = models.DateField(null=True, blank=True)

    class Meta:
        verbose_name_plural = 'History'

    def __str__(self):
        return self.asset.assetNr
