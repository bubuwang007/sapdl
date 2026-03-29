# apdl 模块

SAPDL 的核心命令封装模块，提供 ANSYS APDL 命令的 Python 接口。

## 概述

本模块将 ANSYS APDL 命令封装为 Python 类和方法，支持：

- 以 Python 方式调用 APDL 命令
- 命令流生成

## 结构

```
apdl/                          # 主模块
├── __init__.py                # 导出 Commands, Query, Mac
├── _AllCommands.py            # Commands 类的定义（多重继承聚合）
├── commands/                  # APDL 命令分组（144个py文件）
│   ├── apdl/                  # APDL 通用命令
│   │   ├── abbreviations.py  # ABBSAVE, ABBLIST, ABBDELETE
│   │   ├── array_param.py    # *DIM, *VEDIT, *MOPER
│   │   ├── macro_files.py    # *CREATE, *USE, *END
│   │   ├── matrix_op.py       # *MROW, *MCOL, *MT
│   │   ├── parameter_definition.py  # *SET, *ARGS, *STATUS
│   │   └── process_controls.py     # *GO, *IF, *REPEAT
│   ├── preproc/               # PREP7 预处理
│   │   ├── areas.py           # A, AL, AATT, AESize...
│   │   ├── bodies.py          # K, L, A, V...
│   │   ├── components.py      # CM, CMSEL, CMDEL
│   │   ├── elements.py        # ET, ETYPE, KEYOPT
│   │   ├── materials.py        # MP, TB, TBTEMP
│   │   ├── mesh.py            # ESIZE, MSHAPE, AMESH, VMESH
│   │   └── real_constants.py  # R, RMORE, RMODIF
│   ├── solution/              # 求解器和载荷
│   ├── post1/                 # POST1 后处理
│   ├── post26/                # POST26 时间历史
│   ├── database/              # 数据库操作
│   │   ├── coord_sys.py       # CS, CSLIST, CSKP
│   │   ├── selecting.py       # LSEL, ASEL, KSEL
│   │   ├── working_plane.py   # WPLANE, WPCSYS, WPAVE
│   │   └── ...
│   ├── graphics/              # 图形控制
│   │   ├── annotation.py      # /PLTN, /PMORE
│   │   ├── graphs.py          # /GRID, /AXLAB
│   │   ├── style.py           # /COLOR, /STYLE
│   │   └── views.py           # /VIEW, /ANG, /REP
│   ├── session/               # 会话控制
│   │   ├── processor.py       # /PREP7, /SOLU, /POST1
│   │   └── finish.py          # FINISH
│   ├── aux12/                 # 辐射分析
│   ├── aux2/                  # 文件操作
│   ├── display/               # 显示设置
│   ├── reduced/               # 缩减求解
│   └── misc/                 # 杂项命令
└── inline_functions/          # 内联函数（查询辅助）
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

spadl.core 下 Mac类继承了 Commands，提供了更高层次的接口。

### 命令分组

| 类 | 命令组 | 主要命令 |
|---|---|---|
| **PreprocessorCommands** | 几何、网格、材料、单元 | `K`, `L`, `A`, `V`, `ET`, `MP`, `TB`, `ESIZE`, `AMESH` |
| **APDLCommands** | 宏、参数、数组、流程控制 | `*DIM`, `*SET`, `*IF`, `*DO`, `*CREATE`, `*USE` |
| **DatabaseCommands** | 坐标系、选择、工作平面 | `CS`, `LSEL`, `ASEL`, `KSEL`, `WPLANE`, `CM` |
| **SolutionCommands** | 载荷、边界条件、求解 | `F`, `D`, `SF`, `SFL`, `SOLVE`, `SSTIF` |
| **Post1Commands** | POST1 后处理 | `PRNSOL`, `PLNSOL`, `ETABLE`, `FLIST`, `PRCINT` |
| **Post26Commands** | POST26 时间历史 | `STORE`, `PLVAR`, `ADD`, `DERIV` |
| **SessionCommands** | 处理器进入/退出 | `/PREP7`, `/SOLU`, `/POST1`, `/POST26`, `FINISH` |
| **GraphicsCommands** | 图形控制 | `/VIEW`, `/ANG`, `/REP`, `/COLOR`, `/STYLE` |
| **AuxiliaryCommands** | 辅助功能 | `AUX12` 辐射, `AUX2` 文件, `AUX15` 映射 |

#### 详细说明

- **PreprocessorCommands** (`commands/preproc/`)
  - 几何建模：`K` 关键点, `L` 直线, `A` 面, `V` 体
  - 单元定义：`ET` 单元类型, `KEYOPT` 单元选项, `R` 实常数
  - 材料：`MP` 线性材料, `TB` 非线性数据表
  - 网格：`ESIZE` 网格尺寸, `MSHAPE` 网格形状, `AMESH` 面网格

- **APDLCommands** (`commands/apdl/`)
  - 参数：`*DIM` 定义数组, `*SET` 参数赋值, `*STATUS` 参数状态
  - 流程控制：`*IF`, `*DO`, `*REPEAT` 循环
  - 宏文件：`*CREATE` 创建宏, `*USE` 调用宏, `*END` 结束

- **DatabaseCommands** (`commands/database/`)
  - 坐标系：`CS` 创建坐标系, `CSLIST` 列表显示
  - 选择：`LSEL` 线选择, `ASEL` 面选择, `KSEL` 关键点选择
  - 工作平面：`WPLANE` 工作平面, `WPAVE` 原点平移

- **SolutionCommands** (`commands/solution/`)
  - 载荷：`F` 集中力, `D` 位移约束, `SF` 表面载荷
  - 求解：`SOLVE` 求解, `SSTIF` 应力刚化, `NLGEOM` 几何非线性

- **Post1Commands** (`commands/post1/`)
  - 结果：`PRNSOL` 节点结果, `PLNSOL` 云图显示
  - 单元表：`ETABLE` 定义单元表, `PRETAB` 显示单元表
  - 失效：`FLIST` 失效准则列表

## run() 执行后端

所有命令方法内部调用 `self.run(command_string)`。

`run()` 的实现由外部提供：
通过run方法把命令流收集到容器中。
