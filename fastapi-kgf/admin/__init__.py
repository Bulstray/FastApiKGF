from sqladmin import Admin

from .user import UserAdmin
from .project import ProjectAdmin


def register_admin_views(admin: Admin) -> None:
    admin.add_view(UserAdmin)
    admin.add_view(ProjectAdmin)
