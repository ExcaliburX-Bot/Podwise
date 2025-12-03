import requests
import json
import os
from datetime import datetime

def fetch_hot_podcasts():
    # 小宇宙热榜 API
    url = "https://xyzrank.eddiehe.top/api/episodes/hot"
    print(f"正在抓取数据: {url}...")
    
    try:
        response = requests.get(url, timeout=30)
        response.raise_for_status()
        data = response.json()
        
        # 确保 data 目录存在
        os.makedirs('data', exist_ok=True)
        
        # 保存原始数据
        output_file = 'data/hot_episodes.json'
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
            
        print(f"✅ 成功抓取 {len(data)} 条热门单集数据")
        print(f"💾 数据已保存至: {output_file}")
        
    except Exception as e:
        print(f"❌ 抓取失败: {e}")
        # 抛出异常以终止流程
        raise e

if __name__ == "__main__":
    fetch_hot_podcasts()
