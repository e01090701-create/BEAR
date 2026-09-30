"""配樂產生器（124 BPM 電子流行卡點版）
讀 scenes.js 的同一份時間軸 → output/music.wav ＋ output/music_events.json（每個鼓點/爆點的精確時間，供對拍檢查）

段落（mode）：
  intro  濾波和弦＋輕鼓，文字重擊音效；後半 riser＋小鼓滾奏，最後半拍全靜音
  build  四拍大鼓＋riser＋滾奏，最後半拍全靜音
  drop   四拍大鼓、拍手、開/閉鈸、側鏈壓縮的 supersaw 和弦、低音、pluck 主旋律
  break  只有 pad＋鋼琴琶音
  outro  前 12 拍同 drop，最後一個爆點後只留餘韻
執行：python3 music.py   （需要 numpy、scipy、node）
"""
import json, subprocess, wave
import numpy as np
from scipy.signal import butter, sosfilt

proj = json.loads(subprocess.check_output(
    ['node', '-e', "global.window={};require('./scenes.js');console.log(JSON.stringify(window.PROJECT))"]))
SR = 44100
BEAT = 60 / proj['bpm']
TOTAL_B = sum(s['beats'] for s in proj['scenes'])
D = TOTAL_B * BEAT + proj['tail']
N = int(SR * (D + .5))
rng = np.random.default_rng(7)
EVENTS = []

# 三條匯流排：drums（不壓）、music（被大鼓側鏈壓縮）、fx（爆點/音效）
bus = {k: np.zeros((N, 2)) for k in ('drums', 'music', 'fx')}
kick_times = []
gaps = []
m2f = lambda m: 440 * 2 ** ((m - 69) / 12)
CH = {'Am': [57, 60, 64, 69], 'F': [53, 57, 60, 65], 'C': [55, 60, 64, 67], 'G': [55, 59, 62, 67]}
ROOT = {'Am': 45, 'F': 41, 'C': 48, 'G': 43}
LEAD = {'Am': [76, -1, 72, 76, 79, -1, 76, 74], 'F': [72, -1, 69, 72, 77, -1, 76, 72],
        'C': [72, -1, 67, 72, 76, -1, 74, 72], 'G': [71, -1, 67, 71, 74, -1, 79, 74]}


def put(name, sig, t, pan=0.0):
    i = int(round(t * SR))
    if i < 0: sig = sig[-i:]; i = 0
    j = min(N, i + len(sig))
    if j <= i: return
    s = sig[:j - i]
    if s.ndim == 1: s = np.stack([s * (1 - pan), s * (1 + pan)], 1)
    bus[name][i:j] += s


def lp(x, fc, order=2): return sosfilt(butter(order, min(fc, SR / 2 - 100), 'low', fs=SR, output='sos'), x)
def hp(x, fc, order=2): return sosfilt(butter(order, fc, 'high', fs=SR, output='sos'), x)
def bp(x, lo, hi): return sosfilt(butter(2, [lo, min(hi, SR / 2 - 100)], 'band', fs=SR, output='sos'), x)
noise = lambda n: rng.standard_normal(n)
T = lambda d: np.arange(int(d * SR)) / SR

# 帶限鋸齒波 wavetable
TAB = {h: sum(np.sin(2 * np.pi * k * np.arange(2048) / 2048) / k for k in range(1, h + 1)) * .6 for h in (40, 16, 7)}
def saw(f, n, ph=0.0):
    tab = TAB[40] if f < 450 else TAB[16] if f < 1300 else TAB[7]
    p = (ph + np.arange(n) * f / SR) % 1.0
    return tab[(p * 2048).astype(int)]


# ── 樂器 ──
def kick(t, amp=1.0):
    tt = T(.42); f = 48 + 150 * np.exp(-tt * 38)
    s = np.sin(2 * np.pi * np.cumsum(f) / SR) * np.exp(-tt * 7.5)
    s[:130] += noise(130) * .25 * np.linspace(1, 0, 130)
    put('drums', np.tanh(s * 1.6) * .9 * amp, t); kick_times.append(t); EVENTS.append((t, 'kick'))

