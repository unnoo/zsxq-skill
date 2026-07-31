#!/usr/bin/env node
/**
 * render.js — JSON 数据 → 动画 HTML
 * 用法: node render.js <input.json> [output.html]
 */

const fs = require('fs');
const path = require('path');

const jsonFile = process.argv[2];
const outFile  = process.argv[3];

if (!jsonFile) {
  console.error('用法: node render.js <input.json> [output.html]');
  process.exit(1);
}

const data = JSON.parse(fs.readFileSync(jsonFile, 'utf8'));

// ── 颜色工具 ──────────────────────────────────────────────
const COLOR_MAP = {
  orange: 'var(--orange)',
  gold:   'var(--gold)',
  cream:  'var(--cream)',
  brand:  'var(--brand)',
};
function color(key) { return COLOR_MAP[key] || key; }

// ── 元素生成器 ────────────────────────────────────────────

function topicAnchor(data, gold = false) {
  const highlightColor = gold ? 'var(--gold)' : 'var(--orange)';
  const topic = data.topic.replace(
    data.topic_highlight,
    `<em style="color:${highlightColor};font-style:normal;font-weight:800;">${data.topic_highlight}</em>`
  );
  const label = data.author ? `${data.planet}｜${data.author}` : data.planet;
  return `
    <div class="topic-anchor">
      <div class="ta-label">${label}</div>
      <div class="ta-title">${topic}</div>
    </div>`;
}

function chip(text, gold = false) {
  return `<div class="chip${gold ? ' gold' : ''} anim from-bottom" data-d="200">${text}</div>`;
}

function h1Lines(lines, accentIdx, size = '', gold = false) {
  return lines.map((line, i) => {
    const isAccent = i === accentIdx;
    const accentClass = isAccent ? ' accent' + (gold ? ' gold' : '') : '';
    const sz = size ? ` ${size}` : '';
    return `<div class="h1${sz}${accentClass} anim from-bottom" data-d="${500 + i * 350}">${line}</div>`;
  }).join('\n    ');
}

function sub(text, delay = 1200) {
  return `<div class="sub anim" data-d="${delay}">${text}</div>`;
}

function rule(gold = false, delay = 1600) {
  return `<div class="rule${gold ? ' gold' : ''} anim" data-d="${delay}"></div>`;
}

function items(list, gold = false, startDelay = 1900) {
  return list.map((text, i) => {
    const d = startDelay + i * 350;
    const g = gold ? ' gold' : '';
    return `
    <div class="item anim from-right" data-d="${d}">
      <div class="inum${g}">${String(i + 1).padStart(2, '0')}</div>
      <div class="ibar${g}"></div>
      <div class="itext">${text}</div>
    </div>`;
  }).join('');
}

function trioItem(t, delay) {
  return `
      <div class="anim from-bottom" data-d="${delay}">
        <div style="font-size:51px;font-weight:700;color:${color(t.color)};white-space:nowrap">${t.label}</div>
        <div style="font-size:37px;color:var(--muted);margin-top:6px;white-space:nowrap">${t.desc}</div>
      </div>`;
}

// ── 场景生成 ──────────────────────────────────────────────

function coverScene(cover) {
  const trioHtml = cover.trio
    ? `<div style="display:flex;gap:60px;margin-top:16px;">
      ${cover.trio.map((t, i) => trioItem(t, 1200 + i * 200)).join('')}
    </div>`
    : '';

  // 封面 h1 自动选字号
  const h1Size = cover.h1.join('').length > 10 ? 'sm' : '';

  return `
  <!-- S1 封面 -->
  <div class="scene" id="s1">
    <div class="snum">01 / ${totalScenes()}</div>
    <div class="bgnum">01</div>
    ${chip(cover.chip)}
    ${h1Lines(cover.h1, cover.h1_accent ?? 1, h1Size)}
    ${sub(cover.sub)}
    ${rule()}
    ${trioHtml}
  </div>`;
}

function contentScene(scene, idx) {
  const sceneNum = idx + 2; // s2, s3, s4...
  const total = totalScenes();
  const h1Size = scene.h1.join('').length > 10 ? 'sm' : '';

  return `
  <!-- S${sceneNum} -->
  <div class="scene" id="s${sceneNum}">
    <div class="snum">${String(sceneNum).padStart(2, '0')} / ${String(total).padStart(2, '0')}</div>
    <div class="corner"></div>
    <div class="bgnum">${String(sceneNum).padStart(2, '0')}</div>
    ${topicAnchor(data)}
    ${chip(scene.chip)}
    ${h1Lines(scene.h1, scene.h1_accent ?? 1, h1Size)}
    ${sub(scene.sub)}
    ${rule()}
    ${items(scene.items)}
  </div>`;
}

