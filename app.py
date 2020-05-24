import flask
import sqlite3
app = flask.Flask(__name__, template_folder = 'frontend')
con = sqlite3.connect('db.db', check_same_thread=False)
cur = con.cursor()

@app.route('/')
def index():
    return flask.render_template('index.html', url = flask.url_for)

@app.route('/result', methods = ['POST'])
def result():
    name = flask.request.form['name']
    url = flask.request.form['url']
    res = cur.execute(f'select * from short where name=\'{name}\'')
    if len(res.fetchall()): return flask.render_template('result.html', msg = '이미 사용중인 주소입니다')
    cur.execute(f'insert into short values (?, ?)', (str(name), str(url)))
    con.commit()
    return flask.render_template('result.html', msg = 'kiki', name = name)

@app.route('/short/<name>')
def short(name):
    res = cur.execute(f'select * from short where name=\'{name}\'')
    link = res.fetchall()[0][1]
    return flask.redirect(link)

app.run(port = 5000, debug = True)