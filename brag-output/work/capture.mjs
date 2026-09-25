import { chromium } from 'playwright';
import { spawn } from 'child_process';
const mode = process.argv[2];
const browser = await chromium.launch({ executablePath: '/opt/pw-browsers/chromium-1194/chrome-linux/chrome' });
const page = await browser.newPage({ viewport: { width: +(process.env.W||1920), height: +(process.env.H||1080) } });
await page.goto('http://127.0.0.1:8765/'+(process.env.PAGE||'video.html'));
await page.evaluate(() => window.ready);
if (mode === 'stills') {
  const times = process.argv.slice(3).map(Number);
  for (const t of times) {
    await page.evaluate(t => window.render(t), t);
    await page.screenshot({ path: `${process.env.SDIR||'stills'}/t${t.toFixed(2)}.png` });
  }
} else {
  const fps = 30, dur = await page.evaluate(() => window.DURATION);
  const n = Math.round(dur * fps);
  const ff = spawn('ffmpeg', ['-y','-v','error','-f','image2pipe','-framerate',String(fps),'-i','-','-c:v','libx264','-preset','slow','-crf','16','-pix_fmt','yuv420p',process.env.OUT||'video-silent.mp4'], { stdio: ['pipe','inherit','inherit'] });
  for (let i = 0; i < n; i++) {
    await page.evaluate(t => window.render(t), i / fps);
    const buf = await page.screenshot({ type: 'png' });
    if (!ff.stdin.write(buf)) await new Promise(r => ff.stdin.once('drain', r));
    if (i % 60 === 0) console.log('frame', i, '/', n);
  }
  ff.stdin.end(); await new Promise(r => ff.on('close', r));
}
await browser.close();
