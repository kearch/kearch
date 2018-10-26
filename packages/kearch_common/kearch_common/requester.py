from datetime import datetime
import json
import sys
import traceback
import urllib

import mysql.connector
import requests

from kearch_common.data_format import wrap_json


MAX_WORD_LEN = 200


class RequesterError(Exception):
    def __init__(self, message='This is default messege'):
        self.message = 'RequesterError: ' + message


def get_has_overlap_statement(queries):
    # TODO(gky360): escape words
    json_contains_funcs = map(
        lambda w: 'JSON_CONTAINS(`title_words`, \'"{}"\')'.format(w),
        queries)
    return ' OR '.join(json_contains_funcs)


def get_tfidf_sum_statement(queries):
    # TODO(gky360): escape words
    tfidfs = map(
        lambda w: '`tfidf`->>\'$.{}\''.format(w),
        queries)
    return ' + '.join(tfidfs)


def post_webpage_to_db(db, cur, webpage):
    statement = """
    INSERT INTO `webpages`
    (`url`, `title`, `summary`)
    VALUES (%s, %s, %s)
    ON DUPLICATE KEY UPDATE `title` = VALUES(`title`), `summary` = VALUES(`summary`)
    """
    cur.execute(statement,
                (webpage['url'], webpage['title'], webpage['summary']))
    db.commit()

    statement = """
    SELECT `id` FROM `webpages` WHERE `url` = %s LIMIT 1
    """
    cur.execute(statement, (webpage['url'],))
    row = cur.fetchone()
    webpage_id = row[0]

    statement = """
    INSERT IGNORE INTO `words`
    (`str`)
    VALUES (%s)
    """
    words = list(webpage['tfidf']) + webpage['title_words']
    word_records = map(lambda w: (w,),
                       filter(lambda w: len(w) < MAX_WORD_LEN, words))
    cur.executemany(statement, word_records)
    db.commit()

    statement = """
    INSERT IGNORE INTO `title_words`
    (`webpage_id`, `word_id`)
    SELECT %s, `words`.`id` FROM `words` WHERE `str` = %s LIMIT 1
    """
    title_word_records = map(lambda w: (webpage_id, w), webpage['title_words'])
    for record in title_word_records:
        cur.execute(statement, record)
    db.commit()

    statement = """
    INSERT INTO `tfidfs`
    (`webpage_id`, `word_id`, `value`)
    SELECT %s, `words`.`id`, %s FROM `words` WHERE `str` = %s LIMIT 1
    ON DUPLICATE KEY UPDATE `value` = VALUES(`value`)
    """
    tfidfs_records = map(lambda w: (
        webpage_id, webpage['tfidf'][w], w), webpage['tfidf'].keys())
    for record in tfidfs_records:
        cur.execute(statement, record)
    db.commit()


def dump_summary_form_sp_db(cur):
    page_size = 1000
    statement = """
    SELECT `id`, `word`, `frequency`
    FROM `summary`
    WHERE `id` > %s
    LIMIT %s
    """

    sp_summary = {}
    prev_rowcount = -1
    last_word_id = 0
    while prev_rowcount != 0:
        print('Dumping words word_id >', last_word_id, '...',
              file=sys.stderr, flush=True)
        cur.execute(statement, (last_word_id, page_size))
        for row in cur.fetchall():
            last_word_id = row[0]
            word = row[1]
            cnt = row[2]
            sp_summary[word] = cnt
        prev_rowcount = cur.rowcount
    return sp_summary


