import time
import json
from locust import HttpUser, task, between


class Test(HttpUser):
    wait_time = between(1, 3)

    @task(1)
    def test_crawl(self):
        load = {"url": "https://www.bbc.com"}
        headers = {'Content-Type': 'application/json', 'Accept': 'application/json'}
        self.client.post("/crawl", data=json.dumps(load), headers=headers)
