# 多星球海报布局规格（≥ 2 个星球）

> 由 [`render-poster.md`](render-poster.md) 的「渲染 HTML」步骤引用；截图与高清渲染流程见同文档「截图」节。

## 适用场景

本次入选展示的星球数 **≥ 2** 时使用本布局。整体偏桌面/平板版式，单卡片信息量大，二维码贴在卡片右上角。

## 基础尺寸与排版

- **body 宽度**：1080px
- **body padding**：52px 40px
- **背景**：`linear-gradient(135deg, #667eea, #764ba2)`
- **字体抗锯齿**：`-webkit-font-smoothing: antialiased; text-rendering: optimizeLegibility;`
- **卡片**：白底 / 圆角 24px / `box-shadow: 0 12px 36px rgba(0,0,0,0.14)` / 内边距 34px 38px / 卡片间距 24px

## 头部

居中三行 + 一条 chip：

| 元素 | 字号 | 备注 |
|------|------|------|
| 日期（如 `2026 · 05 · 18`） | 18px | `opacity:0.9` |
| 标题「知识星球日报」 | 44px / 700 | `margin: 12px 0 8px` |
| 副标题「Daily Report · 自动生成」 | 16px | `opacity:0.85` |
| 时间范围 chip（如 `最近 7 天 · 2026-05-08 ~ 2026-05-14`） | 13px | 半透明白底 rounded |

## 星球区块

外层加 `position: relative`，避免右上角二维码被裁切。

```
卡片
├─ group-title    （星球名 26px / 700  +  "新增 N 条" chip 14px）
├─ topic[]
│   ├─ idx        （32px 列宽，16px / 600 / #aaa）
│   └─ body
│       ├─ title  （18px / 600 / line-height 1.55，word-break: break-word）
│       └─ meta   （13px / #888，包含 author / 时间 / stats）
└─ summary        （4 项：新增 / 点赞 / 评论 / 阅读，数字 22px / 700，0 值省略）
```

## 二维码（可选,由 render-poster 的「二维码」步骤决定）

绝对定位卡片右上角：

```css
.qr {
  position: absolute;
  top: 24px;
  right: 28px;
  width: 120px;
  text-align: center;
}
.qr img {
  width: 120px;
  height: 120px;
  background: #fff;
  border: 1px solid #eee;
  border-radius: 8px;
}
.qr .label { font-size: 12px; color: #999; margin-top: 6px; }
```

启用时：
- 卡片整体 `padding-right` 增加到 **180px**，避免长标题被遮挡
- 二维码源 PNG 宽度 ≥ 240px（生成时已留余量，默认 300px）

## 互动数据 0 值省略

主题行 `meta.stats` 中：`likes / comments / readers` 任一为 0 时该字段整段不输出；三者全为 0 时整段 stats 省略，只保留 `author · 时间`。

汇总条同理：`数 = 0` 的项不在卡片底部展示。

## 跳过的星球

海报内不出现任何与跳过星球相关的卡片或文字。跳过提示只放在文字版报告末尾。

## 页脚

居中 12px 浅色文字「由知识星球日报生成器自动生成」。

## 输出体积参考

2 个星球各 3-5 条主题 + 二维码 → 约 700-900K PNG（2x 渲染，1080×约 2400-2800）。
