import sys
import time
import urllib.parse
import urllib.robotparser
from concurrent.futures import ThreadPoolExecutor

from kearch_common.requester import KearchRequester, RequesterError

CRAWLER_CHILD_HOST = 'sp-crawler-child.kearch.svc.cluster.local'
CRAWLER_CHILD_PORT = 10080

DATABASE_HOST = 'sp-db.kearch.svc.cluster.local'
DATABASE_PORT = 3306

NUM_THREAD = 5

REQUESTER_NAME = 'specialist_crawler_parent'

MAX_URLS = 20

# When you change DEBUG_UNIT_TEST true, this program run unit test.
DEBUG_UNIT_TEST = False


class RobotsChecker:
    def __init__(self):
        self.rpcache = dict()

    def isCrawlable(self, url):
        try:
            parsed = urllib.parse.urlparse(url)
            roboturl = parsed.scheme + '://' + parsed.netloc + '/robots.txt'
            if roboturl in self.rpcache:
                return self.rpcache[roboturl].can_fetch('*', url)
            else:
                rp = urllib.robotparser.RobotFileParser()
                rp.set_url(roboturl)
                rp.read()
                self.rpcache[roboturl] = rp
                return rp.can_fetch('*', url)
        except urllib.error.URLError:
            return False


def crawl_a_page(url):
    print('crawling {} ...'.format(url))

    if DEBUG_UNIT_TEST:
        ret = {
            'url': 'www.google.com',
            'title_words': ['google', 'USA'],
            'summary': 'Google is the biggest IT company.',
            'tfidf': {'google': 1.0},
            'inner_links': ['www.facebook.com'],
            'outer_links': []}
        time.sleep(2)
        return ret
    else:
        crawler_requester = KearchRequester(
            CRAWLER_CHILD_HOST, CRAWLER_CHILD_PORT, REQUESTER_NAME)
        ret = crawler_requester.request(
            path='/crawl_a_page', params={'url': url})
        return ret


# DEBUG CODE: Following lines are for debug. They are codes for unit test.
def get_next_urls_dummy(max_urls):
    urls = []
    for i in range(0, max_urls, 2):
        urls.extend(['www.google.com', 'www.facebook.com'])
    ret = {'urls': urls}
    time.sleep(5)
    return ret


if __name__ == '__main__':
    database_requester = KearchRequester(
        DATABASE_HOST, DATABASE_PORT, REQUESTER_NAME, conn_type='sql')
    robots_checker = RobotsChecker()

    if DEBUG_UNIT_TEST:
        resp = get_next_urls_dummy(MAX_URLS)
    else:
        resp = database_requester.request(
            path='/get_next_urls', params={'max_urls': MAX_URLS})
    urls_in_queue = resp['urls']
    urls_to_push = list()
    data_to_push = list()

    while True:
        if DEBUG_UNIT_TEST:
            sys.stderr.write('length of queue = ' +
                             str(len(urls_in_queue)) + '\n')

        if len(urls_in_queue) == 0:
            if DEBUG_UNIT_TEST:
                # DEBUG CODE: Following lines are for debug.
                # They are codes for unit test.
                resp = get_next_urls_dummy(MAX_URLS)
                urls_in_queue = resp['urls']
            else:
                urls_to_push = list(
                    filter(lambda x: len(x) < 200, urls_to_push))

                try:
                    # push data to database
                    print('pushing {} urls ...'.format(len(urls_to_push)))
                    resp = database_requester.request(
                        path='/push_urls_to_queue', method='POST',
                        payload={'urls': urls_to_push})
                except RequesterError as e:
                    print(e, file=sys.stderr)

                try:
                    print('pushing {} webpages ...'.format(len(data_to_push)))
                    resp = database_requester.request(
                        path='/push_webpage_to_database', method='POST',
                        payload={'data': data_to_push})
                except RequesterError as e:
                    print(e, file=sys.stderr)

                try:
                    # fetch urls from database
                    resp = database_requester.request(
                        path='/get_next_urls', params={'max_urls': MAX_URLS})
                    urls_in_queue = resp['urls']
                except RequesterError as e:
                    print(e, file=sys.stderr)

        with ThreadPoolExecutor(max_workers=NUM_THREAD) as executor:
            urls = list(urls_in_queue[:NUM_THREAD])
            urls = filter(robots_checker.isCrawlable, urls)
            results = executor.map(crawl_a_page, urls)
        results = list(filter(lambda x: x != {}, results))
        for r in results:
            urls_to_push.extend(r['inner_links'])
            urls_to_push.extend(r['outer_links'])
        for r in results:
            d = r
            del d['inner_links']
            del d['outer_links']
            data_to_push.append(d)

        urls_in_queue = urls_in_queue[NUM_THREAD:]
        time.sleep(2)
