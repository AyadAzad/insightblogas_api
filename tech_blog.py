import json
import time
from playwright.sync_api import Playwright, sync_playwright
from bs4 import BeautifulSoup


def run(playwright: Playwright):
    blog_info = []
    start_url = "https://www.freecodecamp.org/news"
    chrom = playwright.chromium
    browser = chrom.launch(headless=False)
    page = browser.new_page()
    page.goto(start_url)
    # page.wait_for_load_state("networkidle")
    time.sleep(4)
    for x in range(1, 15):
        page.keyboard.press("End")
        print(f"scrolling {x} times")
        time.sleep(2)
        page.click("[id^='readMoreBtn']")
        time.sleep(2)
        blog_soup = BeautifulSoup(page.content(), 'lxml')

        blog_articles = blog_soup.find_all('article', class_='post-card')

        for blog in blog_articles:
            blog_name = blog.find('h2').text.strip()
            blog_link = blog.find('a', class_='post-card-image-link')['href']
            blog_img = blog.find('img')['src']
            try:
                blog_category = blog.find('span', class_='post-card-tags').text.strip()
            except AttributeError:
                pass
            blog_info.append({
                'blog_name': blog_name,
                'blog_category': blog_category,
                'blog_link': 'https://www.freecodecamp.org' + blog_link,
                'blog_img': blog_img
            })
    print(blog_info)
    with open ('tech_blog.json', 'w') as fp:
        json.dump(blog_info, fp, indent=4)
        fp.close()
        print("Done ! , Json file created successfully ......")
        print(f"We've found {len(blog_info)} blogs")

with sync_playwright() as playwright:
    run(playwright)
