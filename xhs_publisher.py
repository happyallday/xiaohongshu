import os
import time
import json
from typing import List, Dict
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import config


class XHSPublisher:
    def __init__(self):
        self.driver = None
        self.cookies_file = config.COOKIES_FILE

    def init_driver(self):
        options = Options()
        if config.HEADLESS:
            options.add_argument("--headless")
        options.add_argument("--no-sandbox")
        options.add_argument("--disable-dev-shm-usage")
        options.add_argument("--disable-blink-features=AutomationControlled")
        options.add_experimental_option("excludeSwitches", ["enable-automation"])

        driver_path = config.CHROME_DRIVER_PATH
        if driver_path and os.path.exists(driver_path):
            from selenium.webdriver.chrome.service import Service
            self.driver = webdriver.Chrome(service=Service(driver_path), options=options)
        else:
            self.driver = webdriver.Chrome(options=options)

        self.driver.implicitly_wait(10)
        print("浏览器已启动")

    def login(self):
        self.driver.get("https://creator.xiaohongshu.com")
        time.sleep(3)

        if self._load_cookies():
            print("已加载 Cookie，刷新页面...")
            self.driver.refresh()
            time.sleep(3)
            if self._is_logged_in():
                print("登录成功！")
                return True

        print("请扫码登录...")
        input("请在浏览器中扫码登录完成后，按回车继续...")

        self._save_cookies()
        print("Cookie 已保存")
        return True

    def _load_cookies(self) -> bool:
        if not os.path.exists(self.cookies_file):
            return False

        try:
            with open(self.cookies_file, 'r') as f:
                cookies = json.load(f)
            self.driver.get("https://www.xiaohongshu.com")
            time.sleep(2)
            for cookie in cookies:
                self.driver.add_cookie(cookie)
            return True
        except Exception as e:
            print(f"加载 Cookie 失败: {e}")
            return False

    def _save_cookies(self):
        cookies = self.driver.get_cookies()
        with open(self.cookies_file, 'w') as f:
            json.dump(cookies, f)

    def _is_logged_in(self) -> bool:
        try:
            self.driver.find_element(By.CSS_SELECTOR, '[class*="user"]')
            return True
        except:
            return False

    def publish(self, image_paths: List[str], caption: Dict[str, str]) -> bool:
        try:
            print("正在打开发布页面...")
            self.driver.get("https://creator.xiaohongshu.com/publish/publish")
            time.sleep(3)

            self._upload_images(image_paths)
            time.sleep(2)

            self._fill_content(caption)
            time.sleep(2)

            self._click_publish()
            time.sleep(5)

            print("发布成功！")
            return True

        except Exception as e:
            print(f"发布失败: {e}")
            return False

    def _upload_images(self, image_paths: List[str]):
        print(f"正在上传 {len(image_paths)} 张图片...")
        try:
            upload_input = self.driver.find_element(By.CSS_SELECTOR, 'input[type="file"]')
        except:
            upload_input = WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, 'input[type="file"]'))
            )

        for path in image_paths:
            upload_input.send_keys(path)
            time.sleep(1)

        print("图片上传完成")
        time.sleep(3)

    def _fill_content(self, caption: Dict[str, str]):
        print("正在填写内容...")

        try:
            title_input = self.driver.find_element(By.CSS_SELECTOR, 'input[placeholder*="标题"]')
            title_input.send_keys(caption.get("title", ""))
            time.sleep(0.5)
        except:
            print("未找到标题输入框")

        try:
            content_div = self.driver.find_element(By.CSS_SELECTOR, '[contenteditable="true"]')
            content_div.click()
            time.sleep(0.5)

            body = caption.get("body", "")
            tags = caption.get("tags", "")

            full_content = body
            if tags:
                full_content += "\n\n" + tags

            for char in full_content:
                content_div.send_keys(char)
                time.sleep(0.02)

            print("内容填写完成")
        except Exception as e:
            print(f"填写内容失败: {e}")

    def _click_publish(self):
        print("正在点击发布...")
        try:
            publish_btn = WebDriverWait(self.driver, 10).until(
                EC.element_to_be_clickable((By.CSS_SELECTOR, '[class*="publish"]'))
            )
            publish_btn.click()
        except:
            try:
                publish_btn = self.driver.find_element(By.XPATH, "//button[contains(text(), '发布')]")
                publish_btn.click()
            except:
                print("未找到发布按钮，请手动点击")

    def close(self):
        if self.driver:
            self.driver.quit()
            print("浏览器已关闭")
