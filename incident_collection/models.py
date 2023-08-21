from pydantic import BaseModel


class Body(BaseModel):
    body: dict[str, str]


class Problem(BaseModel):
    header: list[dict[str, str]]
    body: list[dict[str, str]]
    hash: str | None = None


class Response(BaseModel):
    header: dict[str, str]
    body: dict[str, str]