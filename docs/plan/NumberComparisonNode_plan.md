# NumberComparisonNode 实现计划

## 目标

实现 6 个比较节点类，继承自 `NumberComparisonNode`。

## 目录结构

```
core/ast/number_parameter_nodes/
    comparison_nodes/
        __init__.py
        gt_node.py      # Greater Than (>)
        lt_node.py      # Less Than (<)
        ge_node.py      # Greater than or Equal (>=)
        le_node.py      # Less than or Equal (<=)
        eq_node.py      # Equal (==)
        ne_node.py      # Not Equal (!=)
```

## 比较节点映射

| 节点类 | APDL 运算符 | 说明 |
|--------|-------------|------|
| `GTNode` | `GT` | 大于 (>) |
| `LTNode` | `LT` | 小于 (<) |
| `GENode` | `GE` | 大于等于 (>=) |
| `LENode` | `LE` | 小于等于 (<=) |
| `EQNode` | `EQ` | 等于 (==) |
| `NENode` | `NE` | 不等于 (!=) |

## 实现步骤

### 1. 创建 `comparison_nodes` 目录

创建 `__init__.py` 文件，导出所有比较节点类。

### 2. 实现各个比较节点类

每个节点类继承 `NumberComparisonNode`，在 `__init__` 中调用父类构造器并传入对应的 APDL 运算符。

示例 (`gt_node.py`)：

```python
from . import NumberComparisonNode


class GTNode(NumberComparisonNode):
    """大于比较节点 (> )"""

    def __init__(self, left, right):
        super().__init__(left, "GT", right)
```

### 3. 更新父类 `NumberComparisonNode`

当前 `NumberComparisonNode` 的 `apdl()` 方法使用 `self.operator`，输出格式为 `{left},{operator},{right}`，可直接复用。

## 任务清单

- [ ] 创建 `comparison_nodes/` 目录
- [ ] 创建 `comparison_nodes/__init__.py`
- [ ] 实现 `GTNode` (gt_node.py)
- [ ] 实现 `LTNode` (lt_node.py)
- [ ] 实现 `GENode` (ge_node.py)
- [ ] 实现 `LENode` (le_node.py)
- [ ] 实现 `EQNode` (eq_node.py)
- [ ] 实现 `NENode` (ne_node.py)
