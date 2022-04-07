import json
from fastapi import FastAPI, Body, Response
from worker import celery_server
from enum import Enum
from fastapi_redis_cache import FastApiRedisCache, cache
import os


class SortOptions(str, Enum):
    COUNT = "count"
    ALPHABETICALLY = "alphabetically"


app = FastAPI()


@app.on_event("startup")
def startup():
    redis_cache = FastApiRedisCache()
    redis_cache.init(
        host_url=os.getenv("REDISSERVER", "redis://redis_server:6379"),
        prefix="myapi-cache",
        response_header="X-MyAPI-Cache",
        ignore_arg_types=[Response]
    )


@app.post("/crawl")
@cache(expire=30)
async def crawl(payload: dict = Body(...)):
    task_name = "crawler.crawl"
    task = celery_server.send_task(task_name, args=[payload["url"]])
    return dict(id=task.id, url='localhost:8000/check_crawl_status/{}'.format(task.id))


@app.get("/check_crawl_status/{task_id}")
async def check_task(task_id: str, sort: SortOptions = "count"):
    task = celery_server.AsyncResult(task_id)
    if task.state == 'SUCCESS':
        sorted_words = await sort_words(sort, task.result)
        response = {
            'status': task.state,
            'result': sorted_words,
            'task_id': task_id
        }
    elif task.state == 'FAILURE':
        response = json.loads(task.backend.get(task.backend.get_key_for_task(task.id)).decode('utf-8'))
        del response['children']
        del response['traceback']
    else:
        response = {
            'status': task.state,
            'task_id': task_id
        }
    return response


@app.get("/health")
def health():
    return "OK"


async def sort_words(sort_option, words):
    sorted_dict = {}
    if sort_option == "count":
        sorted_keys = sorted(words, key=words.get, reverse=True)
    else:
        sorted_keys = sorted(words.keys(), key=lambda x: x.lower())
    for w in sorted_keys:
        sorted_dict[w] = words[w]
    return sorted_dict
