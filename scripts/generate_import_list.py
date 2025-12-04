import json
import os
import urllib.parse
from datetime import datetime

def generate_import_list():
    current_dir = os.path.dirname(os.path.abspath(__file__))
    root_dir = os.path.dirname(current_dir)
    input_file = os.path.join(root_dir, 'data', 'hot_episodes.json')
    debug_file = os.path.join(root_dir, 'debug_log.txt') # 读取日志
    output_file = os.path.join(root_dir, 'PODWISE_IMPORT.html')
    
    episodes = []
    if os.path.exists(input_file):
        with open(input_file, 'r', encoding='utf-8') as f:
            episodes = json.load(f)

    date_str = datetime.now().strftime('%Y-%m-%d')
    
    html = []
    html.append(f"<h2>🎙️ 播客更新日报 ({date_str})</h2>")
    html.append(f"<p>今日更新: <b>{len(episodes)}</b> 集</p><hr>")
    
    html.append("<h3>📖 详细列表</h3>")
    html.append("<ul>")
    for ep in episodes:
        title = ep.get('title', '无标题')
        pod = ep.get('podcast', {}).get('title', '未知播客')
        link = ep.get('link', '')
        
        if not link:
            query = urllib.parse.quote(f"{pod} {title}")
            link = f"https://www.google.com/search?q={query}"
        
        html.append(f"<li>")
        html.append(f"  <b><a href='{link}' style='text-decoration:none; color:#2c3e50;'>{title}</a></b><br>")
        html.append(f"  <span style='color:#7f8c8d; font-size:0.9em;'>📻 {pod}</span>")
        html.append(f"</li><br>")
    html.append("</ul>")

    html.append("<hr><h3>📋 批量复制 (用于 Podwise 导入)</h3>")
    html.append("<pre style='background:#f4f4f4; padding:10px; border-radius:5px;'>")
    for ep in episodes:
        link = ep.get('link', '')
        if link and link.startswith('http'):
            html.append(link)
    html.append("</pre>")

    # ==========================================
    # 新增：在邮件底部显示诊断日志
    # ==========================================
    html.append("<hr><h3>🛠️ 诊断日志 (Debug Info)</h3>")
    html.append("<pre style='background:#333; color:#fff; padding:10px; border-radius:5px; font-size:0.8em;'>")
    if os.path.exists(debug_file):
        with open(debug_file, 'r', encoding='utf-8') as f:
            html.append(f.read())
    else:
        html.append("无日志文件")
    html.append("</pre>")

    with open(output_file, 'w', encoding='utf-8') as f:
        f.write('\n'.join(html))
    
    print(f"✅ 已生成 HTML 邮件内容: {output_file}")

if __name__ == "__main__":
    generate_import_list()
