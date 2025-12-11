// 通用工具函数

// 格式化日期时间
function formatDateTime(date = new Date()) {
    const year = date.getFullYear();
    const month = String(date.getMonth() + 1).padStart(2, '0');
    const day = String(date.getDate()).padStart(2, '0');
    const hours = String(date.getHours()).padStart(2, '0');
    const minutes = String(date.getMinutes()).padStart(2, '0');
    const seconds = String(date.getSeconds()).padStart(2, '0');
    
    return `${year}-${month}-${day} ${hours}:${minutes}:${seconds}`;
}

// 格式化时间
function formatTime(date = new Date()) {
    const hours = String(date.getHours()).padStart(2, '0');
    const minutes = String(date.getMinutes()).padStart(2, '0');
    
    return `${hours}:${minutes}`;
}

// 生成唯一ID
function generateId() {
    return Date.now().toString(36) + Math.random().toString(36).substr(2);
}

// 复制到剪贴板
async function copyToClipboard(text) {
    try {
        await navigator.clipboard.writeText(text);
        return true;
    } catch (err) {
        console.error('复制失败:', err);
        return false;
    }
}

// 显示消息提示
function showToast(message, type = 'info', duration = 3000) {
    // 创建toast元素
    const toast = document.createElement('div');
    toast.className = `toast toast-${type}`;
    toast.innerHTML = `
        <div class="toast-content">
            <i class="fas fa-${type === 'success' ? 'check-circle' : type === 'error' ? 'exclamation-circle' : 'info-circle'}"></i>
            <span>${message}</span>
        </div>
    `;
    
    // 添加到页面
    document.body.appendChild(toast);
    
    // 显示动画
    setTimeout(() => {
        toast.classList.add('show');
    }, 100);
    
    // 自动隐藏
    setTimeout(() => {
        toast.classList.remove('show');
        setTimeout(() => {
            document.body.removeChild(toast);
        }, 300);
    }, duration);
}

// 验证表单
function validateForm(form) {
    const inputs = form.querySelectorAll('input[required], select[required], textarea[required]');
    let isValid = true;
    
    inputs.forEach(input => {
        if (!input.value.trim()) {
            isValid = false;
            input.classList.add('error');
            input.addEventListener('input', () => input.classList.remove('error'), { once: true });
        }
    });
    
    return isValid;
}

// 防抖函数
function debounce(func, delay) {
    let timeoutId;
    return function(...args) {
        clearTimeout(timeoutId);
        timeoutId = setTimeout(() => func.apply(this, args), delay);
    };
}

// 节流函数
function throttle(func, limit) {
    let inThrottle;
    return function(...args) {
        if (!inThrottle) {
            func.apply(this, args);
            inThrottle = true;
            setTimeout(() => inThrottle = false, limit);
        }
    };
}

// 滚动到元素
function scrollToElement(element, offset = 0) {
    const elementPosition = element.getBoundingClientRect().top + window.pageYOffset;
    const offsetPosition = elementPosition - offset;
    
    window.scrollTo({
        top: offsetPosition,
        behavior: 'smooth'
    });
}

// 检查是否为空对象
function isEmptyObject(obj) {
    return Object.keys(obj).length === 0 && obj.constructor === Object;
}

// 深拷贝对象
function deepClone(obj) {
    if (obj === null || typeof obj !== 'object') return obj;
    if (obj instanceof Date) return new Date(obj.getTime());
    if (obj instanceof Array) return obj.map(item => deepClone(item));
    if (typeof obj === 'object') {
        const clonedObj = {};
        for (const key in obj) {
            if (obj.hasOwnProperty(key)) {
                clonedObj[key] = deepClone(obj[key]);
            }
        }
        return clonedObj;
    }
}

// 获取URL参数
function getUrlParams() {
    const params = {};
    const urlParams = new URLSearchParams(window.location.search);
    for (const [key, value] of urlParams) {
        params[key] = value;
    }
    return params;
}

// 设置URL参数
function setUrlParams(params) {
    const url = new URL(window.location.href);
    const urlParams = new URLSearchParams(url.search);
    
    Object.keys(params).forEach(key => {
        if (params[key]) {
            urlParams.set(key, params[key]);
        } else {
            urlParams.delete(key);
        }
    });
    
    url.search = urlParams.toString();
    window.history.pushState({}, '', url);
}

// 清除URL参数
function clearUrlParams() {
    const url = new URL(window.location.href);
    url.search = '';
    window.history.pushState({}, '', url);
}

