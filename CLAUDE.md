# SAPDL

Python 到 ANSYS APDL 转换器。将 APDL 命令封装为 Python 类，支持命令流生成。

## 结构

```
sapdl/
    apdl/           # APDL 命令封装
    docs/           # 文档和设计规范
    core/           # 核心功能
```

## 主要概念

- **Commands 类** — 聚合所有 APDL 命令，通过 `run()` 执行
- **Mac 类** — 命令流宏文件对象，这是一个综合类。

## 技术栈

- Python 3.11+
- pytest（测试框架）

## 开发规范

### 测试驱动（TDD）

- 先写测试，再写实现
- 测试文件放在 `tests/` 目录
- 命名：`test_<模块名>.py`

### 代码规范

- 类：`PascalCase`（如 `KeyPoints`, `Mac`）
- 方法：`snake_case`（如 `k()`, `to_string()`）
- 常量：`UPPER_SNAKE_CASE`
- 文档：Google Style docstring
- 类型注解：函数签名使用类型提示

### Git 规范

- 提交信息：中文描述，简洁明了
- 分支命名：`feature/<功能>`, `fix/<问题>`

### 参考文件

- 当参考apdl目录下的文件时，参考apdl/CLAUSE.md中的说明，避免直接引用文件内容。