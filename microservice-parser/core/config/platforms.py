from pydantic import BaseModel


class BasePlatform(BaseModel):
    base_tek_torg: str = "https://www.tektorg.ru"
    base_etp_gpb: str = "https://new.etpgpb.ru"
    base_sber: str = "https://www.sberbank-ast.ru/Default.aspx"
    base_lukh: str = (
        "https://lukoil.ru/Company/Tendersandauctions/Tenders/TendersofLukoilgroup"
    )


class PlatformPrefixProcedures(BaseModel):
    etp_gpb: str = "/procedures"
    tek_torg: str = "/procedures"


class PlatformConfig(BaseModel):
    base_platform: BasePlatform = BasePlatform()
    platform_prefix_procedures: PlatformPrefixProcedures = (
        PlatformPrefixProcedures()
    )

    @property
    def tek_torg(self) -> str:
        return (
            f"{self.base_platform.base_tek_torg}"
            f"{self.platform_prefix_procedures.tek_torg}"
        )

    @property
    def etp_gpb(self) -> str:
        return (
            f"{self.base_platform.base_etp_gpb}"
            f"{self.platform_prefix_procedures.etp_gpb}"
        )

    @property
    def sber(self) -> str:
        return self.base_platform.base_sber

    @property
    def lukh(self) -> str:
        return self.base_platform.base_lukh
