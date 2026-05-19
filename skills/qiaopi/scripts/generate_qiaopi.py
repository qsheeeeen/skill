#!/usr/bin/env python3
"""生成传统侨批书信风格图片"""

import argparse
import os
import random
import sys
from PIL import Image, ImageDraw, ImageFont

# —— 信纸尺寸 ——
WIDTH = 1000                           # 图片宽度（像素）
HEIGHT = 1400                          # 图片高度（像素）
MARGIN_TOP = 100                       # 顶部留白
MARGIN_BOTTOM = 80                     # 底部留白
MARGIN_LEFT = 80                       # 左侧留白
MARGIN_RIGHT = 80                      # 右侧留白
TEXT_TOP_PAD = 24                      # 列首文字与顶部横线的间距
OUTER_LINE_W = 3                       # 外框线宽
INNER_LINE_W = 1                       # 内部栏线线宽
FONT_SIZE = 46                         # 字号（像素）
LINE_HEIGHT = FONT_SIZE + 10           # 竖排文字行高（像素）
JITTER_XY = 3                          # 手写随机偏移量（像素），0 为完全对齐

# —— 颜色配置 ——
PAPER_COLOR = (242, 228, 195)          # 仿古纸底色
PAPER_COLOR_DARK = (220, 200, 160)     # 边缘做旧深色
RED_LINE = (200, 80, 60)               # 红色栏线
RED_LINE_ALPHA = 160                   # 栏线透明度（0-255），越低纹理越透
INK_ALPHA = 200                        # 文字透明度（0-255），越低纹理越透
BLACK_INK = (40, 30, 20, INK_ALPHA)    # 正文墨色（RGBA）
BLACK_INK_LIGHT = (80, 70, 55)         # 淡墨（未使用）


def find_chinese_font():
    """查找系统中可用的中文字体，返回 (常规字体路径, 粗体字体路径)"""
    search_paths = [
        "/usr/share/fonts",
        "/usr/local/share/fonts",
        os.path.expanduser("~/.fonts"),
        os.path.expanduser("~/.local/share/fonts"),
    ]
    candidates = []
    for base in search_paths:
        if not os.path.isdir(base):
            continue
        for root, _, files in os.walk(base):
            for f in files:
                if f.endswith((".ttf", ".otf", ".ttc")):
                    candidates.append(os.path.join(root, f))

    # 优先匹配中文字体
    preferred = [
        "NotoSerifCJK", "NotoSerifSC", "Noto Serif CJK",
        "SourceHanSerif", "Source Han Serif",
        "SimSun", "NSimSun", "FangSong", "KaiTi", "STSong",
        "AR PL UMing", "AR PL UKai", "TW-Sung",
        "WenQuanYi", "文泉驿",
        "NotoSansCJK", "NotoSansSC", "Noto Sans CJK",
        "SourceHanSans", "Source Han Sans",
    ]
    for pref in preferred:
        for path in candidates:
            basename = os.path.basename(path)
            if pref.lower() in basename.lower():
                return path

    if candidates:
        return candidates[0]
    return None


