# Plan: Array1 二元运算节点实现

## Context

为 `core/ast/array1_nodes/` 添加专用的二元运算节点类，用于支持 `*VOPER` 命令的各种二元运算操作。当前 `Array1FuncRetArray1Node` 只处理一元函数（`*VFUN`），需要专用节点处理二元运算如 ADD, SUB, MULT, DIV 等。

同时在 `Array1` 类中添加魔术方法（`__add__`, `__iadd__`, `__radd__` 等），参照 `NumberParameter` 的实现模式。

## 关键文件

- `core/ast/array1_nodes/__init__.py` - 导出节点
- `core/ast/array1_nodes/array1_node.py` - Array1Node 基类
- `core/ast/array1_nodes/array1_func_ret_array1_node.py` - 已有的一元函数返回节点
- `core/ast/array1_nodes/array1_assign_node.py` - Array1AssignNode，需更新以支持二元运算节点
- `core/ast/array1_nodes/arith_nodes/__init__.py` - 二元运算节点导出
- `core/ast/array1_nodes/arith_nodes/array1_binary_op_node.py` - 二元运算节点基类
- `core/objects/array1.py` - Array1 对象类
- `core/objects/number_parameter.py` - NumberParameter 参考（魔术方法模式）
- `core/apdl/commands/apdl/array_param.py` - `*VOPER` 命令定义

## `*VOPER` 支持的操作

| 操作 | APDL 命令 | 说明 | 类型 |
|------|----------|------|------|
| `ADD` | `*VOPER,ParR,Par1,ADD,Par2` | 加法：Par1+Par2 | 算术 |
| `SUB` | `*VOPER,ParR,Par1,SUB,Par2` | 减法：Par1-Par2 | 算术 |
| `MULT` | `*VOPER,ParR,Par1,MULT,Par2` | 乘法：Par1*Par2 | 算术 |
| `DIV` | `*VOPER,ParR,Par1,DIV,Par2` | 除法：Par1/Par2 | 算术 |
| `MIN` | `*VOPER,ParR,Par1,MIN,Par2` | 最小值 | 算术 |
| `MAX` | `*VOPER,ParR,Par1,MAX,Par2` | 最大值 | 算术 |
| `LT` | `*VOPER,ParR,Par1,LT,Par2` | 小于比较 | 比较 |
| `LE` | `*VOPER,ParR,Par1,LE,Par2` | 小于等于比较 | 比较 |
| `EQ` | `*VOPER,ParR,Par1,EQ,Par2` | 等于比较 | 比较 |
| `NE` | `*VOPER,ParR,Par1,NE,Par2` | 不等于比较 | 比较 |
| `GE` | `*VOPER,ParR,Par1,GE,Par2` | 大于等于比较 | 比较 |
| `GT` | `*VOPER,ParR,Par1,GT,Par2` | 大于比较 | 比较 |
| `DER1` | `*VOPER,ParR,Par1,DER1,Par2` | 一阶导数 | 微积分 |
| `DER2` | `*VOPER,ParR,Par1,DER2,Par2` | 二阶导数 | 微积分 |
| `INT1` | `*VOPER,ParR,Par1,INT1,Par2,CON1` | 单积分（CON1 为积分常数） | 微积分 |
| `INT2` | `*VOPER,ParR,Par1,INT2,Par2,CON1,CON2` | 双积分 | 微积分 |
| `DOT` | `*VOPER,ParR,Par1,DOT,Par2` | 点积 | 向量 |
| `CROSS` | `*VOPER,ParR,Par1,CROSS,Par2` | 叉积 | 向量 |
| `GATH` | `*VOPER,ParR,Par1,GATH,Par2` | gather 操作 | 索引 |
| `SCAT` | `*VOPER,ParR,Par1,SCAT,Par2` | scatter 操作 | 索引 |
| `ATN2` | `*VOPER,ParR,Par1,ATN2,Par2` | 二参数反正切 | 三角 |
| `LOCAL` | `*VOPER,ParR,Par1,LOCAL,Par2,CON1,CON2` | 坐标变换到局部系 | 坐标 |
| `GLOBAL` | `*VOPER,ParR,Par1,GLOBAL,Par2,CON1,CON2` | 坐标变换到全局系 | 坐标 |

