#!/usr/bin/env node
/**
 * render-minimal.js — 金句型模板：极简大字流
 * 每页只有1-2行巨大文字，快节奏，高冲击
 * 用法: node render-minimal.js <input.json> [output.html]
 */

const fs = require('fs');
const path = require('path');

const jsonFile = process.argv[2];
const outFile  = process.argv[3];

if (!jsonFile) {
  console.error('用法: node render-minimal.js <input.json> [output.html]');
  process.exit(1);
}

const data = JSON.parse(fs.readFileSync(jsonFile, 'utf8'));

function totalScenes() {
  return data.pages.length;
}

function sceneDuration() {
  return 3.5; // 金句型节奏更快：2s动画 + 1.5s阅读
}

function timelineJS() {
  const total = totalScenes();
  const lines = [];
  let elapsed = 0;
  for (let i = 0; i < total; i++) {
    const dur = sceneDuration();
    if (i === 0) {
      lines.push(`showScene('s1', 100);`);
    } else {
      lines.push(`setTimeout(() => showScene('s${i + 1}', 100), ${Math.round(elapsed * 1000)});`);
    }
    elapsed += dur;
  }
  return { duration: Math.round(elapsed), lines };
}

function renderPage(page, idx) {
  const num = idx + 1;
  const total = totalScenes();
  const isFinale = idx === total - 1;
  const accentColor = isFinale ? 'var(--gold)' : 'var(--accent)';

  // 根据文字长度自动选字号
  const text = page.text;
  const len = text.replace(/\n/g, '').length;
  let fontSize = 120;
  if (len > 12) fontSize = 100;
  if (len > 20) fontSize = 82;
  if (len > 30) fontSize = 64;

  const lines = text.split('\n').map((line, i) => {
    const isHighlight = page.highlight && line.includes(page.highlight);
    const color = isHighlight ? accentColor : 'var(--cream)';
    return `<div class="line anim from-bottom" data-d="${300 + i * 400}" style="color:${color}">${line}</div>`;
  }).join('\n      ');

  const subHtml = page.sub
    ? `<div class="sub anim" data-d="${300 + text.split('\n').length * 400 + 200}">${page.sub}</div>`
    : '';

  return `
    <div class="scene" id="s${num}">
      <div class="page-num">${String(num).padStart(2,'0')} / ${String(total).padStart(2,'0')}</div>
      ${lines}
      ${subHtml}
      <div class="bg-glow ${isFinale ? 'gold' : ''}"></div>
    </div>`;
}

const { duration, lines } = timelineJS();

const html = `<!DOCTYPE html>
<html lang="zh-CN">
<head>
<meta charset="UTF-8">
<title>${data.title || '金句视频'}</title>
<style>
* { margin:0; padding:0; box-sizing:border-box; }
:root {
  --bg: #0a0a0f;
  --accent: ${data.accent || '#E85D3A'};
  --gold: #D4A843;
  --cream: #F2EDE6;
  --muted: rgba(242,237,230,0.4);
  --sans: "PingFang SC","Hiragino Sans GB","Microsoft YaHei",sans-serif;
}
html,body { width:100%;height:100%;background:#000;overflow:hidden;font-family:var(--sans); }

#stage {
  width:1080px;height:1920px;
  background:var(--bg);
  position:absolute;top:0;left:0;
  transform-origin:top left;
  overflow:hidden;
}

.scene {
  position:absolute;inset:0;
  padding:0 96px;
  display:flex;flex-direction:column;
  justify-content:center;
  align-items:flex-start;
  opacity:0;
  will-change:opacity,transform;
}
.scene.show { opacity:1; }

.line {
  font-size:120px;
  font-weight:900;
  line-height:1.25;
  letter-spacing:-0.03em;
  color:var(--cream);
  margin-bottom:16px;
}

.sub {
  font-size:38px;
  color:var(--muted);
  margin-top:32px;
  line-height:1.6;
}

.page-num {
  position:absolute;
  top:80px;right:96px;
  font-size:24px;
  color:rgba(242,237,230,0.15);
  letter-spacing:0.15em;
}

/* 流动渐变背景光 */
.bg-glow {
  position:absolute;
  bottom:-200px;left:-200px;
  width:600px;height:600px;
  background:radial-gradient(circle, rgba(232,93,58,0.08) 0%, transparent 70%);
  border-radius:50%;
  pointer-events:none;
  animation:float 8s ease-in-out infinite;
}
.bg-glow.gold {
  background:radial-gradient(circle, rgba(212,168,67,0.1) 0%, transparent 70%);
}

@keyframes float {
  0%,100% { transform:translate(0,0); }
  50% { transform:translate(60px,-40px); }
}

/* 进度条 */
#prog {
  position:absolute;bottom:0;left:0;height:4px;
  background:var(--accent);width:0;z-index:99;
  transition:width 0.1s linear;
}

/* 动画 */
.anim { opacity:0;transition:opacity 0.8s ease-out, transform 0.9s cubic-bezier(0.16,1,0.3,1); }
.from-bottom { transform:translateY(40px); }
.anim.in { opacity:1;transform:none; }
</style>
</head>
<body>
<div id="stage">
  <div id="prog"></div>
  ${data.pages.map((p, i) => renderPage(p, i)).join('')}
</div>

<script>
function scale() {
  const s = document.getElementById('stage');
  const r = Math.min(window.innerWidth/1080, window.innerHeight/1920);
  const x = (window.innerWidth - 1080*r)/2;
  const y = (window.innerHeight - 1920*r)/2;
  s.style.transform = \`translate(\${x}px,\${y}px) scale(\${r})\`;
}
scale();
window.addEventListener('resize', scale);

const TOTAL = ${duration * 1000};
const t0 = Date.now();
const prog = document.getElementById('prog');
function tick() {
  const p = Math.min(1,(Date.now()-t0)/TOTAL);
  prog.style.width = (p*100)+'%';
  if(p<1) requestAnimationFrame(tick);
}
requestAnimationFrame(tick);

function showScene(id, baseDelay) {
  document.querySelectorAll('.scene').forEach(s => {
    s.classList.remove('show');
    s.querySelectorAll('.anim').forEach(el => el.classList.remove('in'));
  });
  const scene = document.getElementById(id);
  scene.classList.add('show');
  scene.querySelectorAll('.anim').forEach(el => {
    const d = parseInt(el.dataset.d||0);
    setTimeout(() => el.classList.add('in'), d + (baseDelay||0));
  });
}

// 时间轴
${lines.join('\n')}
</script>
</body>
</html>`;

const outPath = outFile || jsonFile.replace(/\.json$/, '.html');
fs.writeFileSync(outPath, html, 'utf8');
console.log(`✅ 金句模板 HTML 已生成: ${outPath}`);
console.log(`   页数: ${totalScenes()}  时长: ${duration}s`);
