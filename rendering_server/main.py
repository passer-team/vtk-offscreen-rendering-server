"""
@Author: Daryl.Xu
"""
from flask import Flask, request


app = Flask(__name__)


@app.route('/app')
def hello():
    return 'hello, world'


@app.route('/render')
def render():
    data_id= request.args.get('id')
    # TODO render the vtk file
    print(f'the data id: {data_id}')
    return 'success'


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')

