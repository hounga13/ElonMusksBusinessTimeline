import json
import requests
import os
from datetime import datetime

# 디버깅: 스크립트 시작 시 환경 변수 확인
print("Initial TWITTER_API_TOKEN:", os.environ.get("TWITTER_API_TOKEN"))

# Allow List (크롤링 대상 계정)
ALLOW_LIST = {
    "elon-musk": ["@elonmusk"],
    "tesla": ["@Tesla", "@TeslaAI"],
    "spacex": ["@SpaceX"],
    "xai": ["@xAI"]
}

# Twitter API 토큰 가져오기 (GitHub Secrets에서)
TWITTER_API_TOKEN = os.environ.get("TWITTER_API_TOKEN")
print("TWITTER_API_TOKEN after get:", TWITTER_API_TOKEN)  # 디버깅 추가
if not TWITTER_API_TOKEN:
    raise ValueError("TWITTER_API_TOKEN environment variable is not set.")

# 크롤링 함수 (Twitter API 사용 가정)
def crawl_data(category):
    print(f"Starting crawl for {category} with token: ***")  # 토큰 마스킹
    url = f"https://api.twitter.com/2/users/by/username/{ALLOW_LIST[category][0]}/tweets"
    headers = {
        "Authorization": f"Bearer {TWITTER_API_TOKEN}"
    }
    print(f"Request URL: {url}")  # 요청 URL 로그
    response = requests.get(url, headers=headers)
    
    if response.status_code != 200:
        raise Exception(f"Failed to fetch data for {category}: {response.text}")
    
    data = response.json()
    print(f"Response data for {category}: {data}")  # 응답 데이터 로그

    items = []
    for tweet in data.get("data", []):
        items.append({
            "title": tweet.get("text", "").split("\n")[0][:50],
            "summary": tweet.get("text", "")[:200],
            "link": f"https://twitter.com/{ALLOW_LIST[category][0]}/status/{tweet['id']}",
            "timestamp": tweet.get("created_at", datetime.utcnow().isoformat() + "Z"),
            "likes": tweet.get("public_metrics", {}).get("like_count", 0),
            "views": tweet.get("public_metrics", {}).get("impression_count", 0),
            "thumbnail_url": tweet.get("attachments", {}).get("media_keys", ["https://example.com/default-thumb.jpg"])[0]
        })

    with open(f"data/{category}.json", "w", encoding="utf-8") as f:
        json.dump({"items": items}, f, ensure_ascii=False, indent=2)
    print(f"Successfully updated {category}.json")

# 모든 카테고리 크롤링
if __name__ == "__main__":
    for category in ALLOW_LIST.keys():
        try:
            crawl_data(category)
        except Exception as e:
            print(f"Error updating {category}.json: {e}")
