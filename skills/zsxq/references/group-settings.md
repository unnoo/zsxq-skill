# group +settings（修改星球资料）

对应命令：`zsxq-cli group +settings`。

修改星球的公开资料：名称、简介、背景图、亮点图（最多 3 张）。未提供的字段保持不变。

> [!CAUTION]
> 这是**写入操作** —— 修改后的名称 / 简介 / 背景图 / 亮点图对星球全体成员可见。执行前必须向用户确认：
> 1. 目标星球（group_id 和星球名称）
> 2. 要修改的字段及新值（新名称、新简介全文、新背景图、新亮点图清单）

> [!IMPORTANT]
> - 字段为 patch 语义：只传要改的字段，未传的保持不变；名称与简介**无法清空**（不传即保留原值）
> - `--background`、`--promo-images` 只接受**本地图片文件路径**，上传后以星球资源形式引用
> - 背景图与亮点图均为**替换**语义：新图覆盖旧图；亮点图用 `--clear-promo-images` 清空

## 命令

```bash
# 修改名称与简介
zsxq-cli group +settings \
  --group-id 123456789 \
  --name "新星球名" \
  --description "新简介"

# 更换背景图
zsxq-cli group +settings --group-id 123456789 --background bg.png

# 设置亮点图（最多 3 张，逗号分隔）
zsxq-cli group +settings --group-id 123456789 --promo-images a.png,b.png,c.png

# 清空全部亮点图
zsxq-cli group +settings --group-id 123456789 --clear-promo-images
```

## 参数

| 参数 | 必填 | 说明 |
|------|------|------|
| `--group-id <id>` | **是** | 目标星球 ID |
| `--name <name>` | 否 | 新名称（1-15 个字符） |
| `--description <text>` | 否 | 新简介（最多 1000 字符） |
| `--background <path>` | 否 | 背景图本地图片路径（替换现有背景图） |
| `--promo-images <paths>` | 否 | 亮点图本地图片路径，逗号分隔，最多 3 张（全量替换现有亮点图） |
| `--clear-promo-images` | 否 | 清空全部亮点图（不能与 `--promo-images` 同用） |
| `--json` | 否 | 输出原始 JSON |

## 输出

成功后输出 `✓ Group settings updated` 及服务端返回的 JSON；`--json` 模式仅输出 JSON。

## 推荐工作流

```bash
# 第一步：确认目标星球与当前资料
zsxq-cli group +list

# 第二步：向用户确认要改的字段与新值后执行
zsxq-cli group +settings --group-id 123456789 --name "新星球名"

# 第三步：验证（名称可在 group +list 中看到；简介 / 背景图 / 亮点图建议在客户端确认）
zsxq-cli group +list
```

## 失败语义

参数校验或图片上传失败不会修改任何星球资料；上传成功后写入失败则资料保持不变（已上传图片成为未引用的资源，重试会重新上传）。

## 错误说明

| 错误 | 原因 |
|------|------|
| `请至少提供 --name、--description、--background 或 --promo-images 之一` | 没有提供任何要修改的字段（`--clear-promo-images` 除外） |
| `--clear-promo-images 和 --promo-images 不能同时使用` | 两个互斥参数同传 |
| `星球名称长度必须在 1-15 个字符之间` | 名称超出长度限制 |
| `星球描述不能超过 1000 字符` | 简介超出长度限制 |
| `星球亮点最多 3 张图片` | 亮点图超过 3 张 |
| `file not found: <path>` | 图片路径不存在 |
| `笔记不支持文件附件，仅支持图片 (...): <path>` | 传入的不是图片文件（CLI 上传校验的共享错误文案） |
| `上传背景图失败: 未获取到 image_id` | 背景图上传未返回 image_id |
| `API 错误(<code>): <msg>` | 服务端拒绝 |

通用错误（401、`--group-id is required` 等）见 [auth-errors](auth-errors.md#常见错误处理)。

## 参考

- [group-list](group-list.md) — 获取 group_id / 查看星球名称
- [SKILL.md](../SKILL.md) — 能力索引与安全规则