**Par1 和 Par2 可以是数组参数、标量参数或字面量常量。**

## 实现方案

### 阶段一：基础算术与比较运算（MVP）

实现最常用的 12 个操作：ADD, SUB, MULT, DIV, MIN, MAX, LT, LE, EQ, NE, GE, GT。

### 1. 创建 `array1_nodes/arith_nodes/` 目录结构

遵循 `number_parameter_nodes/arith_nodes/` 的模式，创建以下文件：

```
core/ast/array1_nodes/arith_nodes/
    __init__.py
    array1_binary_op_node.py
```

### 2. 创建 `Array1BinaryOpNode` 基类

```python
# array1_binary_op_node.py
from __future__ import annotations
from sapdl import INDENT
from ...base import Node


class Array1BinaryOpNode(Node):
    """Array1 二元运算节点基类 (*VOPER)。

    所有二元运算节点都继承此类。子类只需设置 `oper` 类属性
    即可自动获得正确的 APDL 命令生成能力。

    Attributes:
        oper: APDL *VOPER 操作码（如 "ADD", "SUB" 等）
    """

    oper: str = ""  # 子类覆盖

    __slots__ = ["left", "right", "type", "out"]

    def __init__(self, left, right, out=None):
        self.left = left
        self.right = right
        self.type = "statement"
        self.out = out

    def apdl(self, indent_level: int) -> str:
        if self.out is None:
            raise ValueError(
                "Output parameter is required for Array1BinaryOpNode. "
                "Assign the result to an Array1 first (e.g., result << arr1 + arr2)."
            )
        left_str = self._resolve_operand(self.left)
        right_str = self._resolve_operand(self.right)
        return (
            f"{INDENT * indent_level}*VOPER,"
            f"{self.out.name},"
            f"{left_str},"
            f"{self.oper},"
            f"{right_str}"
        )

    def _resolve_operand(self, operand):
        """解析操作数为 APDL 字符串。

        支持 Array1, ArrayElement, NumberParameter, Array1Node,
        NumberLiteral, int, float 等类型。
        """
        if hasattr(operand, "name"):
            return operand.name
        elif hasattr(operand, "parameter"):
            return str(operand.parameter)
        else:
            return str(operand)
```

### 3. 创建专用二元运算节点

**算术运算节点：**

```python
# array1_binary_op_node.py (续)


class Array1AddNode(Array1BinaryOpNode):
    """加法 (ADD)"""
    oper = "ADD"


class Array1SubNode(Array1BinaryOpNode):
    """减法 (SUB)"""
    oper = "SUB"


class Array1MulNode(Array1BinaryOpNode):
    """乘法 (MULT)"""
    oper = "MULT"


class Array1DivNode(Array1BinaryOpNode):
    """除法 (DIV)"""
    oper = "DIV"


class Array1MinNode(Array1BinaryOpNode):
    """最小值 (MIN)"""
    oper = "MIN"


class Array1MaxNode(Array1BinaryOpNode):
    """最大值 (MAX)"""
    oper = "MAX"
```

**比较运算节点：**

```python
class Array1LtNode(Array1BinaryOpNode):
    """小于比较 (LT)"""
    oper = "LT"


class Array1LeNode(Array1BinaryOpNode):
    """小于等于比较 (LE)"""
    oper = "LE"


class Array1EqNode(Array1BinaryOpNode):
    """等于比较 (EQ)"""
    oper = "EQ"


class Array1NeNode(Array1BinaryOpNode):
    """不等于比较 (NE)"""
    oper = "NE"


class Array1GeNode(Array1BinaryOpNode):
    """大于等于比较 (GE)"""
    oper = "GE"


class Array1GtNode(Array1BinaryOpNode):
    """大于比较 (GT)"""
    oper = "GT"
```

### 3. 更新 `Array1AssignNode`

当前 `Array1AssignNode.apdl()` 只处理 `Array1FuncRetArray1Node`，需要扩展以支持 `Array1BinaryOpNode`：

