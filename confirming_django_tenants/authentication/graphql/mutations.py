import strawberry
from typing import Optional
from strawberry.types import Info
from confirming_django_tenants.authentication.decorators import login_required

from confirming_django_tenants.authentication.services import (
    AuthenticationService,
    AuthenticationError,
)
from confirming_django_tenants.authentication.graphql.types import (
    LoginResponseType,
    RegistrationResponseType,
    TenantSwitchResponseType,
    AuthTokensType,
    LogoutResponseType,
)


@strawberry.type
class AuthMutation:
    
    @strawberry.mutation
    def register_tenant(
        self,
        info: Info,
        email: str,
        password: str,
        company_name: str,
        subdomain: str,
    ) -> RegistrationResponseType:
        """
        Register a new tenant with owner account.
        
        This creates:
        - A new user account
        - A new tenant with schema
        - Default roles and permissions
        - Assigns owner role to the user
        """
        try:
            return AuthenticationService.register_tenant_owner(
                email=email,
                password=password,
                company_name=company_name,
                subdomain=subdomain,
            )
        except Exception as e:
            raise Exception(f"Registration failed: {str(e)}")
    
    @strawberry.mutation
    def login(
        self,
        info: Info,
        email: str,
        password: str,
        tenant_slug: Optional[str] = None,
    ) -> LoginResponseType:
        """
        Login user and get authentication tokens.
        
        The response includes:
        - User information
        - Current tenant details
        - All available tenants for the user
        - User's roles in current tenant
        - User's permissions in current tenant
        - JWT access and refresh tokens
        """
        try:
            # Get client info from request context
            request = info.context.request
            ip_address = request.META.get('REMOTE_ADDR')
            user_agent = request.META.get('HTTP_USER_AGENT', '')
            
            return AuthenticationService.login_user(
                email=email,
                password=password,
                tenant_slug=tenant_slug,
                ip_address=ip_address,
                user_agent=user_agent,
            )
        except AuthenticationError as e:
            raise Exception(str(e))
        except Exception as e:
            raise Exception(f"Login failed: {str(e)}")
    
    @strawberry.mutation
    @login_required
    def switch_tenant(
        self,
        info: Info,
        tenant_slug: str,
    ) -> TenantSwitchResponseType:
        """
        Switch to a different tenant.
        
        The user must be a member of the target tenant.
        Returns updated roles and permissions for the new tenant.
        """
        try:
            user = info.context.request.user
            return AuthenticationService.switch_tenant(user, tenant_slug)
        except AuthenticationError as e:
            raise Exception(str(e))
        except Exception as e:
            raise Exception(f"Tenant switch failed: {str(e)}")
    
    @strawberry.mutation
    def refresh_token(
        self,
        info: Info,
        refresh_token: str,
    ) -> AuthTokensType:
        """
        Refresh an expired access token using a refresh token.
        
        Returns new access and refresh token pair.
        The old refresh token is invalidated (token rotation).
        """
        try:
            return AuthenticationService.refresh_token(refresh_token)
        except AuthenticationError as e:
            raise Exception(str(e))
        except Exception as e:
            raise Exception(f"Token refresh failed: {str(e)}")
    
    @strawberry.mutation
    @login_required
    def logout(
        self,
        info: Info,
        refresh_token: Optional[str] = None,
    ) -> LogoutResponseType:
        """
        Logout user by revoking refresh token(s).
        
        If refresh_token is provided, only that token is revoked.
        Otherwise, all refresh tokens for the user are revoked.
        """
        try:
            user = info.context.request.user
            success = AuthenticationService.logout_user(user, refresh_token)
            
            return LogoutResponseType(
                success=success,
                message="Logged out successfully" if success else "Logout failed"
            )
        except Exception as e:
            return LogoutResponseType(
                success=False,
                message=f"Logout failed: {str(e)}"
            )