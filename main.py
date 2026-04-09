import sys
import argparse
import logging
from datetime import datetime
import config
from image_picker import ImagePicker
from ai_writer import AIWriter
from xhs_publisher import XHSPublisher
from scheduler import Scheduler

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler(config.LOG_FILE, encoding='utf-8'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)


def daily_task():
    logger.info("=" * 50)
    logger.info(f"开始执行发布任务 - {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    
    try:
        image_picker = ImagePicker()
        image_paths = image_picker.get_random_images()
        
        ai_writer = AIWriter()
        caption = ai_writer.generate_caption(image_paths)
        
        logger.info(f"生成的标题: {caption.get('title')}")
        logger.info(f"生成的正文: {caption.get('body')}")
        logger.info(f"生成的标签: {caption.get('tags')}")
        
        publisher = XHSPublisher()
        publisher.init_driver()
        
        if publisher.login():
            success = publisher.publish(image_paths, caption)
            if success:
                logger.info("发布成功!")
            else:
                logger.error("发布失败!")
        else:
            logger.error("登录失败!")
        
        publisher.close()
        
    except Exception as e:
        logger.error(f"任务执行失败: {e}")
        import traceback
        traceback.print_exc()


def login_task():
    logger.info("开始登录流程...")
    publisher = XHSPublisher()
    publisher.init_driver()
    publisher.login()
    publisher.close()


def main():
    parser = argparse.ArgumentParser(description='小红书自动发布工具')
    parser.add_argument('--login', action='store_true', help='仅执行登录流程')
    parser.add_argument('--publish-now', action='store_true', help='立即执行一次发布')
    parser.add_argument('--run', action='store_true', help='启动定时任务（默认）')
    
    args = parser.parse_args()
    
    if args.login:
        login_task()
    elif args.publish_now:
        daily_task()
    else:
        logger.info("小红书自动维护工具已启动")
        logger.info(f"定时任务: 每天 {config.SCHEDULE_HOUR:02d}:{config.SCHEDULE_MINUTE:02d}")
        
        scheduler = Scheduler(daily_task)
        scheduler.run()


if __name__ == "__main__":
    main()
