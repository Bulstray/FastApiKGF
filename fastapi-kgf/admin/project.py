from sqladmin import ModelView
from core.models import Project


class ProjectAdmin(ModelView, model=Project):
    column_list = [Project.name]
    form_columns = [Project.name]
