# AI六爻解卦系统

基于AI技术的传统易学六爻解卦系统，提供专业的六爻分析和解卦服务。

## 功能特性

### 核心功能
- 🧠 **AI六爻解卦**：基于AI技术的六爻分析，提供专业的解卦结果
- 🔍 **用神判断**：自动判断卦象中的用神
- 📊 **卦理分析**：详细的用神卦理和动爻卦理分析
- 📈 **数字量化**：用神和动爻的强弱指数分析
- 💡 **综合解读**：基于卦象信息的综合解读

### 用户系统
- 🔐 **用户认证**：注册、登录、登出功能
- 📝 **个人记录**：保存个人解卦记录
- ⚙️ **自定义模型**：支持添加自定义AI模型

### 其他功能
- 💬 **聊天咨询**：基于解卦结果的进一步咨询
- 🎨 **主题切换**：支持明暗主题切换
- 📱 **响应式设计**：适配不同设备

## 技术栈

### 后端
- **Flask**：Web框架
- **SQLAlchemy**：ORM数据库操作
- **Flask-Login**：用户认证管理
- **bcrypt**：密码哈希加密

### 前端
- **HTML/CSS/JavaScript**：基础前端技术
- **Font Awesome**：图标库

### 数据库
- **SQLite**：开发环境数据库
- **MySQL**：支持生产环境数据库

### AI服务
- **OpenAI API**：默认AI服务
- **自定义API**：支持添加自定义AI模型

## 快速开始

### 环境要求
- Python 3.8+
- pip

### 安装步骤

1. **克隆仓库**
   ```bash
   git clone <repository-url>
   cd AI_LiuYao_web
   ```

2. **创建虚拟环境**
   ```bash
   python -m venv .venv
   ```

3. **激活虚拟环境**
   - Windows: `.\.venv\Scripts\activate`
   - Linux/Mac: `source .venv/bin/activate`

4. **安装依赖**
   ```bash
   pip install -r requirements.txt
   ```

5. **配置环境**
   - 复制 `.env.example` 为 `.env`
   - 编辑 `.env` 文件，配置数据库和其他参数

6. **初始化数据库**
   ```bash
   python -c "from app import app; from models import db; with app.app_context(): db.create_all()"
   ```

7. **启动应用**
   ```bash
   python app.py
   ```

8. **访问应用**
   - 打开浏览器访问 `http://127.0.0.1:5000`

## 项目结构

```
AI_LiuYao_web/
├── app.py                 # 主应用文件
├── auth.py                # 用户认证模块
├── hexagram.py            # 六爻解卦模块
├── models_manager.py      # 模型管理模块
├── models.py              # 数据库模型
├── prompt.py              # AI提示词模块
├── captcha.py             # 验证码生成模块
├── api.py                 # API调用模块（敏感文件，不上传）
├── config.py              # 配置文件
├── requirements.txt       # 依赖列表
├── templates/             # HTML模板
│   ├── base.html          # 基础模板
│   ├── index.html         # 首页
│   ├── result.html        # 解卦结果页
│   ├── history.html       # 历史记录页
│   ├── settings.html      # 设置页面
│   └── auth/              # 认证相关模板
├── static/                # 静态资源
│   ├── css/               # CSS文件
│   ├── js/                # JavaScript文件
│   └── images/            # 图片资源
└── README.md              # 项目说明文档
```

## 配置说明

### 数据库配置
- **SQLite**（默认）：`SQLALCHEMY_DATABASE_URI = 'sqlite:///app.db'`
- **MySQL**：`SQLALCHEMY_DATABASE_URI = 'mysql://username:password@localhost/dbname'`

### 安全配置
- `SECRET_KEY`：用于加密会话数据
- `BCRYPT_LOG_ROUNDS`：bcrypt哈希轮数

### AI服务配置
- 支持OpenAI API和自定义AI模型
- 在设置页面添加自定义模型

## 使用指南

1. **注册/登录**：首次使用需要注册账号并登录
2. **输入信息**：在首页输入问题和卦象信息
3. **选择模型**：选择使用的AI模型
4. **开始解卦**：点击解卦按钮，等待AI分析结果
5. **查看结果**：查看解卦结果，包括用神判断、卦理分析等
6. **聊天咨询**：基于解卦结果进行进一步咨询
7. **历史记录**：查看历史解卦记录
8. **设置**：添加自定义AI模型

## 注意事项

1. **敏感文件**：`api.py` 文件包含API密钥等敏感信息，请勿上传至版本控制系统
2. **数据库安全**：生产环境请使用强密码，并定期备份数据库
3. **API密钥保护**：请勿泄露API密钥
4. **环境变量**：敏感配置请通过环境变量设置

## 开发说明

### 运行开发服务器
```bash
python app.py
```

### 代码规范
- 遵循PEP 8代码规范
- 使用Flask蓝图进行模块化开发
- 使用SQLAlchemy ORM操作数据库

### 添加新功能
1. 创建新的蓝图或模块
2. 在 `app.py` 中注册蓝图
3. 添加路由和视图函数
4. 创建对应的模板文件
5. 更新数据库模型（如果需要）

## 许可证

MIT License

## 贡献

欢迎贡献代码和提出建议！

## 联系方式

如有问题或建议，请通过以下方式联系：
- Email: [zzz1110002023@163.com]
- GitHub Issues: [repository-url]/issues

---

© 2025 AI六爻解卦系统
