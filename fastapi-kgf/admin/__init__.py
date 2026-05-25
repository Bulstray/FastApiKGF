from sqladmin import Admin

from .parser_keyword import ParserKeywordAdmin
from .programs_admin import ProgramAdmin
from .project import ProjectAdmin
from .user import UserAdmin


def register_admin_views(admin: Admin) -> None:
    admin.add_view(UserAdmin)
    admin.add_view(ProjectAdmin)
    admin.add_view(ParserKeywordAdmin)
    admin.add_view(ProgramAdmin)
