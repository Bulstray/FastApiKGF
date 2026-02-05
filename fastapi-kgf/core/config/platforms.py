from pydantic import BaseModel


class TenderPlatformConfig(BaseModel):
    etp_gpb: str = "https://new.etpgpb.ru/procedures.rss"
    tek_torg: str = "https://www.tektorg.ru/procedures"
