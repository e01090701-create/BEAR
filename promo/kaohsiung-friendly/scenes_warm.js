// ─────────────────────────────────────────────────────────────
// 高雄市友善營業場所 宣傳片｜溫馨版時間軸（promo.html?style=warm）
// 畫面與配樂（python3 music.py warm）共用這一份 → 永遠對拍。
//
// mode：soft（鋼琴＋弦樂鋪底）｜swell（加入低音、主旋律、輕鼓）｜break（只剩鋼琴）｜end（收尾）
// hits：溫柔的高光點 → 音樂打音樂盒琶音，畫面出現柔光暈，不震動
// 場景長度（beats）可以加長，但不要短於場景內動畫用到的最後一拍
// ─────────────────────────────────────────────────────────────
(window.PROJECTS = window.PROJECTS || {}).warm = {
  style: 'warm',
  bpm: 90,
  tail: 2.6,
  scenes: [
    { id: 'hook',   beats: 14, name: '開場｜一道台階＝一段距離', mode: 'soft',  chords: ['C', 'Am', 'F', 'G'], tr: 'fade', hits: [8] },
    { id: 'logo',   beats: 12, name: '標章｜友你有我，從心出發', mode: 'swell', chords: ['C', 'G', 'Am'], tr: 'fade', hits: [0] },
    { id: 'ramp',   beats: 8,  name: '動畫｜台階變斜坡', mode: 'swell', chords: ['F', 'G'], tr: 'fade', hits: [5] },
    { id: 'people', beats: 16, name: '人物｜每一個人', mode: 'swell', chords: ['C', 'Em', 'F', 'G'], tr: 'fade' },
    { id: 'stat',   beats: 7,  name: '數字｜285 家', mode: 'swell', chords: ['Am', 'F'], tr: 'fade', hits: [4] },
    { id: 'cats',   beats: 8,  name: '類別｜就在你身邊', mode: 'swell', chords: ['C', 'G'], tr: 'fade' },
    { id: 'std',    beats: 14, name: '標準｜10 項友善指標', mode: 'swell', chords: ['F', 'C', 'Dm', 'G'], tr: 'fade', hits: [12] },
    { id: 'stores', beats: 16, name: '店家｜真實的友善', mode: 'swell', chords: ['C', 'Am', 'F', 'G'], tr: 'fade' },
    { id: 'wall',   beats: 7,  name: '店家牆｜每個角落', mode: 'swell', chords: ['F', 'G'], tr: 'fade' },
    { id: 'break',  beats: 8,  name: '心意｜多想一步', mode: 'break', chords: ['Am', 'F'], tr: 'fade' },
    { id: 'biz',    beats: 8,  name: '給店家的邀請', mode: 'soft',  chords: ['C', 'G'], tr: 'fade' },
    { id: 'steps',  beats: 7,  name: '認證 5 步驟', mode: 'swell', chords: ['F', 'G'], tr: 'fade' },
    { id: 'ben',    beats: 7,  name: '好處｜最高 5,000 元', mode: 'swell', chords: ['Am', 'F'], tr: 'fade', hits: [4] },
    { id: 'outro',  beats: 14, name: '片尾｜方熊 出品', mode: 'end', chords: ['F', 'G', 'C'], tr: 'fade', hits: [0, 12] },
  ],
};
