#!/usr/bin/env python3
"""説明動画用の背景・共通部品 PNG を生成する。

依存: Pillow
例:
    python3 make_template.py --out work/template --chapters 概要 準備 操作 まとめ --current 2
"""

import argparse
import json
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

DEFAULT = {
    "width": 1920,
    "height": 1080,
    "colors": {
        "background": "#F5F7FA",
        "panel": "#E6ECF5",
        "frame": "#C3CEDD",
        "screen": "#FFFFFF",
        "ink": "#1B2A3A",
        "muted": "#5B6B7F",
        "accent": "#2F6FDE",
        "line": "#D8E0EA",
        "subtitle_band": "#111315",
        "title_bg": "#1F4FA8",
        "title_text": "#FFFFFF",
        "title_sub": "#DCE7FA",
    },
    "panel": {"x": 1296},
    "subtitle_band": {"y": 930},
    "screen": {"x": 1407, "y": 92, "width": 362, "height": 804, "radius": 28},
    "header": {"brand": "HOW TO", "subtitle": "操作説明", "x": 76, "y": 40, "rule_y": 92, "rule_width": 1142},
    "progress": {"x": 76, "y": 868, "width": 1124, "height": 5, "gap": 20},
    "fonts": [
        "/System/Library/Fonts/ヒラギノ角ゴシック W6.ttc",
        "/System/Library/Fonts/Hiragino Sans GB.ttc",
        "/usr/share/fonts/opentype/noto/NotoSansCJK-Bold.ttc",
        "/usr/share/fonts/noto-cjk/NotoSansCJK-Bold.ttc",
    ],
}


def deep_merge(base, override):
    for key, value in override.items():
        if isinstance(value, dict) and isinstance(base.get(key), dict):
            deep_merge(base[key], value)
        else:
            base[key] = value
    return base


def load_font(cfg, size):
    for path in cfg["fonts"]:
        if Path(path).exists():
            return ImageFont.truetype(path, size)
    print("警告: 日本語フォントが見つからないため既定フォントを使います。--config の fonts を指定してください。")
    return ImageFont.load_default(size)


def background(cfg):
    c = cfg["colors"]
    img = Image.new("RGB", (cfg["width"], cfg["height"]), c["background"])
    d = ImageDraw.Draw(img)
    d.rectangle([cfg["panel"]["x"], 0, cfg["width"], cfg["height"]], fill=c["panel"])
    d.rectangle([0, cfg["subtitle_band"]["y"], cfg["width"], cfg["height"]], fill=c["subtitle_band"])
    return img


def portrait_layout(cfg):
    img = background(cfg)
    d = ImageDraw.Draw(img)
    s = cfg["screen"]
    box = [s["x"], s["y"], s["x"] + s["width"], s["y"] + s["height"]]
    d.rounded_rectangle([box[0] - 8, box[1] - 8, box[2] + 8, box[3] + 8], s["radius"] + 8, fill=cfg["colors"]["frame"])
    d.rounded_rectangle(box, s["radius"], fill=cfg["colors"]["screen"])
    return img


def components(cfg, chapters, current):
    c = cfg["colors"]
    img = Image.new("RGBA", (cfg["width"], cfg["height"]), (0, 0, 0, 0))
    d = ImageDraw.Draw(img)
    h = cfg["header"]
    brand_font = load_font(cfg, 27)
    d.text((h["x"], h["y"]), h["brand"], font=brand_font, fill=c["accent"])
    brand_w = d.textlength(h["brand"], font=brand_font)
    d.text((h["x"] + brand_w + 24, h["y"] + 4), h["subtitle"], font=load_font(cfg, 19), fill=c["muted"])
    d.line([h["x"], h["rule_y"], h["x"] + h["rule_width"], h["rule_y"]], fill=c["line"], width=2)

    if chapters:
        p = cfg["progress"]
        n = len(chapters)
        seg = (p["width"] - p["gap"] * (n - 1)) / n
        for i in range(n):
            x0 = p["x"] + i * (seg + p["gap"])
            color = c["accent"] if i < current else c["line"]
            d.rectangle([x0, p["y"], x0 + seg, p["y"] + p["height"]], fill=color)
    return img


def title_card(cfg, title, sub):
    c = cfg["colors"]
    img = Image.new("RGB", (cfg["width"], cfg["height"]), c["title_bg"])
    d = ImageDraw.Draw(img)
    cx, cy = cfg["width"] / 2, cfg["height"] / 2
    lines = title.split("\\n")
    font = load_font(cfg, 88)
    line_h = 104
    top = cy - line_h * len(lines) / 2 - (40 if sub else 0)
    for i, line in enumerate(lines):
        d.text((cx, top + i * line_h), line, font=font, fill=c["title_text"], anchor="mt")
    if sub:
        d.text((cx, top + len(lines) * line_h + 60), sub, font=load_font(cfg, 44), fill=c["title_sub"], anchor="mt")
    return img


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--out", required=True, help="出力ディレクトリ")
    ap.add_argument("--config", help="DEFAULT を上書きする JSON ファイル")
    ap.add_argument("--chapters", nargs="*", default=[], help="章名の一覧（進捗バーの分割数になる）")
    ap.add_argument("--current", type=int, default=0, help="現在の章番号（1始まり）。0 なら全章分を生成")
    ap.add_argument("--title", default="動画のタイトル", help="冒頭タイトル（\\n で改行）")
    ap.add_argument("--title-sub", default="", help="冒頭タイトルの補足")
    args = ap.parse_args()

    cfg = json.loads(json.dumps(DEFAULT))
    if args.config:
        deep_merge(cfg, json.loads(Path(args.config).read_text(encoding="utf-8")))

    out = Path(args.out)
    out.mkdir(parents=True, exist_ok=True)
    background(cfg).save(out / "background.png")
    portrait_layout(cfg).save(out / "portrait-layout.png")
    title_card(cfg, args.title, args.title_sub).save(out / "title.png")

    targets = [args.current] if args.current else list(range(1, len(args.chapters) + 1)) or [0]
    for ch in targets:
        components(cfg, args.chapters, ch).save(out / f"components-ch{ch}.png")

    print(f"生成しました: {out}")
    for f in sorted(out.glob("*.png")):
        print(f"  {f.name}")


if __name__ == "__main__":
    main()
