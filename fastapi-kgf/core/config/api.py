from pydantic import BaseModel


class ApiV1Config(BaseModel):
    prefix: str = "/v1"
    programs: str = "/programs"
    users: str = "/users"
    auth: str = "/auth"


class ApiConfig(BaseModel):
    prefix: str = "/api"
    v1: ApiV1Config = ApiV1Config()
