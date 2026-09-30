const { chromium } = require('/opt/node22/lib/node_modules/playwright');
const { spawn } = require('child_process');
const path = require('path');
// 用法：node render.js h|v <輸出.mp4>   或   node render.js h|v <前綴> 3.5,10,20（輸出指定秒數的靜態截圖）
const [,, mode, out, stills] = process.argv;
(async () => {
  const V = mode[0] === 'v', WARM = mode.endsWith('w');  // h｜v｜hw｜vw（w＝溫馨版）
  const [W, H] = V ? [1080, 1920] : [1920, 1080];
  const b = await chromium.launch();
  const p = await b.newPage({ viewport: { width: W, height: H } });
  await p.goto('file://' + path.resolve(__dirname, 'promo.html') + '?render=1' + (V ? '&v=1' : '') + (WARM ? '&style=warm' : ''));
  await p.evaluate(async () => { await document.fonts.ready; await Promise.all([...document.images].map(i => i.decode().catch(()=>{}))); });
  if (stills) {
    const st = await p.evaluate(() => ST); console.log(JSON.stringify(st));
    for (const t of stills.split(',')) { await p.evaluate(t => render(t), +t); await p.screenshot({ path: `${out}_${t}.jpg`, quality: 80, type: 'jpeg' }); }
    await b.close(); return;
  }
  const FPS = 30, N = Math.round(await p.evaluate(() => DURATION) * FPS);
  const ff = spawn(process.env.FF, ['-y','-f','image2pipe','-framerate',String(FPS),'-c:v','mjpeg','-i','-','-c:v','libx264','-pix_fmt','yuv420p','-crf','20','-maxrate','12M','-bufsize','24M','-preset','medium',out + '.video.mp4'], { stdio: ['pipe','ignore','inherit'] });
  for (let i = 0; i < N; i++) {
    await p.evaluate(t => render(t), i / FPS);
    const buf = await p.screenshot({ type: 'jpeg', quality: 95 });
    if (!ff.stdin.write(buf)) await new Promise(r => ff.stdin.once('drain', r));
  }
  ff.stdin.end(); await new Promise(r => ff.on('close', r)); await b.close();
  // 合成配樂（output/music.wav，由 music.py 產生）
  const mux = spawn(process.env.FF, ['-y','-loglevel','error','-i',out + '.video.mp4','-i',path.join(__dirname, WARM ? 'output/music_warm.wav' : 'output/music.wav'),'-c:v','copy','-c:a','aac','-b:a','192k','-shortest','-movflags','+faststart',out], { stdio: 'inherit' });
  await new Promise(r => mux.on('close', r));
  require('fs').unlinkSync(out + '.video.mp4');
})();