// 检测是否为移动设备
function isMobile() {
    return /Android|webOS|iPhone|iPad|iPod|BlackBerry|IEMobile|Opera Mini/i.test(navigator.userAgent);
}

// 检测是否支持触摸事件
function isTouchDevice() {
    return 'ontouchstart' in window || navigator.maxTouchPoints > 0 || navigator.msMaxTouchPoints > 0;
}

// 计算阅读时间
function calculateReadingTime(text, wordsPerMinute = 200) {
    const words = text.trim().split(/\s+/).length;
    const minutes = Math.ceil(words / wordsPerMinute);
    return minutes;
}

// 截断文本
function truncateText(text, maxLength = 100, suffix = '...') {
    if (text.length <= maxLength) return text;
    return text.substring(0, maxLength - suffix.length) + suffix;
}

// 高亮文本中的关键词
function highlightText(text, keyword) {
    if (!keyword) return text;
    const regex = new RegExp(`(${keyword})`, 'gi');
    return text.replace(regex, '<mark>$1</mark>');
}

// 滚动到页面顶部
function scrollToTop() {
    window.scrollTo({
        top: 0,
        behavior: 'smooth'
    });
}

// 滚动到页面底部
function scrollToBottom() {
    window.scrollTo({
        top: document.body.scrollHeight,
        behavior: 'smooth'
    });
}

// 添加加载状态
function addLoading(element) {
    element.classList.add('loading');
    const spinner = document.createElement('div');
    spinner.className = 'spinner';
    element.appendChild(spinner);
}

// 移除加载状态
function removeLoading(element) {
    element.classList.remove('loading');
    const spinner = element.querySelector('.spinner');
    if (spinner) {
        spinner.remove();
    }
}

// 动态加载脚本
function loadScript(url, callback) {
    const script = document.createElement('script');
    script.src = url;
    script.onload = callback;
    script.onerror = () => console.error(`Failed to load script: ${url}`);
    document.head.appendChild(script);
}

// 动态加载样式
function loadStyle(url) {
    const link = document.createElement('link');
    link.rel = 'stylesheet';
    link.href = url;
    document.head.appendChild(link);
}

// 获取浏览器存储数据
function getStorage(key, defaultValue = null) {
    try {
        const item = localStorage.getItem(key);
        return item ? JSON.parse(item) : defaultValue;
    } catch (error) {
        console.error('Error getting storage item:', error);
        return defaultValue;
    }
}

// 设置浏览器存储数据
function setStorage(key, value) {
    try {
        localStorage.setItem(key, JSON.stringify(value));
        return true;
    } catch (error) {
        console.error('Error setting storage item:', error);
        return false;
    }
}

// 删除浏览器存储数据
function removeStorage(key) {
    try {
        localStorage.removeItem(key);
        return true;
    } catch (error) {
        console.error('Error removing storage item:', error);
        return false;
    }
}

// 清空浏览器存储数据
function clearStorage() {
    try {
        localStorage.clear();
        return true;
    } catch (error) {
        console.error('Error clearing storage:', error);
        return false;
    }
}

// 获取主题
function getTheme() {
    return localStorage.getItem('theme') || (window.matchMedia('(prefers-color-scheme: dark)').matches ? 'dark' : 'light');
}

// 设置主题
function setTheme(theme) {
    if (theme === 'dark') {
        document.body.classList.add('dark-theme');
    } else {
        document.body.classList.remove('dark-theme');
    }
    localStorage.setItem('theme', theme);
}

// 切换主题
function toggleTheme() {
    const currentTheme = getTheme();
    const newTheme = currentTheme === 'dark' ? 'light' : 'dark';
    setTheme(newTheme);
    return newTheme;
}

// 初始化主题
function initTheme() {
    const theme = getTheme();
    setTheme(theme);
}

// 导出工具函数（如果支持模块）
if (typeof module !== 'undefined' && module.exports) {
    module.exports = {
        formatDateTime,
        formatTime,
        generateId,
        copyToClipboard,
        showToast,
        validateForm,
        debounce,
        throttle,
        scrollToElement,
        isEmptyObject,
        deepClone,
        getUrlParams,
        setUrlParams,
        clearUrlParams,
        isMobile,
        isTouchDevice,
        calculateReadingTime,
        truncateText,
        highlightText,
        scrollToTop,
        scrollToBottom,
        addLoading,
        removeLoading,
        loadScript,
        loadStyle,
        getStorage,
        setStorage,
        removeStorage,
        clearStorage,
        getTheme,
        setTheme,
        toggleTheme,
        initTheme
    };
}