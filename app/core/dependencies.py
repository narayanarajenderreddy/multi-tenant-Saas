from fastapi import Depends,HTTPException
from app.core.role_permissions import ROLE_PERMISSIONS
from app.models.user import User
from app.api.auth import get_current_user

def require_roles(allowed_roles:list):
    def role_checker(current_user:User = Depends(get_current_user)):
        if current_user.role == "super_admin":
            return current_user
        if current_user.role not in allowed_roles:
            raise HTTPException(status_code=403, detail="Insufficient permissions")
        return current_user
    return role_checker


# def require_permission(permission: str):
#     def permission_checker(current_user = Depends(get_current_user)):

#         user_permissions = ROLE_PERMISSIONS.get(current_user.role, [])

#         if permission not in user_permissions:
#             raise HTTPException(
#                 status_code=403,
#                 detail="Permission denied"
#             )

#         return current_user

#     return permission_checker

#checking role_checking and permission checking together

def require_role_and_permission(allowed_roles: list, permission: str):
    
    def checker(current_user: User = Depends(get_current_user)):

        # Super admin bypass
        if current_user.is_super_admin:
            return current_user

        # Role check
        if current_user.role not in allowed_roles:
            raise HTTPException(
                status_code=403,
                detail="Role not allowed"
            )

        # Permission check
        user_permissions = ROLE_PERMISSIONS.get(current_user.role, [])

        if permission not in user_permissions:
            raise HTTPException(
                status_code=403,
                detail="Permission denied"
            )

        return current_user

    return checker