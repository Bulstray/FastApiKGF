from pydantic import BaseModel


class ApiV1Config(BaseModel):
    prefix: str = "/v1"
    programs: str = "/programs"
    users: str = "/users"


class ApiConfig(BaseModel):
    prefix: str = "/api"
    v1: ApiV1Config = ApiV1Config()
