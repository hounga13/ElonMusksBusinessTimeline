import json
import requests
from datetime import datetime

# Allow List (크롤링 대상 계정)
ALLOW_LIST = {
    "elon-musk": ["@elonmusk"],
    "tesla": ["@Tesla", "@TeslaAI"],
    "spacex": ["@SpaceX"],
    "xai": ["@xAI"]
}

# 크롤링 함수 (예시: Twitter API 사용 가정)
def crawl_data(category):
    url = f"https://api.twitter.com/2/users/by/username/{ALLOW_LIST[category][0]}/tweets"  # API 엔드포인트 예시
    headers = {"Authorization": "Bearer AAAAAAAAAAAAAAAAAAAAAG3y3QEAAAAAW9KxWWMrKkL2ZQK%2FrGlrf%2FvOW60%3DOwild7NSktVkdu06EOauQHEwMOCRuvkGJrGiEfiqS3RLTB49F6"}  # API 토큰 필요
    response = requests.get(url, headers=headers)
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
            "thumbnail_url": "https://example.com/default-thumb.jpg"  # 실제 URL 필요
        })

    with open(f"data/{category}.json", "w", encoding="utf-8") as f:
        json.dump({"items": items}, f, ensure_ascii=False, indent=2)

# 모든 카테고리 크롤링
if __name__ == "__main__":
    for category in ALLOW_LIST.keys():
        crawl_data(category)
