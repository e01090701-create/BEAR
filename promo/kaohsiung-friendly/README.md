# 高雄市友善營業場所｜宣傳片工程檔

一份時間軸，同時驅動畫面與配樂，所以改節奏或場景長度時，畫面和音樂都會跟著改，不會跑拍。

| 檔案 | 用途 |
|---|---|
| `scenes.js` | **時間軸**：BPM、每個場景的拍數、和弦、配器強度（改節奏、改長度都在這裡） |
| `promo.html` | 畫面與文字（直接用瀏覽器打開就是預覽器）；`?v=1` 是 9:16 直式 |
| `music.py` | 配樂產生器，讀 `scenes.js` → `output/music.wav`（同時輸出音符時間表，供對拍檢查） |
| `render.js` | 逐格渲染成 MP4，並合成配樂 |
| `build_preview.py` | 打包成單一 HTML 預覽檔；字型子集化 |
| `assets/` | 圖片素材（店家照片、標章、插畫） |
| `fonts/` | Noto Sans TC／霞鶩文楷 TC／Poppins（只保留用到的字） |

## 預覽（可暫停、逐格、逐拍、循環單一場景）
打開 `promo.html`，或打包後的 `output/preview.html`。
- 空白鍵：播放/暫停　←/→：逐格　Shift+←/→：逐拍　[ ]：上/下一場景
- L：循環目前場景　M：節拍器（檢查對拍）　也可以切換直式/橫式
- 網址參數：`?scene=4` 直接循環第 4 場景；`?t=12.5` 從 12.5 秒開始

## 常見修改
- **換字**：`promo.html` 搜尋該文字直接改。店家清單在 `STORES`，友善標準在 `ENV`／`ACT`，認證流程在 `PROC`，好處在 `BEN`。
- **換鏡頭／照片**：把新圖放進 `assets/`，改 `STORES` 或 `FEAT`（特寫用哪幾家）。
- **改節奏**：`scenes.js` 的 `bpm`；**改場景長度**：該場景的 `beats`。場景內的動畫時間（`data-a="拍數 秒數 效果"`）是以「拍」為單位，會自動跟著節奏走。
- 新增了文字，要重跑 `build_preview.py fonts --src <完整字型目錄>`，確保字型子集有收錄新字。

## 匯出
```bash
pip install numpy imageio-ffmpeg
export FF=$(python3 -c "import imageio_ffmpeg;print(imageio_ffmpeg.get_ffmpeg_exe())")
python3 music.py                        # 產生配樂
python3 build_preview.py bundle         # 單檔預覽 output/preview.html
node render.js h output/friendly_16x9.mp4   # 橫式 1920×1080
node render.js v output/friendly_9x16.mp4   # 直式 1080×1920（Reels／Shorts／限動）
```
需要 Node.js + Playwright（Chromium）。
