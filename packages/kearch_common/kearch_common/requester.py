from datetime import datetime
import sys
import traceback
import urllib

import mysql.connector
import requests


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


def get_summary_from_sp_db(cur):
    page_size = 1000
    statement = """
    SELECT `id`, `word`, `frequency`
    FROM `summary`
    WHERE `id` > %s
    LIMIT %s
    """

    dump = {}
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
            dump[word] = cnt
        prev_rowcount = cur.rowcount

    statement = """
    SELECT `name`, `value`
    FROM `config_variables`
    WHERE `name` = 'engine_name'
    """
    cur.execute(statement)
    engine_name = cur.fetchone()[1]

    statement = """
    SELECT `name`, `value`
    FROM `config_variables`
    WHERE `name` = 'host_name'
    """
    cur.execute(statement)
    host_name = cur.fetchone()[1]

    return {
        'engine_name': engine_name,
        'sp_host': host_name,
        'dump': dump
    }


def dump_summaries_from_me_db(cur):
    page_size = 1000
    statement = """
    SELECT `id`, `host`, `word`, `frequency`
    FROM `sp_servers`
    WHERE `id` > %s
    LIMIT %s
    """

    summaries = {}
    prev_rowcount = -1
    last_word_id = 0
    while prev_rowcount != 0:
        print('Dumping words word_id >', last_word_id, '...',
              file=sys.stderr, flush=True)
        cur.execute(statement, (last_word_id, page_size))
        for row in cur.fetchall():
            last_word_id = row[0]
            host = row[1]
            word = row[2]
            cnt = row[3]
            if host not in summaries:
                summaries[host] = dict()
            summaries[host][word] = cnt
        prev_rowcount = cur.rowcount

    return summaries


