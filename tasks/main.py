from flask import Flask, jsonify, request, make_response, json
from flaskext.mysql import MySQL
from flask_cors import CORS

app = Flask(__name__)

app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = 'trenchqua67'
app.config['MYSQL_DB'] = 'db_tasks'
app.config['MYSQL_CURSORCLASS'] = 'DictCursor'


mysql = MySQL(app)
CORS(app)


@app.route('/api/tasks', methods=['GET'])
def get_all_tasks():
    cur = mysql.get_db().cursor()
    cur.execute("SELECT * FROM db_tasks.tasks")
    rv = cur.fetchall()
    print('rv is : {}'.format(rv))
    print('hello make_reponse(jsonify(rv)) is : {}'.format(jsonify(rv)))
    # return jsonify(rv)
    print('rv.len is : {}'.format(len(rv)))
    empList = []
    for emp in rv:
        print('emp[1] is : {}'.format(emp[1]))
        empDict = {
        'id': emp[0],
        'title' : emp[1]
        }
        empList.append(empDict)

    response = app.response_class(
        response=json.dumps(empList),
        status=200,
        mimetype='application/json'
    )
    print('response is : {}'.format(response))
    return response


@app.route('/api/task', methods=['POST'])
def add_task():
    cur = mysql.get_db().cursor()
    title = request.get_json()['title']

    cur.execute("INSERT INTO db_tasks.tasks (title) VALUES ('" + str(title)+ "')")
    mysql.get_db().commit()
    result = {'title':title}
    print('result is : {}'.format(result))

    return jsonify({"result": result})


@app.route("/api/task/<id>", methods=['PUT'])
def update_task(id):
    cur = mysql.get_db().cursor()
    title = request.get_json()['title']

    cur.execute("UPDATE db_tasks.tasks SET title = '" + str(title)+ "' where id = " + id)
    mysql.get_db().commit()
    result = {'title':title}

    return jsonify({"result": result})


@app.route("/api/task/<id>", methods=['DELETE'])
def delete_task(id):
    cur = mysql.get_db().cursor()
    
    response = cur.execute("DELETE FROM db_tasks.tasks where id = " + id)
    mysql.get_db().commit()
    
    print('response is : {}'.format(response))

    if response > 0:
        result = {'message' : 'recode deleted'}
    else:
        result = {'message' : 'no record found'}
    return jsonify({"result": result})

if __name__ == '__main__':
    app.run(debug=True)
