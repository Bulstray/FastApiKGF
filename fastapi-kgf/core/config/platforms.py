from pydantic import BaseModel


class PlatformConfig(BaseModel):
    etp_gpb: str = "https://new.etpgpb.ru/procedures.rss"
    tek_torg: str = "https://www.tektorg.ru/procedures"
