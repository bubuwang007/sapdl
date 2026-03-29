---
name: apdl-command-retrieval
description: Use when you need to load APDL implementation code and command reference documentation into context. Invoke this skill first to access the relevant files.
---

# APDL Command Generator

## Overview

将 ANSYS APDL 命令封装为 Python 类的开发指南。加载此 skill 可访问 APDL 实现代码和命令参考文档。

## Context Loading

当需要使用 APDL 相关代码时，先执行此 skill 加载以下文件到上下文：

### 1. APDL Python 实现

| 文件 | 说明 |
|------|------|
| `apdl/__init__.py` | 主入口，导出 Commands 和 Query |
| `apdl/_AllCommands.py` | Commands 类的多重继承结构 |
| `apdl/CLAUDE.md` | APDL 模块设计说明 |

### 2. 命令参考文档

命令文档位于：`.claude/skills/apdl-command-generator/references/`

| 文件 | 内容 |
|------|------|
| `Hlp_A_TOC.html` | 字母索引 |
| `Hlp_C_<CMD>.html` | 具体命令文档（如 `Hlp_C_K.html`） |
...

## Quick Reference

**已实现的命令查找：**

在 `apdl/` 中搜索命令名称，查看其实现细节和返回值解析。

**命令文档查找：**
```bash
# 搜索某个命令
ls references/Hlp_C_<COMMAND>.html

# 例如 K 命令
ls references/Hlp_C_K.html
```

找不到的话根据类似名字搜索。

## Command Pattern

APDL 命令封装的标准模式：

```python
def k(self, npt="", x="", y="", z="", **kwargs) -> int:
    """Define a keypoint.

    APDL Command: K

    Parameters
    ----------
    npt : str
        Reference number for keypoint.
    x, y, z : str
        Keypoint location.

    Returns
    -------
    int
        The keypoint number.
    """
    command = f"K,{npt},{x},{y},{z}"
    msg = self.run(command, **kwargs)
    if msg:
        res = re.search(r"KEYPOINT NUMBER\s*=\s*([0-9]+)", msg)
        if res:
            return int(res.group(1))
```

## 文件编码

- Python 文件：`UTF-8`
- HTML 文档：`ISO-8859-1`（部分可能是 `UTF-8`）
