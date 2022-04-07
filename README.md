<h1 align="center">
  Words Counter Crawler
</h1>

<h4 align="center">Distributed web crawler to count to occurrences of words</h4>

<p align="center">
  <a href="#key-features">Key Features</a> •
  <a href="#high-level-design">Design</a> •
  <a href="#documentation">Documentation</a> •
  <a href="#usage">Usage</a> •
  <a href="#testing">Testing</a> •
  <a href="#enhancements">Enhancements</a>
</p>

## Key Features

* Crawling - Crawl any website and count the occurrences of each word
* Distributed - All the heavy work happens in the background by Celery Workers
* Caching using Redis - We don't crawl the same website more than once during small interval

## High Level Design  

<a href="https://drive.google.com/uc?export=view&id=1pD8ZDYwSfn5qxjM-SXPljWHEZHqzS-Hr"><img src="https://drive.google.com/uc?export=view&id=1pD8ZDYwSfn5qxjM-SXPljWHEZHqzS-Hr" style="width: 650px; max-width: 100%; height: auto" title="Click to enlarge picture" />

## Documentation
Visit `http://localhost:8000/docs` for Swagger Documentation

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
docker-compose exec worker pytest .
```

### Test the API
```sh
docker-compose exec fastapi pytest .
```

## Enhancements

* Smart Crawler -> Stream the text instead of downloading it.
* Better Mocks in tests and better test coverage.
