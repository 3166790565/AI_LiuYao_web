# 自定义模型管理功能模块
# 该文件实现了自定义模型的增删改查功能

from flask import Blueprint, render_template, request, jsonify
from flask_login import login_required, current_user
from models import db, CustomModel
from config import config

# 创建自定义模型管理蓝图
models_bp = Blueprint('models', __name__, url_prefix='/models')

@models_bp.route('/list', methods=['GET'])
def get_custom_models():
    """获取自定义模型列表
    
    Returns:
        JSON: 自定义模型列表
    """
    if current_user.is_authenticated:
        # 如果用户已登录，返回该用户的自定义模型
        models = CustomModel.query.filter_by(user_id=current_user.id).all()
    else:
        # 如果用户未登录，返回空列表
        models = []
    
    # 转换为字典列表
    model_list = []
    for model in models:
        model_list.append({
            'id': model.id,
            'name': model.name,
            'api_url': model.api_url,
            'api_key': model.api_key,
            'description': model.description,
            'created_at': model.created_at.strftime('%Y-%m-%d %H:%M:%S')
        })
    
    return jsonify({'models': model_list})

@models_bp.route('/add', methods=['POST'])
@login_required
def add_custom_model():
    """添加自定义模型
    
    Returns:
        JSON: 添加结果
    """
    try:
        data = request.get_json()
        name = data.get('name', '').strip()
        api_url = data.get('api_url', '').strip()
        api_key = data.get('api_key', '').strip()
        description = data.get('description', '').strip()
        
        # 验证数据
        if not name or not api_url or not api_key:
            return jsonify({'success': False, 'error': '模型名称、API URL和API Key不能为空'}), 400
        
        # 创建自定义模型
        custom_model = CustomModel(
            user_id=current_user.id,
            name=name,
            api_url=api_url,
            api_key=api_key,
            description=description
        )
        
        # 保存到数据库
        db.session.add(custom_model)
        db.session.commit()
        
        return jsonify({'success': True, 'message': '模型添加成功'})
    except Exception as e:
        db.session.rollback()
        return jsonify({'success': False, 'error': f'添加模型失败: {str(e)}'}), 500

@models_bp.route('/delete/<int:model_id>', methods=['DELETE'])
@login_required
def delete_custom_model(model_id):
    """删除自定义模型
    
    Args:
        model_id (int): 模型ID
        
    Returns:
        JSON: 删除结果
    """
    try:
        # 查询模型
        custom_model = CustomModel.query.filter_by(id=model_id, user_id=current_user.id).first()
        
        if not custom_model:
            return jsonify({'success': False, 'error': '模型不存在'}), 404
        
        # 删除模型
        db.session.delete(custom_model)
        db.session.commit()
        
        return jsonify({'success': True, 'message': '模型删除成功'})
    except Exception as e:
        db.session.rollback()
        return jsonify({'success': False, 'error': f'删除模型失败: {str(e)}'}), 500

@models_bp.route('/update/<int:model_id>', methods=['PUT'])
def update_custom_model(model_id):
    """更新自定义模型
    
    Args:
        model_id (int): 模型ID
        
    Returns:
        JSON: 更新结果
    """
    try:
        # 查询模型
        custom_model = CustomModel.query.filter_by(id=model_id, user_id=current_user.id).first()
        
        if not custom_model:
            return jsonify({'success': False, 'error': '模型不存在'}), 404
        
        # 获取更新数据
        data = request.get_json()
        name = data.get('name', '').strip()
        api_url = data.get('api_url', '').strip()
        api_key = data.get('api_key', '').strip()
        description = data.get('description', '').strip()
        
        # 验证数据
        if not name or not api_url or not api_key:
            return jsonify({'success': False, 'error': '模型名称、API URL和API Key不能为空'}), 400
        
        # 更新模型
        custom_model.name = name
        custom_model.api_url = api_url
        custom_model.api_key = api_key
        custom_model.description = description
        
        # 保存到数据库
        db.session.commit()
        
        return jsonify({'success': True, 'message': '模型更新成功'})
    except Exception as e:
        db.session.rollback()
        return jsonify({'success': False, 'error': f'更新模型失败: {str(e)}'}), 500

@models_bp.route('/get_all_models', methods=['GET'])
def get_all_models():
    """获取所有可用模型（内置模型 + 自定义模型）
    
    Returns:
        JSON: 所有可用模型列表
    """
    # 内置模型
    all_models = config.SUPPORTED_MODELS.copy()
    
    # 如果用户已登录，添加该用户的自定义模型
    if current_user.is_authenticated:
        custom_models = CustomModel.query.filter_by(user_id=current_user.id).all()
        for model in custom_models:
            all_models.append(model.name)
    
    return jsonify({'models': all_models})
