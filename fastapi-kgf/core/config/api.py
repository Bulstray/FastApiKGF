from pydantic import BaseModel


class ApiV1Config(BaseModel):
    prefix: str = "/v1"
    programs: str = "/programs"
    users: str = "/users"
    auth: str = "/auth"


class ApiConfig(BaseModel):
    prefix: str = "/api"
    v1: ApiV1Config = ApiV1Config()

    @property
    def bearer_token_url(self) -> str:
        parts = (self.prefix, self.v1.prefix, self.v1.auth, "/login")
        path = "".join(parts)
        return path.removeprefix("/")
