import traceback
from celery import states
from crawler import Crawler

from worker import celery_server


@celery_server.task(name='crawler.crawl', bind=True)
def crawl(self, url):
    try:
        self.update_state(state="PROGRESS")
        words = Crawler(url).crawl()
        return words
    except Exception as ex:
        self.update_state(
            state=states.FAILURE,
            meta={
                'exc_type': type(ex).__name__,
                'exc_message': traceback.format_exc().split('\n')
            })
        raise ex
