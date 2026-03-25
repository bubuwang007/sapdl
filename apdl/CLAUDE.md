# apdl 模块

SAPDL 的核心命令封装模块，提供 ANSYS APDL 命令的 Python 接口。

## 概述

本模块将 ANSYS APDL 命令封装为 Python 类和方法，支持：
- 以 Python 方式调用 APDL 命令
- 命令流生成

## 结构

```
apdl/
    __init__.py              # 导出 Commands, Query
    _AllCommands.py          # Commands 类的定义
    commands/                # APDL 命令分组实现
```

## Commands 类

主入口类，通过多重继承聚合所有 APDL 命令：

```python
from apdl import Commands

cmd = Commands()
cmd.prep7()           # /PREP7
cmd.k(1, 0, 0, 0)    # K,1,0,0,0
cmd.et(1, "SOLID186") # ET,1,SOLID186
cmd.finish()           # FINISH
```

### 命令分组

| 类 | 命令组 |
|---|---|
| PreprocessorCommands | 几何、网格、材料、单元 |
| APDLCommands | 宏、参数、数组 |
| DatabaseCommands | 坐标系、选择、工作平面 |
| SolutionCommands | 载荷、边界条件、求解 |
| Post1Commands | POST1 后处理 |
| Post26Commands | POST26 时间历史 |
| SessionCommands | 处理器进入/退出 |

## commands 子目录

- `preproc/` — PREP7 预处理（几何、网格、材料）
- `solution/` — 求解器和载荷
- `post1/` — POST1 后处理器
- `post26/` — POST26 时间历史
- `session/` — 会话控制（/PREP7, FINISH 等）
- `database/` — 数据库操作
- `graphics/` — 图形控制

## run() 执行后端

所有命令方法内部调用 `self.run(command_string)`。

`run()` 的实现由外部提供：
通过run方法把命令流收集到容器中。

## 命名约定

- 类：`PascalCase`（如 `KeyPoints`, `Materials`）
- 方法：`snake_case`（如 `k()`, `esurf()`）
