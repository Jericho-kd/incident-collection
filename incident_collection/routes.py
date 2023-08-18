import hashlib
# import bencodepy
from fastapi import APIRouter, Depends
from pydantic import BaseModel, validator



router = APIRouter()

class Problem(BaseModel):
    header: dict[str, str]
    body: dict[str, str]

    @validator('header', 'body', pre=True)
    def sort_header(cls, value: dict[str, str]):
        return {k: value[k] for k in sorted(value)}


@router.post("/problems")
async def create_problem(problem: Problem) -> dict[str, str|Problem]:
    # Convert json to bencode
    # json_to_bencode = bencodepy.encode(problem.model_dump_json())
    # Get hash of data
    # data_hash = hashlib.sha256(json_to_bencode).hexdigest()
    data_hash = hashlib.sha256(problem.model_dump_json().encode()).hexdigest()

    # Сохраняем данные в базу данных
    # database.append({"hash": data_hash, "header": problem.header, "body": problem.body})

    return {"problem": problem, "hash": data_hash}


@router.post("/find")
async def find_problems(query: dict[str, str]):
    results = []

    # Ищем записи, удовлетворяющие запросу
    # for item in database:
    #     if query.items() <= item["header"].items() or query.items() <= item["body"].items():
    #         results.append(item)

    return results


@router.get("/find2")
async def find_problems_by_hash(h: int):
    results = []

    # Ищем записи с указанным хэшем
    # for item in database:
    #     if item["hash"] == h:
    #         results.append(item)

    return results