def create_aged_paper(width, height):
    """创建做旧纸张背景"""
    img = Image.new("RGB", (width, height), PAPER_COLOR)
    pixels = img.load()

    # 添加噪点模拟纸张纹理
    for y in range(height):
        for x in range(width):
            r, g, b = pixels[x, y]
            noise = random.randint(-12, 12)
            r = max(0, min(255, r + noise))
            g = max(0, min(255, g + noise))
            b = max(0, min(255, b + noise))
            pixels[x, y] = (r, g, b)

    # 边缘做旧（暗角效果）
    mask = Image.new("L", (width, height), 255)
    mask_draw = ImageDraw.Draw(mask)
    for i in range(40):
        alpha = int(255 * (1 - i / 40) * 0.35)
        rect = [i, i, width - i, height - i]
        mask_draw.rectangle(rect, outline=255 - alpha)
    # 简化：用渐变叠加
    edge_overlay = Image.new("RGBA", (width, height), (0, 0, 0, 0))
    edge_draw = ImageDraw.Draw(edge_overlay)
    for i in range(50):
        alpha = int((1 - i / 50) * 80)
        if alpha <= 0:
            break
        edge_draw.rectangle(
            [i, i, width - i - 1, height - i - 1],
            outline=(139, 119, 70, alpha),
        )

    img = img.convert("RGBA")
    img = Image.alpha_composite(img, edge_overlay)
    img = img.convert("RGB")
    pixels = img.load()  # 重新加载 pixel access

    # 随机添加一些斑点（霉斑/虫蛀效果）
    for _ in range(random.randint(3, 8)):
        bx = random.randint(60, width - 60)
        by = random.randint(60, height - 60)
        br = random.randint(2, 5)
        for dy in range(-br, br + 1):
            for dx in range(-br, br + 1):
                nx, ny = bx + dx, by + dy
                if 0 <= nx < width and 0 <= ny < height:
                    if dx * dx + dy * dy <= br * br:
                        r, g, b = pixels[nx, ny]
                        factor = random.uniform(0.7, 0.85)
                        pixels[nx, ny] = (
                            int(r * factor),
                            int(g * factor),
                            int(b * factor),
                        )

    return img


def draw_red_lines(width, height, col_count=8):
    """在独立透明层上绘制红色栏线，返回 (Image, bbox)"""
    content_left = MARGIN_LEFT
    content_right = width - MARGIN_RIGHT
    content_top = MARGIN_TOP
    content_bottom = height - MARGIN_BOTTOM
    content_width = content_right - content_left
    col_width = content_width / col_count

    # 透明层
    overlay = Image.new("RGBA", (width, height), (0, 0, 0, 0))
    draw = ImageDraw.Draw(overlay)
    line_color = (*RED_LINE, RED_LINE_ALPHA)

    # 外框（粗线）
    draw.line([(content_left, content_top), (content_right, content_top)], fill=line_color, width=OUTER_LINE_W)
    draw.line([(content_left, content_bottom), (content_right, content_bottom)], fill=line_color, width=OUTER_LINE_W)
    draw.line([(content_left, content_top), (content_left, content_bottom)], fill=line_color, width=OUTER_LINE_W)
    draw.line([(content_right, content_top), (content_right, content_bottom)], fill=line_color, width=OUTER_LINE_W)

    # 内部竖栏线（细线）
    for i in range(1, col_count):
        x = content_left + i * col_width
        draw.line([(x, content_top), (x, content_bottom)], fill=line_color, width=INNER_LINE_W)

    return overlay, (content_left, content_top, content_right, content_bottom)


def draw_vertical_text(draw, text, font, col_x, col_top, line_height, fill=BLACK_INK):
    """在一列中竖排绘制文字（从上到下）"""
    y = col_top
    for char in text:
        if y + line_height > HEIGHT - MARGIN_BOTTOM:
            break
        bbox = font.getbbox(char)
        char_width = bbox[2] - bbox[0]
        # 居中绘制在列中，加随机微调模拟手写
        jx = random.randint(-JITTER_XY, JITTER_XY) if JITTER_XY else 0
        jy = random.randint(-JITTER_XY, JITTER_XY) if JITTER_XY else 0
        cx = col_x - char_width // 2 + jx
        draw.text((cx, y + jy), char, font=font, fill=fill)
        y += line_height + random.randint(-1, 1)
    return y


def wrap_text(text, max_chars_per_line=20):
    """将文本按指定宽度折行"""
    lines = []
    for para in text.split("\n"):
        para = para.strip()
        if not para:
            lines.append("")
            continue
        for i in range(0, len(para), max_chars_per_line):
            lines.append(para[i : i + max_chars_per_line])
    return lines


