import os
import json
from pathlib import Path

BASE_DIR = Path(__file__).parent

IMAGE_DIR = os.path.join(os.path.expanduser("~"), "Images")

QWEN_API_KEY = ""

QWEN_MODEL = "qwen-turbo"

SCHEDULE_HOUR = 8
SCHEDULE_MINUTE = 0

IMAGE_COUNT_MIN = 5
IMAGE_COUNT_MAX = 6

CHROME_DRIVER_PATH = ""

HEADLESS = False

COOKIES_FILE = BASE_DIR / "cookies.json"

LOG_FILE = BASE_DIR / "xhs.log"

PROMPT_TEMPLATE = """你是一位小红书博主，请为以下图片生成一篇吸引人的笔记配文。

要求：
1. 标题简短有力，20字以内
2. 正文生动有趣，100-200字
3. 添加3-5个热门标签
4. 风格：亲切、自然、适合分享生活

请按以下格式输出：
标题：xxx
正文：xxx
标签：#xxx #xxx #xxx

图片描述：{image_description}
"""
