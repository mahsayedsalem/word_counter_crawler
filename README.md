![Unit Tests](https://github.com/mahsayedsalem/word_counter_crawler/actions/workflows/test.yml/badge.svg)

<h1 align="center">
  Words Counter Crawler
</h1>

<h4 align="center">Distributed web crawler to count to occurrences of words</h4>

<p align="center">
  <a href="#key-features">Key Features</a> •
  <a href="#high-level-design">Design</a> •
  <a href="#stack-decisions">Stack Decisions</a> •
  <a href="#documentation">Documentation</a> •
  <a href="#usage">Usage</a> •
  <a href="#testing">Testing</a> •
  <a href="#load-testing">Load Testing</a> •
  <a href="#tasks-monitoring">Tasks Monitoring</a> •
  <a href="#continuous-integration">Continuous Integration</a> •
  <a href="#enhancements">Enhancements</a>
</p>

## Key Features

* Crawling 🕸️ - Crawl any website and count the occurrences of each word.
* Distributed  🚀 - All the heavy work happens in the background by Celery Workers.
* Caching using Redis 🏪 - We don't crawl the same website more than once during small interval.

## High Level Design  

![ScreenShot](/images/crawler_background.png)

## Stack Decisions 
* FastAPI: Reliable async web server with built-in documentation.
* Celery: Reliable Distributed Task Queue to make sure the solution is scalable when needed.
* Separate the API from the Execution. This way we can scale our workers independently away from the APIs.
* Use Caching to make sure not to scrap the same URL within small interval of time.
* Use Redis to store the workers results since the default timeout is 24 hours, and we don't need to persist the word count for more than that since it's always changing.

## Documentation
```sh
$ sh local_env_up.sh 
```
Then visit `http://localhost:8000/docs` for Swagger Documentation

## Usage

### Start the services
```sh
$ sh local_env_up.sh 
```

### Content of local_env_up.sh
```sh
$ sudo docker-compose -f docker-compose.yml up --scale worker=2 --build
```

### Stop the services

```sh
$ sh local_env_down.sh 
```

### POST a Crawl Request

```sh
$ curl --location --request POST 'http://localhost:8000/crawl' \
--header 'Content-Type: application/json' \
--data-raw '{
    "url": "https://www.bbc.com"
}'
```

### POST a Crawl Response Example
```sh
{
    "id": "8b1766b4-6dc1-4f3d-bc6f-426066edc46f",
    "url": "localhost:8000/check_crawl_status/8b1766b4-6dc1-4f3d-bc6f-426066edc46f"
}
```

### Get Crawl Status Example

```sh
$ curl --location --request \ 
GET 'localhost:8000/check_crawl_status/8b1766b4-6dc1-4f3d-bc6f-426066edc46f'
```

### POST a Crawl Response Example
```sh
{
    "status": "SUCCESS",
    "result": {
        "the": 54,
        "to": 46,
        "in": 22,
        "of": 21,
        ..,
        ..,
        },
    "task_id": "b4035abd-f58f-4ab9-90bb-ebad535869d4"
}
```
The default is to get the words sorted by occurrences. Use `sort` parameter to specify if you want it sorted alphabetically

for example:

```sh
$ curl --location --request \ 
GET 'localhost:8000/check_crawl_status/8b1766b4-6dc1-4f3d-bc6f-426066edc46f?sort=alphabetically'
```

## Testing

### Test the Worker
```sh
$ docker-compose exec worker pytest .
```

### Test the API
```sh
$ docker-compose exec fastapi pytest .
```

## Load Testing
I use `locust` for load testing. 
```sh
$ pip install locust 
```

```sh
$ locust -f load_test.py 
```
 
<a href="https://drive.google.com/uc?export=view&id=1vhiYi7gwIr5mHn3c_-DKY1fl2CqhnwtE"><img src="https://drive.google.com/uc?export=view&id=1vhiYi7gwIr5mHn3c_-DKY1fl2CqhnwtE" style="width: 650px; max-width: 100%; height: auto" title="Click to enlarge picture" /></a>

## Tasks Monitoring

Monitor the tasks and workers using Flower Dashboard from `http://localhost:5555/dashboard`

<a href="https://drive.google.com/uc?export=view&id=1rOlMVErs_sy2HseNJgR9TZ7bI_NSDPb2"><img src="https://drive.google.com/uc?export=view&id=1rOlMVErs_sy2HseNJgR9TZ7bI_NSDPb2" style="width: 650px; max-width: 100%; height: auto" title="Click to enlarge picture" />

<a href="https://drive.google.com/uc?export=view&id=1CGbZtQa71KUqUUnbX4BKO3Dn4thpjvW6"><img src="https://drive.google.com/uc?export=view&id=1CGbZtQa71KUqUUnbX4BKO3Dn4thpjvW6" style="width: 650px; max-width: 100%; height: auto" title="Click to enlarge picture" />



## Continuous Integration

Basic CI is integrated to the repo using Github Actions to run test cases on PRs and Master merges.

## Enhancements

* Smart Crawler: Stream the text instead of downloading it.
* Better Mocks in tests and better test coverage.
* Continuous Delivery Action to publish the docker images to a docker registry.
