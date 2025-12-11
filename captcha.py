# 图形验证码功能模块
# 该文件实现了图形验证码的生成和验证功能

from PIL import Image, ImageDraw, ImageFont
import random
import string
import io
from flask import session
from config import config

# 验证码字符集（去除了容易混淆的字符，如0、O、1、I、l等）
CAPTCHA_CHARS = string.ascii_uppercase + string.digits.replace('0', '').replace('O', '').replace('1', '').replace('I', '').replace('L', '')

class Captcha:
    """图形验证码生成类"""
    
    def __init__(self):
        """初始化验证码生成器"""
        self.length = config.CAPTCHA_LENGTH  # 验证码长度
        self.width = config.CAPTCHA_WIDTH  # 验证码宽度
        self.height = config.CAPTCHA_HEIGHT  # 验证码高度
        self.font_size = config.CAPTCHA_FONT_SIZE  # 验证码字体大小
        self.noise_level = config.CAPTCHA_NOISE_LEVEL  # 验证码噪声级别
        self.expiration = config.CAPTCHA_EXPIRATION  # 验证码有效期（秒）
    
    def generate_captcha(self):
        """生成图形验证码
        
        Returns:
            tuple: (验证码图像字节流, 验证码文本)
        """
        # 生成随机验证码文本
        captcha_text = ''.join(random.sample(CAPTCHA_CHARS, self.length))
        
        # 创建验证码图像
        image = Image.new('RGB', (self.width, self.height), (255, 255, 255))
        
        # 获取绘图对象
        draw = ImageDraw.Draw(image)
        
        # 加载字体（使用默认字体）
        try:
            # 尝试使用系统字体
            font = ImageFont.truetype('arial.ttf', self.font_size)
        except IOError:
            # 如果系统没有arial字体，使用默认字体
            font = ImageFont.load_default()
        
        # 绘制验证码文本
        for i, char in enumerate(captcha_text):
            # 随机字符位置
            x = 10 + i * (self.width - 20) // self.length
            y = random.randint(5, self.height - self.font_size - 5)
            # 随机字符颜色
            color = (random.randint(0, 100), random.randint(0, 100), random.randint(0, 100))
            # 绘制字符
            draw.text((x, y), char, font=font, fill=color)
        
        # 添加干扰线
        for _ in range(5):
            # 随机干扰线颜色
            line_color = (random.randint(0, 150), random.randint(0, 150), random.randint(0, 150))
            # 随机干扰线位置
            x1 = random.randint(0, self.width)
            y1 = random.randint(0, self.height)
            x2 = random.randint(0, self.width)
            y2 = random.randint(0, self.height)
            # 绘制干扰线
            draw.line([(x1, y1), (x2, y2)], fill=line_color, width=2)
        
        # 添加噪点
        for _ in range(int(self.width * self.height * self.noise_level)):
            # 随机噪点位置
            x = random.randint(0, self.width - 1)
            y = random.randint(0, self.height - 1)
            # 随机噪点颜色
            noise_color = (random.randint(0, 200), random.randint(0, 200), random.randint(0, 200))
            # 绘制噪点
            draw.point((x, y), fill=noise_color)
        
        # 将图像转换为字节流
        img_io = io.BytesIO()
        image.save(img_io, format='PNG')
        img_io.seek(0)
        
        # 保存验证码到session中，用于后续验证
        session['captcha'] = captcha_text
        session.permanent = False  # 不使用永久会话
        
        return img_io, captcha_text
    
    @staticmethod
    def verify_captcha(user_input):
        """验证验证码
        
        Args:
            user_input (str): 用户输入的验证码
            
        Returns:
            bool: 验证码是否正确
        """
        # 获取session中保存的验证码
        captcha = session.get('captcha', '')
        
        # 清除session中的验证码，防止重复使用
        if 'captcha' in session:
            del session['captcha']
        
        # 验证验证码（不区分大小写）
        return user_input.upper() == captcha.upper()
