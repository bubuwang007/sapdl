# Launcher 模块

ANSYS Mechanical APDL 启动器模块，支持两种连接方式：GUI 自动化和 gRPC。

## 文件结构

```
launcher/
├── __init__.py       # 配置常量和导出 GUILauncher, GrpcLauncher
├── launcher.py       # Launcher 抽象基类
├── utils.py          # 工具函数
├── gui_launcher.py   # GUI 自动化启动器
└── grpc_launcher.py  # gRPC 启动器
```

## 核心概念

- **Launcher** — 抽象基类，定义 `run_file()` 和 `run_str()` 接口
- **GUILauncher** — 通过 pywin32 GUI 自动化与 ANSYS 交互
- **GrpcLauncher** — 通过 ansys-mapdl-core 库使用 gRPC 连接 MAPDL

## 配置常量 (`__init__.py`)

| 常量 | 默认值 | 说明 |
|------|--------|------|
| `ANSYS_PATH` | `""` | ANSYS 安装路径（空则从环境变量查找） |
| `ANSYS_TEMPFILE_PATH` | `"C:\\ANSYSAPDL\\temp"` | 临时文件目录 |
| `MAPDL_INITIAL_WORKDIR` | `"C:\\ANSYSAPDL\\workdir"` | MAPDL 工作目录 |
| `MAPDL_IP` | `"127.0.0.1"` | MAPDL IP |
| `MAPDL_PORT` | `50001` | MAPDL 端口 |

## 工具函数 (`utils.py`)

| 函数 | 说明 |
|------|------|
| `find_ansys()` | 从环境变量查找 ANSYS 路径，多版本时返回最新 |
| `_find_ansys_path()` | 获取 ANSYS 基础路径（优先配置，其次环境变量） |
| `find_mechanical_apdl()` | 返回 `launcher.exe` 路径 |
| `find_mapdl()` | 返回 `MAPDL.exe` 路径 |
| `tempfile_path(filename)` | 生成临时文件完整路径 |
| `stamp()` | 生成唯一标识用于结果文件追踪 |
| `write_tempfile(filename, content)` | 写入临时文件 |
| `write_with_stamp(filename, content)` | 写入临时文件并附加 stamp 命令 |
| `find_ansys_windows()` | 枚举所有可见窗口，返回 hwnd→标题 字典 |

## 使用方式

```python
from sapdl.launcher import GUILauncher, GrpcLauncher

# GUI 模式（需 ANSYS 已运行）
launcher = GUILauncher(connect=True)
launcher.run_str("FINISH")

# gRPC 模式（自动启动 MAPDL）
launcher = GrpcLauncher(workdir="D:\\work", jobname="myjob")
launcher.run_file("test.apdl")
```

## 依赖

- `pywin32` — GUILauncher 需要，用于窗口自动化
- `ansys-mapdl-core` — GrpcLauncher 需要，用于 gRPC 连接
- `psutil` — GrpcLauncher 需要，用于获取 CPU 核心数
