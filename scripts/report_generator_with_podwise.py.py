"""
智能报告生成器 - 整合 Podwise 分析结果
"""

import json
import os
from datetime import datetime

def generate_report():
    """生成包含 Podwise 分析链接的智能报告"""
    
    # 读取追踪数据
    try:
        with open('data/podwise_tracking.json', 'r', encoding='utf-8') as f:
            tracking = json.load(f)
    except FileNotFoundError:
        print("❌ 错误: 找不到 data/podwise_tracking.json")
        print("请先运行 podwise_import_helper.py")
        return
    
    episodes = tracking.get('episodes', [])
    
    # 统计数据
    total = len(episodes)
    imported = sum(1 for ep in episodes if ep.get('imported', False))
    
    # 生成 README
    readme = f"""# 🎙️ 小宇宙播客热榜 - AI 智能分析版

> 🤖 **AI 分析工具**: [Podwise](https://podwise.ai)  
> 📅 **更新时间**: {datetime.now().strftime('%Y年%m月%d日 %H:%M')}  
> 📊 **分析进度**: {imported}/{total} 已完成

---

## 📈 本期概览

- 🎯 **热榜播客**: {total} 个
- ✅ **AI 分析完成**: {imported} 个
- ⏳ **待分析**: {total - imported} 个

---

## 🎯 Top {total} 热门播客

"""
    
    # 生成每个播客的详细信息
    for episode in episodes:
        rank = episode.get('rank', 0)
        title = episode.get('title', '未知标题')
        podcast = episode.get('podcast', '未知播客')
        xiaoyuzhou_url = episode.get('xiaoyuzhou_url', '')
        audio_url = episode.get('audio_url', '')
        imported = episode.get('imported', False)
        podwise_url = episode.get('podwise_url', '')
        notes = episode.get('notes', '')
        
        # 状态标记
        status = "✅ 已分析" if imported else "⏳ 待分析"
        
        readme += f"""### {rank}. {title}

**播客**: {podcast}

**状态**: {status}

**链接**:
"""
        
        # 添加小宇宙链接
        if xiaoyuzhou_url:
            readme += f"- 🎧 [小宇宙收听]({xiaoyuzhou_url})\n"
        
        # 添加音频链接
        if audio_url:
            readme += f"- 🎵 [音频地址]({audio_url})\n"
        
        # 添加 Podwise 分析链接
        if imported and podwise_url:
            readme += f"- 🤖 [Podwise AI 分析]({podwise_url}) ⭐\n"
        elif not imported:
            readme += f"- 📥 [点击导入到 Podwise](https://podwise.ai) (复制音频链接)\n"
        
        # 添加备注
        if notes:
            readme += f"\n**💡 备注**: {notes}\n"
        
        readme += "\n---\n\n"
    
    # 添加使用说明
    readme += f"""
## 🚀 如何使用

### 查看 AI 分析

点击播客旁边的 **"Podwise AI 分析"** 链接，可以查看：

- 📝 **智能摘要**: AI 生成的内容概要
- 🗺️ **思维导图**: 可视化的内容结构
- 🔑 **关键词**: 核心话题和概念
- 💬 **金句摘录**: 精彩观点集锦
- 📊 **章节划分**: 内容时间轴

### 导入新播客

1. 点击 **"点击导入到 Podwise"**
2. 在 Podwise 点击 **"Import via URL"**
3. 粘贴音频链接
4. 等待 AI 分析完成（3-5 分钟）

### 更新追踪数据

编辑 `data/podwise_tracking.json`:

```json
{{
  "rank": 1,
  "imported": true,
  "podwise_url": "https://podwise.ai/episodes/YOUR_ID",
  "notes": "很棒的内容！"
}}
```

---

## 📊 统计数据

| 指标 | 数值 |
|------|------|
| 📈 总播客数 | {total} |
| ✅ 已分析 | {imported} |
| ⏳ 待分析 | {total - imported} |
| 📊 完成率 | {imported/total*100:.1f}% |

---

## 🔄 自动更新

本报告由 GitHub Actions 自动生成和更新：

- ⏰ **更新频率**: 每 6 小时
- 🤖 **数据来源**: 小宇宙播客热榜 API
- 🧠 **AI 分析**: Podwise

---

## 📝 相关文件

- 📋 [导入清单](PODWISE_IMPORT.md) - 待导入播客列表
- 📊 [追踪数据](data/podwise_tracking.json) - 导入状态追踪
- 🔗 [音频链接](data/audio_urls.txt) - 纯文本链接列表

---

## 🤝 贡献

欢迎提交 Issue 和 PR！

---

**🤖 Powered by [Podwise](https://podwise.ai) | 📡 Data from [小宇宙](https://xiaoyuzhoufm.com)**

*最后更新: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}*
"""
    
    # 保存 README
    with open('README.md', 'w', encoding='utf-8') as f:
        f.write(readme)
    
    print("✅ 智能报告已生成: README.md")
    print(f"\n📊 统计:")
    print(f"   - 总播客数: {total}")
    print(f"   - 已分析: {imported}")
    print(f"   - 待分析: {total - imported}")
    print(f"   - 完成率: {imported/total*100:.1f}%")

if __name__ == '__main__':
    generate_report()