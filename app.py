# 主应用文件
# 该文件是应用程序的入口点，整合了所有蓝图和配置

# 使用pymysql代替MySQLdb
import pymysql
pymysql.install_as_MySQLdb()

from flask import Flask, render_template, request, jsonify, redirect, url_for
from flask_cors import CORS
from flask_login import LoginManager
import os

# 导入配置
from config import config

# 导入数据库模型
from models import db

# 导入蓝图
from auth import auth_bp
from hexagram import hexagram_bp
from models_manager import models_bp

# 创建Flask应用
app = Flask(__name__)
CORS(app)  # 启用CORS支持

# 配置应用
app.config.from_object(config)

# 初始化数据库
app.config['SQLALCHEMY_DATABASE_URI'] = config.SQLALCHEMY_DATABASE_URI
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = config.SQLALCHEMY_TRACK_MODIFICATIONS
app.secret_key = config.SECRET_KEY

# 初始化数据库
db.init_app(app)

# 初始化Flask-Login
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'auth.login'  # 设置登录页面路由

# 加载用户
from models import User

@login_manager.user_loader
def load_user(user_id):
    """加载用户
    
    Args:
        user_id (str): 用户ID
        
    Returns:
        User: 用户对象
    """
    return User.query.get(int(user_id))

# 注册蓝图
app.register_blueprint(auth_bp)
app.register_blueprint(hexagram_bp)
app.register_blueprint(models_bp)

# 首页路由
@app.route('/')
def index():
    """首页"""
    # 检查用户是否已登录
    from flask_login import current_user
    if not current_user.is_authenticated:
        return redirect(url_for('auth.login'))
    
    # 合并内置模型和自定义模型
    from models import CustomModel
    all_models = config.SUPPORTED_MODELS.copy()
    
    # 添加该用户的自定义模型
    custom_models = CustomModel.query.filter_by(user_id=current_user.id).all()
    for model in custom_models:
        all_models.append(model.name)
    
    return render_template('index.html', models=all_models, user=current_user)

# 分析结果页面
@app.route('/result/<record_id>')
def result(record_id):
    """分析结果页面"""
    # 查询解卦记录
    from models import HexagramRecord
    record = HexagramRecord.query.filter_by(record_id=record_id).first()
    
    if not record:
        return jsonify({'error': '记录不存在'}), 404
    
    # 检查用户权限
    from flask_login import current_user
    if record.user_id and (not current_user.is_authenticated or record.user_id != current_user.id):
        return jsonify({'error': '您没有权限查看此记录'}), 403
    
    # 合并内置模型和自定义模型
    all_models = config.SUPPORTED_MODELS.copy()
    from models import CustomModel
    if current_user.is_authenticated:
        custom_models = CustomModel.query.filter_by(user_id=current_user.id).all()
        for model in custom_models:
            all_models.append(model.name)
    
    # 构建返回数据
    import json
    result_data = {
        'id': record.record_id,
        'timestamp': record.timestamp.strftime('%Y-%m-%d %H:%M:%S'),
        'question': record.question,
        'hexagram_info': record.hexagram_info,
        'model': record.model,
        'yongshen': json.loads(record.yongshen),
        'yongshen_guli': json.loads(record.yongshen_guli),
        'dongyao_guli': json.loads(record.dongyao_guli),
        'shuzi_lianghua': json.loads(record.shuzi_lianghua),
        'zonghe_jiedu': record.zonghe_jiedu
    }
    
    return render_template('result.html', record=result_data, models=all_models)

# 历史记录页面
@app.route('/history')
def history():
    """历史记录页面"""
    # 检查用户是否已登录
    from flask_login import current_user
    if not current_user.is_authenticated:
        return redirect(url_for('auth.login'))
    
    from models import HexagramRecord
    
    # 查询当前用户的历史记录
    records = HexagramRecord.query.filter_by(user_id=current_user.id).order_by(HexagramRecord.timestamp.desc()).all()
    
    # 转换为字典列表
    record_list = []
    for record in records:
        import json
        record_list.append({
            'id': record.record_id,
            'timestamp': record.timestamp.strftime('%Y-%m-%d %H:%M:%S'),
            'question': record.question,
            'model': record.model,
            'yongshen': json.loads(record.yongshen)['text']
        })
    
    return render_template('history.html', records=record_list, user=current_user)

# 聊天页面（已移除，只保留解卦结果中的聊天咨询功能）
# @app.route('/chat')
# def chat():
#     """聊天页面"""
#     # 合并内置模型和自定义模型
#     all_models = config.SUPPORTED_MODELS.copy()
#     from models import CustomModel
#     if hasattr(request, 'user') and request.user.is_authenticated:
#         custom_models = CustomModel.query.filter_by(user_id=request.user.id).all()
#         for model in custom_models:
#             all_models.append(model.name)
#     return render_template('chat.html', models=all_models)

