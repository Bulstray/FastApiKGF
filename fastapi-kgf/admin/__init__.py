from sqladmin import Admin

from .user import UserAdmin
from .project import ProjectAdmin
from .parser_keyword import ParserKeywordAdmin


def register_admin_views(admin: Admin) -> None:
    admin.add_view(UserAdmin)
    admin.add_view(ProjectAdmin)
    admin.add_view(ParserKeywordAdmin)
