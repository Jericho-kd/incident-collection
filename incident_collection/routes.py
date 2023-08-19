import hashlib
# import bencodepy
from fastapi import APIRouter, Depends, Request
from pydantic import BaseModel, Field, validator
from pymongo.collection import Collection
from pymongo.cursor import Cursor
from bson.son import SON
from database import db


router = APIRouter()

class Problem(BaseModel):
    header: dict[str, str] | None = Field(None)
    body: dict[str, str]
    hash: str | None = Field(None)

    @validator('header', 'body', pre=True)
    def sort_header(cls, value: dict[str, str]):
        return {k: value[k] for k in sorted(value)}
    

collection: Collection[Problem] = db.incidents


@router.post("/problems")
async def create_problem(problem: Problem, request: Request) -> dict[str, str]:
    # Get hash of data
    data_hash = hashlib.sha256(problem.model_dump_json().encode()).hexdigest()
    problem.header = dict(request.headers)
    problem.hash = data_hash

    # Save data to mongodb
    collection.insert_one(problem.dict())

    return {"hash": data_hash}


@router.post("/find")
async def find_problems(query: dict[str, str]) -> dict[str, str]:
    cursor = collection.find({"body.hello": "world"})
    
    print(list(cursor))

    return {"result": "ok"}


@router.get("/find2")
async def find_problems_by_hash(h: str) -> dict[str, list[Problem]]:
    result = list(collection.find({"hash": h}))

    return {"incidents": result}
