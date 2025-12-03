import requests
import json
import os
from datetime import datetime

def get_mock_data():
    """当 API 挂掉时，生成测试数据，保证流程不报错"""
    return [
        {
            "eid": "655c8096d09983d4a6e88888", # 示例 ID
            "title": "【测试数据】API暂时无法访问，这是自动生成的演示条目",
            "podcast": {
                "title": "测试播客"
            },
            "enclosureUrl": "https://media.xyzcdn.net/example.mp3",
            "duration": 3600,
            "pubDate": datetime.now().isoformat()
        },
        {
            "eid": "655c8096d09983d4a6e99999",
            "title": "请检查 fetch_podcasts.py 中的 API 地址是否最新",
            "podcast": {
                "title": "系统通知"
            },
            "enclosureUrl": "https://media.xyzcdn.net/example2.mp3",
            "duration": 1800,
            "pubDate": datetime.now().isoformat()
        }
    ]

def fetch_hot_podcasts():
    # 尝试使用 API
    url = "https://xyzrank.eddiehe.top/api/episodes/hot"
    
    # 伪装成浏览器，防止被拦截
    headers = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
    }
    
    data = []
    output_file = 'data/hot_episodes.json'
    os.makedirs('data', exist_ok=True)

    print(f"正在抓取数据: {url}...")
    
    try:
        response = requests.get(url, headers=headers, timeout=15)
        
        if response.status_code == 200:
            data = response.json()
            print(f"✅ 成功抓取 {len(data)} 条热门单集数据")
        else:
            print(f"⚠️ API 返回错误代码: {response.status_code}")
            raise Exception("API Error")
            
    except Exception as e:
        print(f"❌ 抓取失败: {e}")
        print("🔄 启动降级模式：使用测试数据，确保后续流程正常运行...")
        data = get_mock_data()

    # 保存数据（无论是真数据还是测试数据）
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
        
    print(f"💾 数据已保存至: {output_file}")

if __name__ == "__main__":
    fetch_hot_podcasts()
