# 知识星球 Skill 安装指南

本文档供 AI Agent 阅读并执行，帮助用户完成知识星球 Skill 的安装与配置。

## 前置条件

- Node.js >= 18（执行 `node -v` 检查）

## 安装步骤

### 1. 安装 CLI 工具

```bash
npm install -g zsxq-cli
```

### 2. 安装 Skill

优先使用 GitHub（海外用户）：

```bash
npx skills add https://github.com/unnoo/zsxq-skill --yes --global
```

如果 GitHub 不可达，使用 Gitee 备用通道（国内用户）：

```bash
npx skills add https://gitee.com/unnoo/zsxq-skill --yes --global
```

### 3. 登录知识星球账号

```bash
zsxq-cli auth login
```

执行后终端会输出授权链接与设备验证码。将链接提供给用户，让用户在浏览器中打开并确认授权。等待用户确认后即可开始使用。

## 网络受限时的备选方案

如果上述地址均不可达，可从以下地址下载离线包手动安装：

```
https://garden.zsxq.com/skill/zsxq-skills.zip
```

下载解压后执行：

```bash
npx skills add ./zsxq-skill --yes
```

## 安装完成

安装并登录后，AI Agent 即可调用单一 `zsxq` 技能，覆盖以下能力：

| 能力 | 用途 |
|------|------|
| 星球管理 | 浏览星球、搜索成员、查询标签 |
| 主题操作 | 搜索、发布、编辑主题，评论回答 |
| 个人笔记 | 创建、编辑、管理笔记 |
| 用户信息 | 查看用户信息与足迹 |
| 认证与排错 | 认证授权、常见错误处理 |

## 从旧版升级

如果这台机器装过旧版的 5 个技能（`zsxq-shared`、`zsxq-group`、`zsxq-topic`、`zsxq-user`、`zsxq-note`），完成上述安装后对 AI 说：

> 检查并迁移旧版知识星球 skill

AI 会先扫描各安装位置并出具报告，经用户确认后才移动文件（先备份、可回滚）。仅检查不清理也可以，说「只检查旧版 zsxq skill」即可。

