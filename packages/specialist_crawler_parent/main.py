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
    ret = crawler_requester.request(path='/crawl_a_page', param={'url': quote(url)})
    return ret


if __name__ == '__main__':
    database_requester = KearchRequester(DATABASE_IP, DATABASE_PORT, REQUESTER_NAME)

    urls_in_queue = database_requester.request(path='api/get_next_urls', param={'max_urls': 100})
    # TODO (kawata) some process to extract url list from urls_in_queue variable.
    links_to_push = list()
    datum_to_push = list()

    while True:
        if len(urls_in_queue) == 0:
            # push datum to database
            database_requester.request(path='api/push_links_to_queue', method='POST', payload={'links': links_to_push})
            database_requester.request(path='api/push_webpage_to_database', method='POST', payload={'datum': datum_to_push})

            # fetch urls from database
            urls_in_queue = database_requester.request(path='api/get_next_urls', param={'max_urls': 100})

        with ThreadPoolExecutor(max_workers=NUM_THREAD, thread_name_prefix="thread") as executor:
            results = executor.map(crawl_a_page, urls_in_queue[:10])

        for r in results:
            links_to_push.extend(r.inner_links)
            links_to_push.extend(r.outer_links)
        for r in results:
            d = r
            del d['inner_links']
            del d['outer_links']
            datum_to_push.append(d)

        urls_in_queue = urls_in_queue[10:]
