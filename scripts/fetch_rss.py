import feedparser
import json
import os
import re  # 👈 引入正则库
from datetime import datetime, timedelta

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
    standard_path = os.path.join(root_dir, 'subscriptions.opml')
    if os.path.exists(standard_path):
        return standard_path
    files = os.listdir(root_dir)
    for f in files:
        if f.lower().endswith('.opml'):
            return os.path.join(root_dir, f)
    return None

def parse_opml(opml_path):
    urls = []
    try:
        # 📖 使用“暴力模式”读取，忽略 XML 语法错误
        with open(opml_path, 'r', encoding='utf-8', errors='ignore') as f:
            content = f.read()
            
            # 使用正则表达式直接提取 http/https 链接
            # 专门匹配 xmlUrl="..." 或 url="..." 里的内容
            matches = re.findall(r'(?:xmlUrl|url)=["\'](http[^"\']+)["\']', content)
            
            # 去重
            urls = list(set(matches))
            
        log(f"📂 解析 OPML 成功 (正则暴力模式): 找到 {len(urls)} 个订阅源")
    except Exception as e:
        log(f"⚠️ 解析 OPML 失败: {str(e)}")
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
    
    opml_path = find_opml_file(root_dir)
    
    rss_feeds = []
    if opml_path:
        log(f"✅ 找到 OPML 文件: {opml_path}")
        rss_feeds = parse_opml(opml_path)
        if not rss_feeds:
            log("⚠️ OPML 提取结果为空，使用保底列表")
            rss_feeds = MANUAL_FEEDS
    else:
        log("❌ 未找到任何 .opml 文件，使用保底列表")
        rss_feeds = MANUAL_FEEDS

    if not os.path.exists(data_dir):
        os.makedirs(data_dir)

    all_episodes = []
    # 抓取过去 7 天
    time_threshold = datetime.now() - timedelta(days=7)

    log(f"🚀 开始抓取 {len(rss_feeds)} 个源 (过去 7 天)...")

    # 限制最大抓取数量，防止 GitHub Action 超时（如果源太多）
    # 如果你的源超过 100 个，可以适当调大这个数字，或者分批处理
    max_feeds = 200 
    if len(rss_feeds) > max_feeds:
        log(f"⚠️ 源太多 ({len(rss_feeds)} 个)，仅处理前 {max_feeds} 个以防超时")
        rss_feeds = rss_feeds[:max_feeds]

    success_count = 0
    
    for feed_url in rss_feeds:
        try:
            # 设置超时时间 10秒，防止卡死
            # 注意：feedparser 本身不支持 timeout 参数，这里依赖 socket 默认超时或快速失败
            feed = feedparser.parse(feed_url)
            
            if not feed.entries:
                continue
                
            podcast_title = feed.feed.get('title', '未知播客')
            success_count += 1

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
            # 这里的错误就不打印了，保持日志清爽
            pass

    log(f"✅ 成功连接并解析了 {success_count} 个播客源")

    all_episodes.sort(key=lambda x: x['pubDate'], reverse=True)

    output_file = os.path.join(data_dir, 'hot_episodes.json')
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(all_episodes, f, ensure_ascii=False, indent=2)

    debug_file = os.path.join(root_dir, 'debug_log.txt')
    with open(debug_file, 'w', encoding='utf-8') as f:
        f.write('\n'.join(debug_log))
    
    print(f"\n🎉 完成！抓取到 {len(all_episodes)} 集。")

if __name__ == "__main__":
    fetch_rss()
