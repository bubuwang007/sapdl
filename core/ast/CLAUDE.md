# AST 模块

APDL 命令流的抽象语法树（AST）表示。

## 结构

```
core/ast/
    base.py                   # Node 基类、Body 容器
    command_node.py           # 命令节点
    comment_node.py           # 注释节点
    function_call_node.py     # 函数调用节点
    literal_node.py           # 字面量节点（数字、字符串）
    macro_call_node.py        # 宏调用节点
    number_parameter_node.py  # 数字参数节点
    controflow_nodes/         # 控制流节点
        do_node.py           # DO 循环
        if_node.py           # IF 条件
    number_parameter_nodes/   # 数字参数表达式节点
        number_arith_node.py      # 算术运算
        number_assign_node.py     # 赋值运算
        number_comparison_node.py # 比较运算
```

## 节点类型

| 类型 | 节点类 | 说明 |
|------|--------|------|
| block | `Body` | 语句块容器 |
| statement | `CommandNode` | APDL 命令 |
| statement | `CommentNode` | 注释 |
| statement | `DoNode` | DO 循环 |
| statement | `IfNode` | IF 条件 |
| statement | `MacroCallNode` | 宏调用 |
| expr | `FunctionCallNode` | 函数调用 |
| expr | `NumberLiteral` | 数字字面量 |
| expr | `StringLiteral` | 字符串字面量 |
| expr | `NumberArithNode` | 算术表达式 |
| expr | `NumberAssignNode` | 赋值表达式 |
| expr | `NumberComparisonNode` | 比较表达式 |

## Node 基类

所有节点继承自 `Node` (ABC)，具有：

- `type`: `Literal["expr", "statement", "block"]`
- `apdl(indent_level)`: 生成 APDL 表示

**注意**: `Body.apdl()` 会过滤表达式节点（expr type），只输出语句。

## Body 类

语句块容器，用于容纳顺序执行的节点序列。

```python
body = Body()
body.add(node)
lines = body.apdl(indent_level)
```

## 开发规范

继承项目根目录 CLAUDE.md 的规范，此处补充 AST 特有规则：

- 节点类：`PascalCase`（如 `DoNode`, `IfNode`）
- 表达式节点：以 `Node` 结尾（如 `NumberLiteralNode`）
- `apdl()` 返回 `str` 或 `list[str]`
- 缩进使用 `sapdl.INDENT`（4空格）
