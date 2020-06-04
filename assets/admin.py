from django.contrib import admin
from assets.models import Department, Asset, History, Status, Manufacturer


@admin.register(Department)
class DepartmentAdmin(admin.ModelAdmin):
    list_display = ('name', 'detailedName',)
    search_fields = ['name', 'detailedName']


@admin.register(Asset)
class AssetAdmin(admin.ModelAdmin):
    list_display = ('assetNr', 'eqNr', 'serialNumber', 'manufacturer', 'description',)  # TODO: '__all__'
    search_fields = ['assetNr', 'eqNr', 'serialNumber', 'manufacturer__name', 'description']


@admin.register(History)
class HistoryAdmin(admin.ModelAdmin):
    list_display = ('asset', 'department', 'status', 'entryDate', 'owner', 'inventoried',)
    search_fields = ['asset__assetNr', 'department__name', 'status__status', 'entryDate', 'owner', 'inventoried']


@admin.register(Status)
class StatusAdmin(admin.ModelAdmin):
    list_display = ('status',)
    search_fields = ['status']


@admin.register(Manufacturer)
class ManufacturerAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ['name']
