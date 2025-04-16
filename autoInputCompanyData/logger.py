import logging
from logging.handlers import TimedRotatingFileHandler
from pathlib import Path
import os
import time
import re

LOG_FORMAT = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
LOG_DIR = Path(__file__).parent / 'logs'
LOG_DIR.mkdir(exist_ok=True)

class CustomTimedRotatingFileHandler(TimedRotatingFileHandler):
    """自定义的TimedRotatingFileHandler，确保日志内容正确写入到带日期的文件中"""
    
    def __init__(self, filename, when='h', interval=1, backupCount=0, encoding=None, delay=False, utc=False, atTime=None):
        # 设置日志文件后缀名格式为 .YYYY-MM-DD
        self.suffix = '%Y-%m-%d'
        # 获取当前日期作为文件名后缀
        self.today_suffix = time.strftime(self.suffix, time.localtime())
        # 构建今天的日志文件名
        self.today_log_file = f"{filename}.{self.today_suffix}"
        # 编译正则表达式用于匹配日志文件
        self.extMatch = re.compile(r"^process\.log\.\d{4}-\d{2}-\d{2}$")
        
        super().__init__(filename, when, interval, backupCount, encoding, delay, utc, atTime)
        
    def _open(self):
        # 同时打开当前日期的日志文件
        today_file = open(self.today_log_file, mode='a', encoding=self.encoding)
        # 打开基础日志文件
        base_file = open(self.baseFilename, mode='a', encoding=self.encoding)
        # 返回基础文件，TimedRotatingFileHandler会使用它
        return base_file
        
    def emit(self, record):
        # 调用父类的emit方法
        super().emit(record)
        # 确保日志也写入到当天的日志文件
        try:
            msg = self.format(record)
            with open(self.today_log_file, 'a', encoding=self.encoding) as f:
                f.write(f"{msg}\n")
        except Exception:
            self.handleError(record)

def setup_logger():
    logger = logging.getLogger()
    logger.setLevel(logging.INFO)

    # 使用自定义的文件处理器（按日期分割，保留30天的日志）
    log_file = LOG_DIR / 'process.log'
    file_handler = CustomTimedRotatingFileHandler(
        filename=str(log_file),
        when='midnight',  # 每天午夜切割
        interval=1,       # 每1天切割一次
        backupCount=30,   # 保留30天的日志
        encoding='utf-8',
        delay=False       # 立即创建日志文件
    )
    
    # 设置日志格式
    file_handler.setFormatter(logging.Formatter(LOG_FORMAT))

    # 控制台处理器
    console_handler = logging.StreamHandler()
    console_handler.setFormatter(logging.Formatter(LOG_FORMAT))

    logger.addHandler(file_handler)
    logger.addHandler(console_handler)
    
    # 强制立即执行一次日志轮转，确保按照正确的格式创建日志文件
    # 注意：必须在添加handler到logger之后执行doRollover
    file_handler.doRollover()

    return logger