def clap(t, amp=1.0):
    n = int(.25 * SR); tt = np.arange(n) / SR
    env = np.exp(-tt * 18) + sum((tt >= d) * np.exp(-(tt - d) * 140) * .8 for d in (0, .011, .022))
    put('drums', bp(noise(n), 900, 2600) * env * .42 * amp, t, 0.05); EVENTS.append((t, 'clap'))

def hat(t, open_=False, amp=1.0, pan=.2):
    n = int((.16 if open_ else .04) * SR); tt = np.arange(n) / SR
    put('drums', hp(noise(n), 7500) * np.exp(-tt * (22 if open_ else 110)) * (.16 if open_ else .10) * amp, t, pan)

def snare(t, amp=1.0, pitch=1.0):
    tt = T(.16)
    s = np.sin(2 * np.pi * 190 * pitch * tt) * np.exp(-tt * 30) * .5 + bp(noise(len(tt)), 1500, 8000) * np.exp(-tt * 26)
    put('drums', s * .35 * amp, t, -.05)

def impact(t, big=1.0):
    tt = T(2.6)
    boom = np.sin(2 * np.pi * np.cumsum(28 + 60 * np.exp(-tt * 5)) / SR) * np.exp(-tt * 1.6)
    crash = hp(noise(len(tt)), 3500) * np.exp(-tt * 1.4) * .22
    body = lp(noise(len(tt)), 900) * np.exp(-tt * 9) * .35
    put('fx', np.tanh((boom * .9 + crash + body) * 1.3) * .85 * big, t); EVENTS.append((t, 'impact'))

def slam(t):  # 文字重擊：低頻打擊＋短鈸
    tt = T(.6)
    s = np.sin(2 * np.pi * np.cumsum(40 + 90 * np.exp(-tt * 25)) / SR) * np.exp(-tt * 6)
    s += hp(noise(len(tt)), 2500) * np.exp(-tt * 9) * .18
    put('fx', np.tanh(s * 1.4) * .6, t); EVENTS.append((t, 'slam'))

def whoosh(t_peak, dur=None):
    dur = dur or BEAT * 1.0; n = int(dur * SR); tt = np.arange(n) / SR
    x = noise(n); out = np.zeros(n); ch = 1024
    for k in range(0, n, ch):
        c = 300 + 5000 * (k / n) ** 2
        out[k:k + ch] = bp(x[k:k + ch + 0], c, c * 2.2)[:len(out[k:k + ch])]
    env = (tt / dur) ** 2.2
    s = out * env * .28
    tail = int(.12 * SR); s = np.concatenate([s, s[-1] * np.exp(-np.arange(tail) / SR * 40)])
    put('fx', s, t_peak - dur, 0)

def riser(t0, beats):
    dur = beats * BEAT; n = int(dur * SR); tt = np.arange(n) / SR; x = noise(n); out = np.zeros(n); ch = 2048
    for k in range(0, n, ch):
        c = 200 + 9000 * (k / n) ** 2.2
        out[k:k + ch] = hp(x[k:k + ch], c)[:len(out[k:k + ch])]
    sweep = np.sin(2 * np.pi * np.cumsum(180 + 1100 * (tt / dur) ** 2) / SR) * .12
    put('fx', (out * .22 + sweep) * (tt / dur) ** 2.5, t0)

def roll(t0, beats):
    b = 0.0
    while b < beats - 1e-6:
        frac = b / beats; step = .5 if frac < .5 else .25 if frac < .75 else .125
        snare(t0 + b * BEAT, .35 + .75 * frac, 1 + .6 * frac); b += step

def ticks(t0, beats):
    k = 0
    while k < beats * 4:
        f = 900 + 2200 * k / (beats * 4); tt = T(.05)
        put('fx', np.sin(2 * np.pi * f * tt) * np.exp(-tt * 70) * .22, t0 + k * BEAT / 4, .3 if k % 2 else -.3); k += 1

