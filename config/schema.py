# config/graphql.py
import strawberry

from confirming_django_tenants.tenants.schema import Query
from confirming_django_tenants.tenants.mutations import Mutation

schema = strawberry.Schema(
    query=Query,
    mutation=Mutation,
)