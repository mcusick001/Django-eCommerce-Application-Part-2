import requests


def fetch_reddit_posts(limit=10):
    url = f"https://www.reddit.com/r/django/new.json?limit={limit}"
    headers = {"User-Agent": "DjangoEcommerceApp/1.0"}

    try:
        response = requests.get(url, headers=headers, timeout=5)
        if response.status_code == 200:
            data = response.json()
            posts = []
            for child in data.get("data", {}).get("children", []):
                post_data = child.get("data", {})
                posts.append({
                    "title": post_data.get("title"),
                    "author": post_data.get("author"),
                    "url": f"https://reddit.com{post_data.get('permalink')}"
                })
            return posts
    except requests.RequestException:
        pass
    return []
