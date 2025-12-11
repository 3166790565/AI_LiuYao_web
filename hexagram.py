# 解卦功能模块
# 该文件实现了解卦相关的功能，包括解卦API、解卦记录管理等

from flask import Blueprint, render_template, request, jsonify
from flask_login import login_required, current_user
from models import db, HexagramRecord
from config import config
import uuid
import time
import json

# 创建解卦蓝图
hexagram_bp = Blueprint('hexagram', __name__, url_prefix='/hexagram')

@hexagram_bp.route('/analyze', methods=['POST'])
def api_analyze():
    """六爻分析API
    
    Returns:
        JSON: 分析结果
    """
    try:
        data = request.get_json()
        question = data.get('question', '')
        hexagram_info = data.get('hexagram_info', '')
        model = data.get('model', 'gpt-4')
        user_yongshen = data.get('user_yongshen', '').strip()
        
        if not question or not hexagram_info:
            return jsonify({'error': '问题和卦象信息不能为空'}), 400
        
        # 生成记录ID
        record_id = str(uuid.uuid4())
        timestamp = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime())
        
        # 1. 用神判断（优先使用用户指定用神）
        if user_yongshen:
            # 使用用户指定的用神
            yongshen_data = {
                'text': user_yongshen,
                'yiju': f'用户指定用神为：{user_yongshen}'
            }
        else:
            # AI判断用神
            from api import AI
            from prompt import yongshen_prompt
            yongshen_result = AI(f"问题：{question}\n卦象信息：{hexagram_info}", model=model, agent=yongshen_prompt)
            try:
                yongshen_data = json.loads(yongshen_result)
            except json.JSONDecodeError as e:
                return jsonify({'error': f'分析失败: 无法解析AI响应 - {str(e)}'}), 500
        
        # 2. 用神卦理分析
        from api import AI
        from prompt import yongshen_guli_prompt
        yongshen_guli_result = AI(
            f"问题：{question}\n卦象信息：{hexagram_info}\n已确定用神：{yongshen_data['text']}",
            model=model,
            agent=yongshen_guli_prompt
        )
        try:
            yongshen_guli_data = json.loads(yongshen_guli_result)
        except json.JSONDecodeError as e:
            return jsonify({'error': f'分析失败: 无法解析AI响应 - {str(e)}'}), 500
        
        # 3. 动爻卦理分析
        from prompt import dongyao_guli_prompt
        dongyao_guli_result = AI(
            f"卦象信息：{hexagram_info}",
            model=model,
            agent=dongyao_guli_prompt
        )
        try:
            dongyao_guli_data = json.loads(dongyao_guli_result)
        except json.JSONDecodeError as e:
            return jsonify({'error': f'分析失败: 无法解析AI响应 - {str(e)}'}), 500
        
        # 4. 数字量化分析
        from prompt import shuzi_lianghua_prompt
        shuzi_lianghua_result = AI(
            f"卦象信息：{hexagram_info}\n已确定用神：{yongshen_data['text']}",
            model=model,
            agent=shuzi_lianghua_prompt
        )
        try:
            shuzi_lianghua_data = json.loads(shuzi_lianghua_result)
        except json.JSONDecodeError as e:
            return jsonify({'error': f'分析失败: 无法解析AI响应 - {str(e)}'}), 500
        
        # 计算用神强弱指数
        yuejian = shuzi_lianghua_data['月建']
        richen = shuzi_lianghua_data['日辰']
        yongshen_dizhi = shuzi_lianghua_data['用神']
        
        from shuzilianghua import shuzilianghua
        yuejianshu, richenshu = shuzilianghua(yuejian, richen, yongshen_dizhi)
        
        # 计算动爻强弱指数
        dongyao_strengths = []
        for dizhi in shuzi_lianghua_data['动爻列表']:
            dy_yuejianshu, dy_richenshu = shuzilianghua(yuejian, richen, dizhi)
            dongyao_strengths.append({
                '地支': dizhi,
                '月建数': dy_yuejianshu,
                '日辰数': dy_richenshu,
                '总指数': dy_yuejianshu + dy_richenshu
            })
        
        # 5. 综合解读
        from prompt import zonghe_jiedu_prompt
        zonghe_jiedu = AI(
            f"问题：{question}\n卦象信息：{hexagram_info}\n用神判断：{yongshen_data['text']}\n用神卦理：{json.dumps(yongshen_guli_data, ensure_ascii=False)}\n动爻卦理：{json.dumps(dongyao_guli_data, ensure_ascii=False)}\n数字量化：月建={yuejian}，日辰={richen}，用神地支={yongshen_dizhi}，用神指数={yuejianshu + richenshu}",
            model=model,
            agent=zonghe_jiedu_prompt
        )
        
        # 构建数字量化分析结果
        shuzi_lianghua_data['用神指数'] = {
            '月建数': yuejianshu,
            '日辰数': richenshu,
            '总指数': yuejianshu + richenshu
        }
        shuzi_lianghua_data['动爻指数'] = dongyao_strengths
        
        # 保存历史记录到数据库
        # 获取当前用户ID（如果用户未登录，user_id为None）
        user_id = current_user.id if current_user.is_authenticated else None
        
        # 创建解卦记录
        hexagram_record = HexagramRecord(
            user_id=user_id,
            record_id=record_id,
            question=question,
            hexagram_info=hexagram_info,
            model=model,
            yongshen=json.dumps(yongshen_data, ensure_ascii=False),
            yongshen_guli=json.dumps(yongshen_guli_data, ensure_ascii=False),
            dongyao_guli=json.dumps(dongyao_guli_data, ensure_ascii=False),
            shuzi_lianghua=json.dumps(shuzi_lianghua_data, ensure_ascii=False),
            zonghe_jiedu=zonghe_jiedu,
            timestamp=timestamp
        )
        
        # 保存到数据库
        db.session.add(hexagram_record)
        db.session.commit()
        
        return jsonify({'success': True, 'record_id': record_id})
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': f'分析失败: {str(e)}'}), 500

