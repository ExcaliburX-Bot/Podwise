import requests
import json
import os
import xml.etree.ElementTree as ET
from datetime import datetime
from email.utils import parsedate_to_datetime

# 默认订阅 (当找不到 OPML 文件时使用)
DEFAULT_RSS = [
    "https://feed.xyzfm.space/a9uD3-3ksD1u",
    "https://pythonhunter.org/episodes/feed.xml"
]

def extract_urls_from_opml(file_path):
    """从 OPML 文件中提取 RSS 链接"""
    urls = []
    try:
        tree = ET.parse(file_path)
        root = tree.getroot()
        # 查找所有含有 xmlUrl 属性的 outline 标签 (支持嵌套文件夹)
        for outline in root.findall('.//outline'):
            url = outline.get('xmlUrl')
            if url:
                urls.append(url)
        print(f"📂 成功从 OPML 加载了 {len(urls)} 个订阅源")
    except Exception as e:
        print(f"⚠️ 读取 OPML 失败: {e}")
    return urls

def parse_rss_episode(rss_url):
    """解析 RSS 并提取最新一集"""
    try:
        headers = {
            'User-Agent': 'Mozilla/5.0 (compatible; PodwiseBot/1.0; +https://github.com/)'
        }
        # 设置 10秒超时，防止某个源卡死整个流程
        response = requests.get(rss_url, headers=headers, timeout=10)
        
        # 如果状态码不是 200，直接跳过
        if response.status_code != 200:
            return None
            
        root = ET.fromstring(response.content)
        channel = root.find('channel')
        
        # 获取播客标题
        podcast_title_tag = channel.find('title')
        podcast_title = podcast_title_tag.text if podcast_title_tag is not None else "未知播客"
        
        # 获取最新的一集 (第一个 item)
        item = channel.find('item')
        if item is None:
            return None
            
        title_tag = item.find('title')
        title = title_tag.text if title_tag is not None else "无标题"
        
        # 尝试获取音频链接
        enclosure = item.find('enclosure')
        if enclosure is None:
            return None # 没有音频文件，跳过
            
        audio_url = enclosure.get('url')
        
        # 尝试获取发布时间
        pub_date_str = item.find('pubDate').text
        try:
            pub_date = parsedate_to_datetime(pub_date_str).isoformat()
        except:
            pub_date = datetime.now().isoformat()

        return {
            "eid": audio_url[-15:], # 简易 ID
            "title": title,
            "podcast": {
                "title": podcast_title
            },
            "enclosureUrl": audio_url,
            "duration": 0,
            "pubDate": pub_date,
            "source_rss": rss_url
        }

    except Exception as e:
        # 某个源解析失败不影响其他源，仅打印错误
        # print(f"   ❌ 解析跳过: {rss_url} ({str(e)[:30]}...)") 
        return None

def fetch_podcasts():
    os.makedirs('data', exist_ok=True)
    opml_path = 'data/subscriptions.opml'
    
    # 1. 确定订阅源列表
    rss_list = []
    if os.path.exists(opml_path):
        print(f"📄 发现订阅文件: {opml_path}")
        rss_list = extract_urls_from_opml(opml_path)
    
    # 如果没找到文件或文件为空，使用默认列表
    if not rss_list:
        print("⚠️ 未找到 OPML 文件，使用默认演示列表")
        rss_list = DEFAULT_RSS

    # 2. 开始抓取
    print(f"🚀 开始检查 {len(rss_list)} 个播客的更新...")
    episodes = []
    
    # 限制最大抓取数量，防止超时 (例如只取前 50 个)
    # 如果你的订阅非常多，可以考虑分批处理
    for i, rss in enumerate(rss_list):
        episode = parse_rss_episode(rss)
        if episode:
            episodes.append(episode)
            print(f"   ✅ [{len(episodes)}] {episode['podcast']['title']}: {episode['title'][:20]}...")
            
    # 按发布时间倒序排序（最新的在前面）
    episodes.sort(key=lambda x: x['pubDate'], reverse=True)
    
    # 只保留最新的 20 条，避免报告太长
    final_data = episodes[:20]

    output_file = 'data/hot_episodes.json'
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(final_data, f, ensure_ascii=False, indent=2)
        
    print(f"\n💾 抓取完成！已保存 {len(final_data)} 条最新单集。")

if __name__ == "__main__":
    fetch_podcasts()
