"""アイコン生成と index.html の取り込み。
正のソースは ../../gas/kagenui_mobile/index.html（GASの画面と同じファイル）。
  python build.py            … index.html を取り込む（API_URL を埋める）
  python build.py --icons    … アイコンも作り直す
"""
import pathlib, re, sys

HERE = pathlib.Path(__file__).parent
SRC = HERE.parent.parent / "gas" / "kagenui_mobile" / "index.html"
API_URL = (HERE / "api_url.txt").read_text(encoding="utf-8").strip() if (HERE / "api_url.txt").exists() else ""


def icons():
    from PIL import Image, ImageDraw
    def draw(size, pad):
        S = 4 * size  # 4倍で描いて縮小（なめらかに）
        im = Image.new("RGB", (S, S), "#0a0c10")
        d = ImageDraw.Draw(im)
        k = (S - 2 * pad * 4) / 32.0
        o = pad * 4
        P = lambda x, y: (o + x * k, o + y * k)
        w = int(2.4 * k)
        d.rounded_rectangle([P(4, 4), P(28, 28)], radius=6 * k, outline="#5eead4", width=w)
        d.line([P(8, 24), P(24, 8)], fill="#5eead4", width=w)
        for x in (8, 24):
            y = 24 if x == 8 else 8
            r = w / 2
            d.ellipse([P(x, y)[0] - r, P(x, y)[1] - r, P(x, y)[0] + r, P(x, y)[1] + r], fill="#5eead4")
        dim = (94 // 2 + 10, 234 // 2 + 10, 212 // 2 + 10)
        d.line([P(11, 13), P(15, 13)], fill=dim, width=int(2 * k))
        d.line([P(17, 19), P(21, 19)], fill=dim, width=int(2 * k))
        return im.resize((size, size), Image.LANCZOS)
    draw(192, 0).save(HERE / "icon-192.png")
    draw(512, 0).save(HERE / "icon-512.png")
    draw(180, 6).save(HERE / "icon-180.png")
    draw(512, 64).save(HERE / "icon-maskable-512.png")


def page():
    s = SRC.read_text(encoding="utf-8")
    if API_URL:
        s = s.replace('var API_URL = "__API_URL__";', 'var API_URL = "%s";' % API_URL)
    (HERE / "index.html").write_text(s, encoding="utf-8", newline="\n")
    print("index.html <-", SRC, "API_URL", "set" if API_URL else "未設定")


if "--icons" in sys.argv:
    icons()
page()
