import json
import os
from datetime import datetime

def generate_import_list():
    # 获取当前脚本所在的目录 (scripts/)
    current_dir = os.path.dirname(os.path.abspath(__file__))
    # 获取项目根目录 (scripts 的上一级)
    root_dir = os.path.dirname(current_dir)
    
    # 拼接绝对路径，确保一定能找到文件
    input_file = os.path.join(root_dir, 'data', 'hot_episodes.json')
    output_file = os.path.join(root_dir, 'PODWISE_IMPORT.md')
    
    if not os.path.exists(input_file):
        print(f"⚠️ 警告: 找不到数据文件 {input_file}")
        # 生成空文件防止报错
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
        url = ep.get('enclosureUrl', '')
        
        lines.append(f"**{title}**")
        lines.append(f"> 📻 {pod}")
        lines.append(f"> 🔗 {url}")
        lines.append("")

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
