import requests
import json
import os
from datetime import datetime

# 注意：xyzrank 的数据统一以 xyz_ 前缀保存，
# 避免覆盖 fetch_rss.py 生成的 data/hot_episodes.json（RSS 格式，其他脚本依赖它）
def main():
    sources = {
        'xyz_full': 'https://xyzrank.eddiehe.top/full.json',
        'xyz_new_podcasts': 'https://xyzrank.eddiehe.top/new_podcasts.json',
        'xyz_hot_episodes': 'https://xyzrank.eddiehe.top/hot_episodes.json',
        'xyz_hot_episodes_new': 'https://xyzrank.eddiehe.top/hot_episodes_new.json'
    }

    os.makedirs('data', exist_ok=True)

    for name, url in sources.items():
        try:
            print(f"\n正在抓取: {name}...")
            response = requests.get(url, timeout=30)
            response.raise_for_status()
            data = response.json()

            filename = f'data/{name}.json'
            with open(filename, 'w', encoding='utf-8') as f:
                json.dump(data, f, ensure_ascii=False, indent=2)

            if isinstance(data, dict) and isinstance(data.get('data'), dict):
                if 'episodes' in data['data']:
                    count = len(data['data']['episodes'])
                    print(f"✓ {name}: 成功抓取 {count} 个播客单集")
                elif 'podcasts' in data['data']:
                    count = len(data['data']['podcasts'])
                    print(f"✓ {name}: 成功抓取 {count} 个播客")
                else:
                    print(f"✓ {name}: 抓取成功")
            else:
                print(f"✓ {name}: 抓取成功")

        except Exception as e:
            print(f"✗ {name}: 抓取失败 - {str(e)}")

    print(f"\n抓取完成时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")

if __name__ == '__main__':
    main()
