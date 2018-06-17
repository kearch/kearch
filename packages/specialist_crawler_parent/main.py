from kearch_common.connection import KearchRequester
from concurrent.futures import ThreadPoolExecutor
from urllib.parse import quote


CRAWLER_CHILD_IP = '192.168.11.10'
CRAWLER_CHILD_PORT = 10080

DATABASE_IP = '192.168.11.11'
DATABASE_PORT = 10080

NUM_THREAD = 5

REQUESTER_NAME = 'specialist_crawler_parent'


def crawl_a_page(url):
    crawler_requester = KearchRequester(CRAWLER_CHILD_IP, CRAWLER_CHILD_PORT, REQUESTER_NAME)
    ret = crawler_requester.request({'url': quote(url)}, '/crawl_a_page')
    return ret


if __name__ == '__main__':
    database_requester = KearchRequester(DATABASE_IP, DATABASE_PORT, REQUESTER_NAME)

    next_urls = database_requester.request({'max_urls': 100}, 'api/get_next_urls')
    # TODO (kawata) some process to extract url list from next_urls variable.

    while True:
        if len(next_urls) == 0:
            next_urls = database_requester.request({'max_urls': 100}, 'api/get_next_urls')

            with ThreadPoolExecutor(max_workers=NUM_THREAD, thread_name_prefix="thread") as executor:
                results = executor.map(crawl_a_page, next_urls[:10])

            next_urls = next_urls[10:]
