import graphene
from graphene_django import DjangoObjectType
from django.db.models import Q
from ..models import Department


class DepartmentType(DjangoObjectType):
    class Meta:
        model = Department


class FindDepartment(graphene.ObjectType):
    department = graphene.List(
        DepartmentType,
        search=graphene.String(),
        id=graphene.ID()
    )

    def resolve_department(self, info, search=None, id=None, **kwargs):
        qs = Department.objects.all()

        if search:
            filter = (
                Q(name__icontains=search) |
                Q(detailedName__icontains=search)
            )
            qs = qs.filter(filter)
        if id:
            qs = qs.filter(id=id)

        return qs


class CreateDepartment(graphene.Mutation):
    id = graphene.Int()
    name = graphene.String()
    detailed_name = graphene.String()

    class Arguments:
        name = graphene.String()
        detailed_name = graphene.String()

    def mutate(self, info, name, detailed_name):
        department = Department(
            name=name,
            detailedName=detailed_name
        )
        department.save()

        return CreateDepartment(
            id=department.id,
            name=department.name,
            detailed_name=department.detailedName
        )


class EditDepartment(graphene.Mutation):
    id = graphene.Int()
    name = graphene.String()
    detailed_name = graphene.String()

    class Arguments:
        id = graphene.Int()
        name = graphene.String()
        detailed_name = graphene.String()

    def mutate(self, info, id, name, detailed_name):
        department = Department(
            id=id,
            name=name,
            detailedName=detailed_name
        )
        department.save()

        return CreateDepartment(
            id=department.id,
            name=department.name,
            detailed_name=department.detailedName
        )


class DeleteDepartment(graphene.Mutation):
    id = graphene.Int()

    class Arguments:
        id = graphene.Int()

    def mutate(self, info, id):
        department = Department(
            id=id
        )
        department.delete()

        return "done"


class Mutation(graphene.ObjectType):
    create_department = CreateDepartment.Field()
    edit_department = EditDepartment.Field()
    delete_department = DeleteDepartment.Field()
