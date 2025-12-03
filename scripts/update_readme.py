import json
import os
from datetime import datetime

def update_readme():
    json_path = 'data/hot_episodes.json'
    readme_path = 'README.md'
    
    if not os.path.exists(json_path):
        print("数据文件不存在，跳过更新")
        return

    with open(json_path, 'r', encoding='utf-8') as f:
        episodes = json.load(f)

    # 生成 Markdown 表格
    table_lines = []
    table_lines.append("| 封面 | 标题 (点击跳转) | 播客 | 更新时间 |")
    table_lines.append("| :---: | :--- | :--- | :--- |")

    for ep in episodes:
        title = ep.get('title', '无标题').replace('|', '-')
        link = ep.get('enclosureUrl', '#')
        podcast = ep.get('podcast', {}).get('title', '未知')
        # 截取日期 YYYY-MM-DD
        pub_date = ep.get('pubDate', '')[:10]
        
        # 这里的封面图暂时用占位符，因为 RSS 里提取封面比较耗时，先从简
        img = "https://placehold.co/60x60/png?text=POD"
        
        row = f"| <img src='{img}' width='40'> | [{title}]({link}) | {podcast} | {pub_date} |"
        table_lines.append(row)

    # 读取现有的 README (如果有的话)
    header = "# 🎙️ 我的播客订阅日报\n\n每天自动抓取最新单集，方便导入 Podwise。\n\n"
    footer = f"\n\n_最后更新: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}_"
    
    content = header + "\n".join(table_lines) + footer

    with open(readme_path, 'w', encoding='utf-8') as f:
        f.write(content)
        
    print("✅ README 更新完成")

if __name__ == "__main__":
    update_readme()
