import json
import requests
import os
from datetime import datetime

# Allow List (크롤링 대상 계정)
ALLOW_LIST = {
    "elon-musk": ["@elonmusk"],
    "tesla": ["@Tesla", "@TeslaAI"],
    "spacex": ["@SpaceX"],
    "xai": ["@xAI"]
}

# Twitter API 토큰 가져오기 (GitHub Secrets에서)
TWITTER_API_TOKEN = os.environ.get("TWITTER_API_TOKEN")
if not TWITTER_API_TOKEN:
    raise ValueError("TWITTER_API_TOKEN environment variable is not set.")

# 크롤링 함수 (Twitter API 사용 가정)
def crawl_data(category):
    url = f"https://api.twitter.com/2/users/by/username/{ALLOW_LIST[category][0]}/tweets"
    headers = {
        "Authorization": f"Bearer {TWITTER_API_TOKEN}"
    }
    response = requests.get(url, headers=headers)
    
    # API 응답 처리
    if response.status_code != 200:
        raise Exception(f"Failed to fetch data for {category}: {response.text}")
    
    data = response.json()

    items = []
    for tweet in data.get("data", []):
        items.append({
            "title": tweet.get("text", "").split("\n")[0][:50],  # 첫 줄을 제목으로
            "summary": tweet.get("text", "")[:200],  # 텍스트 요약
            "link": f"https://twitter.com/{ALLOW_LIST[category][0]}/status/{tweet['id']}",
            "timestamp": tweet.get("created_at", datetime.utcnow().isoformat() + "Z"),
            "likes": tweet.get("public_metrics", {}).get("like_count", 0),
            "views": tweet.get("public_metrics", {}).get("impression_count", 0),
            "thumbnail_url": tweet.get("attachments", {}).get("media_keys", ["https://example.com/default-thumb.jpg"])[0]  # 예시, 실제 썸네일 URL 필요
        })

    with open(f"data/{category}.json", "w", encoding="utf-8") as f:
        json.dump({"items": items}, f, ensure_ascii=False, indent=2)

# 모든 카테고리 크롤링
if __name__ == "__main__":
    for category in ALLOW_LIST.keys():
        try:
            crawl_data(category)
            print(f"Successfully updated {category}.json")
        except Exception as e:
            print(f"Error updating {category}.json: {e}")
