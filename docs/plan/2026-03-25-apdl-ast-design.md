# SAPDL AST 实现方案

## Context

用户希望将 `sapdl` 项目的命令存储从扁平结构改为 AST（抽象语法树），以支持 `*DO/*ENDDO` 循环和 `*IF/*ENDIF` 条件等分支结构。这是实现真正 APDL 宏的必要基础。

## 目标

1. 建立轻量级 AST 节点类层次结构
2. Mac 类作为 AST 根节点和收集器
3. 支持嵌套的分支/循环结构
4. 自动处理缩进
5. 保持 TDD 开发模式

## 文件结构

```
sapdl/
    core/
        ast/
            __init__.py      # 导出所有 AST 类
            base.py          # Node 基类, Body 类
            nodes.py         # CommandNode, DoNode, IfNode 等
        mac.py               # Mac 类（改造）
    tests/
        test_ast.py          # AST 节点测试
```

## 核心设计

### 1. 节点基类 (core/ast/base.py)

```python
class Node(ABC):
    @abstractmethod
    def to_string(self, indent_level: int = 0) -> str: ...

class Body:
    nodes: List[Node]
    def add(self, node: Node): ...
    def to_string(self, indent_level: int = 0) -> str: ...
```

### 2. 节点类型 (core/ast/nodes.py)

| 节点类 | 对应 APDL | 属性 |
|--------|-----------|------|
| `CommandNode` | 普通命令 | `cmd: str` |
| `CommentNode` | 注释 | `text: str` |
| `DoNode` | `*DO/*ENDDO` | `var, start, end, step, body: Body` |
| `IfNode` | `*IF/*ELIF/*ELSE/*ENDIF` | `condition, then_body, elif_conditions, else_body` |
| `MacroNode` | 宏定义 | `name, params, body` |

### 3. Mac 类集成 (core/mac.py)

- `Mac` 继承 `Commands`
- `run()` 方法被替换为 AST 构建逻辑
- 维护 `_body_stack` 追踪当前嵌套上下文
- 上下文管理器：`do_ctx()`, `if_ctx()`

### 4. 上下文管理器 API

```python
mac = Mac()

with mac.prep7():
    mac.k(1, 0, 0, 0)

    with mac.do_ctx("i", "1", "10"):
        mac.k(i, i, 0, 0)

    with mac.if_ctx("val,GT,0"):
        mac.k(100, 0, 0, 0)
```

## 实现步骤

1. **Phase 1**: `core/ast/base.py` - 基类和 Body
2. **Phase 2**: `core/ast/nodes.py` - 所有节点类型
3. **Phase 3**: `core/ast/__init__.py` - 导出
4. **Phase 4**: `core/mac.py` - 集成 AST，注入 runner
5. **Phase 5**: `tests/` - TDD 测试

## 关键文件

- `core/mac.py` - Mac 类改造
- `core/commands/command.py` - 参考现有 Command 设计
- `apdl/_AllCommands.py` - Commands 类（不改动）
- `sapdl/__init__.py` - INDENT 常量

## 验证方法

1. 编写 `tests/test_ast.py` 测试节点序列化
2. 编写 `tests/test_mac.py` 测试 Mac 类收集和输出
3. 验证嵌套 DO/IF 的缩进正确
4. 验证 `to_string()` 和 `to_file()` 输出正确格式
