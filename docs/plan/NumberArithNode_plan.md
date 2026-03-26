# NumberArithNode 实现计划

## 目标

实现 6 个算术运算节点类，继承自 `NumberArithNode`。

## 目录结构

```
core/ast/number_parameter_nodes/
    arith_nodes/
        __init__.py
        add_node.py     # 加法 (+)
        sub_node.py     # 减法 (-)
        mul_node.py     # 乘法 (*)
        div_node.py     # 除法 (/)
        pow_node.py     # 幂运算 (**)
        neg_node.py     # 负号/unary minus (-)
```

## 算术节点映射

| 节点类 | APDL 运算符 | 说明 | 优先级 |
|--------|-------------|------|--------|
| `AddNode` | `+` | 加法 | 4 |
| `SubNode` | `-` | 减法 | 4 |
| `MulNode` | `*` | 乘法 | 3 |
| `DivNode` | `/` | 除法 | 3 |
| `NegNode` | `-` | 负号（一元） | 2 |
| `PowNode` | `**` | 幂运算 | 1 |

**APDL 运算符优先级**：幂运算(`**`) > 负号(`-`) > 乘除(`*`, `/`) > 加减(`+`, `-`)

## 基类分析

`NumberArithNode` 有 `__slots__ = ["left", "operator", "right", "type", "priority"]`，但没有 `apdl()` 方法。子类需要实现 `apdl()` 方法。

APDL 算术表达式格式：`{left}{operator}{right}`（无逗号分隔）

## 括号生成规则

子节点优先级 < 当前节点优先级时，需要加括号。

**结合性差异**：
- **左结合**（`+`, `-`, `*`, `/`, `%`）：左侧和右侧判断方式相同
  - 左：`left_priority < self.priority`
  - 右：`right_priority < self.priority`
- **右结合**（`**`）：左侧相同优先级也需要括号，右侧则不需要
  - 左：`left_priority <= self.priority`
  - 右：`right_priority < self.priority`

```python
def apdl(self, indent: int) -> str:
    left_str = self.left.apdl(indent) if hasattr(self.left, 'apdl') else str(self.left)
    right_str = self.right.apdl(indent) if hasattr(self.right, 'apdl') else str(self.right)

    left_pri = getattr(self.left, 'priority', 0)
    right_pri = getattr(self.right, 'priority', 0)

    if left_pri < self.priority:
        left_str = f"({left_str})"
    if right_pri < self.priority:
        right_str = f"({right_str})"

    return f"{left_str}{self.operator}{right_str}"
```

**PowNode 特殊处理**（右结合）：

```python
class PowNode(NumberArithNode):
    """幂运算节点 (**)"""

    __slots__ = []
    priority = 2
    left_associative = False

    def apdl(self, indent: int) -> str:
        left_str = self.left.apdl(indent) if hasattr(self.left, 'apdl') else str(self.left)
        right_str = self.right.apdl(indent) if hasattr(self.right, 'apdl') else str(self.right)

        left_pri = getattr(self.left, 'priority', 0)
        right_pri = getattr(self.right, 'priority', 0)

        # 右结合：左侧相同优先级需要括号，右侧不需要
        if left_pri <= self.priority:
            left_str = f"({left_str})"
        if right_pri < self.priority:
            right_str = f"({right_str})"

        return f"{left_str}**{right_str}"
```

## 实现步骤

### 1. 创建 `arith_nodes` 目录

创建 `__init__.py` 文件，导出所有算术节点类。

### 2. 实现各个算术节点类

每个节点类继承 `NumberArithNode`，定义 `__slots__ = []`，实现 `apdl()` 方法。

示例 (`add_node.py`)：

```python
from ..number_arith_node import NumberArithNode


class AddNode(NumberArithNode):
    """加法运算节点 (+)"""

    __slots__ = []
    priority = 4

    def __init__(self, left, right):
        super().__init__(left, "+", right)

    def apdl(self, indent: int) -> str:
        left_str = self.left.apdl(indent) if hasattr(self.left, 'apdl') else str(self.left)
        right_str = self.right.apdl(indent) if hasattr(self.right, 'apdl') else str(self.right)

        left_paren = getattr(self.left, 'priority', 0) < self.priority
        right_paren = getattr(self.right, 'priority', 0) < self.priority

        left_str = f"({left_str})" if left_paren else left_str
        right_str = f"({right_str})" if right_paren else right_str

        return f"{left_str}+{right_str}"
```

## 任务清单

- [ ] 创建 `arith_nodes/` 目录
- [ ] 创建 `arith_nodes/__init__.py`
- [ ] 实现 `AddNode` (add_node.py)
- [ ] 实现 `SubNode` (sub_node.py)
- [ ] 实现 `MulNode` (mul_node.py)
- [ ] 实现 `DivNode` (div_node.py)
- [ ] 实现 `PowNode` (pow_node.py)
- [ ] 实现 `NegNode` (neg_node.py) — 一元负号
