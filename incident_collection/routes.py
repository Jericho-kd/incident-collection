from fastapi import APIRouter, Request

from data_processing import compute_hash, find_data, find_entries_by_hash
from models import Body, Response


router = APIRouter(tags=["Items"])
   
@router.post("/problems")
async def create_problem(body: Body, request: Request) -> dict[str, str]:
    result = compute_hash(body, request)

    return {"hash": result}


@router.post("/find")
async def find_problems(query: dict[str, str]) -> dict[str, list[Response]]:
    result = find_data(query)

    return {"result": result}


@router.get("/find2")
async def find_problems_by_hash(h: str) -> dict[str, list[Response]]:
    result = find_entries_by_hash(h)

    return {"result": result}