import os
from contextlib import contextmanager

@contextmanager
def goto(directory: str):
    """进入目标目录 -> 操作 -> 返回之前目录
    用于临时进入目标目录进行操作，如果目标目录不存在，则会被创建

    with goto('/my/directory'):
        process()
    """
    cwd = os.getcwd()
    if not os.path.exists(directory):
        os.makedirs(directory)
    os.chdir(directory)
    yield None
    os.chdir(cwd)
