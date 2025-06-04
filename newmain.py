import csv
import re
from instagrapi import Client

USERNAME = "usrname"
PASSWORD = "password"

def extract_shortcode(url):
    match = re.search(r"instagram\.com/p/([^/]+)/?", url)
    return match.group(1) if match else None

def fetch_text_data(cl, shortcode):
    try:
        media_id = cl.media_pk_from_code(shortcode)
        media = cl.media_info(media_id)
        caption = media.caption_text or ""
        comments = cl.media_comments(media_id, amount=20)
        comment_texts = [c.text for c in comments]
        return {
            "shortcode": shortcode,
            "caption": caption,
            "comments": " | ".join(comment_texts)
        }
    except Exception as e:
        print(f"Error when parse {shortcode}: {e}")
        return None

def main():
    cl = Client()
    cl.login(USERNAME, PASSWORD)
    print("Auth sucessful")

    with open("links.txt", "r") as file:
        urls = [line.strip() for line in file if line.strip()]

    all_texts = []
    for url in urls:
        shortcode = extract_shortcode(url)
        if not shortcode:
            print(f"Wrong url: {url}")
            continue
        print(f"Post parse in process: {shortcode}")
        post_data = fetch_text_data(cl, shortcode)
        if post_data:
            all_texts.append(post_data)

    if not all_texts:
        print("nothing")
        return

    with open("output.csv", "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=["shortcode", "caption", "comments"])
        writer.writeheader()
        for row in all_texts:
            writer.writerow(row)

    print("Done >> output.csv")

if __name__ == "__main__":
    main()
