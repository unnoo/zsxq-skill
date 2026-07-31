# 海报渲染与截图机制

> 由场景入口 [`../generate-daily-poster.md`](../generate-daily-poster.md) 的「执行流程 · 渲染海报」步骤引用。本文档只讲**如何把已选主题渲染成 PNG**；选星球、拉数据、打分、文字报告在入口文档。

海报采用 **HTML 模板 → 本地 HTTP 服务 → Playwright 截图（2x 高清 / PNG 无损）** 的链路。渲染依赖 Playwright MCP（浏览器渲染工具）与本地 HTTP 服务；不可用时降级为保留 HTML 源文件。

## 子文档索引

| 文件 | 内容 |
|------|------|
| [`layout-multi.md`](layout-multi.md) | 多星球（≥ 2）布局：1080px / 二维码卡片右上角 |
| [`layout-single.md`](layout-single.md) | 单星球布局：320px 紧凑 / 二维码底部右侧 |

## 二维码（可选）

在渲染 HTML 前，若用户已确认「海报加入二维码」（默认关闭，见入口「用户确认点」），对每个**未跳过、本次会出现卡片**的星球生成一张 PNG：

```bash
npx --yes qrcode "https://m.zsxq.com/groups/<group_id>/join.html" \
    -o <tmpdir>/zsxq-qr-<group_id>.png -t png -w 300
```

- 存到与 HTML 同一临时目录，便于 `http-server` 同源访问；HTML 内用相对路径 `./zsxq-qr-<group_id>.png` 引用，避免协议/CORS 问题
- 宽度由布局决定（多星球 300px / 单星球 200px，按对应布局文件留余量）
- 任一张生成失败（如无网络无法 `npx`）**不阻塞海报**：该星球卡片省略二维码，文字报告末尾追加一行「星球 X 二维码生成失败，已省略」

## 渲染 HTML

按本次入选展示的星球数选布局：

| 入选星球数 | 布局文件 | 关键特征 |
|----------|--------|---------|
| **= 1** | [`layout-single.md`](layout-single.md) | 320px 紧凑窄屏 / 二维码与汇总条同行 / 手机优先 |
| **≥ 2** | [`layout-multi.md`](layout-multi.md) | 1080px 桌面版式 / 二维码绝对定位卡片右上角 |

两布局共享：渐变背景 `linear-gradient(135deg, #667eea, #764ba2)`；字体抗锯齿；互动数据 0 值省略；跳过星球不出现。

把 HTML 写入系统临时目录 `zsxq-report-<timestamp>.html`。临时目录按 OS 解析：

- **macOS / Linux**：`$TMPDIR`，否则 `/tmp`
- **Windows**：`%TEMP%`（cmd）/ `$env:TEMP`（PowerShell），通常 `C:\Users\<user>\AppData\Local\Temp`

## 截图（生成高清 PNG）

> 若入口「浏览器可用性预检」时用户已选「降级模式」，**跳过本节**，直接走下方「截图失败兜底」。

```
1. 启动本地 HTTP 服务（按顺序尝试，成功即停）：
   a. npx --yes http-server <tmpdir> -p <port> --silent
   b. python3 -m http.server <port> --directory <tmpdir>
   c. python  -m http.server <port> --directory <tmpdir>
   全部失败 → 走「截图失败兜底」

2. viewport 放大到约 2 倍 body 宽度：
   - 多星球：browser_resize(width=2160, height=1800)   # body 1080 × 2
   - 单星球：browser_resize(width=700,  height=1400)    # body 320 × 2 + 余量

3. 截图分两步，不要塞进单个 evaluate：
   a. browser_navigate(url='http://127.0.0.1:<port>/zsxq-report-<timestamp>.html')
   b. 用接受 async (page) => {...} 的工具执行 2x zoom + PNG 截图
      （browser_evaluate 拿不到 page 对象）：
      async (page) => {
        await page.evaluate(() => { document.body.style.zoom = '2'; });
        await page.waitForTimeout(200);
        const target = await page.$('body');           // 单星球用 body 截图
        await target.screenshot({
          path: '<tmpdir>/zsxq-report-<timestamp>.png',
          type: 'png'
        });
        // 多星球可改 page.screenshot({ fullPage: true, type: 'png', path: ... })
      }
   禁止用 browser_take_screenshot（filename 不落盘）。

4. 复制并改名到用户指定目录：
   mac/Linux: cp <tmpdir>/zsxq-report-<ts>.png <用户目录>/日报-<ts>.png
   Windows  : Copy-Item <tmpdir>\zsxq-report-<ts>.png <用户目录>\日报-<ts>.png

5. 清理：删临时 HTML、临时截图、临时二维码 PNG（zsxq-qr-*.png）、
   停止 HTTP 服务、调用 browser_close。
```

本地 HTTP 服务优先 `npx http-server`（与 Playwright MCP 共享 npx 依赖）；无 Node 时回退 Python。

## 截图失败兜底

预检通过后 `browser_navigate` / `page.screenshot` 仍可能因临时原因（端口冲突、HTTP 服务起不来、Playwright 调用超时等）失败。任一调用报错：

1. **不重试**，立即把临时 HTML 复制到用户指定目录，命名 `日报-<timestamp>.html`
2. 停止 HTTP 服务（若已起）、调用 `browser_close`（若已开窗）
3. 告知用户：

> ⚠️ 海报截图失败（原因：<具体错误>）。已为您保留 HTML 源文件：
>
> `<用户指定目录>/日报-<timestamp>.html`
>
> 您可用浏览器手动打开后截图或导出 PDF。文字报告已完整输出，不受影响。

## 参考

- 场景入口：[`../generate-daily-poster.md`](../generate-daily-poster.md)
- 布局规格：[`layout-multi.md`](layout-multi.md) / [`layout-single.md`](layout-single.md)