def main():
    parser = argparse.ArgumentParser(description="生成传统侨批书信图片")
    parser.add_argument("--output", "-o", required=True, help="输出图片路径")
    parser.add_argument("--recipient", default="", help="收信人称呼")
    parser.add_argument("--body", required=True, help="正文内容")
    parser.add_argument("--sender", default="", help="寄信人署名")
    parser.add_argument("--font", default="", help="自定义字体路径（默认自动查找系统中文字体）")
    args = parser.parse_args()

    # 加载字体：优先 --font 参数 > 内置手写体 > 系统中文字体
    script_dir = os.path.dirname(os.path.abspath(__file__))
    bundled_font = os.path.join(script_dir, "..", "fonts", "ToneOZ-Tsuipita-TC.ttf")

    if args.font and os.path.exists(args.font):
        FONT_PATH = args.font
    elif os.path.exists(bundled_font):
        FONT_PATH = bundled_font
    else:
        FONT_PATH = find_chinese_font()

    if not FONT_PATH:
        print("警告：未找到中文字体", file=sys.stderr)
        body_font = ImageFont.load_default()
    else:
        print(f"使用字体：{FONT_PATH}")
        try:
            body_font = ImageFont.truetype(FONT_PATH, size=FONT_SIZE)
        except Exception:
            body_font = ImageFont.load_default()

    # 创建纸张背景
    paper = create_aged_paper(WIDTH, HEIGHT)

    # 创建 RGBA 内容层（栏线 + 文字都画在这里，半透明让纸张纹理透出）
    content_layer = Image.new("RGBA", (WIDTH, HEIGHT), (0, 0, 0, 0))
    ctx = ImageDraw.Draw(content_layer)

    # 绘制红色栏线
    line_overlay, (content_left, _, content_right, _) = draw_red_lines(WIDTH, HEIGHT, col_count=8)
    content_layer = Image.alpha_composite(content_layer, line_overlay)
    ctx = ImageDraw.Draw(content_layer)

    content_width = content_right - content_left
    col_count = 8
    col_width = content_width / col_count

    # 收信人（最右列顶部）
    current_col = 0  # 最右列
    col_top = MARGIN_TOP + TEXT_TOP_PAD
    if args.recipient:
        col_x = content_right - col_width * (current_col + 0.5)
        draw_vertical_text(ctx, args.recipient.replace(" ", ""), body_font, col_x, col_top, LINE_HEIGHT)
        current_col += 1

    # 正文（新开一列，从右向左排列），每列字符数根据可用高度动态计算
    max_chars_per_col = (HEIGHT - MARGIN_TOP - MARGIN_BOTTOM - TEXT_TOP_PAD) // LINE_HEIGHT
    body_lines = wrap_text(args.body, max_chars_per_line=max_chars_per_col)
    col_top = MARGIN_TOP + TEXT_TOP_PAD

    for line in body_lines:
        if line == "":
            col_top += LINE_HEIGHT
            continue

        col_x = content_right - col_width * (current_col + 0.5)
        if current_col >= col_count:
            break

        draw_vertical_text(ctx, line, body_font, col_x, col_top, LINE_HEIGHT)
        current_col += 1

    # 寄信人（左下角），从底部向上推算起始位置避免越界
    if args.sender:
        sender_chars = args.sender.replace(" ", "")
        text_height = len(sender_chars) * LINE_HEIGHT
        col_center = content_left + col_width * 0.5  # 列中轴线
        sender_y = HEIGHT - MARGIN_BOTTOM - text_height
        for char in sender_chars:
            char_width = body_font.getbbox(char)[2] - body_font.getbbox(char)[0]
            jx = random.randint(-JITTER_XY, JITTER_XY) if JITTER_XY else 0
            jy = random.randint(-JITTER_XY, JITTER_XY) if JITTER_XY else 0
            char_x = col_center - char_width // 2 + jx
            ctx.text((char_x, sender_y + jy), char, font=body_font, fill=BLACK_INK)
            sender_y += LINE_HEIGHT + random.randint(-1, 1)

    # 叠加内容层到纸张
    paper = paper.convert("RGBA")
    paper = Image.alpha_composite(paper, content_layer)
    img = paper.convert("RGB")

    # 保存
    ext = os.path.splitext(args.output)[1].lower()
    if ext not in (".png", ".jpg", ".jpeg"):
        args.output += ".png"
    img.save(args.output, quality=95)
    print(f"侨批图片已生成：{args.output}")


if __name__ == "__main__":
    main()
