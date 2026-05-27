import strawberry
from strawberry_django import DjangoModelType
from confirming_django_tenants.authentication.graphql.mutations import AuthMutation
from confirming_django_tenants.authentication.graphql.queries import AuthQuery
from confirming_django_tenants.rbac.graphql.mutations import RBACMutation
from confirming_django_tenants.rbac.graphql.queries import RBACQuery
from confirming_django_tenants.employees.graphql.mutations import EmployeeMutation
from confirming_django_tenants.employees.graphql.queries import EmployeeQuery


@strawberry.type
class Query(AuthQuery, RBACQuery, EmployeeQuery):
    """Root query combining all domain queries."""
    
    @strawberry.field
    def hello(self) -> str:
        return "Hello from multi-tenant SaaS!"


@strawberry.type
class Mutation(AuthMutation, RBACMutation, EmployeeMutation):
    """Root mutation combining all domain mutations."""
    pass


schema = strawberry.Schema(
    query=Query,
    mutation=Mutation,
)