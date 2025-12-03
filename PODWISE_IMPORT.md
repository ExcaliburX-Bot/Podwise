# 🎙️ Podwise 导入清单

> 📅 生成时间: 2025-12-03 09:19:06
> 📊 总计: 1 个播客

---

## 📋 导入步骤

1. 复制下方的音频链接
2. 打开 [Podwise](https://podwise.ai)
3. 点击顶部的 **"Import via URL"**
4. 粘贴音频链接并提交
5. 等待 AI 分析完成（3-5 分钟）
6. 复制 Podwise 页面链接
7. 更新 `data/podwise_tracking.json`

---

## 🎯 Top 10 热门播客

### 1. Ep 56. 对话 Hawstein：从独立开发，到追寻人生的意义

**播客名称**: 捕蛇者说

**简介**: 暂无简介

**音频链接**:
```
https://chrt.fm/track/6AGABB/r.typlog.com/eyJzIjozNTIsImUiOjgzMjIzLCJ0IjoxfQ.Fge4WkWpBXPcBM2Cr80utVUzDCs/pythonhunter/8245279839_643518.mp3
```

**导入状态**: ⬜ 待导入

**Podwise 链接**: _导入后填写_

<details>
<summary>📋 快速复制</summary>

音频链接（点击复制）:
```
https://chrt.fm/track/6AGABB/r.typlog.com/eyJzIjozNTIsImUiOjgzMjIzLCJ0IjoxfQ.Fge4WkWpBXPcBM2Cr80utVUzDCs/pythonhunter/8245279839_643518.mp3
```

</details>

---


## 💡 使用技巧

### 批量导入
1. 可以一次性复制多个链接
2. 在 Podwise 中连续导入
3. 稍后统一查看分析结果

### 创建 Collection
1. 在 Podwise 中创建 Collection: "小宇宙热榜"
2. 将导入的播客添加到 Collection
3. 方便统一管理

### 标记重点
- ⭐ 特别推荐
- 🔥 热点话题
- 💡 关键洞察

---

## 📝 下一步

完成导入后，请更新 `data/podwise_tracking.json`:

```json
{
  "rank": 1,
  "imported": true,
  "podwise_url": "https://podwise.ai/episodes/YOUR_EPISODE_ID",
  "notes": "你的备注"
}
```

然后运行:
```bash
python scripts/report_generator_with_podwise.py
```

或者提交更新让 GitHub Actions 自动运行。

---

**🤖 祝你使用愉快！**
