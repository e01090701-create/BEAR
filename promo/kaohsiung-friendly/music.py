"""配樂產生器：讀 scenes.js 的同一份時間軸，逐拍合成配樂 → output/music.wav

每個場景起點都落在拍點上，並在該點換和弦；energy 決定配器密度。
執行：python3 music.py   （需要 numpy、node）
"""
import json, subprocess, wave
import numpy as np

proj = json.loads(subprocess.check_output(
    ['node', '-e', "global.window={};require('./scenes.js');console.log(JSON.stringify(window.PROJECT))"]))
SR = 44100
BEAT = 60 / proj['bpm']
total_beats = sum(s['beats'] for s in proj['scenes'])
D = total_beats * BEAT + proj['tail']
N = int(SR * (D + 0.5))
L = np.zeros(N); R = np.zeros(N)
m2f = lambda x: 440 * 2 ** ((x - 69) / 12)
CH = {'C': [48, 60, 64, 67], 'G': [43, 59, 62, 67], 'Am': [45, 60, 64, 69], 'F': [41, 60, 65, 69]}
rng = np.random.default_rng(3)
EVENTS = []  # (秒, 類型) — 給對拍檢查用


def put(sig, t, pan=0.0):
    i = int(t * SR); j = min(N, i + len(sig))
    if j <= i: return
    L[i:j] += sig[:j - i] * (1 - pan); R[i:j] += sig[:j - i] * (1 + pan)


def keys(midi, t, dur, amp, bright=1.0, pan=0.0):
    n = int(dur * SR); tt = np.arange(n) / SR; f = m2f(midi)
    env = np.exp(-tt * 6.5 / dur) * np.minimum(1, tt / 0.006)
    s = sum(a * np.sin(2 * np.pi * f * k * tt) * np.exp(-tt * k * 0.9)
            for k, a in [(1, 1), (2, .45 * bright), (3, .18 * bright), (4, .08 * bright)])
    put(s * env * amp, t, pan)


def pad(chord, t, dur, amp):
    n = int(dur * SR); tt = np.arange(n) / SR
    env = np.minimum(1, tt / 0.6) * np.clip((dur - tt) / 0.6, 0, 1)
    s = sum(np.sin(2 * np.pi * m2f(x) * tt) + .3 * np.sin(2 * np.pi * m2f(x) * 2.003 * tt) for x in chord[1:])
    put(s * env * amp, t)


def kick(t, amp):
    n = int(.35 * SR); tt = np.arange(n) / SR
    f = 55 + 70 * np.exp(-tt * 30)
    put(np.sin(2 * np.pi * np.cumsum(f) / SR) * np.exp(-tt * 9) * amp, t)


def shaker(t, amp, pan):
    n = int(.08 * SR); tt = np.arange(n) / SR
    s = np.diff(rng.standard_normal(n + 1)) * np.exp(-tt * 60)
    put(s * amp, t, pan)


def swell(t_end, dur, amp):  # 反向噪音，衝進重點畫面
    n = int(dur * SR); tt = np.arange(n) / SR
    s = np.diff(rng.standard_normal(n + 1)) * (tt / dur) ** 3
    put(s * amp, t_end - dur)


b0 = 0
for si, sc in enumerate(proj['scenes']):
    t0 = b0 * BEAT; e = sc['energy']; nb = sc['beats']
    if sc.get('accent') is not None:
        at = t0 + sc['accent'] * BEAT
        for k, x in enumerate([84, 88, 91, 96]):
            keys(x, at + k * .09, 1.8, .05, .4, (k - 1.5) / 3)
        if si > 0 and e == 2: swell(t0, BEAT * 2, .05)
    for cb in range(0, nb, 4):
        name = sc['chords'][(cb // 4) % len(sc['chords'])]
        ch = CH[name]; ct = t0 + cb * BEAT; cl = min(4, nb - cb)
        last = sc.get('end') and cb + 4 >= nb
        if last:  # 片尾最後和弦延音到結束
            EVENTS.append((ct, f'final:{name}'))
            for x in [ch[0], ch[0] + 12] + ch[1:] + [ch[1] + 12]:
                keys(x, ct, D - ct + .3, .09, .7)
            pad(ch, ct, D - ct, .02)
            continue
        pad(ch, ct, cl * BEAT + .6, .018 if e else .014)
        keys(ch[0], ct, cl * BEAT * 1.2, .16, .6); EVENTS.append((ct, f'bass:{name}'))
        if e == 2 and cl >= 3: keys(ch[0], ct + 2 * BEAT, 2 * BEAT, .10, .5)
        arp = [ch[1] + 12, ch[2] + 12, ch[3] + 12, ch[2] + 12, ch[3] + 12, ch[1] + 24, ch[3] + 12, ch[2] + 12]
        step = 1 if e == 0 else .5
        k = 0; x = 0.0
        while x < cl - 1e-6:
            keys(arp[int(x * 2) % 8], ct + x * BEAT, 1.6, .08, 1, .3 if k % 2 else -.3)
            if e == 2: shaker(ct + x * BEAT, .018 if k % 2 else .01, .25 if k % 2 else -.25)
            x += step; k += 1
        if e == 2:
            for bb in range(cl):
                if bb % 2 == 0: kick(ct + bb * BEAT, .28)
            mel = {'C': [76, 74, 72, 74], 'G': [74, 71, 67, 71], 'Am': [72, 76, 79, 76], 'F': [77, 76, 74, 72]}[name]
            for bb in range(cl):
                keys(mel[bb], ct + bb * BEAT, BEAT * 1.8, .065, .8, .1)
    b0 += nb

# 簡易殘響
for d, g in [(.083, .35), (.127, .28), (.191, .22), (.263, .16), (.37, .1)]:
    k = int(d * SR); L[k:] += R[:-k] * g * .5; R[k:] += L[:-k] * g * .5
out = np.stack([L, R], 1)
tt = np.arange(N) / SR
out *= (np.minimum(1, tt / 1.0) * np.clip((D - tt) / 1.4, 0, 1))[:, None]
out = np.tanh(out / np.abs(out).max() * 1.3) * .8
with wave.open('output/music.wav', 'wb') as w:
    w.setnchannels(2); w.setsampwidth(2); w.setframerate(SR)
    w.writeframes((out * 32767).astype('<i2').tobytes())
json.dump(EVENTS, open('output/music_events.json', 'w'))
print(f'music: {D:.2f}s, {total_beats} beats @ {proj["bpm"]} bpm')