```python
# array1_assign_node.py

def apdl(self, indent_level: int) -> str:
    from ..array1_nodes import Array1FuncRetArray1Node, Array1BinaryOpNode

    if isinstance(self.value, Array1FuncRetArray1Node):
        self.value.out = self.array1_node.parameter
        return self.value.apdl(indent_level)
    elif isinstance(self.value, Array1BinaryOpNode):
        self.value.out = self.array1_node.parameter
        return self.value.apdl(indent_level)
    else:
        # Handle other cases (scalar fill, copy, etc.)
        pass
```

### 4. 更新 `array1_nodes/arith_nodes/__init__.py`

```python
# array1_nodes/arith_nodes/__init__.py
from .array1_binary_op_node import (
    Array1BinaryOpNode,
    Array1AddNode,
    Array1SubNode,
    Array1MulNode,
    Array1DivNode,
    Array1MinNode,
    Array1MaxNode,
    Array1LtNode,
    Array1LeNode,
    Array1EqNode,
    Array1NeNode,
    Array1GeNode,
    Array1GtNode,
)

__all__ = [
    "Array1BinaryOpNode",
    "Array1AddNode",
    "Array1SubNode",
    "Array1MulNode",
    "Array1DivNode",
    "Array1MinNode",
    "Array1MaxNode",
    "Array1LtNode",
    "Array1LeNode",
    "Array1EqNode",
    "Array1NeNode",
    "Array1GeNode",
    "Array1GtNode",
]
```

### 5. 更新 `array1_nodes/__init__.py`

导出所有节点（包括 arith_nodes 子模块）：

```python
from .array1_node import Array1Node
from .array1_define_node import Array1DefineNode
from .array1_delete_node import Array1DeleteNode
from .array1_func_ret_number_node import Array1FuncRetNumberNode
from .array1_func_ret_array1_node import Array1FuncRetArray1Node
from .array1_assign_node import Array1AssignNode
from . import arith_nodes

__all__ = [
    "Array1Node",
    "Array1DefineNode",
    "Array1DeleteNode",
    "Array1FuncRetNumberNode",
    "Array1FuncRetArray1Node",
    "Array1AssignNode",
    "arith_nodes",
]
```

### 6. 在 `Array1` 类中添加魔术方法

在 `core/objects/array1.py` 中添加（参照 NumberParameter）：

```python
# ==================== 二元运算 ====================

def __add__(self, other) -> Array1AddNode:
    """加法 (+)

    Args:
        other: 右操作数，可以是 Array1、数字或其他支持运算的对象

    Returns:
        Array1AddNode: 加法节点
    """
    from sapdl.core.ast.array1_nodes import Array1AddNode
    return Array1AddNode(self, other)

def __radd__(self, other) -> Array1AddNode:
    """反射加法 (other + self)"""
    from sapdl.core.ast.array1_nodes import Array1AddNode
    return Array1AddNode(other, self)

def __sub__(self, other) -> Array1SubNode:
    """减法 (-)"""
    from sapdl.core.ast.array1_nodes import Array1SubNode
    return Array1SubNode(self, other)

def __rsub__(self, other) -> Array1SubNode:
    """反射减法 (other - self)"""
    from sapdl.core.ast.array1_nodes import Array1SubNode
    return Array1SubNode(other, self)

def __mul__(self, other) -> Array1MulNode:
    """乘法 (*)"""
    from sapdl.core.ast.array1_nodes import Array1MulNode
    return Array1MulNode(self, other)

def __rmul__(self, other) -> Array1MulNode:
    """反射乘法 (other * self)"""
    from sapdl.core.ast.array1_nodes import Array1MulNode
    return Array1MulNode(other, self)

def __truediv__(self, other) -> Array1DivNode:
    """除法 (/)"""
    from sapdl.core.ast.array1_nodes import Array1DivNode
    return Array1DivNode(self, other)

def __rtruediv__(self, other) -> Array1DivNode:
    """反射除法 (other / self)"""
    from sapdl.core.ast.array1_nodes import Array1DivNode
    return Array1DivNode(other, self)

# ==================== 增强赋值 ====================

def __iadd__(self, other) -> "Array1":
    """增强赋值 +="""
    from sapdl.core.ast.array1_nodes import Array1AddNode
    self.assign(Array1AddNode(self, other))
    return self

def __isub__(self, other) -> "Array1":
    """增强赋值 -= """
    from sapdl.core.ast.array1_nodes import Array1SubNode
    self.assign(Array1SubNode(self, other))
    return self

def __imul__(self, other) -> "Array1":
    """增强赋值 *= """
    from sapdl.core.ast.array1_nodes import Array1MulNode
    self.assign(Array1MulNode(self, other))
    return self

def __itruediv__(self, other) -> "Array1":
    """增强赋值 /= """
    from sapdl.core.ast.array1_nodes import Array1DivNode
    self.assign(Array1DivNode(self, other))
    return self

# ==================== 比较运算 ====================

def __lt__(self, other) -> Array1LtNode:
    """小于 (<)"""
    from sapdl.core.ast.array1_nodes import Array1LtNode
    return Array1LtNode(self, other)

def __le__(self, other) -> Array1LeNode:
    """小于等于 (<=)"""
    from sapdl.core.ast.array1_nodes import Array1LeNode
    return Array1LeNode(self, other)

def __eq__(self, other) -> Array1EqNode:
    """等于 (==)"""
    from sapdl.core.ast.array1_nodes import Array1EqNode
    return Array1EqNode(self, other)

def __ne__(self, other) -> Array1NeNode:
    """不等于 (!=)"""
    from sapdl.core.ast.array1_nodes import Array1NeNode
    return Array1NeNode(self, other)

def __gt__(self, other) -> Array1GtNode:
    """大于 (>)"""
    from sapdl.core.ast.array1_nodes import Array1GtNode
    return Array1GtNode(self, other)

def __ge__(self, other) -> Array1GeNode:
    """大于等于 (>=)"""
    from sapdl.core.ast.array1_nodes import Array1GeNode
    return Array1GeNode(self, other)
```

