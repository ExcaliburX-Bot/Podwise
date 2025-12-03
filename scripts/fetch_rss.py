import feedparser
import json
import os
from datetime import datetime, timedelta

# ---在此处修改你的订阅源---
RSS_FEEDS = [
    "https://feeds.xyz/123", # 请替换成你真实的 RSS 地址
    "https://feeds.xyz/456",
]
# -----------------------

def fetch_rss():
    # 获取当前脚本所在目录 (scripts/)
    current_dir = os.path.dirname(os.path.abspath(__file__))
    # 获取项目根目录 (scripts 的上一级)
    root_dir = os.path.dirname(current_dir)
    # 数据存储目录
    data_dir = os.path.join(root_dir, 'data')
    
    # 如果 data 目录不存在，创建它
    if not os.path.exists(data_dir):
        os.makedirs(data_dir)

    all_episodes = []
    # 筛选最近 24 小时
    yesterday = datetime.now() - timedelta(days=1)

    print(f"开始抓取 {len(RSS_FEEDS)} 个订阅源...")

    for feed_url in RSS_FEEDS:
        try:
            print(f"正在连接: {feed_url} ...")
            feed = feedparser.parse(feed_url)
            podcast_title = feed.feed.get('title', 'Unknown Podcast')
            print(f"✅ 成功获取: {podcast_title}")

            for entry in feed.entries:
                try:
                    # 解析发布时间
                    if hasattr(entry, 'published_parsed'):
                        pub_date_parsed = entry.published_parsed
                        pub_date = datetime(*pub_date_parsed[:6])
                    else:
                        continue
                except:
                    continue

                # 如果是最近 24 小时更新的
                if pub_date > yesterday:
                    # 1. 优先获取网页链接 (link)
                    web_link = entry.get('link', '')
                    
                    # 2. 如果没有网页链接，尝试找 enclosure (音频链接)
                    if not web_link and hasattr(entry, 'enclosures') and len(entry.enclosures) > 0:
                        web_link = entry.enclosures[0].href

                    # 3. 存入列表
                    all_episodes.append({
                        'title': entry.title,
                        'podcast': {'title': podcast_title},
                        'link': web_link, # 这里存的是网页链接
                        'pubDate': str(pub_date)
                    })
        except Exception as e:
            print(f"❌ 抓取失败 {feed_url}: {e}")

    # 保存结果到 data/hot_episodes.json
    output_file = os.path.join(data_dir, 'hot_episodes.json')
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(all_episodes, f, ensure_ascii=False, indent=2)

    print(f"🎉 抓取完成！共找到 {len(all_episodes)} 个新单集。")

if __name__ == "__main__":
    fetch_rss()
