import feedparser
import json
import os
import xml.etree.ElementTree as ET
from datetime import datetime, timedelta
import glob

# 保底链接
MANUAL_FEEDS = [
    "https://feed.xyzfm.space/dk4yh3pkpjp3"
]

# 全局诊断日志
debug_log = []

def log(msg):
    print(msg)
    debug_log.append(msg)

def find_opml_file(root_dir):
    # 1. 尝试标准路径
    standard_path = os.path.join(root_dir, 'subscriptions.opml')
    if os.path.exists(standard_path):
        return standard_path
    
    # 2. 尝试不区分大小写搜索
    files = os.listdir(root_dir)
    for f in files:
        if f.lower().endswith('.opml'):
            return os.path.join(root_dir, f)
            
    return None

def parse_opml(opml_path):
    urls = []
    try:
        tree = ET.parse(opml_path)
        root = tree.getroot()
        # 递归查找所有 outline 标签
        for outline in root.findall('.//outline'):
            # 尝试多种属性名 (有的 OPML 用 xmlUrl，有的用 url)
            url = outline.get('xmlUrl') or outline.get('url')
            if url:
                urls.append(url)
        log(f"📂 解析 OPML 成功: 找到 {len(urls)} 个订阅源")
    except Exception as e:
        log(f"⚠️ 解析 OPML 出错: {str(e)}")
    return urls

def get_best_link(entry):
    if entry.get('link'): return entry.get('link')
    if entry.get('links'):
        for l in entry.get('links', []):
            if l.get('type') == 'text/html' or l.get('rel') == 'alternate':
                if l.get('href'): return l.get('href')
    id_val = entry.get('id', '')
    if id_val.startswith('http'): return id_val
    if entry.get('enclosures'): return entry.get('enclosures')[0].get('href')
    return ''

def fetch_rss():
    current_dir = os.path.dirname(os.path.abspath(__file__))
    root_dir = os.path.dirname(current_dir)
    data_dir = os.path.join(root_dir, 'data')
    
    log(f"📍 脚本运行目录: {current_dir}")
    log(f"🏠 项目根目录: {root_dir}")
    
    # 查找 OPML
    opml_path = find_opml_file(root_dir)
    
    rss_feeds = []
    if opml_path:
        log(f"✅ 找到 OPML 文件: {opml_path}")
        rss_feeds = parse_opml(opml_path)
        if not rss_feeds:
            log("⚠️ OPML 文件是空的或格式不对，使用保底列表")
            rss_feeds = MANUAL_FEEDS
    else:
        log("❌ 未找到任何 .opml 文件！将在根目录下列出所有文件以供排查:")
        try:
            files = os.listdir(root_dir)
            log(f"📄 根目录文件列表: {', '.join(files)}")
        except:
            pass
        log("👉 使用保底列表")
        rss_feeds = MANUAL_FEEDS

    if not os.path.exists(data_dir):
        os.makedirs(data_dir)

    all_episodes = []
    # 抓取过去 7 天
    time_threshold = datetime.now() - timedelta(days=7)

    log(f"🚀 开始抓取 {len(rss_feeds)} 个源...")

    for feed_url in rss_feeds:
        try:
            feed = feedparser.parse(feed_url)
            podcast_title = feed.feed.get('title', '未知播客')
            
            if not feed.entries:
                continue

            for entry in feed.entries:
                try:
                    if hasattr(entry, 'published_parsed') and entry.published_parsed:
                        pub_date_parsed = entry.published_parsed
                        pub_date = datetime(*pub_date_parsed[:6])
                    else:
                        continue
                except:
                    continue

                if pub_date > time_threshold:
                    final_link = get_best_link(entry)
                    all_episodes.append({
                        'title': entry.title,
                        'podcast': {'title': podcast_title},
                        'link': final_link,
                        'pubDate': str(pub_date)
                    })
        except Exception as e:
            # 单个源失败不记录到全局日志，免得太长
            print(f"❌ 错误 {feed_url}: {e}")

    all_episodes.sort(key=lambda x: x['pubDate'], reverse=True)

    # 保存数据
    output_file = os.path.join(data_dir, 'hot_episodes.json')
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(all_episodes, f, ensure_ascii=False, indent=2)

    # ==========================================
    # 重点：把诊断日志也保存下来，稍后发邮件用
    # ==========================================
    debug_file = os.path.join(root_dir, 'debug_log.txt')
    with open(debug_file, 'w', encoding='utf-8') as f:
        f.write('\n'.join(debug_log))
    
    print(f"\n🎉 完成！抓取到 {len(all_episodes)} 集。")

if __name__ == "__main__":
    fetch_rss()

