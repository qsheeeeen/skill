# qsheeeeen/skills

个人 Claude Code skill 仓库。

## 安装

在 Claude Code 中执行其中一条：

```
/plugin install qiaopi-plugin@qsheeeeen-skills
```

或先添加市场再安装：

```
/plugin marketplace add qsheeeeen/skills
/plugin install qiaopi-plugin@qsheeeeen-skills
```

## 已有 Skill

### qiaopi — 侨批书信生成器

化身民国写批先生，帮你代笔侨批家书，最终生成仿古手写图片。

```
/qiaopi
```

加载后，写批先生会逐一询问收信人、想写的内容、寄信人署名，代笔润色后确认，最终调用脚本生成侨批图片。

## 使用

```bash
/qiaopi-plugin:qiaopi 帮我写一封侨批
```

## 手动安装

```bash
git clone git@github.com:qsheeeeen/skills.git
ln -s $(pwd)/skills/skills/qiaopi ~/.claude/skills/qiaopi
```
