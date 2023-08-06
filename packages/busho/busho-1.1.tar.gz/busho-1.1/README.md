# Busho

## 介绍
部署分布式项目，仅针对Linux、MacOS。

## 安装
```
pip3 install busho
```

## 使用
```
from busho import Busho

busho = Busho('project_path')  # 完整项目路径

@busho.local_host('host')  # 本地
def local_host():
    pass  # 在本地主机上运行此函数

@busho.remote_host('host', 'username', 'password')  # 远程主机一
def remote_host1():
    pass  # 在相应的远程主机上运行此函数

@busho.remote_host('host', 'username', 'password')  # 远程主机二
def remote_host2():
    pass

if __name__ == '__main__':
    busho.deploy()
```
- 需要有 Python3 环境
- 每个 host 只能出现一次