from pydantic import BaseModel


class BasePlatform(BaseModel):
    base_tek_torg: str = "https://www.tektorg.ru"
    base_etp_gpb: str = "https://new.etpgpb.ru"


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
        return f"{self.base_platform.base_tek_torg}{self.platform_prefix_procedures.tek_torg}"

    @property
    def etp_gpb(self) -> str:
        return f"{self.base_platform.base_etp_gpb}{self.platform_prefix_procedures.etp_gpb}"
