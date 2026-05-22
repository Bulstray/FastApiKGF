from sqladmin import Admin

from .parser_keyword import ParserKeywordAdmin
from .project import ProjectAdmin
from .user import UserAdmin
from .programs_admin import ProgramAdmin


def register_admin_views(admin: Admin) -> None:
    admin.add_view(UserAdmin)
    admin.add_view(ProjectAdmin)
    admin.add_view(ParserKeywordAdmin)
    admin.add_view(ProgramAdmin)