# API: 六爻分析（重定向到hexagram_bp的analyze路由）
@app.route('/api/analyze', methods=['POST'])
def api_analyze():
    """六爻分析API（重定向）"""
    # 重定向到hexagram_bp的analyze路由
    return hexagram_bp.view_functions['api_analyze'](request)

# API: 聊天功能
@app.route('/api/chat', methods=['POST'])
def api_chat():
    """聊天功能API"""
    try:
        from api import AI_chat
        data = request.get_json()
        messages = data.get('messages', [])
        model = data.get('model', 'gpt-4')
        
        if not messages:
            return jsonify({'error': '消息不能为空'}), 400
        
        # 调用AI聊天接口
        response = AI_chat({
            'model': model,
            'messages': messages
        })
        
        return jsonify({'success': True, 'response': response})
        
    except Exception as e:
        app.logger.error(f'聊天失败: {str(e)}')
        return jsonify({'error': f'聊天失败: {str(e)}'}), 500

# API: 获取历史记录（重定向到hexagram_bp的get_history路由）
@app.route('/api/history', methods=['GET'])
def api_get_history():
    """获取历史记录API（重定向）"""
    # 重定向到hexagram_bp的get_history路由
    return hexagram_bp.view_functions['get_history'](request)

# API: 删除历史记录（重定向到hexagram_bp的delete_record路由）
@app.route('/api/history/<record_id>', methods=['DELETE'])
def api_delete_history(record_id):
    """删除历史记录API（重定向）"""
    # 重定向到hexagram_bp的delete_record路由
    from models import HexagramRecord
    record = HexagramRecord.query.filter_by(record_id=record_id).first()
    if not record:
        return jsonify({'error': '记录不存在'}), 404
    
    return hexagram_bp.view_functions['delete_record'](request, record.id)

# 设置页面路由
@app.route('/settings')
def settings():
    """设置页面"""
    # 检查用户是否已登录
    from flask_login import current_user
    if not current_user.is_authenticated:
        return redirect(url_for('auth.login'))
    
    from models import CustomModel
    
    # 获取该用户的自定义模型
    custom_models = CustomModel.query.filter_by(user_id=current_user.id).all()
    
    return render_template('settings.html', custom_models=custom_models, user=current_user)

# API: 从自定义API获取模型列表
@app.route('/api/settings/fetch-models', methods=['POST'])
def api_fetch_models():
    """从自定义API获取模型列表"""
    try:
        import requests
        data = request.get_json()
        api_url = data.get('apiUrl')
        api_key = data.get('apiKey')
        
        if not api_url or not api_key:
            return jsonify({'success': False, 'error': 'API URL和API Key不能为空'}), 400
        
        # 尝试获取模型列表（支持OpenAI兼容的API）
        # 首先尝试OpenAI格式的模型列表端点
        models_endpoint = api_url.rsplit('/', 2)[0] + '/models'
        
        headers = {
            'Authorization': f'Bearer {api_key}',
            'Content-Type': 'application/json'
        }
        
        response = requests.get(models_endpoint, headers=headers)
        
        if response.status_code != 200:
            # 如果失败，返回空列表或错误信息
            return jsonify({'success': True, 'models': []})
        
        models_data = response.json()
        model_list = [model['id'] for model in models_data.get('data', [])]
        
        return jsonify({'success': True, 'models': model_list})
        
    except Exception as e:
        app.logger.error(f'获取模型列表失败: {str(e)}')
        return jsonify({'success': False, 'error': f'获取模型列表失败: {str(e)}'}), 500

# API: 添加自定义模型（重定向到models_bp的add_custom_model路由）
@app.route('/api/settings/models', methods=['POST'])
def api_add_model():
    """添加自定义模型API（重定向）"""
    # 重定向到models_bp的add_custom_model路由
    return models_bp.view_functions['add_custom_model'](request)

# API: 获取所有自定义模型（重定向到models_bp的get_custom_models路由）
@app.route('/api/settings/models', methods=['GET'])
def api_get_models():
    """获取所有自定义模型API（重定向）"""
    # 重定向到models_bp的get_custom_models路由
    return models_bp.view_functions['get_custom_models'](request)

# API: 删除自定义模型（重定向到models_bp的delete_custom_model路由）
@app.route('/api/settings/models/<model_id>', methods=['DELETE'])
def api_delete_model(model_id):
    """删除自定义模型API（重定向）"""
    # 重定向到models_bp的delete_custom_model路由
    return models_bp.view_functions['delete_custom_model'](request, int(model_id))

# 初始化数据库
with app.app_context():
    """初始化数据库"""
    # 创建数据库表
    db.create_all()
    
    # 确保历史记录目录存在（暂时保留，用于迁移旧数据）
    if not os.path.exists(config.HISTORY_DIR):
        os.makedirs(config.HISTORY_DIR)

if __name__ == '__main__':
    app.run(debug=config.DEBUG, host='0.0.0.0', port=5000)

