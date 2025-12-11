// API调用封装

const api = {
    // 基础URL
    baseUrl: '/api',
    
    // 通用请求方法
    async request(endpoint, method = 'GET', data = null, headers = {}) {
        const url = `${this.baseUrl}${endpoint}`;
        
        const options = {
            method,
            headers: {
                'Content-Type': 'application/json',
                ...headers
            }
        };
        
        if (data && (method === 'POST' || method === 'PUT' || method === 'PATCH')) {
            options.body = JSON.stringify(data);
        }
        
        try {
            const response = await fetch(url, options);
            const result = await response.json();
            
            if (!response.ok) {
                throw new Error(result.error || `请求失败: ${response.status}`);
            }
            
            return result;
        } catch (error) {
            console.error(`API请求错误 (${url}):`, error);
            throw error;
        }
    },
    
    // GET请求
    async get(endpoint, headers = {}) {
        return this.request(endpoint, 'GET', null, headers);
    },
    
    // POST请求
    async post(endpoint, data = null, headers = {}) {
        return this.request(endpoint, 'POST', data, headers);
    },
    
    // PUT请求
    async put(endpoint, data = null, headers = {}) {
        return this.request(endpoint, 'PUT', data, headers);
    },
    
    // DELETE请求
    async delete(endpoint, headers = {}) {
        return this.request(endpoint, 'DELETE', null, headers);
    },
    
    // 六爻分析
    async analyze(data) {
        return this.post('/analyze', data);
    },
    
    // 聊天功能
    async chat(data) {
        return this.post('/chat', data);
    },
    
    // 获取历史记录
    async getHistory() {
        return this.get('/history');
    },
    
    // 删除历史记录
    async deleteHistory(recordId) {
        return this.delete(`/history/${recordId}`);
    },
    
    // 健康检查
    async health() {
        return this.get('/health');
    },
    
    // 获取模型列表
    async getModels() {
        return this.get('/models');
    }
};

// 导出API对象
if (typeof module !== 'undefined' && module.exports) {
    module.exports = api;
}