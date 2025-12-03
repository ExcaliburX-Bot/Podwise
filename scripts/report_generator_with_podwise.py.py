import json
import os
from datetime import datetime

def main():
    # 读取追踪数据
    tracking_file = 'data/podwise_tracking.json'
    
    # 如果没有追踪数据，说明还没运行过 import helper，或者出错了
    if not os.path.exists(tracking_file):
        print(f"⚠️ 未找到追踪数据 {tracking_file}，尝试直接读取热榜数据作为兜底...")
        # 兜底逻辑：如果 tracking 文件不存在，尝试读取 hot_episodes
        hot_file = 'data/hot_episodes.json'
        if os.path.exists(hot_file):
            with open(hot_file, 'r', encoding='utf-8') as f:
                hot_data = json.load(f)
            # 构造临时的 episodes 数据结构用于生成报告
            episodes = []
            for i, item in enumerate(hot_data[:10], 1):
                episodes.append({
                    "rank": i,
                    "title": item.get('title', '未知标题'),
                    "podcast": item.get('podcast', {}).get('title', '未知播客'),
                    "xiaoyuzhou_url": f"https://www.xiaoyuzhoufm.com/episode/{item.get('eid', '')}",
                    "audio_url": item.get('enclosureUrl', ''),
                    "imported": False,
                    "podwise_url": "",
                    "notes": ""
                })
        else:
            print("❌ 连热榜数据也没找到，无法生成报告。")
            return
    else:
        with open(tracking_file, 'r', encoding='utf-8') as f:
            data = json.load(f)
        episodes = data.get('episodes', [])

    total = len(episodes)
    imported_count = sum(1 for e in episodes if e.get('imported'))
    
    # 生成 README 内容
    content = f"""# 🎙️ 小宇宙播客热榜 - AI 智能分析版

> 🤖 **AI 分析**: [Podwise](https://podwise.ai)  
> 📅 **更新时间**: {datetime.now().strftime('%Y-%m-%d %H:%M')}  
> 📊 **分析进度**: {imported_count}/{total} 已完成

---

## 🎯 Top {total} 热门播客

"""

    for ep in episodes:
        status = "✅ AI 已分析" if ep.get('imported') else "⏳ 等待导入"
        podwise_link = ep.get('podwise_url', '')
        
        content += f"### {ep['rank']}. {ep['title']}\n\n"
        content += f"**播客**: {ep['podcast']}\n\n"
        content += f"**状态**: {status}\n\n"
        
        content += "**链接**:\n"
        content += f"- 🎧 [小宇宙收听]({ep['xiaoyuzhou_url']})\n"
        content += f"- 🎵 [音频文件]({ep['audio_url']})\n"
        
        if ep.get('imported') and podwise_link:
            content += f"- 🧠 **[Podwise 智能分析]({podwise_link})** (摘要/思维导图/金句)\n"
        else:
            content += f"- 📥 [去 Podwise 导入](https://podwise.ai) (复制音频链接)\n"
            
        if ep.get('notes'):
            content += f"\n> 💡 **笔记**: {ep['notes']}\n"
            
        content += "\n---\n\n"

    content += """## 🛠️ 如何使用

1. 查看 [PODWISE_IMPORT.md](PODWISE_IMPORT.md) 获取待导入的音频链接。
2. 在 [Podwise](https://podwise.ai) 点击 "Import via URL" 导入。
3. 分析完成后，将 Podwise 链接更新到 `data/podwise_tracking.json`。
4. 提交代码，本报告将自动更新。

*Powered by GitHub Actions & Podwise*
"""

    with open('README.md', 'w', encoding='utf-8') as f:
        f.write(content)
    
    print(f"✅ 报告已生成: README.md (已分析: {imported_count}/{total})")

if __name__ == "__main__":
    main()