### 7. 文件修改清单

| 文件 | 操作 | 说明 |
|------|------|------|
| `core/ast/array1_nodes/arith_nodes/__init__.py` | 新建 | 导出所有二元运算节点 |
| `core/ast/array1_nodes/arith_nodes/array1_binary_op_node.py` | 新建 | 基类 + 12 个运算节点 |
| `core/ast/array1_nodes/__init__.py` | 更新 | 导出 arith_nodes 子模块 |
| `core/ast/array1_nodes/array1_assign_node.py` | 修改 | 支持 Array1BinaryOpNode |
| `core/objects/array1.py` | 修改 | 添加 18 个魔术方法 |

## 阶段二：高级运算（后续迭代）

以下操作需要额外参数支持，可在后续阶段实现：

- **DER1/DER2**：一阶/二阶导数（无额外参数）
- **INT1/INT2**：单积分/双积分（需 CON1, CON2 常数）
- **DOT/CROSS**：向量点积/叉积（Par1, Par2 必须是 3 列数据）
- **GATH/SCAT**：索引 gather/scatter
- **ATN2**：二参数反正切
- **LOCAL/GLOBAL**：坐标系变换（需 CON1 坐标系编号, CON2 标志）

## 使用示例

```python
from sapdl import Mac

mac = Mac()
arr1 = mac.Array1(10, name="A")
arr2 = mac.Array1(10, name="B")
result = mac.Array1(10, name="C")

# 使用魔术方法
result << arr1 + arr2      # *VOPER,C,A,ADD,B
result << arr1 - arr2      # *VOPER,C,A,SUB,B
result << arr1 * arr2      # *VOPER,C,A,MULT,B
result << arr1 / arr2      # *VOPER,C,A,DIV,B

# 标量运算
result << arr1 + 5         # *VOPER,C,A,ADD,5
result << arr1 * 2         # *VOPER,C,A,MULT,2

# 原地运算
arr1 += arr2               # *VOPER,A,A,ADD,B

# 比较运算（生成掩码数组）
mask = mac.Array1(10, name="MASK")
mask << arr1 > arr2        # *VOPER,MASK,A,GT,B
```

## 验证

1. **单元测试**：为每个节点类编写测试，验证 APDL 输出正确
2. **集成测试**：测试 `arr1 + arr2` 生成的完整命令流
3. **边界测试**：
   - 标量与数组运算
   - 数组元素（ArrayElement）与数组运算
   - 空数组（未 dimensioned）的错误处理
4. 运行现有测试确保没有破坏
