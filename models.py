# 数据库模型文件
# 该文件定义了应用程序的所有数据库模型

from datetime import datetime
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Text
from sqlalchemy.orm import relationship
import bcrypt
from flask_login import UserMixin

# 创建数据库对象
# 注意：db对象将在app.py中初始化，这里只定义模型
# 所以先创建一个空的SQLAlchemy对象，不传递app参数
db = SQLAlchemy()

class User(db.Model, UserMixin):
    """用户模型"""
    __tablename__ = 'users'  # 表名
    
    id = Column(Integer, primary_key=True, autoincrement=True)  # 主键，自增
    username = Column(String(50), unique=True, nullable=False, index=True)  # 用户名，唯一，非空，添加索引
    password_hash = Column(String(128), nullable=False)  # 密码哈希，非空
    created_at = Column(DateTime, default=datetime.utcnow)  # 创建时间，默认当前时间
    
    # 关联关系
    custom_models = relationship('CustomModel', backref='user', cascade='all, delete-orphan')  # 自定义模型，一对多关系
    hexagram_records = relationship('HexagramRecord', backref='user', cascade='all, delete-orphan')  # 解卦记录，一对多关系
    
    def __repr__(self):
        """返回用户对象的字符串表示"""
        return f'<User {self.username}>'
    
    def set_password(self, password):
        """设置密码，使用bcrypt算法加密"""
        self.password_hash = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
    
    def check_password(self, password):
        """验证密码"""
        return bcrypt.checkpw(password.encode('utf-8'), self.password_hash.encode('utf-8'))

class CustomModel(db.Model):
    """自定义模型配置模型"""
    __tablename__ = 'custom_models'  # 表名
    
    id = Column(Integer, primary_key=True, autoincrement=True)  # 主键，自增
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False)  # 外键，关联users表的id字段
    name = Column(String(100), nullable=False)  # 模型名称，非空
    api_url = Column(String(255), nullable=False)  # API地址，非空
    api_key = Column(String(255), nullable=False)  # API密钥，非空
    description = Column(Text, nullable=True)  # 模型描述，可为空
    created_at = Column(DateTime, default=datetime.utcnow)  # 创建时间，默认当前时间
    
    def __repr__(self):
        """返回自定义模型对象的字符串表示"""
        return f'<CustomModel {self.name}>'

class HexagramRecord(db.Model):
    """解卦记录模型"""
    __tablename__ = 'hexagram_records'  # 表名
    
    id = Column(Integer, primary_key=True, autoincrement=True)  # 主键，自增
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False)  # 外键，关联users表的id字段
    record_id = Column(String(36), unique=True, nullable=False, index=True)  # 记录ID，UUID格式，唯一，非空，添加索引
    question = Column(Text, nullable=False)  # 问题，非空
    hexagram_info = Column(Text, nullable=False)  # 卦象信息，非空
    model = Column(String(50), nullable=False)  # 使用的模型，非空
    yongshen = Column(Text, nullable=False)  # 用神判断结果，JSON格式，非空
    yongshen_guli = Column(Text, nullable=False)  # 用神卦理分析，JSON格式，非空
    dongyao_guli = Column(Text, nullable=False)  # 动爻卦理分析，JSON格式，非空
    shuzi_lianghua = Column(Text, nullable=False)  # 数字量化分析，JSON格式，非空
    zonghe_jiedu = Column(Text, nullable=False)  # 综合解读，非空
    timestamp = Column(DateTime, default=datetime.utcnow)  # 解卦时间，默认当前时间
    
    def __repr__(self):
        """返回解卦记录对象的字符串表示"""
        return f'<HexagramRecord {self.record_id}>'
