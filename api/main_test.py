from fastapi.testclient import TestClient
from main import app
import json

client = TestClient(app)


def test_crawl():
    data = {"url": "https://www.yahoo.com"}
    response = client.post("/crawl", json.dumps(data))
    assert response.status_code == 200


def test_check_crawl_status():
    data = {"url": "https://www.yahoo.com"}
    post_response = client.post("/crawl", json.dumps(data))
    get_response = client.get("/check_crawl_status/{}".format(post_response.json()["id"]))
    assert get_response.json()["task_id"] == post_response.json()["id"]
    assert get_response.json()["status"] in ["STARTED", "SUCCESS"]


def test_health():
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == "OK"

