import graphene
from graphene_django import DjangoObjectType
from django.db.models import Q
from ..models import Asset, Manufacturer, History
from .manufacturer_schema import FindManufacturer
from .history_schema import HistoryType, CreateHistoryInput


class AssetType(DjangoObjectType):
    class Meta:
        model = Asset


class FindAsset(graphene.ObjectType):
    asset = graphene.List(
        AssetType,
        search=graphene.String(),
        id=graphene.Int(),
        department=graphene.String(),
        owner=graphene.String(),
        status=graphene.String(),
        manufacturer=graphene.String(),
        skip=graphene.Int(),
        last=graphene.Int()
    )

    def resolve_asset(self, info, search=None, id=None, department=None, owner=None, status=None, manufacturer=None,
                      last=None, skip=None, **kwargs):
        qs = Asset.objects.all()

        if search:
            filter = (
                Q(assetNr__icontains=search) |
                Q(eqNr__icontains=search) |
                Q(serialNumber__icontains=search) |
                Q(description__icontains=search)
            )
            qs = qs.filter(filter)

        if id:
            qs = qs.filter(id=id)

        if department:
            filter = (
                Q(history__department__detailedName__icontains=department) |
                Q(history__department__name__icontains=department)
            )
            qs = qs.filter(filter).order_by('-history__entryDate')

        if owner:
            filter = (
                Q(history__owner__icontains=owner)
            )
            qs = qs.filter(filter).order_by('-history__entryDate')

        if status:
            filter = (
                Q(history__status__status__icontains=status)
            )
            qs = qs.filter(filter).order_by('-history__entryDate')

        if manufacturer:
            filter = (
                    Q(manufacturer__name__icontains=manufacturer)
            )
            qs = qs.filter(filter)

        if skip:
            qs = qs[skip::]

        if last:
            qs = qs.order_by('-entryDate')[:last]

        return qs


class CreateAsset(graphene.Mutation):
    id = graphene.Int()
    assetNr = graphene.String()
    eqNr = graphene.String()
    serialNumber = graphene.String()
    manufacturer = graphene.Field(FindManufacturer)
    description = graphene.String()
    history = graphene.List(HistoryType)

    class Arguments:
        assetNr = graphene.String()
        eqNr = graphene.String()
        serialNumber = graphene.String()
        manufacturer = graphene.Int()
        description = graphene.String()
        history = graphene.List(CreateHistoryInput)

    def mutate(self, info, assetNr, eqNr, serialNumber, manufacturer, description, history):
        asset = Asset(
            assetNr=assetNr,
            eqNr=eqNr,
            serialNumber=serialNumber,
            manufacturer=Manufacturer.objects.get(id=manufacturer),
            description=description
        )
        asset.save()

        hist = []

        for n in history:
            History(
                asset_id=asset.id,
                department_id=n.department_id,
                status_id=n.status,
                owner=n.owner,
                inventoried=n.inventoried
            ).save()
            hist.append(n)

        return CreateAsset(
            id=asset.id,
            assetNr=asset.assetNr,
            eqNr=asset.eqNr,
            serialNumber=asset.serialNumber,
            manufacturer=asset.manufacturer.id,
            description=asset.description,
            history=hist
        )


class EditAsset(graphene.Mutation):
    id = graphene.Int()
    assetNr = graphene.String()
    eqNr = graphene.String()
    serialNumber = graphene.String()
    manufacturer = graphene.Field(FindManufacturer)
    description = graphene.String()
    history = graphene.List(HistoryType)

    class Arguments:
        id = graphene.Int()
        assetNr = graphene.String()
        eqNr = graphene.String()
        serialNumber = graphene.String()
        manufacturer = graphene.Int()
        description = graphene.String()
        history = graphene.List(CreateHistoryInput)

    def mutate(self, info, id, assetNr, eqNr, serialNumber, manufacturer, description, history):
        asset = Asset(
            id=id,
            assetNr=assetNr,
            eqNr=eqNr,
            serialNumber=serialNumber,
            manufacturer=Manufacturer.objects.get(id=manufacturer),
            description=description
        )
        asset.save()

        hist = []

        for n in history:
            History(
                asset_id=asset.id,
                department_id=n.department_id,
                status_id=n.status,
                owner=n.owner,
                inventoried=n.inventoried
            ).save()
            hist.append(n)

        return EditAsset(
            id=asset.id,
            assetNr=asset.assetNr,
            eqNr=asset.eqNr,
            serialNumber=asset.serialNumber,
            manufacturer=asset.manufacturer.id,
            description=asset.description,
            history=hist
        )


class DeleteAsset(graphene.Mutation):
    id = graphene.Int()

    class Arguments:
        id = graphene.Int()

    def mutate(self, info, id):
        asset = Asset(
            id=id
        )
        asset.delete()

        return "done"


class Mutation(graphene.ObjectType):
    create_asset = CreateAsset.Field()
    edit_asset = EditAsset.Field()
    delete_asset = DeleteAsset.Field()
