// ─────────────────────────────────────────────────────────────
// 高雄市友善營業場所 宣傳片｜時間軸（單一真實來源）
// 畫面（promo.html）與配樂（music.py）都讀這一份。
// 改節奏：改 bpm；改場景長度：改 beats（整數拍，場景切換會落在重拍）。
// chords：每個場景的和弦（每 4 拍換一個，循環）；energy：0=安靜 1=鋪陳 2=完整＋主旋律
// ─────────────────────────────────────────────────────────────
window.PROJECT = {
  bpm: 84,
  crossfade: 0.5,   // 場景交疊秒數（以切點為中心）
  tail: 1.5,        // 片尾延長秒數（最後和弦的尾音）
  scenes: [
    { id: 's1',    beats: 8,  name: '開場｜一扇門、一道台階', chords: ['Am', 'F'],        energy: 0 },
    { id: 's2',    beats: 9,  name: '人物｜每一天都有人這樣出門', chords: ['C', 'G', 'Am'], energy: 1 },
    { id: 's3',    beats: 6,  name: '轉折｜只是一個友善的空間', chords: ['F', 'G'],        energy: 1 },
    { id: 's4',    beats: 9,  name: '標章｜高雄市友善營業場所', chords: ['C', 'G', 'Am'],  energy: 2, accent: 1 },
    { id: 'sStat', beats: 7,  name: '數字｜285 家', chords: ['F', 'C'],                    energy: 2 },
    { id: 's5',    beats: 7,  name: '類別｜餐飲・診所・藥局・商店', chords: ['G', 'Am'],     energy: 2 },
    { id: 'sStd',  beats: 11, name: '標準｜友善環境＋友善措施', chords: ['F', 'C', 'G'],    energy: 2 },
    { id: 's6',    beats: 12, name: '店家特寫（4 家，每家 3 拍）', chords: ['C', 'G', 'Am'], energy: 2 },
    { id: 's7',    beats: 10, name: '店家牆｜每個角落', chords: ['F', 'G', 'C'],            energy: 2 },
    { id: 's8',    beats: 7,  name: '訊息｜多想一步的心意', chords: ['Am', 'F'],             energy: 0 },
    { id: 'sProc', beats: 9,  name: '給店家｜認證 5 步驟', chords: ['C', 'G', 'Am'],        energy: 2, accent: 0 },
    { id: 'sBen',  beats: 9,  name: '給店家｜加入的好處', chords: ['F', 'C', 'G'],          energy: 2 },
    { id: 's9',    beats: 12, name: '片尾｜官網・FB・分享', chords: ['F', 'G', 'C'],        energy: 1, accent: 0.5, end: true },
  ],
};
