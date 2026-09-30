// ─────────────────────────────────────────────────────────────
// 高雄市友善營業場所 宣傳片｜時間軸（單一真實來源）
// 畫面（promo.html）與配樂（music.py）都讀這一份 → 永遠對拍。
//
// bpm     ：節奏。改了之後畫面動畫、轉場、音效全部跟著走。
// beats   ：場景長度（拍）。場景切點一定落在拍上。
// mode    ：配樂段落  intro｜build｜drop｜break｜outro
// chords  ：和弦，每 4 拍換一個（循環）
// tr      ：進場轉場  cut｜flash｜wipe｜zoom｜fade
// hits    ：爆點（場景內第幾拍）→ 音樂打「重擊＋鈸」，畫面同時閃白＋震動＋RGB 殘影
// sfx     ：[拍, 音效]  slam（文字重擊）｜whoosh（在「拍+0.5」達到峰值，配轉場）｜ticksN（N 拍的 16 分音計數聲）
//           riserN（N 拍漸強）｜rollN（N 拍小鼓滾奏）｜gap（全靜音到場景結束，製造 Drop 前的停頓）
// ─────────────────────────────────────────────────────────────
window.PROJECT = {
  bpm: 124,
  tail: 1.6,
  scenes: [
    { id: 'hook',   beats: 16, name: '開場｜一道台階＝一段距離', mode: 'intro', chords: ['Am', 'F', 'C', 'G'], tr: 'cut',
      hits: [8], sfx: [[0, 'slam'], [2, 'slam'], [4, 'slam'], [10, 'slam'], [11, 'slam'], [13, 'slam'], [8, 'riser8'], [12, 'roll4'], [15.5, 'gap']] },
    { id: 'logo',   beats: 12, name: '爆點｜標章登場', mode: 'drop', chords: ['Am', 'F', 'C'], tr: 'flash', hits: [0] },
    { id: 'ramp',   beats: 8,  name: '動畫｜台階變斜坡', mode: 'drop', chords: ['G', 'Am'], tr: 'wipe', hits: [5], sfx: [[-0.5, 'whoosh']] },
    { id: 'people', beats: 16, name: '人物｜鏡頭卡點推近', mode: 'drop', chords: ['F', 'C', 'G', 'Am'], tr: 'wipe',
      sfx: [[-0.5, 'whoosh'], [1.5, 'whoosh'], [4.5, 'whoosh'], [7.5, 'whoosh'], [10.5, 'whoosh'], [13.5, 'whoosh']] },
    { id: 'stat',   beats: 8,  name: '數字｜285 家', mode: 'drop', chords: ['F', 'G'], tr: 'cut', hits: [4], sfx: [[0, 'ticks4']] },
    { id: 'cats',   beats: 8,  name: '類別｜四連切', mode: 'drop', chords: ['Am', 'F'], tr: 'wipe',
      sfx: [[-0.5, 'whoosh'], [1.5, 'whoosh'], [3.5, 'whoosh'], [5.5, 'whoosh']] },
    { id: 'std',    beats: 16, name: '標準｜10 項一拍一個', mode: 'drop', chords: ['C', 'G', 'Am', 'F'], tr: 'zoom', hits: [12] },
    { id: 'stores', beats: 16, name: '店家｜特寫＋照片連甩', mode: 'drop', chords: ['F', 'C', 'G', 'Am'], tr: 'flash', hits: [0],
      sfx: [[2.5, 'whoosh'], [5.5, 'whoosh'], [8.5, 'whoosh']] },
    { id: 'wall',   beats: 8,  name: '店家牆｜每個角落', mode: 'drop', chords: ['F', 'G'], tr: 'cut', hits: [0] },
    { id: 'break',  beats: 8,  name: '喘息｜多想一步的心意', mode: 'break', chords: ['F', 'C'], tr: 'fade' },
    { id: 'biz',    beats: 8,  name: 'Build｜給店家的邀請', mode: 'build', chords: ['F', 'G'], tr: 'cut',
      hits: [6], sfx: [[0, 'riser8'], [4, 'roll4'], [7.5, 'gap']] },
    { id: 'steps',  beats: 8,  name: '認證 5 步驟', mode: 'drop', chords: ['Am', 'F'], tr: 'flash', hits: [0] },
    { id: 'ben',    beats: 8,  name: '好處｜最高 5,000 元', mode: 'drop', chords: ['C', 'G'], tr: 'wipe', hits: [4], sfx: [[-0.5, 'whoosh'], [3, 'ticks1']] },
    { id: 'outro',  beats: 16, name: '片尾｜官網・FB・分享', mode: 'outro', chords: ['F', 'G', 'Am', 'C'], tr: 'flash', hits: [0, 12] },
  ],
};