@hexagram_bp.route('/record/<record_id>')
def get_record(record_id):
    """获取解卦记录
    
    Args:
        record_id (str): 记录ID
        
    Returns:
        JSON: 解卦记录
    """
    # 查询解卦记录
    record = HexagramRecord.query.filter_by(record_id=record_id).first()
    
    if not record:
        return jsonify({'error': '记录不存在'}), 404
    
    # 检查用户权限
    if record.user_id and (not current_user.is_authenticated or record.user_id != current_user.id):
        return jsonify({'error': '您没有权限查看此记录'}), 403
    
    # 构建返回数据
    result = {
        'id': record.id,
        'record_id': record.record_id,
        'question': record.question,
        'hexagram_info': record.hexagram_info,
        'model': record.model,
        'yongshen': json.loads(record.yongshen),
        'yongshen_guli': json.loads(record.yongshen_guli),
        'dongyao_guli': json.loads(record.dongyao_guli),
        'shuzi_lianghua': json.loads(record.shuzi_lianghua),
        'zonghe_jiedu': record.zonghe_jiedu,
        'timestamp': record.timestamp.strftime('%Y-%m-%d %H:%M:%S')
    }
    
    return jsonify({'record': result})

@hexagram_bp.route('/history')
@login_required
def get_history():
    """获取历史记录
    
    Returns:
        JSON: 历史记录列表
    """
    # 查询当前用户的历史记录
    records = HexagramRecord.query.filter_by(user_id=current_user.id).order_by(HexagramRecord.timestamp.desc()).all()
    
    # 转换为字典列表
    record_list = []
    for record in records:
        record_list.append({
            'id': record.id,
            'record_id': record.record_id,
            'question': record.question,
            'model': record.model,
            'timestamp': record.timestamp.strftime('%Y-%m-%d %H:%M:%S'),
            'yongshen': json.loads(record.yongshen)
        })
    
    return jsonify({'records': record_list})

@hexagram_bp.route('/delete/<int:record_id>', methods=['DELETE'])
@login_required
def delete_record(record_id):
    """删除解卦记录
    
    Args:
        record_id (int): 记录ID
        
    Returns:
        JSON: 删除结果
    """
    try:
        # 查询记录
        record = HexagramRecord.query.filter_by(id=record_id, user_id=current_user.id).first()
        
        if not record:
            return jsonify({'success': False, 'error': '记录不存在'}), 404
        
        # 删除记录
        db.session.delete(record)
        db.session.commit()
        
        return jsonify({'success': True, 'message': '记录删除成功'})
    except Exception as e:
        db.session.rollback()
        return jsonify({'success': False, 'error': f'删除记录失败: {str(e)}'}), 500
