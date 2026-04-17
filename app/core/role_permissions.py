from app.core.roles import Roles
from app.core.permissions import Permission


ROLE_PERMISSIONS = {
    Roles.SUPER_ADMIN: [
        Permission.CREATE_PROJECT,
        Permission.VIEW_PROJECT,
        Permission.UPDATE_PROJECT,
        Permission.DELETE_PROJECT,
    ],
    Roles.ADMIN: [
        Permission.CREATE_PROJECT,
        Permission.VIEW_PROJECT,
        Permission.UPDATE_PROJECT,
    ],
    Roles.MEMBER: [
        Permission.VIEW_PROJECT
    ]
}