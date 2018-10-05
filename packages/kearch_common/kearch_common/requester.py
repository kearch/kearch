import json
import urllib

import mysql.connector
import requests

from kearch_common.data_format import wrap_json


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
    REPLACE INTO `webpages`
    (`url`, `title`, `summary`)
    VALUES (%s)
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
    REPLACE INTO `words`
    (`str`)
    VALUES (%s)
    """
    words = list(webpage['tfidf']) + webpage['title_words']
    word_records = map(lambda w: (w,), words)
    cur.executemany(statement, word_records)
    db.commit()

    statement = """
    REPLACE INTO `title_words`
    (`webpage_id`, `word_id`)
    SELECT %s, `words`.`id` FROM `words` WHERE `str` = %s LIMIT 1
    """
    title_word_records = map(lambda w: (webpage_id, w), webpage['title_words'])
    cur.execute(statement, params=title_word_records, multi=True)
    db.commit()

    statement = """
    REPLACE INTO `tfidfs`
    (`webpage_id`, `word_id`, `value`)
    SELECT %s, `words`.`id`, %s FROM `words` WHERE `str` = %s LIMIT 1
    """
    tfidfs_records = map(lambda w: (
        webpage_id, webpage['tfidf'][w], w), webpage['tfidf'].keys())
    cur.execute(statement, params=tfidfs_records, multi=True)
    db.commit()


def dump_summary_form_sp_db(cur):
    page_size = 1000
    statement = """
    SELECT JSON_KEYS(`tfidf`) AS `tfidf_keys` FROM `webpages`
    LIMIT %s
    OFFSET %s;
    """

    sp_summary = {}
    prev_rowcount = -1
    page_cnt = 0
    while prev_rowcount != 0:
        cur.execute(statement, (page_size, page_cnt * page_size))
        tfidf_keys = [json.loads(row[0]) for row in cur.fetchall()]
        for words in tfidf_keys:
            for word in words:
                if not word in sp_summary:
                    sp_summary[word] = 0
                sp_summary[word] += 1

        prev_rowcount = cur.rowcount
        page_cnt += 1
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
        if self.conn_type == 'json':
            return self.request_json(path, method, params, payload,
                                     headers, timeout)
        elif self.conn_type == 'sql':
            return self.request_sql(path, method, params, payload,
                                    headers, timeout)
        else:
            raise ValueError('conn_type should be "json" or "sql".')

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
            elif parsed_path == '/get_next_urls':
                max_urls = int(params['max_urls'])
                select_statement = """
                SELECT `url` FROM `url_queue` ORDER BY `updated_at` LIMIT %s
                """
                delete_statement = """
                DELETE FROM `url_queue` ORDER BY `updated_at` LIMIT %s
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
                REPLACE INTO `url_queue` (`url`) VALUES (%s);
                """

                cur.executemany(statement, url_queue_records)
                db.commit()
                ret = cur.rowcount
            elif parsed_path == '/retrieve_webpages':
                queries = params['queries']
                max_urls = int(params['max_urls'])

                select_statement = """
                SELECT
                    `url`, `title`, `title_words`, `summary`, `tfidf`,
                    ({}) AS has_overwrap,
                    ({}) AS tfidf_sum
                FROM `webpages`
                ORDER BY has_overwrap DESC, tfidf_sum DESC
                LIMIT %s;
                """.format(get_has_overlap_statement(queries),
                           get_tfidf_sum_statement(queries))

                cur.execute(select_statement, (max_urls,))
                result_webpages = [{
                    'url': row[0],
                    'title': row[1],
                    'title_words': json.loads(row[2]),
                    'summary': row[3],
                    'tfidf': json.loads(row[4])
                } for row in cur.fetchall()]

                ret = {
                    'data': result_webpages
                }
            elif parsed_path == '/dump_database':
                ret = dump_summary_form_sp_db(cur)
            elif parsed_path == '/retrieve_sp_servers':
                queries = params['queries']

                format_strings = ','.join(['%s'] * len(queries))
                statement = """
                SELECT `word`, `host`, `frequency` FROM `sp_servers`
                WHERE `word` IN ({:s});
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
                                     if len(word) <= 200]

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
            raise
        finally:
            cur.close()
            db.close()

        return ret
