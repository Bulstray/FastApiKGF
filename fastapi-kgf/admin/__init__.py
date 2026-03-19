from sqladmin import Admin

from .user import UserAdmin


def register_admin_views(admin: Admin):
    admin.add_view(UserAdmin)
