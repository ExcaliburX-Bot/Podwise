import feedparser
import json
import os
import xml.etree.ElementTree as ET
from datetime import datetime, timedelta

# ==========================================
# 备用手动列表 (如果没有上传 OPML 文件，会用这个)
MANUAL_FEEDS = [
    "https://feeds.xyz/example1",
    "https://feeds.xyz/example2",
]
# ==========================================

def parse_opml(opml_path):
    """解析 OPML 文件提取 RSS 链接"""
    urls = []
    try:
        tree = ET.parse(opml_path)
        root = tree.getroot()
        # 递归查找所有 outline 标签
        for outline in root.findall('.//outline'):
            # 标准 OPML 通常把链接放在 xmlUrl 属性里
            url = outline.get('xmlUrl')
            if url:
                urls.append(url)
        print(f"📂 成功从 OPML 加载了 {len(urls)} 个订阅源")
    except Exception as e:
        print(f"⚠️ 读取 OPML 失败: {e}")
    return urls

def get_best_link(entry):
    """强力提取链接逻辑"""
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
    
    # 1. 尝试寻找根目录下的 subscriptions.opml
    opml_path = os.path.join(root_dir, 'subscriptions.opml')
    
    rss_feeds = []
    if os.path.exists(opml_path):
        rss_feeds = parse_opml(opml_path)
    else:
        print("ℹ️ 未找到 subscriptions.opml，使用手动列表")
        rss_feeds = MANUAL_FEEDS

    if not os.path.exists(data_dir):
        os.makedirs(data_dir)

    all_episodes = []
    yesterday = datetime.now() - timedelta(days=1)

    print(f"🚀 开始处理 {len(rss_feeds)} 个订阅源...")

    for feed_url in rss_feeds:
        try:
            # 设置超时，防止卡死
            feed = feedparser.parse(feed_url)
            podcast_title = feed.feed.get('title', '未知播客')
            
            # 简单的日志输出，避免刷屏
            # print(f"Checking: {podcast_title}") 

            for entry in feed.entries:
                try:
                    if hasattr(entry, 'published_parsed') and entry.published_parsed:
                        pub_date_parsed = entry.published_parsed
                        pub_date = datetime(*pub_date_parsed[:6])
                    else:
                        continue
                except:
                    continue

                if pub_date > yesterday:
                    final_link = get_best_link(entry)
                    
                    print(f"   ✅ 新更新: {podcast_title} - {entry.title[:20]}...")

                    all_episodes.append({
                        'title': entry.title,
                        'podcast': {'title': podcast_title},
                        'link': final_link,
                        'pubDate': str(pub_date)
                    })
        except Exception as e:
            print(f"❌ 错误 {feed_url}: {e}")

    output_file = os.path.join(data_dir, 'hot_episodes.json')
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(all_episodes, f, ensure_ascii=False, indent=2)

    print(f"\n🎉 全部完成！共抓取到 {len(all_episodes)} 个新单集。")

if __name__ == "__main__":
    fetch_rss()
