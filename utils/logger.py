import logging
import os
from logging.handlers import RotatingFileHandler

# 日志文件目录
LOG_DIR = 'logs'
if not os.path.exists(LOG_DIR):
    os.makedirs(LOG_DIR)

# 日志文件路径
LOG_FILE = os.path.join(LOG_DIR, 'app.log')

# 日志级别
LOG_LEVEL = logging.INFO

# 日志格式
LOG_FORMAT = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'

# 日志日期格式
DATE_FORMAT = '%Y-%m-%d %H:%M:%S'

def setup_logger(name):
    """
    设置日志记录器
    
    参数:
        name (str): 日志记录器名称
        
    返回:
        logging.Logger: 配置好的日志记录器
    """
    # 创建日志记录器
    logger = logging.getLogger(name)
    logger.setLevel(LOG_LEVEL)
    
    # 检查是否已经添加了处理器，避免重复添加
    if not logger.handlers:
        # 创建控制台处理器
        console_handler = logging.StreamHandler()
        console_handler.setLevel(LOG_LEVEL)
        console_formatter = logging.Formatter(LOG_FORMAT, DATE_FORMAT)
        console_handler.setFormatter(console_formatter)
        logger.addHandler(console_handler)
        
        # 创建文件处理器（带轮转）
        file_handler = RotatingFileHandler(
            LOG_FILE, 
            maxBytes=10*1024*1024,  # 10MB
            backupCount=5  # 保留5个备份文件
        )
        file_handler.setLevel(LOG_LEVEL)
        file_formatter = logging.Formatter(LOG_FORMAT, DATE_FORMAT)
        file_handler.setFormatter(file_formatter)
        logger.addHandler(file_handler)
    
    return logger
