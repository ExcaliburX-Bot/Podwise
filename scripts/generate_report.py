import json
import os
from datetime import datetime

def generate_import_list():
    input_file = 'data/hot_episodes.json'
    output_file = 'PODWISE_IMPORT.md'
    
    if not os.path.exists(input_file):
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write("暂无更新数据")
        return

    with open(input_file, 'r', encoding='utf-8') as f:
        episodes = json.load(f)

    date_str = datetime.now().strftime('%Y-%m-%d')
    
    lines = []
    lines.append(f"# 🎙️ 播客更新日报 ({date_str})")
    lines.append(f"今日更新: {len(episodes)} 集\n")
    
    # 1. 详细列表
    lines.append("## 📖 详细列表")
    for ep in episodes:
        title = ep.get('title', '无标题').replace('|', '-')
        pod = ep.get('podcast', {}).get('title', '未知播客')
        url = ep.get('enclosureUrl', '')
        
        lines.append(f"**{title}**")
        lines.append(f"> 📻 {pod}")
        lines.append(f"> 🔗 {url}")
        lines.append("") # 空行

    # 2. 纯链接列表 (方便批量复制)
    lines.append("\n## 📋 批量复制 (用于 Podwise 导入)")
    lines.append("```text")
    for ep in episodes:
        url = ep.get('enclosureUrl', '')
        if url:
            lines.append(url)
    lines.append("```")

    with open(output_file, 'w', encoding='utf-8') as f:
        f.write('\n'.join(lines))
    
    print(f"✅ 已生成邮件内容: {output_file}")

if __name__ == "__main__":
    generate_import_list()

