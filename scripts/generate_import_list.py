import json
import os
import urllib.parse
from datetime import datetime

def generate_import_list():
    current_dir = os.path.dirname(os.path.abspath(__file__))
    root_dir = os.path.dirname(current_dir)
    input_file = os.path.join(root_dir, 'data', 'hot_episodes.json')
    output_file = os.path.join(root_dir, 'PODWISE_IMPORT.md')
    
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
    
    lines.append("## 📖 详细列表")
    for ep in episodes:
        title = ep.get('title', '无标题').replace('|', '-')
        pod = ep.get('podcast', {}).get('title', '未知播客')
        link = ep.get('link', '')
        
        # --- 🛡️ 保底机制 ---
        # 如果链接为空，生成一个 Google 搜索链接
        if not link:
            query = urllib.parse.quote(f"{pod} {title}")
            link = f"https://www.google.com/search?q={query}"
        # ------------------
        
        lines.append(f"**[{title}]({link})**")
        lines.append(f"> 📻 {pod}")
        lines.append("")

    lines.append("\n## 📋 批量复制 (用于 Podwise 导入)")
    lines.append("```text")
    for ep in episodes:
        link = ep.get('link', '')
        if link and link.startswith('http'):
            lines.append(link)
    lines.append("```")

    with open(output_file, 'w', encoding='utf-8') as f:
        f.write('\n'.join(lines))
    
    print(f"✅ 已生成邮件内容: {output_file}")

if __name__ == "__main__":
    generate_import_list()
