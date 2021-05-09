"""
@author: Daryl.Xu
"""
from flask import Flask, request
import os


app = Flask(__name__)


@app.route('/app')
def hello():
    return 'hello, world'


@app.route('/render')
def render():
    data_id= request.args.get('id')
    # TODO render the vtk file
    # print(f'the data id: {data_id}')
    # os.system('ls /')
    cmd = f'/opt/paraview/bin/pvpython ./script/render.py {data_id} {data_id}'
    print(cmd)
    os.system(cmd)
    return 'success'


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')

