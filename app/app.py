from flask import make_response, jsonify
from typing import List, Dict
import simplejson as json
from flask import Flask, request, Response, redirect
from flask import render_template
from flaskext.mysql import MySQL
from pymysql.cursors import DictCursor

app = Flask(__name__)
mysql = MySQL(cursorclass=DictCursor)

app.config['MYSQL_DATABASE_HOST'] = 'db'
app.config['MYSQL_DATABASE_USER'] = 'root'
app.config['MYSQL_DATABASE_PASSWORD'] = 'root'
app.config['MYSQL_DATABASE_PORT'] = 3306
app.config['MYSQL_DATABASE_DB'] = 'dataDeniro'
mysql.init_app(app)


@app.route("/", methods=['GET'])
def hello():
    if request.method != 'GET':
        return make_response('Malformed request', 400)
    my_dict = {'key': 'dictionary value'}
    headers = {"Content-Type": "application/json"}
    return make_response(jsonify(my_dict), 200, headers)


@app.route('/', methods=['GET'])
def index():
    user = {'username': 'deniro Project'}
    cursor = mysql.get_db().cursor()
    cursor.execute('SELECT * FROM ImportDeniro')
    result = cursor.fetchall()
    return render_template('index.html', title='Home', user=user, year=result)


@app.route('/view/<int:year_id>', methods=['GET'])
def record_view(year_id):
    cursor = mysql.get_db().cursor()
    cursor.execute('SELECT * FROM ImportDeniro WHERE id=%s', year_id)
    result = cursor.fetchall()
    return render_template('view.html', title='View Form', year=result[0])


@app.route('/edit/<int:year_id>', methods=['GET'])
def form_edit_get(year_id):
    cursor = mysql.get_db().cursor()
    cursor.execute('SELECT * FROM ImportDeniro WHERE id=%s', year_id)
    result = cursor.fetchall()
    return render_template('edit.html', title='Edit Form', year=result[0])


@app.route('/edit/<int:year_id>', methods=['POST'])
def form_update_post(year_id):
    cursor = mysql.get_db().cursor()
    inputData = (request.form.get('intYear'), request.form.get('intScore'), request.form.get('fldTitle'),
                 year_id)
    sql_update_query = """UPDATE ImportDeniro  SET t.intYear = %s, t.intScore = %s, t.fldTitle = %s """
    cursor.execute(sql_update_query, inputData)
    mysql.get_db().commit()
    return redirect("/", code=302)


@app.route('/deniro/new', methods=['GET'])
def form_insert_get():
    return render_template('new.html', title='New City Form')


@app.route('/deniro/new', methods=['POST'])
def form_insert_post():
    cursor = mysql.get_db().cursor()
    inputData = (request.form.get('intYear'), request.form.get('intScore'), request.form.get('fldTitle'))
    sql_insert_query = """INSERT INTO ImportDeniro (intYear,intScore,fldTitle) VALUES (%s, %s,%s) """
    cursor.execute(sql_insert_query, inputData)
    mysql.get_db().commit()
    return redirect("/", code=302)


@app.route('/delete/<int:year_id>', methods=['POST'])
def form_delete_post(year_id):
    cursor = mysql.get_db().cursor()
    sql_delete_query = """DELETE FROM ImportDeniro WHERE id = %s """
    cursor.execute(sql_delete_query, year_id)
    mysql.get_db().commit()
    return redirect("/", code=302)


@app.route('/api/v1/deniro', methods=['GET'])
def api_browse() -> str:
    cursor = mysql.get_db().cursor()
    cursor.execute('SELECT * FROM ImportDeniro')
    result = cursor.fetchall()
    json_result = json.dumps(result);
    resp = Response(json_result, status=200, mimetype='application/json')
    return resp


@app.route('/api/v1/deniro/<int:year_id>', methods=['GET'])
def api_retrieve(year_id) -> str:
    cursor = mysql.get_db().cursor()
    cursor.execute('SELECT * FROM ImportDeniro WHERE id=%s', year_id)
    result = cursor.fetchall()
    json_result = json.dumps(result);
    resp = Response(json_result, status=200, mimetype='application/json')
    return resp


@app.route('/api/v1/deniro/<int:year_id>', methods=['PUT'])
def api_edit(year_id) -> str:
    cursor = mysql.get_db().cursor()
    content = request.json
    inputData = (content['intYear'], content['intScore'], content['fldTitle'], year_id)
    sql_update_query = """UPDATE ImportDeniro t SET t.intYear = %s, t.intScore = %s, t.fldTitle = %s, WHERE t.id = %s """
    cursor.execute(sql_update_query, inputData)
    mysql.get_db().commit()
    resp = Response(status=200, mimetype='application/json')
    return resp


@app.route('/api/v1/deniro', methods=['POST'])
def api_add() -> str:
    content = request.json

    cursor = mysql.get_db().cursor()
    inputData = (content['intYear'], content['intScore'], content['fldTitle'])
    sql_insert_query = """INSERT INTO ImportDeniro (intYear,intScore,fldTitle) VALUES (%s, %s,%s) """
    cursor.execute(sql_insert_query, inputData)
    mysql.get_db().commit()
    resp = Response(status=201, mimetype='application/json')
    return resp


@app.route('/api/v1/deniro/<int:year_id>', methods=['DELETE'])
def api_delete(city_id) -> str:
    cursor = mysql.get_db().cursor()
    sql_delete_query = """DELETE FROM ImportDeniro WHERE id = %s """
    cursor.execute(sql_delete_query, city_id)
    mysql.get_db().commit()
    resp = Response(status=200, mimetype='application/json')
    return resp


if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)
