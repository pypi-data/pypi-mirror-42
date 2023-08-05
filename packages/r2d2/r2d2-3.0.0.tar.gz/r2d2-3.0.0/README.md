# r2d2

some handy functions

## APIS:

### `goto(directroy: str)`

进入目标目录 `directroy` -> 操作 -> 返回之前目录。

用于临时进入目标目录进行操作，如果目标目录不存在，则会被创建。

```py
os.getcwd()
# /current/directory

with goto('/my/directory'):
    os.getcwd()
    # /my/directory

    process()

os.getcwd()
# /current/directory
```
