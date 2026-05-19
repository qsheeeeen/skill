---
name: qiaopi
description: 将收信人、正文、寄信人生成为传统侨批书信风格的图片，仿古纸张、红色栏线、竖排排版。
---

## qiaopi — 侨批书信图片生成器

将此 skill 加载后，用户可以用自然语言描述想要生成的侨批内容，Claude 会整理文字内容，然后调用 `scripts/generate_qiaopi.py` 脚本生成侨批风格的图片。

### 工作流程

1. **收集内容**：请用户提供侨批的文字内容，只需三个要素：
   - 收信人称呼（如"父母亲大人膝下"）
   - 正文（问候、汇款金额、用途说明等）
   - 寄信人署名（如"儿 永昌 叩上"）

2. **整理文字**：将用户提供的文字整理为竖排格式（传统侨批从右向左书写）。

3. **生成图片**：执行以下命令生成侨批图片：

   ```bash
   python3 skills/qiaopi/scripts/generate_qiaopi.py \
     --output <输出文件路径> \
     --recipient "<收信人>" \
     --body "<正文>" \
     --sender "<寄信人>"
   ```

   参数说明：
   - `--output`：输出图片路径（必需），支持 `.png` / `.jpg`
   - `--recipient`：收信人称呼
   - `--body`：正文内容（可用 `\n` 分段）
   - `--sender`：寄信人署名
   - `--font`：自定义字体路径（默认使用内置 ToneOZ-Tsuipita-TC）

4. **展示结果**：生成完成后告知用户图片路径。

### 注意事项

- 依赖 Pillow（`sudo apt install python3-pillow`）
- 内置字体 `fonts/ToneOZ-Tsuipita-TC.ttf`，无需额外安装字体
- 生成的图片为 PNG 格式
