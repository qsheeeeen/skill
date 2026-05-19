# qsheeeeen/skill

个人 Claude Code skill 仓库。

## 安装

在 Claude Code 中执行：

```
/plugin marketplace add qsheeeeen/skill
```

## 已有 Skill

### qiaopi — 侨批书信生成器

化身民国写批先生，帮你代笔侨批家书，最终生成仿古手写图片。

```
/qiaopi
```

加载后，写批先生会逐一询问收信人、想写的内容、寄信人署名，代笔润色后确认，最终调用脚本生成侨批图片。

## 手动安装

```bash
git clone git@github.com:qsheeeeen/skill.git
ln -s $(pwd)/skill/skills/qiaopi ~/.claude/skills/qiaopi
```
