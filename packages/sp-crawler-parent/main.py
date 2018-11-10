import sys
import time
import urllib.parse
import urllib.robotparser
import ssl
from concurrent.futures import ThreadPoolExecutor

from kearch_common.requester import KearchRequester, RequesterError

CRAWLER_CHILD_HOST = 'sp-crawler-child.kearch.svc.cluster.local'
CRAWLER_CHILD_PORT = 10080

DATABASE_HOST = 'sp-db.kearch.svc.cluster.local'
DATABASE_PORT = 3306

ELASTIC_HOST = 'sp-es.kearch.svc.cluster.local'
ELASTIC_PORT = 9200
ELASTIC_INDEX = 'sp'
ELASTIC_TYPE = 'webpage'

NUM_THREAD = 10
SP_CHILD_TIMEOUT = 300

REQUESTER_NAME = 'specialist_crawler_parent'

MAX_URLS = 20

NUM_OF_WORDS_FOR_DUMP = 100

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
        except ssl.CertificateError:
            return False
        except ConnectionResetError:
            return False
        except UnicodeDecodeError:
            return False


def crawl_a_page(url):
    if DEBUG_UNIT_TEST:
        ret = {
            'url': 'www.google.com',
            'title': 'Google is the biggest IT company.',
            'text': 'hello world!',
            'inner_links': ['www.facebook.com'],
            'outer_links': []}
        time.sleep(2)
        return ret
    else:
        crawler_requester = KearchRequester(
            CRAWLER_CHILD_HOST, CRAWLER_CHILD_PORT, REQUESTER_NAME)
        try:
            print('requesting   /crawl_a_page?url={} ...'.format(url))
            ret = crawler_requester.request(
                path='/crawl_a_page', params={'url': url}, timeout=SP_CHILD_TIMEOUT)
            print('get response /crawl_a_page?url={}'.format(url))
        except RequesterError as e:
            print(e, file=sys.stderr)
            ret = {}
        return ret


# DEBUG CODE: Following lines are for debug. They are codes for unit test.
def get_next_urls_dummy(max_urls):
    urls = []
    for i in range(0, max_urls, 2):
        urls.extend(['www.google.com', 'www.facebook.com'])
    ret = {'urls': urls}
    time.sleep(5)
    return ret


def exclude_deeper_link(original, derives):
    res = list()
    for d in derives:
        original_parsed = urllib.parse.urlparse(original)
        derived_parsed = urllib.parse.urlparse(d)
        if original_parsed.path.count('/') >= derived_parsed.path.count('/'):
            res.append(d)
    return res


if __name__ == '__main__':
    database_requester = KearchRequester(
        DATABASE_HOST, DATABASE_PORT, REQUESTER_NAME, conn_type='sql')
    elastic_requester = KearchRequester(
        ELASTIC_HOST, ELASTIC_PORT, REQUESTER_NAME, conn_type='elastic')
    robots_checker = RobotsChecker()

    if DEBUG_UNIT_TEST:
        resp = get_next_urls_dummy(MAX_URLS)
    else:
        resp = database_requester.request(
            path='/get_next_urls', params={'max_urls': MAX_URLS})
    urls_in_queue = resp['urls']
    urls_to_push = list()
    data_to_push = list()
    dump_to_push = dict()

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
                urls_to_push = list()

                try:
                    print('pushing {} dumps ...'.format(len(dump_to_push)))
                    resp = database_requester.request(
                        path='/update_dump', method='POST',
                        payload={'data': dump_to_push})
                except RequesterError as e:
                    print(e, file=sys.stderr)
                dump_to_push = dict()

                print('pushing {} crawled urls'.format(len(data_to_push)))
                crawled_url = list()
                for d in data_to_push:
                    crawled_url.append({'url': d['url']})
                try:
                    resp = database_requester.request(
                        path='/push_crawled_urls', method='POST',
                        payload={'data': crawled_url})
                except RequesterError as e:
                    print(e, file=sys.stderr)

                print('pushing {} webpages ...'.format(len(data_to_push)))
                for d in data_to_push:
                    try:
                        resp = elastic_requester.request(
                            path='/' + ELASTIC_INDEX + '/' + ELASTIC_TYPE + '/',
                            method='POST', payload=d)
                        print('resp = ', resp)
                    except RequesterError as e:
                        print(e, file=sys.stderr)
                data_to_push = list()

                try:
                    # fetch urls from database
                    resp = database_requester.request(
                        path='/get_next_urls', params={'max_urls': MAX_URLS})
                    urls_in_queue = resp['urls']
                except RequesterError as e:
                    print(e, file=sys.stderr)

        with ThreadPoolExecutor(max_workers=NUM_THREAD) as executor:
            urls = list(urls_in_queue[:NUM_THREAD])
            urls = list(filter(bool, urls))
            print('after filter bool', urls, file=sys.stderr)
            urls = list(filter(robots_checker.isCrawlable, urls))
            print('after filter isCrawlable', urls, file=sys.stderr)
            results = executor.map(crawl_a_page, urls)
        results = list(filter(lambda x: x != {}, results))
        for r in results:
            urls_to_push.extend(exclude_deeper_link(
                r['url'], r['inner_links']))
            urls_to_push.extend(r['outer_links'])
        for r in results:
            data_to_push.append(
                {'url': r['url'], 'title': r['title'], 'text': r['text']})
        for r in results:
            tfidf = list(r['tfidf'].items())
            tfidf.sort(key=lambda x: x[1], reverse=True)
            for t in tfidf[:NUM_OF_WORDS_FOR_DUMP]:
                if t[0] in dump_to_push:
                    dump_to_push[t[0]] += 1
                else:
                    dump_to_push[t[0]] = 1

        urls_in_queue = urls_in_queue[NUM_THREAD:]
        time.sleep(2)
