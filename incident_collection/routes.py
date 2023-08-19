import hashlib
from fastapi import APIRouter, Request
from pydantic import BaseModel, Field, validator
from pymongo.collection import Collection
from database import db


router = APIRouter()

class Problem(BaseModel):
    header: list[dict[str, str]] | None = Field(None)
    body: list[dict[str, str]]
    hash: list[dict[str, str]] | None = Field(None)

    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "body": [
                        {"key": "name1", "value": "value1"},
                        {"key": "name2", "value": "value2"},
                        {"key": "name3", "value": "value3"}
                    ]
                }
            ]
        }
    }

    # @validator('body', pre=True)
    # def sort_header(cls, values: list[dict[str, str]]):
    #     return sorted(values, key=lambda x: x['key']) 
        # return {k: value[k] for k in sorted(value)}
    

collection: Collection[Problem] = db.incidents


@router.post("/problems")
async def create_problem(problem: Problem, request: Request) -> dict[str, str]:
    headers: list[dict[str, str]] = []
    hashes: list[dict[str, str]] = []

    for header in request.headers.items():
        headers.append({"key": header[0], "value": header[1]})
    

    problem.header = headers
    problem.hash = hashes
    problem.body.sort(key=lambda x: x['key'])
    problem.header.sort(key=lambda x: x['key'])

    # Get hash of data
    data_hash = hashlib.sha256(problem.model_dump_json().encode()).hexdigest()
    # print(request.headers)

    hashes.append({"key": "hash", "value": data_hash})
    # Save data to mongodb
    collection.insert_one(problem.dict())

    return {"hash": data_hash}



@router.post("/find")
async def find_problems(query: dict[str, str]) -> dict[str, str]:
    cursor = collection.find({
        "$and": [
        {"$or": [
            {"header": {"$elemMatch": {"key": "host", "value": "localhost:8080"}}},
            {"body": {"$elemMatch": {"key": "host", "value": "localhost:8080"}}}
        ]},
        {"$or": [
            {"header": {"$elemMatch": {"key": "name1", "value": "value1"}}},
            {"body": {"$elemMatch": {"key": "name1", "value": "value1"}}}
        ]}
    ]
    })

    return {"result": "ok"}


@router.get("/find2")
async def find_problems_by_hash(h: str) -> dict[str, list[Problem]]:
    result = list(collection.find({"hash": h}))

    return {"incidents": result}
