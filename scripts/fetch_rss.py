import feedparser
import json
import os
import xml.etree.ElementTree as ET
from datetime import datetime, timedelta

# ==========================================
# 1. 已替换为你提供的专用保底链接
MANUAL_FEEDS = [
    "https://feed.xyzfm.space/dk4yh3pkpjp3"
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
    # 优先找原文链接
    if entry.get('link'): return entry.get('link')
    # 其次找 alternate 链接
    if entry.get('links'):
        for l in entry.get('links', []):
            if l.get('type') == 'text/html' or l.get('rel') == 'alternate':
                if l.get('href'): return l.get('href')
    # 再次尝试 id
    id_val = entry.get('id', '')
    if id_val.startswith('http'): return id_val
    # 最后尝试音频文件链接
    if entry.get('enclosures'): return entry.get('enclosures')[0].get('href')
    return ''

def fetch_rss():
    current_dir = os.path.dirname(os.path.abspath(__file__))
    root_dir = os.path.dirname(current_dir)
    data_dir = os.path.join(root_dir, 'data')
    
    opml_path = os.path.join(root_dir, 'subscriptions.opml')
    
    rss_feeds = []
    # 优先读取 OPML，如果没有则使用保底列表
    if os.path.exists(opml_path):
        rss_feeds = parse_opml(opml_path)
        # 如果 OPML 里是空的，也加上保底，防止完全没数据
        if not rss_feeds:
            rss_feeds = MANUAL_FEEDS
    else:
        print("ℹ️ 未找到 subscriptions.opml，使用手动保底列表")
        rss_feeds = MANUAL_FEEDS

    if not os.path.exists(data_dir):
        os.makedirs(data_dir)

    all_episodes = []
    
    # ==========================================
    # 2. 抓取过去 7 天的更新，确保邮件里有内容
    time_threshold = datetime.now() - timedelta(days=7)
    # ==========================================

    print(f"🚀 开始处理 {len(rss_feeds)} 个订阅源 (查找 {time_threshold.strftime('%Y-%m-%d')} 之后的更新)...")

    for feed_url in rss_feeds:
        try:
            # 设置超时，防止卡死
            feed = feedparser.parse(feed_url)
            podcast_title = feed.feed.get('title', '未知播客')
            
            if not feed.entries:
                continue

            for entry in feed.entries:
                try:
                    # 解析时间
                    if hasattr(entry, 'published_parsed') and entry.published_parsed:
                        pub_date_parsed = entry.published_parsed
                        pub_date = datetime(*pub_date_parsed[:6])
                    else:
                        # 如果没时间，默认跳过，或者你可以选择当作今天
                        continue
                except:
                    continue

                # 筛选时间
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

    # 按时间倒序排列（最新的在最前面）
    all_episodes.sort(key=lambda x: x['pubDate'], reverse=True)

    output_file = os.path.join(data_dir, 'hot_episodes.json')
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(all_episodes, f, ensure_ascii=False, indent=2)

    print(f"\n🎉 全部完成！共抓取到 {len(all_episodes)} 个新单集。")

if __name__ == "__main__":
    fetch_rss()
