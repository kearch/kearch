from flask import Flask, render_template, request, redirect, url_for
from retrieve_query import retrieve

app = Flask(__name__)


@app.route('/search', methods=['GET', 'POST'])
def post():
    if request.method == 'GET':
        query = request.args['query']
        results = retrieve(query)
        return render_template('result.html', results=results, query=query)
    else:
        return redirect(url_for('index.html'))


@app.route("/")
def hello():
    return render_template('index.html')


if __name__ == '__main__':
    app.debug = False
    app.run(host='0.0.0.0', port=2222)  # どこからでもアクセス可能に
