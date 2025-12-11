# 配置文件
# 该文件包含应用程序的所有配置信息

import os
from dotenv import load_dotenv

# 加载环境变量
load_dotenv()

class Config:
    """应用程序配置类"""
    
    # 基本配置
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'ai-liuyao-secret-key'  # 用于会话加密
    DEBUG = os.environ.get('DEBUG', 'True').lower() == 'true'  # 调试模式
    
    # 数据库配置
    # SQLite数据库连接URI，格式：sqlite:///database.db
    # 示例：sqlite:///ai_liuyao.db
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URI') or 'sqlite:///ai_liuyao.db'
    SQLALCHEMY_TRACK_MODIFICATIONS = False  # 禁用跟踪修改，提高性能
    
    # 图形验证码配置
    CAPTCHA_LENGTH = 4  # 验证码长度
    CAPTCHA_WIDTH = 120  # 验证码宽度
    CAPTCHA_HEIGHT = 40  # 验证码高度
    CAPTCHA_FONT_SIZE = 20  # 验证码字体大小
    CAPTCHA_NOISE_LEVEL = 0.3  # 验证码噪声级别
    CAPTCHA_EXPIRATION = 300  # 验证码有效期（秒）
    
    # 支持的AI模型
    SUPPORTED_MODELS = [
        "gpt-4",
        "gpt-4.1",
        "gpt-4o"
    ]
    
    # 历史记录存储目录（暂时保留，用于迁移旧数据）
    HISTORY_DIR = 'history'

# 创建配置实例
config = Config()