class KearchRequester(object):
    """Interface for communicating between containers or servers."""

    def __init__(self,
                 host='localhost', port=None,
                 requester_name='', conn_type='json'):
        super(KearchRequester, self).__init__()
        self.host = host
        self.port = port
        self.conn_type = conn_type
        self.requester_name = requester_name

    def __repr__(self):
        return '<KearchRequester host: {}, port: {}, conn_type: {}>'.\
            format(self.host, self.port, self.conn_type)

    def request(self, path='', method='GET',
                params=None, payload=None,
                headers=None, timeout=None):
        result = None
        try:
            if self.conn_type == 'json':
                result = self.request_json(path, method, params, payload,
                                           headers, timeout)
            elif self.conn_type == 'sql':
                result = self.request_sql(path, method, params, payload,
                                          headers, timeout)
            elif self.conn_type == 'elastic':
                result = self.request_elastic(path, method, params, payload,
                                              headers, timeout)
            else:
                raise ValueError('conn_type should be "json", "elastic" or "sql".')
        except e:
            print(traceback.format_exc(), file=sys.stderr)
            raise RequesterError('at {}\n{}'.format(parsed_path, e))

        return result

    def request_json(self, path='', method='GET',
                     params=None, payload=None,
                     headers=None, timeout=None):
        if self.port is None:
            url = urllib.parse.urljoin(self.host, path)
        else:
            url = urllib.parse.urljoin(
                'http://{}:{}'.format(self.host, self.port), path)

        if method == 'GET':
            # GET の場合は payload を url param にする
            resp = requests.get(url, params=params, timeout=timeout)
        else:
            # GET 以外は json に payload を含めて送る
            meta = {
                'requester': self.requester_name,
            }
            data = wrap_json(payload, meta)
            resp = requests.request(
                method, url, params=params, json=data, timeout=timeout)

        return resp.json()

    def request_elastic(self, path='', method='GET',
                        params=None, payload=None,
                        headers=None, timeout=None):
        if self.port is None:
            url = urllib.parse.urljoin(self.host, path)
        else:
            url = urllib.parse.urljoin(
                'http://{}:{}'.format(self.host, self.port), path)

        if method == 'GET':
            # GET の場合は payload を url param にする
            resp = requests.get(url, params=params, timeout=timeout)
        else:
            # In the other cases, send the payload just as it is.
            resp = requests.request(
                method, url, params=params, json=payload, timeout=timeout)

        return resp.json()

    def request_sql(self, path='', method='GET',
                    params=None, payload=None,
                    headers=None, timeout=None):

        parsed = urllib.parse.urlparse(path)
        parsed_path = parsed.path
        db_name = ''
        if parsed_path in ['/add_new_sp_server', '/retrieve_sp_servers']:
            db_name = 'kearch_me_dev'
        else:
            db_name = 'kearch_sp_dev'
        config = {
            'host': self.host,
            'database': db_name,
            'user': 'root',
            'password': 'password',
            'charset': 'utf8',
            'use_unicode': True,
            'get_warnings': True,
        }

        db = mysql.connector.Connect(**config)
        cur = db.cursor()
        ret = None

        try:
            if parsed_path == '/push_webpage_to_database':
                for webpage in payload['data']:
                    post_webpage_to_db(db, cur, webpage)
                ret = len(payload['data'])
            elif parsed_path == '/push_crawled_urls':
                now = datetime.now()
                url_queue_records = map(
                    lambda w: (w['url'], now), payload['data'])
                statement = """
                INSERT INTO `url_queue`
                (`url`, `crawled_at`)
                VALUES (%s, %s)
                ON DUPLICATE KEY UPDATE `crawled_at` = VALUES(`crawled_at`)
                """

                cur.executemany(statement, url_queue_records)
                db.commit()
                ret = cur.rowcount
            elif parsed_path == '/get_next_urls':
                max_urls = int(params['max_urls'])
                select_statement = """
                SELECT `url` FROM `url_queue`
                WHERE `crawled_at` IS NULL
                ORDER BY `updated_at`
                LIMIT %s
                """
                delete_statement = """
                DELETE FROM `url_queue`
                WHERE `crawled_at` IS NULL
                ORDER BY `updated_at`
                LIMIT %s
                """

                cur.execute(select_statement, (max_urls,))
                result_urls = [row[0] for row in cur.fetchall()]
                ret = {
                    'urls': result_urls
                }
                cur.execute(delete_statement, (max_urls,))
                db.commit()
            elif parsed_path == '/push_urls_to_queue':
                url_queue_records = [(url,) for url in payload['urls']]
                statement = """
                INSERT IGNORE INTO `url_queue` (`url`) VALUES (%s);
                """

                cur.executemany(statement, url_queue_records)
                db.commit()
                ret = cur.rowcount
            elif parsed_path == '/retrieve_webpages':
                queries = params['queries']
                max_urls = int(params['max_urls'])

                statement = """
                SELECT `webpages`.`id`, `url`, `title`, `summary`, SUM(`value`) AS `score`
                FROM `words`
                JOIN `tfidfs` ON `words`.`id` = `tfidfs`.`word_id`
                JOIN `webpages` ON `tfidfs`.`webpage_id` = `webpages`.`id`
                WHERE `words`.`str` IN ({})
                GROUP BY `webpages`.`id`
                ORDER BY `score` DESC
                LIMIT %s;
                """.format(','.join(['%s'] * len(queries)))
                cur.execute(statement, tuple(queries) + (max_urls,))
                result_webpages = [{
                    'id': row[0],
                    'url': row[1],
                    'title': row[2],
                    'summary': row[3],
                    'score': row[4],
                } for row in cur.fetchall()]

                ret = {
                    'data': result_webpages
                }
            elif parsed_path == '/dump_database':
                ret = dump_summary_form_sp_db(cur)
            elif parsed_path == '/update_dump':
                summary_records = [(word, freq)
                                   for word, freq in payload['data'].items()]
                statement = """
                INSERT INTO `summary`
                (`word`, `frequency`)
                VALUES (%s, %s)
                ON DUPLICATE KEY UPDATE `frequency` = `frequency` + VALUES(`frequency`)
                """
                cur.executemany(statement, summary_records)
                db.commit()
                ret = cur.rowcount
            elif parsed_path == '/retrieve_sp_servers':
                queries = params['queries']

                format_strings = ','.join(['%s'] * len(queries))
                statement = """
                SELECT `word`, `host`, `frequency` FROM `sp_servers`
                WHERE `word` IN ({:s})
                """.format(format_strings)

                cur.execute(statement, tuple(queries))

                ret = {}
                for row in cur.fetchall():
                    word, host, freq = row[0], row[1], row[2]
                    if not word in ret:
                        ret[word] = {}
                    ret[word][host] = freq
            elif parsed_path == '/add_new_sp_server':
                sp_host = payload['host']
                summary = payload['summary']
                sp_server_records = [(word, sp_host, frequency)
                                     for word, frequency in summary.items()
                                     if len(word) <= MAX_WORD_LEN]

                statement = """
                REPLACE INTO `sp_servers` (`word`, `host`, `frequency`)
                VALUES (%s, %s, %s);
                """

                cur.executemany(statement, sp_server_records)
                db.commit()
                ret = {
                    'host': sp_host,
                }
            else:
                raise ValueError('Invalid path: {}'.format(path))
        except Exception as e:
            print(traceback.format_exc(), file=sys.stderr)
            raise RequesterError('at {}\n{}'.format(parsed_path, e))
        finally:
            cur.close()
            db.close()

        return ret
