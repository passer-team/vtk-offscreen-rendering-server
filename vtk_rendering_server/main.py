"""
@author: Daryl.Xu <xuziqiang@zyheal.com>
"""
import os
import logging

from flask import Flask, request


app = Flask(__name__)


# 相对于script存放路径的路径
SCRIPT = {
    'face_visualization.render1': 'face_visualization/render1.py',
    'liver_worker.pipeline1': 'liver_worker/pipeline1.py'
}


def config_logger():
    logger_ = logging.getLogger(__name__)
    formatter = logging.Formatter(
        # "%(asctime)s %(name)s %(filename)s %(lineno)s %(levelname)s %(message)s",
        "%(asctime)s.%(msecs)03d %(filename)s %(lineno)s %(levelname)s %(message)s",
        datefmt='%Y-%m-%d %H:%M:%S',
    )
    logger_.setLevel(logging.DEBUG)

    handler = logging.StreamHandler()
    handler.setFormatter(formatter)
    logger_.addHandler(handler)

    logger_.info('The logger has configed!')
    return logger_


logger = config_logger()


def _get_script(id_: str, check_exist: bool = True) -> str:
    current_dir = os.path.dirname(__file__)
    script_root = os.path.join(current_dir, '../script')
    try:
        script_relative_path = SCRIPT[id_]
    except KeyError:
        logging.error(f'Render script not found: {id_}')
        raise RuntimeError(f'Render script not found: {id_}')
    script_path = os.path.join(script_root, script_relative_path)
    if check_exist:
        assert os.path.exists(script_path)
    return os.path.abspath(script_path)


@app.route('/app')
def hello():
    return 'hello, world'


@app.route('/render')
def render():
    data_id= request.args.get('data')
    script_id = request.args.get('script')
    logger.debug(f'render invoke, data: {data_id}, script: {script_id}')
    # TODO 执行出错的时候抛出异常
    
    script_path = _get_script(script_id)
    data_path = os.path.join('/data', data_id)
    cmd = f'/opt/paraview/bin/pvpython {script_path} {data_path}'
    if os.path.exists('/opt/paraview/bin/pvpython'):
        if os.system(cmd):
            msg = f'Failed to run: {script_id}, {script_path}'
            logging.error(msg)
            raise RuntimeError(msg)
        else:
            return 'success'    
    else:
        # in the test enviroment
        logger.debug(f'The script path: {script_path}')
        return 'success from dev server'


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5001)

