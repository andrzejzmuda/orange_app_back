import graphene
from graphene_django import DjangoObjectType
from django.db.models import Q
from ..models import History, Asset, Department, Status
from .status_schema import FindStatus, GetStatus
from .department_schema import FindDepartment


class CreateHistoryInput(graphene.InputObjectType):
    department_id = graphene.Int(required=True)
    status = graphene.Int(required=True)
    owner = graphene.String(required=False)
    inventoried = graphene.Date(required=False)


class EditHistoryInput(graphene.InputObjectType):
    id = graphene.Int(required=True)
    asset = graphene.Int(required=True)
    department_id = graphene.Int(required=True)
    status = graphene.Int(required=True)
    owner = graphene.String(required=False)
    inventoried = graphene.Date(required=False)


class HistoryType(DjangoObjectType):
    class Meta:
        model = History


class FindHistory(graphene.ObjectType):
    history = graphene.List(
        HistoryType,
        search=graphene.String(),
        id=graphene.Int(),
        entryDate=graphene.Date(),
        inventoried=graphene.Date()
    )

    def resolve_history(self, info, search=None, id=None, entryDate=None, inventoried=None, **kwargs):
        qs = History.objects.all()

        if search:
            filter = (
                Q(asset__assetNr__icontains=search) |
                Q(department__name__icontains=search) |
                Q(department__detailedName__icontains=search) |
                Q(status__status__icontains=search) |
                Q(owner__icontains=search)
            )
            qs = qs.filter(filter)

        if entryDate:
            filter = (
                Q(entryDate=entryDate)
            )
            qs = qs.filter(filter)

        if inventoried:
            filter = (
                Q(inventoried=inventoried)
            )
            qs = qs.filter(filter)

        if id:
            qs = qs.filter(id=id)

        return qs


class CreateHistory(graphene.Mutation):
    id = graphene.Int()
    asset = graphene.Int()
    department = graphene.Field(FindDepartment)
    status = graphene.Field(GetStatus)
    entryDate = graphene.DateTime()
    owner = graphene.String(required=False)
    inventoried = graphene.Date(required=False)

    class Arguments:
        asset = graphene.Int()
        department = graphene.Int()
        status = graphene.Int()
        owner = graphene.String(required=False)
        inventoried = graphene.Date(required=False)

    def mutate(self, info, asset, department, status, owner, inventoried, **kwargs):
        history = History(
            asset=Asset.objects.get(id=asset),
            department=Department.objects.get(id=department),
            status=Status.objects.get(id=status),
            owner=owner,
            inventoried=inventoried
        )
        history.save()

        return CreateHistory(
            id=history.id,
            asset=history.asset,
            department=(history.department.name, history.department.detailedName),
            status=history.status,
            entryDate=history.entryDate,
            owner=history.owner,
            inventoried=history.inventoried
        )


class EditHistory(graphene.Mutation):
    id = graphene.Int()
    asset = graphene.Int()
    department = graphene.Int()
    status = graphene.Field(GetStatus)
    entryDate = graphene.DateTime()
    owner = graphene.String(required=False)
    inventoried = graphene.Date(required=False)

    class Arguments:
        id = graphene.Int()
        asset = graphene.Int()
        department = graphene.Int()
        status = graphene.Int()
        owner = graphene.String(required=False)
        inventoried = graphene.Date(required=False)

    def mutate(self, info, id, asset, department, status, owner, inventoried, **kwargs):
        history = History(
            id=id,
            asset=Asset.objects.get(id=asset),
            department=Department.objects.get(id=department),
            status=Status.objects.get(id=status),
            entryDate=History.objects.get(id=id).entryDate,
            owner=owner,
            inventoried=inventoried
        )
        history.save()

        return EditHistory(
            id=history.id,
            asset=history.asset,
            department=(history.department.name, history.department.detailedName),
            status=history.status,
            entryDate=history.entryDate,
            owner=history.owner,
            inventoried=history.inventoried
        )


class DeleteHistory(graphene.Mutation):
    id = graphene.Int()

    class Arguments:
        id = graphene.Int()

    def mutate(self, info, id):
        item = History(
            id=id
        )
        item.delete()

        return "done"


class Mutation(graphene.ObjectType):
    create_history = CreateHistory.Field()
    edit_history = EditHistory.Field()
    delete_history = DeleteHistory.Field()
