# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## 仓库概述

这是一个 Claude Code skill 仓库，每个 skill 是一个可被 `/skill-name` 调用的功能模块。

## 目录结构

```
skills/
  <skill-name>/
    SKILL.md     — skill 定义文件（必需）
    scripts/     — skill 使用的脚本
```

## 添加新 skill

1. 在 `skills/` 下创建以 skill 名称命名的目录
2. 编写 `SKILL.md`，包含 skill 的元数据和加载后的行为指令
3. 将辅助脚本放在 `scripts/` 子目录中

## 常用命令

```bash
# 运行 Python 脚本
python3 skills/<name>/scripts/<script>.py
```
