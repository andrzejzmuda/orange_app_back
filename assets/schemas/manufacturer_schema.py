import graphene
from graphene_django import DjangoObjectType
from django.db.models import Q
from ..models import Manufacturer


class ManufacturerType(DjangoObjectType):
    class Meta:
        model = Manufacturer


class FindManufacturer(graphene.ObjectType):
    manufacturer = graphene.List(
        ManufacturerType,
        search=graphene.String(),
        id=graphene.Int()
    )

    def resolve_manufacturer(self, info, search=None, id=None, **kwargs):
        qs = Manufacturer.objects.all()

        if search:
            filter = (
                Q(name__icontains=search)
            )
            qs = qs.filter(filter)
        if id:
            qs = qs.filter(id=id)

        return qs


class CreateManufacturer(graphene.Mutation):
    id = graphene.Int()
    name = graphene.String()

    class Arguments:
        name = graphene.String()

    def mutate(self, info, name):
        manufacturer = Manufacturer(
            name=name
        )
        manufacturer.save()

        return CreateManufacturer(
            id=manufacturer.id,
            name=manufacturer.name,
        )


class EditManufacturer(graphene.Mutation):
    id = graphene.Int()
    name = graphene.String()

    class Arguments:
        id = graphene.Int()
        name = graphene.String()

    def mutate(self, info, id, name):
        manufacturer = Manufacturer(
            id=id,
            name=name
        )
        manufacturer.save()

        return CreateManufacturer(
            id=manufacturer.id,
            name=manufacturer.name
        )


class DeleteManufacturer(graphene.Mutation):
    id = graphene.Int()

    class Arguments:
        id = graphene.Int()

    def mutate(self, info, id):
        manufacturer = Manufacturer(
            id=id
        )
        manufacturer.delete()

        return "done"


class Mutation(graphene.ObjectType):
    create_manufacturer = CreateManufacturer.Field()
    edit_manufacturer = EditManufacturer.Field()
    delete_manufacturer = DeleteManufacturer.Field()
