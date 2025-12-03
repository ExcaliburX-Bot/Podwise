import json
import os
from datetime import datetime

def main():
    data_files = {
        'full': 'data/full.json',
        'new_podcasts': 'data/new_podcasts.json',
        'hot_episodes': 'data/hot_episodes.json',
        'hot_episodes_new': 'data/hot_episodes_new.json'
    }
    
    datasets = {}
    for name, filepath in data_files.items():
        if os.path.exists(filepath):
            with open(filepath, 'r', encoding='utf-8') as f:
                datasets[name] = json.load(f)
    
    report = f"""# 🎙️ 中文播客热榜

> 数据来源: [xyzrank.eddiehe.top](https://xyzrank.eddiehe.top)  
> 更新时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}  
> 自动更新: 每6小时

---

## 📊 数据统计

"""
    
    if 'hot_episodes' in datasets and 'data' in datasets['hot_episodes']:
        hot_count = len(datasets['hot_episodes']['data'].get('episodes', []))
        report += f"- 🔥 热门单集: {hot_count} 个\n"
    
    if 'hot_episodes_new' in datasets and 'data' in datasets['hot_episodes_new']:
        new_hot_count = len(datasets['hot_episodes_new']['data'].get('episodes', []))
        report += f"- 🆕 新热门单集: {new_hot_count} 个\n"
    
    if 'new_podcasts' in datasets and 'data' in datasets['new_podcasts']:
        new_podcast_count = len(datasets['new_podcasts']['data'].get('podcasts', []))
        report += f"- ✨ 新播客: {new_podcast_count} 个\n"
    
    if 'full' in datasets and 'data' in datasets['full']:
        full_count = len(datasets['full']['data'].get('podcasts', []))
        report += f"- 📚 全部播客: {full_count} 个\n"
    
    report += "\n---\n\n"
    
    if 'hot_episodes' in datasets and 'data' in datasets['hot_episodes']:
        episodes = datasets['hot_episodes']['data'].get('episodes', [])
        report += "## 🔥 热门单集 Top 10\n\n"
        
        for i, ep in enumerate(episodes[:10], 1):
            report += f"### {i}. {ep.get('title', '未知标题')}\n\n"
            report += f"- **播客**: {ep.get('podcastName', '未知')}\n"
            report += f"- **播放量**: {ep.get('playCount', 0):,}\n"
            report += f"- **评论数**: {ep.get('commentCount', 0):,}\n"
            report += f"- **时长**: {ep.get('duration', 0)} 分钟\n"
            report += f"- **发布时间**: {ep.get('postTime', '未知')[:10]}\n"
            report += f"- **链接**: [收听]({ep.get('link', '#')})\n\n"
    
    if 'hot_episodes_new' in datasets and 'data' in datasets['hot_episodes_new']:
        episodes_new = datasets['hot_episodes_new']['data'].get('episodes', [])
        report += "\n---\n\n## 🆕 新热门单集 Top 5\n\n"
        
        for i, ep in enumerate(episodes_new[:5], 1):
            report += f"### {i}. {ep.get('title', '未知标题')}\n\n"
            report += f"- **播客**: {ep.get('podcastName', '未知')}\n"
            report += f"- **播放量**: {ep.get('playCount', 0):,}\n"
            report += f"- **评论数**: {ep.get('commentCount', 0):,}\n"
            report += f"- **时长**: {ep.get('duration', 0)} 分钟\n"
            report += f"- **链接**: [收听]({ep.get('link', '#')})\n\n"
    
    if 'new_podcasts' in datasets and 'data' in datasets['new_podcasts']:
        podcasts = datasets['new_podcasts']['data'].get('podcasts', [])
        report += "\n---\n\n## ✨ 新播客推荐 Top 5\n\n"
        
        for i, pod in enumerate(podcasts[:5], 1):
            report += f"### {i}. {pod.get('title', '未知标题')}\n\n"
            report += f"- **作者**: {pod.get('author', '未知')}\n"
            report += f"- **订阅数**: {pod.get('subscription', 0):,}\n"
            report += f"- **单集数**: {pod.get('totalEpisodesCount', 0)}\n"
            report += f"- **分类**: {pod.get('primaryGenreName', '未知')}\n"
            report += f"- **链接**: [订阅]({pod.get('link', '#')})\n\n"
    
    report += """
---

## 📁 数据文件

- [完整播客列表](data/full.json)
- [新播客列表](data/new_podcasts.json)
- [热门单集](data/hot_episodes.json)
- [新热门单集](data/hot_episodes_new.json)

---

*本项目由 GitHub Actions 自动更新*
"""
    
    with open('README.md', 'w', encoding='utf-8') as f:
        f.write(report)
    
    print("✓ 报告生成完成！")

if __name__ == '__main__':
    main()
