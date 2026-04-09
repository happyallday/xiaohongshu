import os
import random
from pathlib import Path
from typing import List
import config


class ImagePicker:
    def __init__(self, image_dir: str = None):
        self.image_dir = image_dir or config.IMAGE_DIR

    def get_random_images(self, min_count: int = None, max_count: int = None) -> List[str]:
        min_count = min_count or config.IMAGE_COUNT_MIN
        max_count = max_count or config.IMAGE_COUNT_MAX

        if not os.path.exists(self.image_dir):
            raise FileNotFoundError(f"图片目录不存在: {self.image_dir}")

        supported_extensions = ('.jpg', '.jpeg', '.png', '.webp')
        image_files = [
            os.path.join(self.image_dir, f)
            for f in os.listdir(self.image_dir)
            if f.lower().endswith(supported_extensions)
        ]

        if not image_files:
            raise ValueError(f"目录中没有图片文件: {self.image_dir}")

        count = random.randint(min_count, min(max_count, len(image_files)))
        selected = random.sample(image_files, count)

        print(f"已选择 {len(selected)} 张图片:")
        for img in selected:
            print(f"  - {os.path.basename(img)}")

        return selected

    def get_image_description(self, image_path: str) -> str:
        filename = os.path.basename(image_path)
        name_without_ext = os.path.splitext(filename)[0]
        return name_without_ext.replace('_', ' ').replace('-', ' ')
