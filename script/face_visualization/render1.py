import os

# TODO 保证该生成的文件都生成，没有生成的话执行失败

def run(task_dir: str):
    pass


if __name__ == '__main__':
    import argparse

    parser = argparse.ArgumentParser(description='面部可视化项目的渲染脚本 | Rendering script for the face_visualization project')
    parser.add_argument('task_dir', help='要处理数据的所在的路径 | Path to the task directory')
    args = parser.parse_args()

    task_dir = os.path.abspath(args.task_dir)
    run(task_dir)
