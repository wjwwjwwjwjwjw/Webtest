// 主题切换功能
document.addEventListener('DOMContentLoaded', function() {
    // 创建主题切换按钮
    const themeSwitch = document.createElement('div');
    themeSwitch.className = 'theme-switch';
    themeSwitch.innerHTML = '<i class="fas fa-moon"></i>';
    document.body.appendChild(themeSwitch);
    
    // 检查当前主题设置
    const isDarkMode = localStorage.getItem('darkMode') === 'true';
    if (isDarkMode) {
        document.body.classList.add('dark-mode');
        themeSwitch.innerHTML = '<i class="fas fa-sun"></i>';
    }
    
    // 监听点击事件
    themeSwitch.addEventListener('click', function() {
        const isDark = document.body.classList.toggle('dark-mode');
        localStorage.setItem('darkMode', isDark);
        
        // 更新图标
        themeSwitch.innerHTML = isDark ? 
            '<i class="fas fa-sun"></i>' : 
            '<i class="fas fa-moon"></i>';
    });
}); 