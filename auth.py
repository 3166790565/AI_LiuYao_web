# 用户认证功能模块
# 该文件实现了用户的注册、登录、登出等功能

from flask import Blueprint, render_template, redirect, url_for, request, jsonify
from flask_login import login_user, logout_user, login_required, current_user
from models import db, User
from captcha import Captcha

# 创建认证蓝图
auth_bp = Blueprint('auth', __name__, url_prefix='/auth')

# 创建验证码生成器实例
captcha_generator = Captcha()

@auth_bp.route('/register', methods=['GET', 'POST'])
def register():
    """用户注册
    
    GET: 返回注册页面
    POST: 处理注册请求
    """
    if request.method == 'POST':
        # 获取表单数据
        username = request.form.get('username', '').strip()
        password = request.form.get('password', '')
        confirm_password = request.form.get('confirm_password', '')
        captcha = request.form.get('captcha', '').strip()
        
        # 验证验证码
        if not Captcha.verify_captcha(captcha):
            return render_template('auth/register.html', error='验证码错误')
        
        # 验证表单数据
        if not username:
            return render_template('auth/register.html', error='用户名不能为空')
        
        if len(username) < 3 or len(username) > 50:
            return render_template('auth/register.html', error='用户名长度必须在3-50个字符之间')
        
        if not password:
            return render_template('auth/register.html', error='密码不能为空')
        
        if len(password) < 6:
            return render_template('auth/register.html', error='密码长度不能少于6个字符')
        
        if password != confirm_password:
            return render_template('auth/register.html', error='两次输入的密码不一致')
        
        # 检查用户名是否已存在
        existing_user = User.query.filter_by(username=username).first()
        if existing_user:
            return render_template('auth/register.html', error='用户名已存在')
        
        # 创建新用户
        user = User()
        user.username = username
        user.set_password(password)
        
        # 保存用户到数据库
        db.session.add(user)
        db.session.commit()
        
        # 自动登录新用户
        login_user(user)
        
        # 重定向到首页
        return redirect(url_for('index'))
    
    # GET请求，返回注册页面
    return render_template('auth/register.html')

@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    """用户登录
    
    GET: 返回登录页面
    POST: 处理登录请求
    """
    if request.method == 'POST':
        # 获取表单数据
        username = request.form.get('username', '').strip()
        password = request.form.get('password', '')
        captcha = request.form.get('captcha', '').strip()
        
        # 验证验证码
        if not Captcha.verify_captcha(captcha):
            return render_template('auth/login.html', error='验证码错误')
        
        # 验证表单数据
        if not username or not password:
            return render_template('auth/login.html', error='用户名和密码不能为空')
        
        # 查询用户
        user = User.query.filter_by(username=username).first()
        
        # 验证用户和密码
        if not user or not user.check_password(password):
            return render_template('auth/login.html', error='用户名或密码错误')
        
        # 登录用户
        login_user(user)
        
        # 重定向到首页
        return redirect(url_for('index'))
    
    # GET请求，返回登录页面
    return render_template('auth/login.html')

@auth_bp.route('/logout')
@login_required
def logout():
    """用户登出"""
    logout_user()
    return redirect(url_for('auth.login'))

@auth_bp.route('/captcha')
def get_captcha():
    """获取图形验证码
    
    Returns:
        Response: 验证码图像
    """
    from flask import Response
    
    # 生成验证码
    img_io, captcha_text = captcha_generator.generate_captcha()
    
    # 返回验证码图像
    return Response(img_io.getvalue(), mimetype='image/png')

@auth_bp.route('/check_username', methods=['POST'])
def check_username():
    """检查用户名是否已存在
    
    Returns:
        JSON: {'exists': True/False}
    """
    username = request.json.get('username', '').strip()
    if not username:
        return jsonify({'exists': False})
    
    user = User.query.filter_by(username=username).first()
    return jsonify({'exists': user is not None})
