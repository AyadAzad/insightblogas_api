import json
import time
from playwright.sync_api import Playwright, sync_playwright
from bs4 import BeautifulSoup


def run(playwright: Playwright):
    blog_info = []
    start_url = "https://www.businessblogshub.com/category/accounting-finance/"
    chrom = playwright.chromium
    browser = chrom.launch(headless=False)
    page = browser.new_page()
    page.goto(start_url)
    # page.wait_for_load_state("networkidle")
    time.sleep(4)
    for x in range(1, 5):
        page.keyboard.press("End")
        print(f"scrolling {x} times")
        time.sleep(2)
        page.click("[class=\"mvp-inf-more-but\"]")
        time.sleep(3)
        blog_soup = BeautifulSoup(page.content(), 'lxml')

        blog_articles = blog_soup.find_all('li', class_='mvp-blog-story-wrap left relative infinite-post')

        for blog in blog_articles:
            blog_name = blog.find('h2').text.strip()
            blog_link = blog.find('a', rel='bookmark')['href']
            blog_img = blog.find('img')['src']
            try:
                blog_category = blog.find('span', class_='mvp-cd-cat left relative').text.strip()
            except AttributeError:
                pass
            blog_info.append({
                'blog_name': blog_name,
                'blog_category': blog_category,
                'blog_link': blog_link,
                'blog_img': blog_img
            })
    print(blog_info)
    with open ('Finance_blog.json', 'w') as fp:
        json.dump(blog_info, fp, indent=4)
        fp.close()
        print("Done ! , Json file created successfully ......")
        print(f"We've found {len(blog_info)} blogs")

with sync_playwright() as playwright:
    run(playwright)
