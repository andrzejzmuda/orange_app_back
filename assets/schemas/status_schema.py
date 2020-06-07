import graphene
from graphene_django import DjangoObjectType
from django.db.models import Q
from ..models import Status


class StatusType(DjangoObjectType):
    class Meta:
        model = Status


class GetStatus(graphene.ObjectType):
    one = graphene.List(
        StatusType,
        id=graphene.Int()
    )

    def resolve_one(self, info, id=None, **kwargs):
        qs = Status.objects.all()

        if id:
            get = (
                Q(id=id)
            )
            qs = qs.get(get)

        return qs


class FindStatus(graphene.ObjectType):
    status = graphene.List(
        StatusType,
        search=graphene.String(),
        id=graphene.Int()
    )

    def resolve_status(self, info, search=None, id=None, **kwargs):
        qs = Status.objects.all()

        if search:
            filter = (
                Q(status__icontains=search)
            )
            qs = qs.filter(filter)
        if id:
            qs = qs.filter(id=id)

        return qs


class CreateStatus(graphene.Mutation):
    id = graphene.Int()
    status = graphene.String()

    class Arguments:
        status = graphene.String()

    def mutate(self, info, status):
        status = Status(
            status=status
        )
        status.save()

        return CreateStatus(
            id=status.id,
            status=status.status
        )


class EditStatus(graphene.Mutation):
    id = graphene.Int()
    status = graphene.String()

    class Arguments:
        id = graphene.Int()
        status = graphene.String()

    def mutate(self, info, id, status):
        status = Status(
            id=id,
            status=status
        )
        status.save()

        return CreateStatus(
            id=status.id,
            status=status.status
        )


class DeleteStatus(graphene.Mutation):
    id = graphene.Int()

    class Arguments:
        id = graphene.Int()

    def mutate(self, info, id):
        status = Status(
            id=id
        )
        status.delete()

        return "done"


class Mutation(graphene.ObjectType):
    create_status = CreateStatus.Field()
    edit_status = EditStatus.Field()
    delete_status = DeleteStatus.Field()
