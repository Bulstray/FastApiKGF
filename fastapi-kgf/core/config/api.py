from pydantic import BaseModel


class ApiV1Config(BaseModel):
    prefix: str = "/v1"
    programs: str = "/programs"


class ApiConfig(BaseModel):
    prefix: str = "/api"
    v1: ApiV1Config = ApiV1Config()