def supersaw(notes, t, dur, cutoff, amp):
    n = int((dur + .25) * SR); tt = np.arange(n) / SR; s = np.zeros((n, 2))
    for m in notes:
        for d, pan in [(-17, -.7), (-7, -.3), (0, 0), (7, .3), (17, .7)]:
            v = saw(m2f(m) * 2 ** (d / 1200), n, rng.random())
            s[:, 0] += v * (1 - pan); s[:, 1] += v * (1 + pan)
    env = np.minimum(1, tt / .012) * np.clip((dur + .25 - tt) / .25, 0, 1)
    s = np.stack([lp(s[:, 0], cutoff), lp(s[:, 1], cutoff)], 1) * env[:, None]
    put('music', s * amp / len(notes), t)

def bass(root, t, dur, amp=1.0):
    n = int(dur * SR); tt = np.arange(n) / SR; f = m2f(root)
    s = np.sin(2 * np.pi * f * tt) * .8 + lp(saw(f * 2, n), 500) * .35
    env = np.minimum(1, tt / .005) * np.clip((dur - tt) / .02, 0, 1)
    put('music', s * env * .55 * amp, t)

def pluck(m, t, amp=1.0, pan=0.0):
    n = int(.5 * SR); tt = np.arange(n) / SR; x = saw(m2f(m), n)
    env = np.exp(-tt * 7) * np.minimum(1, tt / .003)
    s = lp(x, 1400) * env + (x - lp(x, 1400)) * env ** 4
    s *= .30 * amp
    put('music', s, t, pan)
    for k, (dl, g, p) in enumerate([(.75, .35, -.6), (1.5, .18, .6)]):  # 附點八分回音
        put('music', s * g, t + dl * BEAT, p)

def keys(m, t, dur, amp, pan=0.0):
    n = int(dur * SR); tt = np.arange(n) / SR; f = m2f(m)
    s = sum(a * np.sin(2 * np.pi * f * k * tt) * np.exp(-tt * k * .9) for k, a in [(1, 1), (2, .4), (3, .15)])
    put('music', s * np.exp(-tt * 4.5 / dur) * np.minimum(1, tt / .006) * amp, t, pan)

def pad(notes, t, dur, amp):
    n = int(dur * SR); tt = np.arange(n) / SR
    s = sum(np.sin(2 * np.pi * m2f(m) * tt) + .25 * np.sin(2 * np.pi * m2f(m) * 2.003 * tt) for m in notes)
    put('music', s * np.minimum(1, tt / .5) * np.clip((dur - tt) / .5, 0, 1) * amp, t)


