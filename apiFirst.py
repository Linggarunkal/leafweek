from flask import Flask, jsonify, abort, make_response, request, url_for
from flask_httpauth import HTTPBasicAuth
auth = HTTPBasicAuth()

app = Flask(__name__)

task = [
    {
        'id': 1,
        'nama': 'Linggar Dedi Kurniawan',
        'Alamat': 'Tangerang'
    },
    {
        'id': 2,
        'nama': 'Siti Mari Ulfa',
        'Alamat': 'Pasuruan'
    }
]

@auth.get_password
def get_password(username):
    if username == 'unkal':
        return 'python'
    return None


@app.route('/todo/api/v1.0/task', methods=['GET'])
@auth.login_required
def get_task():
    return jsonify({'tasks': [make_public_task(tasks) for tasks in task]})


@app.route('/todo/api/v1.0/task/<int:task_id>', methods=["GET"])
def detail_task(task_id):
    tasks = [tasks for tasks in task if tasks['id'] == task_id]
    if len(tasks) == 0:
        abort(404)
    return jsonify({'task': tasks[0]})


@app.route('/todo/api/v1.0/task', methods=['POST'])
def create_task():

    if not request.json or not 'nama' in request.json:
        abort(400)
    print request.json['nama'], request.json['alamat']
    tasks = {
        'id': task[-1]['id'] + 1,
        'nama': request.json['nama'],
        'alamat': request.json['alamat']
    }

    task.append(tasks)
    return jsonify({'task': tasks}),201


@app.route('/todo/api/v1.0/task/<int:task_id>', methods=['PUT'])
def update_task(task_id):
    tasks = [tasks for tasks in task if tasks['id'] == task_id]
    if len(tasks) == 0:
        abort(404)
    if not request.json:
        abort(400)
    if 'nama' in request.json and type(request.json['nama']) != unicode:
        abort(400)
    if 'alamat' in request.json and type(request.json['alamat']) is not unicode:
        abort(400)
    tasks[0]['nama'] = request.json.get('nama', tasks[0]['nama'])
    tasks[0]['Alamat'] = request.json.get('Alamat', tasks[0]['Alamat'])
    print tasks[0]['nama'], tasks[0]['Alamat']
    return jsonify({'task': tasks[0]})


@app.route('/todo/api/v1.0/task/<int:task_id>', methods=['DELETE'])
def delete_task(task_id):
    tasks = [tasks for tasks in task if tasks['id'] == task_id]
    if len(tasks) == 0:
        abort(404)
    tasks.remove(tasks[0])
    return jsonify({'result': True})


@app.errorhandler(404)
def not_found(error):
    return make_response(jsonify({'Error': '404', 'Message': 'Data Not Found in Database'}), 404)


@auth.error_handler
def unauthorized():
    return make_response(jsonify({'Error': '403', 'Message': 'Forbidden Access'}), 403)


def make_public_task(task):
    new_task = {}
    for field in task:

        if field == 'id':
            new_task['uri'] = url_for('get_task', task_id=task['id'], _external=True)
            print new_task['uri']
        else:
            new_task[field] = task[field]
    return new_task

if __name__ == '__main__':
    app.run(debug=True)