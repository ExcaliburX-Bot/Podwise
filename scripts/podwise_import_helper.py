"""
Podwise 导入助手
生成导入清单，方便手动在 Podwise 导入播客
"""

import json
import os
from datetime import datetime

def generate_import_list():
    """生成导入清单"""
    
    # 确保数据目录存在
    os.makedirs('data', exist_ok=True)
    
    # 读取热门播客数据
    try:
        with open('data/hot_episodes.json', 'r', encoding='utf-8') as f:
            episodes = json.load(f)
    except FileNotFoundError:
        print("❌ 错误: 找不到 data/hot_episodes.json")
        print("请先运行 fetch_podcasts.py")
        return
    
    # 只处理 Top 10
    top_episodes = episodes[:10]
    
    # 生成 Markdown 导入清单
    markdown = f"""# 🎙️ Podwise 导入清单

> 📅 生成时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
> 📊 总计: {len(top_episodes)} 个播客

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

"""
    
    # 生成每个播客的详细信息
    for i, episode in enumerate(top_episodes, 1):
        title = episode.get('title', '未知标题')
        podcast_name = episode.get('podcast', {}).get('title', '未知播客')
        audio_url = episode.get('enclosureUrl', '')
        description = episode.get('description', '暂无简介')
        
        # 截取简介前150字
        if len(description) > 150:
            description = description[:150] + '...'
        
        markdown += f"""### {i}. {title}

**播客名称**: {podcast_name}

**简介**: {description}

**音频链接**:
```
{audio_url}
```

**导入状态**: ⬜ 待导入

**Podwise 链接**: _导入后填写_

<details>
<summary>📋 快速复制</summary>

音频链接（点击复制）:
```
{audio_url}
```

</details>

---

"""
    
    # 添加使用说明
    markdown += """
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
"""
    
    # 保存 Markdown 文件
    with open('PODWISE_IMPORT.md', 'w', encoding='utf-8') as f:
        f.write(markdown)
    
    print("✅ 导入清单已生成: PODWISE_IMPORT.md")
    
    # 生成纯文本链接列表（方便批量复制）
    with open('data/audio_urls.txt', 'w', encoding='utf-8') as f:
        for i, episode in enumerate(top_episodes, 1):
            title = episode.get('title', '未知标题')
            audio_url = episode.get('enclosureUrl', '')
            f.write(f"# {i}. {title}\n")
            f.write(f"{audio_url}\n\n")
    
    print("✅ 音频链接列表已生成: data/audio_urls.txt")
    
    # 生成追踪数据文件
    tracking_data = {
        "generated_at": datetime.now().isoformat(),
        "total_count": len(top_episodes),
        "episodes": []
    }
    
    for i, episode in enumerate(top_episodes, 1):
        tracking_data["episodes"].append({
            "rank": i,
            "title": episode.get('title', '未知标题'),
            "podcast": episode.get('podcast', {}).get('title', '未知播客'),
            "audio_url": episode.get('enclosureUrl', ''),
            "xiaoyuzhou_url": episode.get('url', ''),
            "imported": False,
            "podwise_url": "",
            "notes": ""
        })
    
    with open('data/podwise_tracking.json', 'w', encoding='utf-8') as f:
        json.dump(tracking_data, f, ensure_ascii=False, indent=2)
    
    print("✅ 追踪数据已生成: data/podwise_tracking.json")
    print(f"\n📊 共 {len(top_episodes)} 个播客待导入")

if __name__ == '__main__':
    generate_import_list()