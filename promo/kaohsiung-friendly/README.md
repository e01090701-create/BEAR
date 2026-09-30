# 高雄市友善營業場所｜宣傳片工程檔（124 BPM 卡點版）

一份時間軸（`scenes.js`）同時驅動畫面與配樂：場景切點、文字重擊、爆點（閃白＋震動＋RGB 殘影）、轉場音效都寫在同一個地方，改節奏或場景長度時，畫面和音樂一起跟著變，不會跑拍。

## 分鏡（14 場景、156 拍、約 77 秒）
| # | 場景 | 拍 | 段落 | 重點 |
|---|---|---|---|---|
| 1 | 開場 | 16 | Intro | 「一扇門／一道台階／一個門檻」逐拍重擊 → 輪椅被台階擋住（爆點）→「這就是一段距離」→「直到——」→ 全靜音半拍 |
| 2 | 標章 | 12 | Drop | 閃白＋標章蓋章登場、彩帶、放射光、巨型滾動字 |
| 3 | 台階變斜坡 | 8 | Drop | 動畫：台階變形成斜坡，輪椅開上去，愛心爆開 |
| 4 | 人物 | 16 | Drop | 鏡頭每 3 拍推近一位人物，標籤卡點 |
| 5 | 285 家 | 8 | Drop | 數字跟著 16 分音計數聲跳動，第 4 拍爆點 |
| 6 | 類別 | 8 | Drop | 每 2 拍一個斜切色塊（餐飲／診所／藥局／一般商店） |
| 7 | 友善標準 | 16 | Drop | 10 項一拍一個 → 第 12 拍總覽爆點 |
| 8 | 店家 | 16 | Drop | 4 家特寫各 3 拍 → 8 張照片按 8 分音連甩 |
| 9 | 店家牆 | 8 | Drop | 8 家卡片逐一蓋章 |
| 10 | 喘息 | 8 | Break | 「更是願意多想一步的心意」 |
| 11 | 給店家 | 8 | Build | 「你的店／也能是／下一個／友善角落」加速重擊 → 靜音半拍 |
| 12 | 認證 5 步驟 | 8 | Drop | 一拍一步 |
| 13 | 好處 | 8 | Drop | 4 項好處 8 分音滑入 → 5,000 元計數，第 4 拍爆點 |
| 14 | 片尾 | 16 | Outro | 標章、官網、FB、分享 → 第 12 拍最後一擊

| 檔案 | 用途 |
|---|---|
| `scenes.js` | **時間軸**：BPM、每個場景的拍數、和弦、配器強度（改節奏、改長度都在這裡） |
| `promo.html` | 畫面與文字（直接用瀏覽器打開就是預覽器）；`?v=1` 是 9:16 直式 |
| `music.py` | 配樂產生器（電子流行：四拍大鼓、拍手、側鏈壓縮和弦、pluck 主旋律、riser、爆點），讀 `scenes.js` → `output/music.wav`＋`output/music_events.json`（每個鼓點/爆點的精確時間，供對拍檢查） |
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
- **換字**：`promo.html` 搜尋該文字直接改。店家清單在 `STORES`，特寫用哪幾家在 `FEAT`，友善標準在 `STD`。
- **換鏡頭／照片**：把新圖放進 `assets/`，在 `STORES` 加一列（最後一欄是檔名）。
- **改節奏**：`scenes.js` 的 `bpm`；**改場景長度**：該場景的 `beats`；**加爆點**：在 `hits` 加拍數（音樂和畫面同時生效）。
- 動畫時間寫法：`data-a="第幾拍 秒數 效果"`、`data-u="第幾拍"`（到這拍消失）。效果：slam（重擊）、stamp（蓋章）、pop、up、left、blur、wipe、chars（逐字）、cut。
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
