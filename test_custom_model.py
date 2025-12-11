# 测试自定义模型功能
import requests
import json
import os

# 测试URL
base_url = 'http://localhost:5000'

# 测试数据
mock_model_data = {
    "apiUrl": "https://api.example.com/v1/chat/completions",
    "apiKey": "test-api-key",
    "modelName": "test-model-1",
    "modelDescription": "测试自定义模型"
}

def test_custom_model_workflow():
    """测试自定义模型的完整工作流程"""
    print("=== 测试自定义模型功能 ===")
    
    # 1. 测试获取模型列表
    print("\n1. 测试获取模型列表")
    try:
        response = requests.get(f'{base_url}/api/settings/models')
        result = response.json()
        print(f"状态码: {response.status_code}")
        print(f"成功: {result.get('success')}")
        print(f"模型数量: {len(result.get('models', []))}")
    except Exception as e:
        print(f"获取模型列表失败: {str(e)}")
    
    # 2. 测试添加自定义模型
    print("\n2. 测试添加自定义模型")
    try:
        response = requests.post(
            f'{base_url}/api/settings/models',
            headers={'Content-Type': 'application/json'},
            json=mock_model_data
        )
        result = response.json()
        print(f"状态码: {response.status_code}")
        print(f"成功: {result.get('success')}")
        if not result.get('success'):
            print(f"错误信息: {result.get('error')}")
    except Exception as e:
        print(f"添加模型失败: {str(e)}")
    
    # 3. 再次获取模型列表，验证添加成功
    print("\n3. 验证模型添加成功")
    try:
        response = requests.get(f'{base_url}/api/settings/models')
        result = response.json()
        models = result.get('models', [])
        test_model = next((m for m in models if m['name'] == mock_model_data['modelName']), None)
        if test_model:
            print(f"✅ 模型添加成功！模型ID: {test_model['id']}")
        else:
            print("❌ 模型添加失败，未在列表中找到")
    except Exception as e:
        print(f"验证模型添加失败: {str(e)}")
    
    # 4. 测试首页模型列表包含自定义模型
    print("\n4. 测试首页模型列表")
    try:
        response = requests.get(f'{base_url}/')
        content = response.text
        if mock_model_data['modelName'] in content:
            print(f"✅ 首页模型列表包含自定义模型 '{mock_model_data['modelName']}'")
        else:
            print(f"❌ 首页模型列表不包含自定义模型 '{mock_model_data['modelName']}'")
    except Exception as e:
        print(f"测试首页模型列表失败: {str(e)}")
    
    # 5. 测试聊天页面模型列表包含自定义模型
    print("\n5. 测试聊天页面模型列表")
    try:
        response = requests.get(f'{base_url}/chat')
        content = response.text
        if mock_model_data['modelName'] in content:
            print(f"✅ 聊天页面模型列表包含自定义模型 '{mock_model_data['modelName']}'")
        else:
            print(f"❌ 聊天页面模型列表不包含自定义模型 '{mock_model_data['modelName']}'")
    except Exception as e:
        print(f"测试聊天页面模型列表失败: {str(e)}")
    
    # 6. 测试清理：删除测试模型
    print("\n6. 测试删除测试模型")
    try:
        # 获取模型ID
        response = requests.get(f'{base_url}/api/settings/models')
        result = response.json()
        test_model = next((m for m in result.get('models', []) if m['name'] == mock_model_data['modelName']), None)
        
        if test_model:
            model_id = test_model['id']
            response = requests.delete(f'{base_url}/api/settings/models/{model_id}')
            result = response.json()
            print(f"状态码: {response.status_code}")
            print(f"成功: {result.get('success')}")
        else:
            print("❌ 未找到测试模型，跳过删除")
    except Exception as e:
        print(f"删除模型失败: {str(e)}")
    
    # 7. 验证模型删除成功
    print("\n7. 验证模型删除成功")
    try:
        response = requests.get(f'{base_url}/api/settings/models')
        result = response.json()
        models = result.get('models', [])
        test_model = next((m for m in models if m['name'] == mock_model_data['modelName']), None)
        if not test_model:
            print(f"✅ 模型删除成功！")
        else:
            print(f"❌ 模型删除失败，模型仍存在")
    except Exception as e:
        print(f"验证模型删除失败: {str(e)}")

if __name__ == "__main__":
    test_custom_model_workflow()
