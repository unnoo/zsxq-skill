# 单星球海报布局规格（仅 1 个星球）

> 由 [`render-poster.md`](render-poster.md) 的「渲染 HTML」步骤引用；截图与高清渲染流程见同文档「截图」节。

## 适用场景

本次入选展示的星球数 = **1** 时使用本布局。手机优先紧凑版式：窄宽度、低留白、二维码移到卡片底部右侧（与汇总条同行），不抢主标题/内容视线。

## 基础尺寸与排版

- **body 宽度**：320px（紧凑窄屏）
- **body padding**：16px 10px 12px
- **背景**：`linear-gradient(135deg, #667eea, #764ba2)`
- **字体抗锯齿**：`-webkit-font-smoothing: antialiased; text-rendering: optimizeLegibility;`
- **卡片**：白底 / 圆角 10px / `box-shadow: 0 4px 12px rgba(0,0,0,0.12)` / 内边距 10px / 卡片间距 8px

## 头部

居中三行 + 一条 chip：

| 元素 | 字号 | 备注 |
|------|------|------|
| 日期（如 `2026 · 05 · 18`） | 10px | `opacity:0.85`，letter-spacing 1.5px |
| 标题「知识星球日报」 | 18px / 700 | `margin: 3px 0 2px` |
| 副标题「Daily Report · 自动生成」 | 10px | `opacity:0.8` |
| 时间范围 chip（如 `最近 7 天`） | 9px | 半透明白底 rounded |

## 星球区块

唯一一张卡片，**不需要** `position: relative`（二维码不再绝对定位）。

```
卡片
├─ group-title    （星球名 13px / 700  +  "展示 N 条" chip 9px）
├─ topic[]
│   ├─ idx        （14px 列宽，11px / 600 / #aaa）
│   └─ body
│       ├─ title  （12px / 600 / line-height 1.4
│       │         word-break: break-word; overflow-wrap: anywhere）
│       └─ meta   （9px / #888，author / 时间 / stats）
└─ footer-row     （汇总 + 二维码,同一行,见下）
```

## 汇总 + 二维码同行（footer-row）

```css
.footer-row {
  margin-top: 6px;
  padding-top: 6px;
  border-top: 1px solid #f0f0f5;
  display: flex;
  align-items: center;
  gap: 6px;
}
.summary { flex: 1; display: flex; justify-content: space-around; font-size: 9px; color: #666; }
.summary .num { font-size: 12px; font-weight: 700; color: #667eea; }   /* 4 项数字 */
.qr { flex: 0 0 56px; text-align: center; }
.qr img {
  width: 56px; height: 56px;
  background: #fff;
  border: 1px solid #eee;
  border-radius: 3px;
}
.qr .label { font-size: 8px; color: #999; margin-top: 2px; }
```

二维码源 PNG 推荐宽度 ≥ 200px（清晰度足够支撑 2x 渲染下的 56px 显示）。

二维码不启用时，`footer-row` 内只有 `summary`，不需要左侧 padding 调整。

## 互动数据 0 值省略

主题行 `meta.stats` 中：`likes / comments / readers` 任一为 0 时该字段整段不输出；三者全为 0 时整段 stats 省略，只保留 `author · 时间`。

汇总条同理：`数 = 0` 的项不在卡片底部展示。

## 主题数量与海报高度

参考输出尺寸（2x 渲染，body 截图）：

| 主题数 | 海报高度（px） | 文件大小 |
|--------|---------------|---------|
| 5 条 | ≈ 1152 | ~200K |
| 10 条 | ≈ 1768 | ~325K |

> 10 条以上滑动成本明显升高，单星球场景仍建议默认 **5 条**（与全局默认一致）。

## 页脚

居中 8px 浅色文字「由知识星球日报生成器自动生成」（单星球场景下文案稍简）。