# ── 依場景排程 ──
b0 = 0
for sc in proj['scenes']:
    t0 = b0 * BEAT; nb = sc['beats']; mode = sc['mode']
    for cb in range(0, nb, 4):
        name = sc['chords'][(cb // 4) % len(sc['chords'])]; ct = t0 + cb * BEAT; cl = min(4, nb - cb)
        notes = CH[name]; EVENTS.append((ct, f'chord:{name}'))
        drop_part = mode == 'drop' or (mode == 'outro' and cb < 12)
        if mode == 'intro':
            prog = cb / nb
            supersaw(notes, ct, cl * BEAT, 500 + 3500 * prog ** 2, .28)
            bass(ROOT[name], ct, cl * BEAT, .6)
            for k in range(cl):
                if cb + k < 8 and k % 2 == 0: kick(ct + k * BEAT, .75)
                if cb + k >= 8 and cb + k < 12: kick(ct + k * BEAT, .9)
                hat(ct + (k + .5) * BEAT, False, .7)
        elif mode == 'build':
            supersaw(notes, ct, cl * BEAT, 1500 + 3000 * cb / nb, .3)
            for k in range(cl): kick(ct + k * BEAT, .9)
        elif drop_part:
            supersaw(notes, ct, cl * BEAT, 5200, .42)
            for k in range(cl):
                bt = ct + k * BEAT
                kick(bt)
                if (cb + k) % 2 == 1: clap(bt)
                hat(bt + .5 * BEAT, True, .9)
                for q in (.25, .75): hat(bt + q * BEAT, False, .6, -.2)
                bass(ROOT[name], bt + .5 * BEAT, .5 * BEAT * .9)
                bass(ROOT[name] + 12, bt + .75 * BEAT, .25 * BEAT * .8, .5)
            for k in range(cl * 2):
                m = LEAD[name][k % 8]
                if m > 0: pluck(m, ct + k * BEAT / 2, 1.0, .15 if k % 2 else -.15)
        elif mode == 'break':
            pad(notes, ct, cl * BEAT + .4, .06)
            arp = [notes[1] + 12, notes[2] + 12, notes[3] + 12, notes[2] + 12]
            for k in range(cl * 2): keys(arp[k % 4], ct + k * BEAT / 2, 1.4, .19, .3 if k % 2 else -.3)
            keys(ROOT[name] + 12, ct, cl * BEAT, .32)
        elif mode == 'outro' and cb >= 12:
            pass
    # 爆點 & 音效
    for h in sc.get('hits', []):
        impact(t0 + h * BEAT)
        if sc['mode'] == 'outro' and h == 12:  # 最後一擊：和弦延音
            n = CH[sc['chords'][-1]]
            supersaw(n + [n[0] + 12], t0 + h * BEAT, (nb - h) * BEAT + proj['tail'] - .3, 3000, .5)
            bass(ROOT[sc['chords'][-1]], t0 + h * BEAT, 2.5, 1.0)
    for sb, kind in sc.get('sfx', []):
        st = t0 + sb * BEAT
        if kind == 'slam': slam(st)
        elif kind == 'whoosh': whoosh(st + .5 * BEAT)
        elif kind.startswith('riser'): riser(st, float(kind[5:]))
        elif kind.startswith('roll'): roll(st, float(kind[4:]))
        elif kind.startswith('ticks'): ticks(st, float(kind[5:]))
        elif kind == 'gap': gaps.append((st, t0 + nb * BEAT))
    b0 += nb

# 側鏈壓縮（大鼓一下，和弦/低音就「呼吸」一次）
tt = np.arange(N) / SR
duck = np.ones(N)
for k in kick_times:
    i = int(k * SR); j = min(N, i + int(.4 * SR))
    duck[i:j] = np.minimum(duck[i:j], 1 - .72 * np.exp(-(tt[i:j] - k) / .085))
music = bus['music'] * duck[:, None]
# 殘響（多重回音，只加在音樂與音效）
wet = music * .0 + bus['fx'] * .5 + music * .5
rv = np.zeros_like(wet)
for d, g in [(.043, .30), (.071, .26), (.113, .22), (.167, .17), (.241, .12), (.337, .08)]:
    k = int(d * SR); rv[k:, 0] += wet[:-k, 1] * g; rv[k:, 1] += wet[:-k, 0] * g
mix = bus['drums'] + music + bus['fx'] + rv * .6
for a, b in gaps:  # 靜音停頓
    i, j = int(a * SR), int(b * SR)
    r = int(.004 * SR); mix[i:i + r] *= np.linspace(1, 0, r)[:, None]; mix[i + r:j] = 0
mix *= np.clip((D - tt) / 1.2, 0, 1)[:, None]
mix = np.tanh(mix / np.percentile(np.abs(mix), 99.9) * 1.1)
mix = mix / np.abs(mix).max() * .93
with wave.open('output/music.wav', 'wb') as w:
    w.setnchannels(2); w.setsampwidth(2); w.setframerate(SR)
    w.writeframes((mix * 32767).astype('<i2').tobytes())
json.dump(sorted(EVENTS), open('output/music_events.json', 'w'))
print(f'music: {D:.2f}s, {TOTAL_B} beats @ {proj["bpm"]} bpm')
