import flask
import sys
import base64
from flask import jsonify
import kearch_evaluator.evaluator
from kearch_common.requester import KearchRequester

DATABASE_HOST = 'me-db.kearch.svc.cluster.local'
DATABASE_PORT = 3306

timestamp = dict()
app = flask.Flask(__name__)
evaluator = kearch_evaluator.evaluator.Evaluator()


def update_param_file(filename):
    db_req = KearchRequester(
        DATABASE_HOST, DATABASE_PORT, conn_type='sql')
    ret = db_req.request(path='/me/db/check_binary_file_timestamp',
                         params={'name': filename})
    dt = ret['updated_at']
    print('db:', dt, file=sys.stderr)
    if filename not in timestamp or timestamp[filename] < dt:
        timestamp[filename] = dt
        ret = db_req.request(path='/me/db/pull_binary_file',
                             params={'name': filename})
        body = base64.b64decode(ret['body'].encode())
        with open(filename, 'wb') as f:
            f.write(body)
        evaluator.load_params(kearch_evaluator.evaluator.PARAMS_FILE)


def evaluate_main(query):
    print('Start checking parameter files.', file=sys.stderr)
    update_param_file(kearch_evaluator.evaluator.PARAMS_FILE)
    print('End checking parameter files.', file=sys.stderr)

    queries = query.split(' ')

    # Some specialist servers in the evaluator may be deleted
    # by /me/gateway/delete_a_connection_request.
    # Therefore, we must confirm all specialist servers in the evaluator
    # exist in the database truly.
    db_req = KearchRequester(
        DATABASE_HOST, DATABASE_PORT, conn_type='sql')
    sp_servers = db_req.request(path='/me/db/list_up_sp_servers')
    res_eval = evaluator.evaluate(queries)
    res = dict()
    for s in sp_servers.keys():
        if s in res_eval:
            res[s] = res_eval[s]
    return res


@app.route('/me/evaluator/evaluate', methods=['GET'])
def evaluate():
    query = flask.request.args.get('query')
    res = evaluate_main(query)
    return jsonify(res)


def test_evaluate():
    res = evaluate_main('google')
    assert(type(res) is dict)
    for k, v in res.items():
        assert(type(k) is str)
        db_req = KearchRequester(
            DATABASE_HOST, DATABASE_PORT, conn_type='sql')
        sp_servers = db_req.request(path='/me/db/list_up_sp_servers')
        assert(k in sp_servers.keys())


if __name__ == '__main__':
    app.debug = True
    app.run(host='0.0.0.0', port=10080)  # どこからでもアクセス可能に
