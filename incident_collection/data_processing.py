import hashlib
from fastapi import Request

from database import collection
from models import Body, Problem, Response


def compute_hash(body: Body, request: Request) -> str:
    problem: Problem = request_to_problem(body, request)

    data_hash = hashlib.sha256(problem.model_dump_json().encode()).hexdigest()
    problem.hash = data_hash
    insert_data(problem)

    return data_hash


def request_to_problem(body: Body, request: Request) -> Problem:
    h: list[dict[str, str]] = []
    b: list[dict[str, str]] = []

    for header in sorted(request.headers.items()):
        h.append({"key": header[0], "value": header[1]})

    for element in sorted(body.model_dump().values()):
        for key, value in sorted(element.items()):
            b.append({"key": key, "value": value})

    return Problem(header=h, body=b)


def insert_data(problem: Problem) -> None:
    collection.insert_one(problem.model_dump())
    

    
    