function finaleScene(finale) {
  const sceneNum = data.cta ? totalScenes() - 1 : totalScenes();

  return `
  <!-- S${sceneNum} 结语（金色）-->
  <div class="scene" id="s${sceneNum}">
    <div class="snum">${String(sceneNum).padStart(2, '0')} / ${String(totalScenes()).padStart(2, '0')}</div>
    <div class="corner gold"></div>
    <div class="bgnum" style="color:rgba(212,168,67,0.05)">${String(sceneNum).padStart(2, '0')}</div>
    ${topicAnchor(data, true)}
    ${chip(finale.chip, true)}
    ${h1Lines(finale.h1, -1, 'xs', true).replace(/class="h1/g, 'class="h1').replace(/var\(--orange\)/g, 'var(--gold)')}
    ${sub(finale.sub)}
    ${rule(true)}
    ${items(finale.items, true)}
    <div class="finale anim from-scale" data-d="2200">${finale.finale_text.replace(/\n/g, '<br>')}</div>
  </div>`;
}

function ctaScene(cta) {
  if (!cta) return '';
  const sceneNum = totalScenes();
  return `
  <!-- CTA -->
  <div class="scene cta-scene" id="s${sceneNum}">
    <div class="cta-glow"></div>
    <div class="cta-planet anim from-scale" data-d="200">${cta.planet_name}</div>
    <div class="cta-tagline anim from-bottom" data-d="600">${cta.tagline}</div>
    <div class="cta-action anim from-bottom" data-d="1000">${cta.action}</div>
  </div>`;
}

function totalScenes() {
  return 1 + data.scenes.length + 1 + (data.cta ? 1 : 0);
}

// ── JS 时间轴 ─────────────────────────────────────────────

function sceneDuration(sceneIdx) {
  if (sceneIdx === 0) return 2; // 封面无动画，2秒停留即可
  return 5; // 内容页：动画3秒 + 2秒阅读
}

function timelineJS() {
  const total = totalScenes();
  const lines = [];
  let elapsed = 0;
  let duration = 0;

  for (let i = 0; i < total; i++) {
    const dur = sceneDuration(i);
    if (i === 0) {
      lines.push(`showSceneImmediate('s1');`);
    } else {
      lines.push(`setTimeout(() => showScene('s${i + 1}', 100), ${Math.round(elapsed * 1000)});`);
    }
    elapsed += dur;
    duration = elapsed;
  }
  return { duration: Math.round(duration), lines };
}

// ── 完整 HTML ─────────────────────────────────────────────

