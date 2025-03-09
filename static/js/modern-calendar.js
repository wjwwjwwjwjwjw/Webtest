// 现代日历功能实现
class ModernCalendar {
  constructor() {
    this.currentDate = new Date();
    this.selectedDate = new Date();
    this.view = 'month';
    this.todos = [];
    this.weatherApiKey = '您的API密钥'; // 需要替换为实际的API密钥
    
    // DOM元素
    this.monthDisplay = document.getElementById('month-display');
    this.daysContainer = document.getElementById('days-container');
    this.todoList = document.getElementById('todo-list');
    this.todoForm = document.getElementById('todo-form');
    this.locationDisplay = document.getElementById('current-location');
    this.weatherDisplay = document.getElementById('current-weather');
    this.weatherIcon = document.getElementById('weather-icon');
    
    // 初始化
    this.init();
  }
  
  // 初始化方法
  init() {
    // 绑定事件处理器
    this.bindEvents();
    
    // 加载待办事项
    this.loadTodos();
    
    // 获取位置和天气
    this.getLocationAndWeather();
    
    // 渲染日历
    this.renderCalendar();
    
    // 渲染待办事项
    this.renderTodos();
    
    // 注册通知
    this.registerNotifications();
  }
  
  // 设置提醒
  setReminder(todo) {
    if (!todo.time || todo.remind === 0) return;
    
    const [hours, minutes] = todo.time.split(':').map(Number);
    const reminderDate = new Date(
      this.selectedDate.getFullYear(),
      this.selectedDate.getMonth(),
      this.selectedDate.getDate(),
      hours,
      minutes - todo.remind
    );
    
    // 如果提醒时间已经过去，则不设置提醒
    if (reminderDate < new Date()) return;
    
    // 计算提醒时间与当前时间的时间差（毫秒）
    const timeUntilReminder = reminderDate.getTime() - new Date().getTime();
    
    // 设置定时器
    setTimeout(() => {
      // 显示浏览器通知
      if ('Notification' in window && Notification.permission === 'granted') {
        new Notification('待办事项提醒', {
          body: todo.title,
          icon: '/static/img/calendar-icon.png'
        });
      }
      
      // 播放提醒音效
      const audio = new Audio('/static/sound/notification.mp3');
      audio.play();
    }, timeUntilReminder);
  }
}

// 初始化日历
document.addEventListener('DOMContentLoaded', () => {
  const calendar = new ModernCalendar();
  
  // 绑定全局函数
  window.prevMonth = () => calendar.prevMonth();
  window.nextMonth = () => calendar.nextMonth();
  window.goToToday = () => calendar.goToToday();
  window.switchView = (viewMode) => calendar.switchView(viewMode);
}); 