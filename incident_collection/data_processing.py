import hashlib
from fastapi import Request
from typing import Any

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

    for key, value in sorted(body.model_dump()["body"].items()):
        b.append({"key": key, "value": value})

    return Problem(header=h, body=b)


def insert_data(problem: Problem) -> None:
    collection.insert_one(problem.model_dump())


def find_data(query: dict[str, str]) -> list[Response]:
    search_query: dict[str, list[Any]] = {"$and": []}

    for cnt in range(len(query)):
        search_query["$and"].append({"$or": []})
        key = list(query.items())[cnt][0]
        value = list(query.items())[cnt][1]
        
        search_query["$and"][cnt]["$or"].append({"header": {"$elemMatch": {"key": key, "value": value}}})
        search_query["$and"][cnt]["$or"].append({"body": {"$elemMatch": {"key": key, "value": value}}})

    answer = list(collection.find(search_query))
    result = problem_to_response(answer)

    return result
    
    
def problem_to_response(list_of_answers: list[dict[str, str | list[dict[str, str]]]]) -> list[Response]:
    response: list[Response] = []

    for answer in list_of_answers:
        h = {header_data['key']: header_data['value'] for header_data in answer['header']} # type: ignore
        b = {body_data['key']: body_data['value'] for body_data in answer['body']} # type: ignore
        response.append(Response(header=h, body=b))
    
    return response


def find_data_by_hash(hash_value: str) -> list[Response]:
    answer = list(collection.find({"hash": hash_value}))
    result = problem_to_response(answer)

    return result