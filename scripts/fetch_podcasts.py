import requests
import json
import os
import re
import xml.etree.ElementTree as ET
from datetime import datetime
from email.utils import parsedate_to_datetime

# 默认演示列表 (仅当 OPML 彻底失败时使用)
DEFAULT_RSS = [
    "https://pythonhunter.org/episodes/feed.xml"
]

def parse_rss_episode(rss_url):
    """解析 RSS 并提取最新一集"""
    try:
        headers = {'User-Agent': 'Mozilla/5.0 (PodwiseBot)'}
        # 设置 8秒超时
        response = requests.get(rss_url, headers=headers, timeout=8)
        
        if response.status_code != 200:
            return None
            
        # 尝试处理 encoding 问题
        response.encoding = response.apparent_encoding

        root = ET.fromstring(response.content)
        channel = root.find('channel')
        if channel is None: channel = root 

        title_tag = channel.find('title')
        podcast_title = title_tag.text if title_tag is not None else "未知播客"
        
        item = channel.find('item')
        if item is None: return None
            
        ep_title = item.find('title').text or "无标题"
        enclosure = item.find('enclosure')
        
        if enclosure is None: return None
            
        audio_url = enclosure.get('url')
        pub_date_str = item.find('pubDate').text
        
        try:
            pub_date = parsedate_to_datetime(pub_date_str).isoformat()
        except:
            pub_date = datetime.now().isoformat()

        return {
            "eid": audio_url[-15:],
            "title": ep_title,
            "podcast": {"title": podcast_title},
            "enclosureUrl": audio_url,
            "pubDate": pub_date,
            "source_rss": rss_url
        }
    except Exception:
        return None

def extract_urls_from_opml(file_path):
    urls = []
    print(f"📂 正在读取文件: {file_path}")
    
    # --- 方法 A: 标准 XML 解析 (严格) ---
    try:
        tree = ET.parse(file_path)
        root = tree.getroot()
        # 递归查找所有 xmlUrl 或 url 属性
        for elem in root.iter():
            url = elem.get('xmlUrl') or elem.get('url')
            if url: urls.append(url)
        print(f"🎉 标准模式解析成功！找到 {len(urls)} 个源")
        
    except Exception as e:
        print(f"⚠️ 标准解析失败 ({e})，切换到暴力提取模式...")
        
        # --- 方法 B: 正则表达式暴力提取 (容错率极高) ---
        try:
            with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                content = f.read()
                # 查找所有 xmlUrl="..." 或 url="..." 的模式
                # 这里的正则会忽略 XML 结构，直接找链接
                found = re.findall(r'(?:xmlUrl|url)=["\']([^"\']+)["\']', content)
                urls.extend(found)
            print(f"💪 暴力模式成功！强行提取到 {len(urls)} 个源")
        except Exception as e2:
            print(f"❌ 暴力模式也失败了: {e2}")

    # 去重并过滤非 http 开头的垃圾数据
    clean_urls = list(set([u for u in urls if u.startswith('http')]))
    return clean_urls

def fetch_podcasts():
    os.makedirs('data', exist_ok=True)
    opml_path = 'data/subscriptions.opml'
    
    rss_list = []
    if os.path.exists(opml_path):
        rss_list = extract_urls_from_opml(opml_path)
    
    if not rss_list:
        print("⚠️ 未找到有效订阅，使用默认列表")
        rss_list = DEFAULT_RSS

    print(f"\n🚀 开始处理 {len(rss_list)} 个播客 (只取最新前 30 条)...")
    
    episodes = []
    # 为了防止超时，如果订阅太多，这里限制只处理前 50 个订阅源
    # 如果你想处理更多，可以把 [:50] 去掉
    target_list = rss_list[:50] 
    
    for i, rss in enumerate(target_list):
        print(f"[{i+1}/{len(target_list)}] 检查中...", end="\r")
        episode = parse_rss_episode(rss)
        if episode:
            episodes.append(episode)
            
    # 按时间倒序
    episodes.sort(key=lambda x: x['pubDate'], reverse=True)
    final_data = episodes[:30]

    with open('data/hot_episodes.json', 'w', encoding='utf-8') as f:
        json.dump(final_data, f, ensure_ascii=False, indent=2)
        
    print(f"\n\n💾 完成！已保存 {len(final_data)} 条最新单集。")

if __name__ == "__main__":
    fetch_podcasts()

