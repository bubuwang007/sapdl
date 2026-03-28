# NumberParameter 数学方法实现计划

## 背景

`NumberParameter` 类（`core/objects/number_parameter.py`）目前只有 `delete()` 和 `assign()` 方法。需要添加 Python 算术运算符支持，使 `NumberParameter` 对象可以直接参与数学运算。

参考 `core/ast/number_parameter_nodes/arith_nodes/` 中的节点实现模式。

## 目标

实现以下魔术方法，使 `NumberParameter` 支持算术运算：

| 运算符 | 魔术方法 | APDL 节点 | 优先级 |
|--------|----------|-----------|--------|
| `+` | `__add__` | `AddNode` | 4 |
| `-` | `__sub__` | `SubNode` | 4 |
| `*` | `__mul__` | `MulNode` | 3 |
| `/` | `__truediv__` | `DivNode` | 3 |
| `**` | `__pow__` | `PowNode` | 1 |
| `-x` | `__neg__` | `NegNode` | 2 |
| `+=` | `__iadd__` | 同上 | - |
| `-=` | `__isub__` | 同上 | - |
| `*=` | `__imul__` | 同上 | - |
| `/=` | `__itruediv__` | 同上 | - |
| `**=` | `__ipow__` | 同上 | - |
| `+` (反) | `__radd__` | `AddNode` | 4 |
| `-` (反) | `__rsub__` | `SubNode` | 4 |
| `*` (反) | `__rmul__` | `MulNode` | 3 |
| `/` (反) | `__rtruediv__` | `DivNode` | 3 |
| `**` (反) | `__rpow__` | `PowNode` | 1 |

## 修改文件

### 1. `core/objects/number_parameter.py`

在 `NumberParameter` 类中添加以下方法：

```python
def __add__(self, other):
    """加法 (+)"""
    from sapdl.core.ast.number_parameter_nodes.arith_nodes import AddNode
    return AddNode(self, other)

def __radd__(self, other):
    """反加法 (右侧 + self)"""
    from sapdl.core.ast.number_parameter_nodes.arith_nodes import AddNode
    return AddNode(other, self)

def __iadd__(self, other):
    """增强赋值 += """
    from sapdl.core.ast.number_parameter_nodes.arith_nodes import AddNode
    node = AddNode(self, other)
    self.assign(node)
    return self

# 类似实现 __sub__, __rsub__, __isub__ 等...
```

### 2. `tests/core/objects/test_number_parameter.py` (新建)

测试文件，验证所有运算符：

```python
"""Tests for NumberParameter arithmetic operations."""

import pytest
from sapdl.core import Mac
from sapdl.core.objects import NumberParameter


class TestNumberParameterAdd:
    def test_add_two_parameters(self):
        mac = Mac()
        A = NumberParameter(mac, "A")
        B = NumberParameter(mac, "B")
        result = A + B
        assert result.apdl(0) == "A+B"

    def test_add_with_literal(self):
        mac = Mac()
        A = NumberParameter(mac, "A")
        result = A + 5
        assert result.apdl(0) == "A+5"

    def test_iadd(self):
        mac = Mac()
        A = NumberParameter(mac, "A")
        A += 5
        # A 被赋值为 A+5 的表达式
        assert "A+5" in str(mac.body.apdl(0))


# ... 类似测试其他运算符
```

## 实现细节

### 优先级

APDL 优先级（数字越小优先级越高）：
- `PowNode`: 1
- `NegNode`: 2
- `MulNode`, `DivNode`: 3
- `AddNode`, `SubNode`: 4

### 反射运算 (R喃法)

当左操作数不支持运算时调用（如 `5 + A`）：
- `__radd__` → `AddNode(5, self)`
- `__rsub__` → `SubNode(5, self)` (注意：顺序是 `other - self`)
- 其他同理

### 增强赋值 (i喃法)

`__iadd__` 等方法必须返回 `self`，因为 Python 执行 `A += B` 等价于 `A = A.__iadd__(B)`。

## 验证

```bash
pytest tests/core/objects/test_number_parameter.py -v
```

## 依赖

- `sapdl.core.ast.number_parameter_nodes.arith_nodes` 已存在，包含所有需要的节点类
