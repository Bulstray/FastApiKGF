from pydantic import BaseModel


class ApiV1Prefix(BaseModel):
    prefix: str = "/v1"
    tenders: str = "/tenders"


class ApiPrefix(BaseModel):
    prefix: str = "/api"
    v1: ApiV1Prefix = ApiV1Prefix()
