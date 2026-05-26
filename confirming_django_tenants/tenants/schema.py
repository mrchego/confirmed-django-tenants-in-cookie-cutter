import strawberry
from strawberry.types import Info
from confirming_django_tenants.tenants.models import Tenant
from confirming_django_tenants.tenants.types import UserType, TenantType

@strawberry.type
class Query:
    @strawberry.field
    def me(self, info:Info) -> UserType:
        return info.context.request.user

    # @strawberry.field
    # def tenants(self) -> list(TenantType):
    #     return Tenant.objects.all()