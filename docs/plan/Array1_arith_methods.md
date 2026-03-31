# Plan: Array1 二元运算节点实现

## Context

为 `core/ast/array1_nodes/` 添加专用的二元运算节点类，用于支持 `*VOPER` 命令的各种二元运算操作。当前 `Array1FuncRetArray1Node` 只处理一元函数，需要专用节点处理二元运算如 ADD, SUB, MULT, DIV 等。

同时在 `Array1` 类中添加魔术方法（`__add__`, `__iadd__`, `__radd__` 等），参照 `NumberParameter` 的实现模式。

## 关键文件

- `core/ast/array1_nodes/__init__.py` - 导出节点
- `core/ast/array1_nodes/array1_node.py` - Array1Node 基类
- `core/ast/array1_nodes/array1_func_ret_array1_node.py` - 已有的一元函数返回节点
- `core/objects/array1.py` - Array1 对象类
- `core/objects/number_parameter.py` - NumberParameter 参考
- `core/apdl/commands/apdl/array_param.py` - *VOPER 命令定义

## 实现方案

### 1. 创建 `Array1BinaryOpNode` 基类

```python
# array1_binary_op_node.py
class Array1BinaryOpNode(Node):
    """Array1 二元运算节点基类 (*VOPER)"""

    __slots__ = ["left", "right", "type", "out"]

    def __init__(self, left, right, out=None):
        self.left = left
        self.right = right
        self.type = "statement"
        self.out = out

    def apdl(self, indent_level: int) -> str:
        # *VOPER,out,left,OPER,right
```

### 2. 创建专用二元运算节点

| 节点类 | APDL 命令 | 说明 |
|--------|----------|------|
| `Array1AddNode` | ADD | 加法 |
| `Array1SubNode` | SUB | 减法 |
| `Array1MulNode` | MULT | 乘法 |
| `Array1DivNode` | DIV | 除法 |
| `Array1LtNode` | LT | 小于比较 |
| `Array1LeNode` | LE | 小于等于比较 |
| `Array1EqNode` | EQ | 等于比较 |
| `Array1NeNode` | NE | 不等于比较 |
| `Array1GeNode` | GE | 大于等于比较 |
| `Array1GtNode` | GT | 大于比较 |

每个节点继承 `Array1BinaryOpNode`，设置对应的 `oper` 属性。

### 3. 更新 `array1_nodes/__init__.py`

导出所有新节点。

### 4. 在 `Array1` 类中添加魔术方法

在 `core/objects/array1.py` 中添加（参照 NumberParameter）：

```python
# 魔术方法
def __add__(self, other) -> Array1AddNode:
    return Array1AddNode(self, other)

def __radd__(self, other) -> Array1AddNode:
    return Array1AddNode(other, self)

def __iadd__(self, other) -> "Array1":
    self.assign(Array1AddNode(self, other))
    return self

def __sub__(self, other) -> Array1SubNode:
    return Array1SubNode(self, other)

def __rsub__(self, other) -> Array1SubNode:
    return Array1SubNode(other, self)

def __isub__(self, other) -> "Array1":
    self.assign(Array1SubNode(self, other))
    return self

# ... 其他运算类似
```

### 5. 文件修改清单

1. `core/ast/array1_nodes/array1_binary_op_node.py` - 新建基类
2. `core/ast/array1_nodes/__init__.py` - 更新导出
3. `core/objects/array1.py` - 添加魔术方法

## 验证

1. 运行现有测试确保没有破坏
2. 手动测试生成 APDL 命令流
