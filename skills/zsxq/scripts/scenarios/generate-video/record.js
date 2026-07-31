#!/usr/bin/env node
/**
 * record.js — 通用 HTML → MP4 录制脚本（确定性虚拟时钟版）
 * 用法: node record.js <input.html> <output.mp4> [duration_seconds]
 */

const puppeteer = require('puppeteer');
const path = require('path');
const fs = require('fs');
const { execSync } = require('child_process');

const htmlFile   = process.argv[2];
const outputFile = process.argv[3];
const arg4       = process.argv[4];

// 封面模式：--cover 参数或输出文件为 .png
const isCoverMode = arg4 === '--cover' || (outputFile && outputFile.endsWith('.png'));
const duration   = isCoverMode ? 1 : parseInt(arg4 || '36', 10);

if (!htmlFile || !outputFile) {
  console.error('用法: node record.js <input.html> <output.mp4> [duration_seconds]');
  console.error('封面: node record.js <input.html> <output.png> --cover');
  process.exit(1);
}

const FRAMES_DIR = path.join(path.dirname(outputFile), '.frames-' + Date.now());
const FPS   = 30;
const TOTAL = FPS * duration;

// 查找 ffmpeg
function findFfmpeg() {
  for (const p of ['/opt/homebrew/bin/ffmpeg', '/usr/local/bin/ffmpeg', 'ffmpeg']) {
    try { execSync(`${p} -version`, { stdio: 'ignore' }); return p; } catch (_) {}
  }
  throw new Error('找不到 ffmpeg，请先安装: brew install ffmpeg');
}

async function main() {
  const browser = await puppeteer.launch({
    args: ['--no-sandbox', '--disable-setuid-sandbox'],
    headless: true,
  });

  const page = await browser.newPage();
  await page.setViewport({ width: 1080, height: 1920, deviceScaleFactor: 2 });

  // 在页面加载前劫持时间 — 用虚拟时钟控制 setTimeout/setInterval/Date.now/RAF
  await page.evaluateOnNewDocument(() => {
    window.__virtualTime = 0;

    // 劫持 Date.now
    const _origNow = Date.now;
    Date.now = () => window.__virtualTime;

    // 劫持 performance.now
    if (window.performance) {
      performance.now = () => window.__virtualTime;
    }

    // 劫持 setTimeout
    const _timers = [];
    const _origSetTimeout = window.setTimeout;
    window.setTimeout = (fn, delay, ...args) => {
      _timers.push({ fn, time: window.__virtualTime + (delay || 0), args });
      return _timers.length;
    };

    // 劫持 setInterval
    const _intervals = [];
    const _origSetInterval = window.setInterval;
    window.setInterval = (fn, delay, ...args) => {
      _intervals.push({ fn, delay: delay || 16, nextTime: window.__virtualTime + (delay || 16), args });
      return _intervals.length + 100000;
    };

    // 劫持 requestAnimationFrame
    const _rafs = [];
    window.requestAnimationFrame = (fn) => {
      _rafs.push(fn);
      return _rafs.length;
    };

    // 推进时间的函数
    window.__advanceTime = (ms) => {
      window.__virtualTime += ms;
      const now = window.__virtualTime;

      // 触发到期的 setTimeout
      const ready = _timers.filter(t => t && t.time <= now);
      ready.forEach(t => {
        const idx = _timers.indexOf(t);
        _timers[idx] = null;
        t.fn(...t.args);
      });

      // 触发到期的 setInterval
      _intervals.forEach(iv => {
        if (iv && iv.nextTime <= now) {
          iv.fn(...iv.args);
          iv.nextTime = now + iv.delay;
        }
      });

      // 触发 RAF
      const rafs = _rafs.splice(0);
      rafs.forEach(fn => fn(now));
    };
  });

  await page.goto('file://' + path.resolve(htmlFile), { waitUntil: 'networkidle0' });

  // ─── 封面截图模式 ───
  if (isCoverMode) {
    console.log('▶ 封面截图模式...');
    // 推进少量时间确保 showSceneImmediate 执行完毕
    await page.evaluate((ms) => window.__advanceTime(ms), 100);
    await page.screenshot({ path: outputFile });
    await browser.close();
    console.log(`✅ 封面已生成: ${outputFile}`);
    return;
  }

  // ─── 视频录制模式 ───
  fs.mkdirSync(FRAMES_DIR, { recursive: true });
  console.log(`▶ 启动录制 (${FPS}fps × ${duration}s = ${TOTAL} 帧)...`);

  const frameInterval = 1000 / FPS; // 每帧虚拟时间 ~33.33ms

  for (let i = 0; i < TOTAL; i++) {
    // 推进虚拟时间
    await page.evaluate((ms) => window.__advanceTime(ms), frameInterval);

    // 截帧
    const framePath = path.join(FRAMES_DIR, `frame-${String(i).padStart(5, '0')}.png`);
    await page.screenshot({ path: framePath });

    if (i % 90 === 0) {
      const pct = ((i / TOTAL) * 100).toFixed(0);
      console.log(`  ${pct}% (${i}/${TOTAL})`);
    }
  }

  await browser.close();
  console.log('✔ 截帧完成，合成视频中...');

  const ffmpeg = findFfmpeg();
  execSync(
    `${ffmpeg} -y -framerate ${FPS} -i "${path.join(FRAMES_DIR, 'frame-%05d.png')}" ` +
    `-c:v libx264 -pix_fmt yuv420p -crf 18 -preset slow "${outputFile}"`,
    { stdio: 'inherit' }
  );

  fs.rmSync(FRAMES_DIR, { recursive: true });
  console.log(`✅ 视频已生成: ${outputFile}`);
}

main().catch(err => { console.error('错误:', err.message); process.exit(1); });
