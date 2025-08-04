import requests
import json
import os

# بهتر است توکن را از متغیر محیطی بخوانید
GITHUB_TOKEN = os.getenv("GITHUB_TOKEN", "")
REPO_OWNER = "HanzoDev1375"
REPO_NAME = "svg-icon"
API_URL = (
    f"https://api.github.com/repos/{REPO_OWNER}/{REPO_NAME}/git/trees/main?recursive=1"
)

HEADERS = {
    "Authorization": f"token {GITHUB_TOKEN}" if GITHUB_TOKEN else "",
    "Accept": "application/vnd.github+json",
}


def fetch_svg_links():
    try:
        response = requests.get(API_URL, headers=HEADERS)
        response.raise_for_status()  # خطاهای HTTP را بررسی می‌کند

        tree = response.json().get("tree", [])
        svg_links = []

        for item in tree:
            path = item.get("path", "")
            if path.endswith(".svg"):
                # ساخت آدرس raw به صورت صحیح
                raw_url = f"https://raw.githubusercontent.com/{REPO_OWNER}/{REPO_NAME}/main/{path}"
                svg_links.append({"icon": raw_url, "name": os.path.basename(path)})

        return svg_links

    except requests.exceptions.RequestException as e:
        print(f"Error fetching repo tree: {e}")
        return []


def save_json(data, filename):
    try:
        with open(filename, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
        print(f"Saved {len(data)} items to {filename}")
        return True
    except Exception as e:
        print(f"Error saving JSON file: {e}")
        return False


if __name__ == "__main__":
    output_file = "/sdcard/hsi.json"  # مسیر ساده‌تر برای تست
    links = fetch_svg_links()

    if links:
        if save_json(links, output_file):
            print("Operation completed successfully!")
        else:
            print("Failed to save JSON file.")
    else:
        print("No SVG files found or error occurred.")