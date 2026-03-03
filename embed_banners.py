"""
embed_banners.py
────────────────
SVGバナーをBase64に変換し、article.html の <img src="banners/..."> を
data URI に直接差し替えるスクリプト。

使い方:
    python embed_banners.py

出力:
    article_embedded.html  ← 画像が全部コードに埋め込まれた完全単体ファイル
"""

import base64
import re
from pathlib import Path

# ── パス設定 ───────────────────────────────────────────────
HTML_INPUT  = Path("article.html")
HTML_OUTPUT = Path("article_embedded.html")
BANNER_DIR  = Path("banners")

# ── SVG → Base64 data URI に変換 ──────────────────────────
def svg_to_data_uri(svg_path: Path) -> str:
    raw = svg_path.read_bytes()
    b64 = base64.b64encode(raw).decode("utf-8")
    return f"data:image/svg+xml;base64,{b64}"

# ── HTMLを読み込み ─────────────────────────────────────────
html = HTML_INPUT.read_text(encoding="utf-8")

# ── 全バナーファイルを検索して差し替え ─────────────────────
# 対象パターン: src="banners/ファイル名.svg"
pattern = re.compile(r'src="(banners/[^"]+\.svg)"')
replaced = 0

def replacer(match):
    global replaced
    rel_path = match.group(1)          # "banners/banner_abm_guide.svg"
    svg_file = BANNER_DIR / Path(rel_path).name

    if not svg_file.exists():
        print(f"  ⚠️  見つかりません: {svg_file}")
        return match.group(0)          # そのまま残す

    data_uri = svg_to_data_uri(svg_file)
    size_kb   = svg_file.stat().st_size // 1024
    replaced += 1
    print(f"  ✓  {svg_file.name}  ({size_kb} KB)")
    return f'src="{data_uri}"'

html_out = pattern.sub(replacer, html)

# ── 保存 ───────────────────────────────────────────────────
HTML_OUTPUT.write_text(html_out, encoding="utf-8")

out_kb = HTML_OUTPUT.stat().st_size // 1024
print(f"\n✅ {replaced} 枚の画像を埋め込みました")
print(f"📄 出力: {HTML_OUTPUT}  ({out_kb} KB)")
