"""打包工具
1) fonts：從完整 Google Fonts 子集（--src）只挑出影片用到的字，寫入 fonts/
2) bundle：把 promo.html + scenes.js + 圖片 + 字型 + 配樂 打包成單一 HTML（可直接在瀏覽器開）

用法：
  python3 build_preview.py fonts --src <下載的 fonts 目錄>
  python3 build_preview.py bundle           → output/preview.html
"""
import base64, json, re, shutil, subprocess, sys, os

HERE = os.path.dirname(os.path.abspath(__file__))
os.chdir(HERE)


def used_chars():
    txt = open('promo.html', encoding='utf-8').read() + open('scenes.js', encoding='utf-8').read()
    return {ord(c) for c in txt} | set(range(0x20, 0x7f))


def ranges(ur):
    for part in ur.split(','):
        part = part.strip().replace('U+', '')
        if '-' in part:
            a, b = part.split('-'); yield int(a, 16), int(b, 16)
        elif '?' in part:
            yield int(part.replace('?', '0'), 16), int(part.replace('?', 'f'), 16)
        else:
            yield int(part, 16), int(part, 16)


def build_fonts(src):
    css = open(os.path.join(src, 'fonts.css'), encoding='utf-8').read()
    chars = used_chars(); keep = []
    for block in re.findall(r'(?:/\*[^*]*\*/\s*)?@font-face\s*{[^}]*}', css):
        ur = re.search(r'unicode-range:\s*([^;]+);', block)
        if ur and not any(a <= c <= b for a, b in ranges(ur.group(1)) for c in chars):
            continue
        f = re.search(r'url\(([^)]+)\)', block).group(1)
        shutil.copy(os.path.join(src, f), os.path.join('fonts', f))
        keep.append(re.sub(r'/\*[^*]*\*/\s*', '', block))
    open('fonts/fonts.css', 'w', encoding='utf-8').write('\n'.join(keep))
    print(f'fonts: kept {len(keep)} subsets')


def b64(path, mime):
    return f'data:{mime};base64,' + base64.b64encode(open(path, 'rb').read()).decode()


def bundle():
    ff = os.environ.get('FF', 'ffmpeg')
    subprocess.run([ff, '-y', '-loglevel', 'error', '-i', 'output/music.wav', '-c:a', 'aac', '-b:a', '160k', 'output/music.m4a'], check=True)
    html = open('promo.html', encoding='utf-8').read()
    css = open('fonts/fonts.css', encoding='utf-8').read()
    css = re.sub(r'url\(([^)]+\.woff2)\)', lambda m: f"url({b64('fonts/' + m.group(1), 'font/woff2')})", css)
    html = html.replace('<link rel="stylesheet" href="fonts/fonts.css">', f'<style>{css}</style>')
    html = html.replace('<script src="scenes.js"></script>',
                        '<script>' + open('scenes.js', encoding='utf-8').read() +
                        f"\nwindow.MUSIC_SRC='{b64('output/music.m4a', 'audio/mp4')}';</script>")
    amap = {}
    for f in sorted(os.listdir('assets')):
        amap[f] = b64(f'assets/{f}', 'image/png' if f.endswith('.png') else 'image/jpeg')
        html = html.replace(f'"assets/{f}"', f'"{amap[f]}"')
    html = html.replace('<script>\nconst Q', '<script>\nwindow.ASSETS=' + json.dumps(amap) + ';\nconst Q', 1)
    open('output/preview.html', 'w', encoding='utf-8').write(html)
    print(f'bundle: output/preview.html {os.path.getsize("output/preview.html") / 1e6:.1f} MB')


if __name__ == '__main__':
    if sys.argv[1] == 'fonts':
        build_fonts(sys.argv[sys.argv.index('--src') + 1])
    else:
        bundle()
