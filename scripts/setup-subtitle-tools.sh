#!/usr/bin/env bash
# One-time setup: ffmpeg, faster-whisper, Pillow, jf open 粉圓 (jf-openhuninn) font.
set -euo pipefail

FONT_URL="https://github.com/justfont/open-huninn-font/releases/download/v2.1/jf-openhuninn-2.1.ttf"
case "$(uname -s)" in
  Darwin) FONT_DIR="$HOME/Library/Fonts" ;;
  *)      FONT_DIR="$HOME/.local/share/fonts" ;;
esac

# 1. ffmpeg
if ! command -v ffmpeg >/dev/null; then
  if   command -v brew    >/dev/null; then brew install ffmpeg
  elif command -v apt-get >/dev/null; then (sudo -n true 2>/dev/null && SUDO=sudo || SUDO=; $SUDO apt-get update -y || true;  $SUDO apt-get install -y ffmpeg)
  elif command -v dnf     >/dev/null; then sudo dnf install -y ffmpeg
  elif command -v pacman  >/dev/null; then sudo pacman -S --noconfirm ffmpeg
  else echo "請手動安裝 ffmpeg" >&2; exit 1; fi
fi

# 2. faster-whisper + Pillow
if command -v uv >/dev/null; then uv pip install --system faster-whisper "pillow>=12.1.0" 2>/dev/null || uv pip install faster-whisper "pillow>=12.1.0"
else python3 -m pip install --upgrade faster-whisper "pillow>=12.1.0"; fi

# 3. 粉圓 font
mkdir -p "$FONT_DIR"
[ -f "$FONT_DIR/jf-openhuninn-2.1.ttf" ] || curl -fL "$FONT_URL" -o "$FONT_DIR/jf-openhuninn-2.1.ttf"
command -v fc-cache >/dev/null && fc-cache -f "$FONT_DIR" || true

echo "== 驗證 =="
ffmpeg -version | head -1
python3 -c "import faster_whisper, PIL; print('faster-whisper OK, Pillow', PIL.__version__)"
ls -l "$FONT_DIR/jf-openhuninn-2.1.ttf"
