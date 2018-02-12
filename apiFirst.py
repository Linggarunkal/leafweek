from flask import Flask, jsonify, abort, make_response, request


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

@app.route('/todo/api/v1.0/task', methods=['GET'])
def get_task():
    return jsonify({'tasks': task})

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

@app.errorhandler(404)
def not_found(error):
    return make_response(jsonify({'Error': '404','Message': 'Data Not Found in Database'}), 404)


if __name__ == '__main__':
    app.run(debug=True)