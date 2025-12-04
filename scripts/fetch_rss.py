import feedparser
import json
import os
import xml.etree.ElementTree as ET
from datetime import datetime, timedelta

# ==========================================
# 1. 这里加了一个真实的 RSS (机核网)，保证测试时一定有数据！
MANUAL_FEEDS = [
    "https://feed.xyz/example1", 
    "https://www.gcores.com/rss",  # <--- 这是一个真实的测试源
]
# ==========================================

def parse_opml(opml_path):
    urls = []
    try:
        tree = ET.parse(opml_path)
        root = tree.getroot()
        for outline in root.findall('.//outline'):
            url = outline.get('xmlUrl')
            if url:
                urls.append(url)
        print(f"📂 成功从 OPML 加载了 {len(urls)} 个订阅源")
    except Exception as e:
        print(f"⚠️ 读取 OPML 失败: {e}")
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
    
    opml_path = os.path.join(root_dir, 'subscriptions.opml')
    
    rss_feeds = []
    if os.path.exists(opml_path):
        rss_feeds = parse_opml(opml_path)
    else:
        print("ℹ️ 未找到 subscriptions.opml，使用手动列表 (含测试源)")
        rss_feeds = MANUAL_FEEDS

    if not os.path.exists(data_dir):
        os.makedirs(data_dir)

    all_episodes = []
    
    # ==========================================
    # 2. 修改这里：把 days=1 改成 days=7 (抓取过去一周的)
    time_threshold = datetime.now() - timedelta(days=7)
    # ==========================================

    print(f"🚀 开始处理 {len(rss_feeds)} 个订阅源 (查找 {time_threshold.strftime('%Y-%m-%d')} 之后的更新)...")

    for feed_url in rss_feeds:
        try:
            feed = feedparser.parse(feed_url)
            podcast_title = feed.feed.get('title', '未知播客')
            
            for entry in feed.entries:
                try:
                    if hasattr(entry, 'published_parsed') and entry.published_parsed:
                        pub_date_parsed = entry.published_parsed
                        pub_date = datetime(*pub_date_parsed[:6])
                    else:
                        continue
                except:
                    continue

                # 使用新的 7 天时间阈值
                if pub_date > time_threshold:
                    final_link = get_best_link(entry)
                    print(f"   ✅ 抓取到: {podcast_title} - {entry.title[:15]}...")

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
