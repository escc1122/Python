import os
import logging
from dotenv import load_dotenv
from playwright.sync_api import Playwright, sync_playwright
import time

# 載入 .env 檔案中的環境變數
load_dotenv()

LOGIN_EMAIL = os.getenv("LOGIN_EMAIL")
LOGIN_PASSWORD = os.getenv("LOGIN_PASSWORD")
log_path = os.getenv("LOG_PATH", "logs/site_update.log")

logging.basicConfig(
    filename=log_path,
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s"
)

# 讀取網址清單
with open("site_urls.txt", "r", encoding="utf-8") as f:
    urls = f.read().strip()

url_dict = {
}

def login(page):
    try:
        page.goto(url_dict["login"])
        page.get_by_placeholder("您的邮箱").fill(LOGIN_EMAIL)
        page.get_by_placeholder("您的密码").fill(LOGIN_PASSWORD)
        page.get_by_role("button", name="登 录").click()
        page.wait_for_url(url_dict["after_login"])
        logging.info("登入成功")
    except Exception as e:
        logging.error(f"登入失敗: {e}")
        raise

def site_flow(context, task_id, site_name, site_url):
    try:
        logging.info(f"{site_name} 開始")
        site_url = site_url.strip()
        if not site_url:
            logging.warning(f"{site_name} url不能為空")
            return

        view_url = f"{url_dict['view_url']}{task_id}"
        edit_url = f"{url_dict['edit_url']}{task_id}"

        logging.info(f"{site_name} 修改開始")

        page = context.new_page()
        page.goto(edit_url, wait_until="networkidle")
        page.get_by_placeholder("http://").fill(site_url)
        page.get_by_role("button", name="保存").first.click()

        page.wait_for_url(url_dict["after_save"])
        page.wait_for_selector(".ant-table-tbody")

        page.goto(view_url, wait_until="networkidle")
        page.wait_for_selector(f"text='{site_url}'", timeout=5000)

        if page.get_by_text(site_url).is_visible():
            logging.info(f"{site_name}：{site_url} 修改成功")
        else:
            logging.error(f"{site_name}：{site_url} 修改失敗")

    except Exception as e:
        logging.error(f"{site_name} 失敗: {e}")

def run(playwright: Playwright) -> None:
    site_task_id = {
    }

    site_urls = {name: "" for name in site_task_id}

    for line in urls.strip().split("\n"):
        name, url = line.split("：")
        site_urls[name.strip()] = url.strip()

    with playwright.chromium.launch(headless=True) as browser:
        with browser.new_context() as context:
            page = context.new_page()
            login(page)
            for site_name, task_id in site_task_id.items():
                site_flow(context, task_id, site_name, site_urls[site_name])
            time.sleep(5)

if __name__ == '__main__':
    with sync_playwright() as playwright:
        run(playwright)
