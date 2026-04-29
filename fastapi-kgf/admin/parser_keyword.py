from sqladmin import ModelView

from core.models import ParsingKeyword


class ParserKeywordAdmin(ModelView, model=ParsingKeyword):
    column_list = [
        ParsingKeyword.decoding,
        ParsingKeyword.keyword,
    ]
    form_columns = [
        ParsingKeyword.decoding,
        ParsingKeyword.keyword,
    ]
