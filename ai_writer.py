import json
from typing import Dict, List
import config


class AIWriter:
    def __init__(self, api_key: str = None):
        self.api_key = api_key or config.QWEN_MODEL
        self.model = config.QWEN_MODEL
        self.prompt_template = config.PROMPT_TEMPLATE

    def generate_caption(self, image_paths: List[str]) -> Dict[str, str]:
        if not config.QWEN_API_KEY:
            return self._generate_fallback_caption(image_paths)

        try:
            from openai import OpenAI
            client = OpenAI(
                api_key=config.QWEN_API_KEY,
                base_url="https://dashscope.aliyuncs.com/compatible-mode/v1"
            )

            image_descriptions = [self._get_image_description(p) for p in image_paths]
            combined_description = "、".join(image_descriptions)

            response = client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": "你是一位小红书博主，擅长生成吸引人的种草文案。"},
                    {"role": "user", "content": self.prompt_template.format(image_description=combined_description)}
                ],
                max_tokens=500
            )

            content = response.choices[0].message.content
            return self._parse_caption(content)

        except Exception as e:
            print(f"AI 生成失败: {e}")
            return self._generate_fallback_caption(image_paths)

    def _generate_fallback_caption(self, image_paths: List[str]) -> Dict[str, str]:
        import random
        titles = [
            "分享一组美图",
            "今日分享",
            "来看看这些",
            "绝美分享",
            "日常记录"
        ]
        bodies = [
            "今天的分享就到这里啦～喜欢的话记得点个赞👍",
            "分享一组好看的图片，希望你们喜欢",
            "日常记录，每一张都很喜欢",
            "近期最爱，分享给大家",
            "一组超赞的图片，快来看看吧"
        ]
        tags = ["#分享", "#美图", "#记录", "#生活", "#日常"]

        selected_tags = random.sample(tags, 3)

        return {
            "title": random.choice(titles),
            "body": random.choice(bodies),
            "tags": " ".join(selected_tags)
        }

    def _get_image_description(self, image_path: str) -> str:
        import os
        filename = os.path.basename(image_path)
        name_without_ext = os.path.splitext(filename)[0]
        return name_without_ext.replace('_', ' ').replace('-', ' ')

    def _parse_caption(self, content: str) -> Dict[str, str]:
        title = ""
        body = ""
        tags = ""

        lines = content.strip().split('\n')
        for line in lines:
            line = line.strip()
            if line.startswith("标题："):
                title = line.replace("标题：", "").strip()
            elif line.startswith("正文："):
                body = line.replace("正文：", "").strip()
            elif line.startswith("标签："):
                tags = line.replace("标签：", "").strip()

        if not title:
            for line in lines:
                if line and not line.startswith("#"):
                    title = line.strip()
                    break

        if not body:
            body = " ".join([l.strip() for l in lines if l and not l.startswith("#") and not l.startswith("标题") and not l.startswith("正文") and not l.startswith("标签")])

        return {
            "title": title,
            "body": body,
            "tags": tags
        }
