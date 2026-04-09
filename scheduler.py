from apscheduler.schedulers.blocking import BlockingScheduler
from apscheduler.triggers.cron import CronTrigger
import config


class Scheduler:
    def __init__(self, task_func):
        self.scheduler = BlockingScheduler()
        self.task_func = task_func

    def start(self):
        trigger = CronTrigger(
            hour=config.SCHEDULE_HOUR,
            minute=config.SCHEDULE_MINUTE
        )
        self.scheduler.add_job(
            self.task_func,
            trigger,
            id='daily_publish'
        )
        print(f"定时任务已启动: 每天 {config.SCHEDULE_HOUR:02d}:{config.SCHEDULE_MINUTE:02d} 执行")

    def run(self):
        self.start()
        try:
            self.scheduler.start()
        except (KeyboardInterrupt, SystemExit):
            self.stop()

    def stop(self):
        self.scheduler.shutdown()
        print("定时任务已停止")
