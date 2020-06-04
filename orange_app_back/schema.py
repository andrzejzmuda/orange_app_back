import graphene
from assets.schemas import department_schema
from assets.schemas import manufacturer_schema
from assets.schemas import status_schema
from assets.schemas import asset_schema
from assets.schemas import history_schema


class Query(department_schema.FindDepartment,
            manufacturer_schema.FindManufacturer,
            status_schema.FindStatus,
            status_schema.GetStatus,
            asset_schema.FindAsset,
            history_schema.FindHistory,
            graphene.ObjectType):
    pass


class Mutation(department_schema.Mutation,
               manufacturer_schema.Mutation,
               status_schema.Mutation,
               asset_schema.Mutation,
               history_schema.Mutation,
               graphene.ObjectType):
    pass


schema = graphene.Schema(query=Query, mutation=Mutation)