function render(data) {
  const { duration, lines } = timelineJS();
  const total = totalScenes();

  // 封面 h1 大小
  const coverH1Big = (data.cover.h1.join('').length <= 8) ? 130 : 100;

  const html = `<!DOCTYPE html>
<html lang="zh-CN">
<head>
<meta charset="UTF-8">
<title>${data.planet} · ${data.author}：${data.topic}</title>
<style>
* { margin:0; padding:0; box-sizing:border-box; }
:root {
  --bg:#0D0F14; --orange:#C84B1F; --gold:#D4A843;
  --cream:#EDE9E0; --muted:rgba(237,233,224,0.5);
  --brand:${data.brand_color};
  --sans:"PingFang SC","Hiragino Sans GB","Microsoft YaHei",sans-serif;
}
html,body { width:100%;height:100%;background:#111;overflow:hidden;font-family:var(--sans); }

#stage {
  width:1080px;height:1920px;
  background:var(--bg);
  position:absolute; top:0;left:0;
  transform-origin:top left;
  overflow:hidden;
}

/* scenes */
.scene {
  position:absolute;inset:0;
  padding:360px 60px 120px;
  display:flex;flex-direction:column;justify-content:flex-start;
  opacity:0;
  will-change:opacity,transform;
}
.scene.show { opacity:1; }

#s1 { padding:480px 60px 120px; justify-content:flex-start; }

/* progress */
#prog {
  position:absolute;bottom:0;left:0;height:6px;
  background:var(--orange);width:0;z-index:99;
  transition:width 0.15s linear;
}

/* topic anchor */
.topic-anchor { display:flex;align-items:stretch;margin-bottom:52px;overflow:hidden; }
.ta-label {
  flex-shrink:0; padding:22px 28px;
  background:var(--brand);
  font-size:42px;font-weight:800;letter-spacing:0.04em;
  color:#fff; white-space:nowrap;
  display:flex;align-items:center;
}
.ta-title {
  flex:1; padding:22px 28px;
  background:rgba(255,255,255,0.08);
  font-size:42px;font-weight:800;letter-spacing:0.03em;
  color:#fff; display:flex;align-items:center;
  white-space:nowrap;overflow:hidden;text-overflow:ellipsis;
}

/* scene number */
.snum { position:absolute;top:72px;right:96px;font-size:22px;color:rgba(237,233,224,0.2);letter-spacing:0.15em; }

/* bg number */
.bgnum {
  position:absolute;bottom:80px;right:60px;
  font-size:240px;font-weight:900;line-height:1;
  color:rgba(200,75,31,0.05);letter-spacing:-0.05em;
  pointer-events:none;
}

/* corner */
.corner { position:absolute;top:0;left:0;width:260px;height:260px;border-left:4px solid var(--orange);border-top:4px solid var(--orange);opacity:0.3; }
.corner.gold { border-color:var(--gold); }

/* chip */
.chip {
  display:inline-block;
  font-size:36px;letter-spacing:0.18em;
  color:var(--orange);
  border:1px solid rgba(200,75,31,0.4);
  padding:12px 28px;margin-bottom:36px;
  width:fit-content;
}
.chip.gold { color:var(--gold);border-color:rgba(212,168,67,0.4); }

/* typography */
.h1 { font-size:${coverH1Big}px;font-weight:900;color:var(--cream);line-height:1.26;letter-spacing:-0.02em; }
.h1.sm { font-size:100px; }
.h1.xs { font-size:82px; }
.accent { color:var(--orange); }
.accent.gold { color:var(--gold); }

.sub { font-size:38px;color:var(--muted);line-height:1.65;margin-top:20px;margin-bottom:6px; }

.rule { width:100%;height:2px;background:linear-gradient(to right,var(--orange),transparent);margin:32px 0;opacity:0.6; }
.rule.gold { background:linear-gradient(to right,var(--gold),transparent); }

/* list */
.item { display:flex;align-items:flex-start;gap:20px;margin-bottom:28px; }
.inum { font-size:24px;font-weight:700;color:var(--orange);min-width:44px;padding-top:8px; }
.inum.gold { color:var(--gold); }
.ibar { width:3px;background:var(--orange);flex-shrink:0;margin-top:10px;align-self:stretch;min-height:16px; }
.ibar.gold { background:var(--gold); }
.itext { font-size:44px;color:var(--cream);line-height:1.5;font-weight:500; }

.finale {
  font-size:82px;font-weight:900;color:var(--gold);
  line-height:1.3;text-align:left;
  margin-top:40px;padding:0;
  border:none;
  background:none;
}

/* animations */
.anim { opacity:0;transition:opacity 0.9s ease-out, transform 1s cubic-bezier(0.16,1,0.3,1); }
.from-bottom { transform:translateY(30px); }
.from-right  { transform:translateX(40px); }
.from-scale  { transform:scale(0.92); }
.anim.in { opacity:1;transform:none; }

/* CTA scene */
.cta-scene {
  justify-content:center;
  align-items:center;
  text-align:center;
  padding:200px 96px;
}
.cta-glow {
  position:absolute;
  top:50%;left:50%;
  width:800px;height:800px;
  transform:translate(-50%,-50%);
  background:radial-gradient(circle, rgba(200,75,31,0.06) 0%, transparent 70%);
  border-radius:50%;
  pointer-events:none;
}
.cta-planet {
  font-size:72px;font-weight:900;
  color:var(--cream);
  letter-spacing:0.02em;
  margin-bottom:40px;
}
.cta-tagline {
  font-size:38px;
  color:var(--muted);
  line-height:1.6;
  margin-bottom:64px;
}
.cta-action {
  font-size:42px;font-weight:700;
  color:var(--orange);
  border:2px solid rgba(200,75,31,0.5);
  padding:24px 56px;
  display:inline-block;
  letter-spacing:0.1em;
}
</style>
</head>
<body>
<div id="stage">
  <div id="prog"></div>
  ${coverScene(data.cover)}
  ${data.scenes.map((s, i) => contentScene(s, i)).join('')}
  ${finaleScene(data.finale)}
  ${ctaScene(data.cta)}
</div>

<script>
// 响应式缩放
function scale() {
  const s = document.getElementById('stage');
  const r = Math.min(window.innerWidth/1080, window.innerHeight/1920);
  const x = (window.innerWidth  - 1080*r)/2;
  const y = (window.innerHeight - 1920*r)/2;
  s.style.transform = \`translate(\${x}px,\${y}px) scale(\${r})\`;
}
scale();
window.addEventListener('resize', scale);

// 进度条
const TOTAL = ${duration * 1000};
const t0 = Date.now();
const prog = document.getElementById('prog');
function tick() {
  const p = Math.min(1,(Date.now()-t0)/TOTAL);
  prog.style.width = (p*100)+'%';
  if(p<1) requestAnimationFrame(tick);
}
requestAnimationFrame(tick);

// 场景切换
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

// 封面场景：立即显示所有元素，跳过动画延迟
function showSceneImmediate(id) {
  const scene = document.getElementById(id);
  scene.classList.add('show');
  scene.querySelectorAll('.anim').forEach(el => el.classList.add('in'));
}

// 时间轴
${lines.join('\n')}
</script>
</body>
</html>`;

  return html;
}

// ── 主流程 ───────────────────────────────────────────────

const { duration, lines } = timelineJS();
const html = render(data);

const outPath = outFile || jsonFile.replace(/\.json$/, '.html');
fs.writeFileSync(outPath, html, 'utf8');
console.log(`✅ HTML 已生成: ${outPath}`);
console.log(`   场景数: ${totalScenes()}  时长: ${timelineJS().duration}s`);
