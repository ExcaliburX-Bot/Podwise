# 🎯 Podwise 半自动化使用指南

## 📖 概述

这个系统通过 GitHub Actions 自动抓取播客热榜，生成导入清单，你手动在 Podwise 导入并分析，最后自动生成包含 AI 分析链接的智能报告。

---

## 🚀 快速开始

### 第一步：部署自动化系统

1. **添加脚本到仓库**

```bash
# 进入你的仓库
cd Podwise

# 创建目录
mkdir -p scripts .github/workflows data

# 添加以下文件：
# scripts/podwise_import_helper.py
# scripts/report_generator_with_podwise.py
# .github/workflows/podcast_intelligence_podwise.yml
```

2. **提交并推送**

```bash
git add .
git commit -m "✨ 添加 Podwise 半自动化集成"
git push
```

---

### 第二步：首次运行

1. **触发工作流**
   - 进入 GitHub 仓库的 **Actions** 标签
   - 选择 **Podcast Intelligence with Podwise**
   - 点击 **Run workflow**

2. **等待完成**
   - 工作流会自动抓取热榜
   - 生成 `PODWISE_IMPORT.md` 导入清单
   - 生成初始版 `README.md`

---

### 第三步：在 Podwise 导入播客

1. **打开导入清单**
   - 在仓库中打开 `PODWISE_IMPORT.md`
   - 查看 Top 10 播客列表

2. **逐个导入到 Podwise**
   
   对于每个播客：
   
   a. 复制音频链接
   ```
   https://example.com/podcast.mp3
   ```
   
   b. 打开 [Podwise](https://podwise.ai)
   
   c. 点击顶部的 **"Import via URL"**
   
   d. 粘贴音频链接并提交
   
   e. 等待 AI 分析完成（通常 3-5 分钟）

3. **记录 Podwise 链接**
   
   分析完成后：
   
   a. 在 Podwise 中打开该播客
   
   b. 复制页面 URL，例如：
   ```
   https://podwise.ai/episodes/abc123
   ```
   
   c. 在 `PODWISE_IMPORT.md` 中标记为 ✅

---

### 第四步：更新追踪数据

编辑 `data/podwise_tracking.json`：

```json
{
  "generated_at": "2024-01-01T12:00:00",
  "total_count": 10,
  "episodes": [
    {
      "rank": 1,
      "title": "播客标题",
      "podcast": "播客名称",
      "audio_url": "https://...",
      "imported": true,           // ← 改为 true
      "podwise_url": "https://podwise.ai/episodes/abc123",  // ← 填入链接
      "notes": "很棒的内容！"     // ← 可选备注
    }
  ]
}
```

---

### 第五步：重新生成报告

```bash
# 本地运行（推荐）
python scripts/report_generator_with_podwise.py

# 或者提交更新，让 GitHub Actions 自动运行
git add data/podwise_tracking.json
git commit -m "📝 更新 Podwise 分析链接"
git push
```

---

## 🔄 日常使用流程

### 自动部分（GitHub Actions 每 6 小时）

1. ✅ 抓取最新热榜
2. ✅ 生成导入清单
3. ✅ 生成基础报告

### 手动部分（你需要做的，每周约15分钟）

1. 📋 查看 `PODWISE_IMPORT.md`
2. 📥 在 Podwise 导入新播客
3. 🔗 复制 Podwise 分析链接
4. 📝 更新 `podwise_tracking.json`
5. 🚀 提交更新

---

## 📊 文件说明

| 文件 | 说明 | 更新方式 |
|------|------|----------|
| `data/hot_episodes.json` | 原始热榜数据 | 自动 |
| `PODWISE_IMPORT.md` | 导入清单 | 自动生成，手动标记 |
| `data/podwise_tracking.json` | 追踪数据 | 手动更新 |
| `data/audio_urls.txt` | 纯文本链接列表 | 自动 |
| `README.md` | 最终报告 | 自动 |

---

## 💡 高级技巧

### 1. 批量导入

使用 `data/audio_urls.txt` 快速复制所有链接：

```
# 1. 东腔西调 东南亚（上）
https://xxx.mp3

# 2. 商业就是这样 第394期
https://yyy.mp3
```

### 2. 使用 Collections

在 Podwise 中创建 Collection：
- 名称：`小宇宙热榜 - 2024-01`
- 将导入的播客添加到 Collection
- 方便统一管理和查看

### 3. 标记重点

在 `podwise_tracking.json` 的 `notes` 字段记录：
- ⭐ 特别推荐
- 🔥 热点话题
- 💡 关键洞察

---

## 🐛 常见问题

### Q1: 某些播客无法导入到 Podwise？

**A**: 可能原因：
- 音频链接需要登录或付费
- 音频格式不支持
- 链接已过期

**解决方案**：
- 跳过该播客
- 在 `podwise_tracking.json` 中标记 `imported: false`
- 在 `notes` 中说明原因

### Q2: Podwise 分析时间太长？

**A**: 
- 正常情况下 3-5 分钟
- 长播客（>2小时）可能需要 10-15 分钟
- 可以先导入，稍后再回来查看结果

### Q3: 如何批量更新 Podwise 链接？

**A**: 
- 使用文本编辑器打开 `podwise_tracking.json`
- 批量替换和编辑
- 确保 JSON 格式正确

---

## 🎯 最佳实践

### 每周工作流：

**周一早上（15 分钟）**
1. 查看 GitHub Actions 自动生成的导入清单
2. 选择感兴趣的 5-10 个播客
3. 批量导入到 Podwise

**周三晚上（10 分钟）**
1. 查看 Podwise 分析结果
2. 复制链接并更新追踪数据
3. 提交更新

**周五下午（5 分钟）**
1. 查看更新后的 README
2. 分享给团队或朋友

---

## 📈 示例文件

### `PODWISE_IMPORT.md` 示例：

```markdown
# 🎙️ Podwise 导入清单

### 1. 东腔西调 东南亚（上）

**音频链接**:
```
https://xxx.mp3
```

**导入状态**: ⬜ 待导入

**Podwise 链接**: _导入后填写_
```

### `README.md` 示例：

```markdown
# 🎙️ 小宇宙播客热榜 - AI 智能分析版

## 🎯 Top 10 热门播客

### 1. 东腔西调 东南亚（上）

**状态**: ✅ 已分析

**链接**:
- 🎧 [小宇宙收听](...)
- 🤖 [Podwise AI 分析](https://podwise.ai/episodes/abc123) ⭐
```

---

## 🤝 贡献

欢迎提交 Issue 和 PR！

---

**🤖 祝你使用愉快！**