class KearchRequester(object):
    """Interface for communicating between containers or servers."""

    def __init__(self,
                 host='localhost', port=None, conn_type='json'):
        super(KearchRequester, self).__init__()
        self.host = host
        self.port = port
        self.conn_type = conn_type

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
                raise ValueError(
                    'conn_type should be "json", "elastic" or "sql".')
        except Exception as e:
            print(traceback.format_exc(), file=sys.stderr)
            raise RequesterError('at {}\n{}'.format(path, e))

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
            resp = requests.request(
                method, url, params=params, json=payload, timeout=timeout)

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
        splited_path = list(
            filter((lambda x: x != ''), parsed_path.split('/')))

        # The purpose of this extension is to avoid out-of-range reference.
        splited_path.extend(["", "", ""])

        db_name = ''
        if splited_path[0] == 'me':
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
            if splited_path[0] == 'sp' and splited_path[1] == 'db' and \
               splited_path[2] == 'get_connection_requests':
                ret = dict()
                ret['in'] = dict()
                in_statement = """
                SELECT `me_hosts`.`name`, `is_approved`, `host_id`
                FROM `in_requests`
                INNER JOIN `me_hosts` ON
                `in_requests`.`host_id` = `me_hosts`.`id`
                """
                cur.execute(in_statement)
                for row in cur.fetchall():
                    ret['in'][row[0]] = row[1]

                ret['out'] = dict()
                out_statement = """
                SELECT `me_hosts`.`name`, `is_approved` FROM `out_requests`
                INNER JOIN `me_hosts` ON
                `out_requests`.`host_id` = `me_hosts`.`id`
                """
                cur.execute(out_statement)
                for row in cur.fetchall():
                    ret['out'][row[0]] = row[1]

            elif splited_path[0] == 'me' and splited_path[1] == 'db' and \
                    splited_path[2] == 'get_connection_requests':
                ret = dict()
                ret['in'] = dict()
                in_statement = """
                SELECT `sp_hosts`.`name`, `is_approved` FROM `in_requests`
                INNER JOIN `sp_hosts` ON
                `sp_hosts`.`id` = `in_requests`.`host_id`
                """
                cur.execute(in_statement)
                for row in cur.fetchall():
                    ret['in'][row[0]] = row[1]

                ret['out'] = dict()
                out_statement = """
                SELECT `sp_hosts`.`name`, `is_approved` FROM `out_requests`
                INNER JOIN `sp_hosts` ON
                `sp_hosts`.`id` = `out_requests`.`host_id`
                """
                cur.execute(out_statement)
                for row in cur.fetchall():
                    ret['out'][row[0]] = row[1]

            elif splited_path[0] == 'sp' and splited_path[1] == 'db' and \
                    splited_path[2] == 'add_a_connection_request':
                scheme = payload['scheme']
                in_or_out = payload['in_or_out']
                me_host = payload['me_host']
                hosts_insert_statement = """
                INSERT IGNORE INTO me_hosts (`scheme`, `name`) VALUES (%s, %s)
                """
                cur.execute(hosts_insert_statement, (scheme, me_host))
                db.commit()
                host_id_statement = """
                SELECT `id` FROM `me_hosts` WHERE `name` = %s
                """
                cur.execute(host_id_statement, (me_host,))
                host_id = cur.fetchone()[0]

                if in_or_out == 'in':
                    table_name = 'in_requests'
                else:
                    table_name = 'out_requests'
                requests_statement = """
                INSERT INTO {} (`host_id`, `is_approved`) VALUES (%s, false)
                ON DUPLICATE KEY UPDATE `is_approved` = false
                """.format(table_name)

                cur.execute(requests_statement, (host_id,))
                db.commit()
                ret = {'me_host': me_host}
            elif splited_path[0] == 'me' and splited_path[1] == 'db' and \
                    splited_path[2] == 'add_a_connection_request':
                in_or_out = payload['in_or_out']
                scheme = payload['scheme']
                sp_host = payload['sp_host']
                engine_name = payload.get('engine_name', '')
                hosts_insert_statement = """
                INSERT IGNORE INTO sp_hosts (`scheme`, `name`, `engine_name`)
                VALUES (%s, %s, %s)
                """
                cur.execute(hosts_insert_statement,
                            (scheme, sp_host, engine_name))
                db.commit()
                host_id_statement = """
                SELECT `id` FROM `sp_hosts` WHERE `name` = %s
                """
                cur.execute(host_id_statement, (sp_host,))
                host_id = cur.fetchone()[0]

                if in_or_out == 'in':
                    table_name = 'in_requests'
                else:
                    table_name = 'out_requests'
                requests_statement = """
                INSERT INTO {} (`host_id`, `is_approved`) VALUES (%s, false)
                ON DUPLICATE KEY UPDATE `is_approved` = false
                """.format(table_name)

                cur.execute(requests_statement, (host_id,))
                db.commit()
                ret = {'sp_host': sp_host}
            elif splited_path[0] == 'sp' and splited_path[1] == 'db' and \
                    splited_path[2] == 'approve_a_connection_request':
                in_or_out = payload['in_or_out']
                me_host = payload['me_host']
                host_id_statement = """
                SELECT `id` FROM `me_hosts` WHERE `name` = %s"""
                cur.execute(host_id_statement, (me_host,))
                host_id = cur.fetchone()[0]

                if in_or_out == 'in':
                    table_name = 'in_requests'
                else:
                    table_name = 'out_requests'
                requests_statement = """
                INSERT INTO {} (`host_id`, `is_approved`) VALUES (%s, true)
                ON DUPLICATE KEY UPDATE `is_approved` = true
                """.format(table_name)
                cur.execute(requests_statement, (host_id,))
                db.commit()

            elif splited_path[0] == 'me' and splited_path[1] == 'db' and \
                    splited_path[2] == 'approve_a_connection_request':
                in_or_out = payload['in_or_out']
                sp_host = payload['sp_host']
                host_id_statement = """
                SELECT `id` FROM `sp_hosts` WHERE `name` = %s"""
                cur.execute(host_id_statement, (sp_host,))
                host_id = cur.fetchone()[0]

                if in_or_out == 'in':
                    table_name = 'in_requests'
                else:
                    table_name = 'out_requests'
                requests_statement = """
                INSERT INTO {} (`host_id`, `is_approved`) VALUES (%s, true)
                ON DUPLICATE KEY UPDATE `is_approved` = true
                """.format(table_name)
                cur.execute(requests_statement, (host_id,))
                db.commit()
            elif splited_path[0] == 'sp' and splited_path[1] == 'db' and \
                    splited_path[2] == 'delete_a_connection_request':
                me_host = payload['me_host']

                host_id_statement = """
                SELECT `id` FROM `me_hosts` WHERE `name` = %s"""
                cur.execute(host_id_statement, (me_host,))
                host_id = cur.fetchone()[0]

                statement = """DELETE FROM {} WHERE `host_id` = %s"""
                cur.execute(statement.format('in_requests'), (host_id,))
                cur.execute(statement.format('out_requests'), (host_id,))

                me_host_statement = """
                DELETE FROM `me_hosts` WHERE `name` = %s"""
                cur.execute(me_host_statement, (me_host,))

                db.commit()
                ret = {'me_host': me_host}
            elif splited_path[0] == 'me' and splited_path[1] == 'db' and \
                    splited_path[2] == 'delete_a_connection_request':
                sp_host = payload['sp_host']

                host_id_stateme = """
                SELECT `id` FROM `sp_hosts` WHERE `name` = %s"""
                cur.execute(host_id_stateme, (sp_host,))
                host_id = cur.fetchone()[0]

                statement = """DELETE FROM {} WHERE `host_id` = %s"""
                cur.execute(statement.format('in_requests'), (host_id,))
                cur.execute(statement.format('out_requests'), (host_id,))

                sp_host_statement = """
                DELETE FROM `sp_hosts` WHERE `name` = %s"""
                cur.execute(sp_host_statement, (sp_host,))

                sp_servers_statement = """
                DELETE FROM `sp_servers` WHERE `host` = %s"""
                cur.execute(sp_servers_statement, (sp_host,))
                db.commit()

                ret = {'sp_host': sp_host}
            elif splited_path[1] == 'db' and \
                    splited_path[2] == 'get_config_variables':
                select_statement = """
                SELECT `name`,`value` FROM `config_variables`
                """
                cur.execute(select_statement)
                ret = dict()
                for r in cur.fetchall():
                    ret[r[0]] = r[1]
            elif splited_path[1] == 'db' and \
                    splited_path[2] == 'set_config_variables':
                statement = """
                INSERT INTO config_variables (`name`, `value`) VALUES (%s, %s)
                ON DUPLICATE KEY UPDATE `value` = VALUES(`value`)
                """
                records = list()
                for n, v in payload.items():
                    records.append((n, v))
                cur.executemany(statement, records)
                db.commit()
                ret = cur.rowcount
            elif (splited_path[0] == 'sp' or splited_path[0] == 'me') and \
                    splited_path[1] == 'db' and \
                    splited_path[2] == 'push_binary_file':
                name = params['name']
                body = params['body']
                statement = """
                INSERT INTO `binary_files`
                (`name`, `body`)
                VALUES (%s, %s)
                ON DUPLICATE KEY UPDATE `body` = VALUES(`body`)
                """

                cur.execute(statement, (name, body))
                db.commit()
                ret = {'name': name}
            elif (splited_path[0] == 'sp' or splited_path[0] == 'me') and \
                    splited_path[1] == 'db' and \
                    splited_path[2] == 'pull_binary_file':
                name = params['name']
                statement = """
                SELECT `body`, `updated_at` FROM `binary_files`
                WHERE `name` = %s
                """

                cur.execute(statement, (name,))
                row = cur.fetchone()
                ret = {
                    'name': name,
                    'body': row[0],
                    'updated_at': row[1],
                }
            elif (splited_path[0] == 'sp' or splited_path[0] == 'me') and \
                    splited_path[1] == 'db' and \
                    splited_path[2] == 'check_binary_file_timestamp':
                name = params['name']
                statement = """
                SELECT `updated_at` FROM `binary_files`
                WHERE `name` = %s
                """

                cur.execute(statement, (name,))
                row = cur.fetchone()
                ret = {
                    'name': name,
                    'updated_at': row[0],
                }
            elif splited_path[0] == 'me' and splited_path[1] == 'db' and \
                    splited_path[2] == 'get_sp_summaries':
                ret = dump_summaries_from_me_db(cur)
            elif (splited_path[0] == 'sp' or splited_path[0] == 'me') and \
                    splited_path[1] == 'db' and \
                    splited_path[2] == 'get_authentication':
                statement = """
                SELECT `id`,`username`,`password_hash` FROM `authentication`
                """

                ret = dict()
                cur.execute(statement)
                for row in cur.fetchall():
                    ret[int(row[0])] = {'id': int(row[0]),
                                        'username': row[1],
                                        'password_hash': row[2]}
            elif (splited_path[0] == 'sp' or splited_path[0] == 'me') and \
                    splited_path[1] == 'db' and \
                    splited_path[2] == 'update_password_hash':
                username = payload['username']
                passhash = payload['password_hash']
                statement = """
                UPDATE `authentication` SET `password_hash` = %s
                WHERE `username` = %s
                """

                cur.execute(statement, (passhash, username))
                db.commit()
                ret = {'username': username}
            elif splited_path[0] == 'sp' and splited_path[1] == 'db' and \
                    splited_path[2] == 'push_crawled_urls':
                now = datetime.now()
                url_queue_records = list(map(
                    lambda w: (w['url'], now), payload['data']))
                statement = """
                INSERT INTO `url_queue`
                (`url`, `crawled_at`)
                VALUES (%s, %s)
                ON DUPLICATE KEY UPDATE `crawled_at` = VALUES(`crawled_at`)
                """

                if len(url_queue_records) == 0:
                    ret = 0
                else:
                    cur.executemany(statement, url_queue_records)
                    db.commit()
                    ret = cur.rowcount
            elif splited_path[0] == 'sp' and splited_path[1] == 'db' and \
                    splited_path[2] == 'get_next_urls':
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
            elif splited_path[0] == 'sp' and splited_path[1] == 'db' and \
                    splited_path[2] == 'push_urls_to_queue':
                url_queue_records = [(url,) for url in payload['urls']]
                statement = """
                INSERT IGNORE INTO `url_queue` (`url`) VALUES (%s);
                """

                cur.executemany(statement, url_queue_records)
                db.commit()
                ret = cur.rowcount
            elif splited_path[0] == 'sp' and splited_path[1] == 'db' and \
                    splited_path[2] == 'dump_database':
                ret = get_summary_from_sp_db(cur)
            elif splited_path[0] == 'sp' and splited_path[1] == 'db' and \
                    splited_path[2] == 'update_dump':
                summary_records = [(word, freq)
                                   for word, freq in payload['data'].items()]
                statement = """
                INSERT INTO `summary`
                (`word`, `frequency`)
                VALUES (%s, %s)
                ON DUPLICATE KEY UPDATE
                `frequency` = `frequency` + VALUES(`frequency`)
                """
                cur.executemany(statement, summary_records)
                db.commit()
                ret = cur.rowcount
            elif splited_path[0] == 'me' and splited_path[1] == 'db' and \
                    splited_path[2] == 'retrieve_sp_servers':
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
                    if word not in ret:
                        ret[word] = {}
                    ret[word][host] = freq
            elif splited_path[0] == 'me' and splited_path[1] == 'db' and \
                    splited_path[2] == 'add_new_sp_server':
                sp_host = payload['sp_host']
                engine_name = payload['engine_name']
                dump = payload['dump']
                sp_server_records = [(word, sp_host, frequency)
                                     for word, frequency in dump.items()
                                     if len(word) <= MAX_WORD_LEN]

                sp_host_statement = """
                INSERT INTO `sp_hosts` (`name`, `engine_name`)
                VALUES (%s, %s)
                ON DUPLICATE KEY UPDATE `engine_name` = VALUES(`engine_name`)
                """
                cur.execute(sp_host_statement, (sp_host, engine_name))
                db.commit()

                statement = """
                REPLACE INTO `sp_servers` (`word`, `host`, `frequency`)
                VALUES (%s, %s, %s)
                """

                cur.executemany(statement, sp_server_records)
                db.commit()
                ret = {
                    'host': sp_host,
                    'engine_name': engine_name,
                }
            elif splited_path[0] == 'me' and splited_path[1] == 'db' and \
                    splited_path[2] == 'list_up_sp_servers':
                statement = """
                SELECT `name`, `engine_name` FROM `sp_hosts`
                """
                cur.execute(statement)
                ret = {}
                for row in cur.fetchall():
                    ret[row[0]] = {
                        'name': row[0],
                        'engine_name': row[1],
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
