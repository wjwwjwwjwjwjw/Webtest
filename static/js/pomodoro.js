class PomodoroTimer {
  constructor() {
    // 时间配置（分钟）
    this.pomodoroTime = 25;
    this.shortBreakTime = 5;
    this.longBreakTime = 15;
    
    // 状态
    this.currentMode = 'pomodoro';
    this.isRunning = false;
    this.timeLeft = this.pomodoroTime * 60; // 秒
    this.interval = null;
    this.completedPomodoros = 0;
    this.totalFocusTime = 0;
    this.currentTask = '';
    
    // DOM元素
    this.minutesDisplay = document.getElementById('timer-minutes');
    this.secondsDisplay = document.getElementById('timer-seconds');
    this.startButton = document.getElementById('timer-start');
    this.pauseButton = document.getElementById('timer-pause');
    this.resetButton = document.getElementById('timer-reset');
    this.pomodoroButton = document.getElementById('pomodoro-mode');
    this.shortBreakButton = document.getElementById('short-break-mode');
    this.longBreakButton = document.getElementById('long-break-mode');
    this.taskInput = document.getElementById('task-input');
    this.saveTaskButton = document.getElementById('save-task');
    this.focusCountDisplay = document.getElementById('focus-count');
    this.focusTimeDisplay = document.getElementById('focus-time');
    this.timerPathRemaining = document.querySelector('.timer-path-remaining');
    
    // 初始化
    this.init();
  }
  
  init() {
    // 加载保存的数据
    this.loadStats();
    
    // 计算圆形进度条周长
    const pathLength = 2 * Math.PI * 45;
    this.timerPathRemaining.style.strokeDasharray = `${pathLength} ${pathLength}`;
    this.timerPathRemaining.style.strokeDashoffset = '0';
    this.totalPathLength = pathLength;
    
    // 更新显示
    this.updateTimerDisplay();
    this.updateStats();
    
    // 绑定事件处理器
    this.bindEvents();
    
    // 加载上次保存的任务
    this.loadTask();
  }
  
  bindEvents() {
    // 开始按钮
    this.startButton.addEventListener('click', () => this.startTimer());
    
    // 暂停按钮
    this.pauseButton.addEventListener('click', () => this.pauseTimer());
    
    // 重置按钮
    this.resetButton.addEventListener('click', () => this.resetTimer());
    
    // 模式按钮
    this.pomodoroButton.addEventListener('click', () => this.setMode('pomodoro'));
    this.shortBreakButton.addEventListener('click', () => this.setMode('shortBreak'));
    this.longBreakButton.addEventListener('click', () => this.setMode('longBreak'));
    
    // 保存任务按钮
    this.saveTaskButton.addEventListener('click', () => this.saveTask());
  }
  
  // 设置模式
  setMode(mode) {
    // 如果计时器正在运行，先暂停
    if (this.isRunning) {
      this.pauseTimer();
    }
    
    // 设置当前模式
    this.currentMode = mode;
    
    // 更新模式按钮状态
    this.pomodoroButton.classList.toggle('mode-active', mode === 'pomodoro');
    this.shortBreakButton.classList.toggle('mode-active', mode === 'shortBreak');
    this.longBreakButton.classList.toggle('mode-active', mode === 'longBreak');
    
    // 根据模式设置时间
    switch (mode) {
      case 'pomodoro':
        this.timeLeft = this.pomodoroTime * 60;
        this.timerPathRemaining.style.stroke = '#e74c3c';
        break;
      case 'shortBreak':
        this.timeLeft = this.shortBreakTime * 60;
        this.timerPathRemaining.style.stroke = '#3498db';
        break;
      case 'longBreak':
        this.timeLeft = this.longBreakTime * 60;
        this.timerPathRemaining.style.stroke = '#2ecc71';
        break;
    }
    
    // 更新显示
    this.updateTimerDisplay();
    this.updateProgressCircle();
  }
  
  // 开始计时
  startTimer() {
    if (this.isRunning) return;
    
    this.isRunning = true;
    
    // 切换按钮显示
    this.startButton.style.display = 'none';
    this.pauseButton.style.display = 'flex';
    
    // 设置定时器
    this.interval = setInterval(() => {
      this.timeLeft--;
      
      // 更新显示
      this.updateTimerDisplay();
      this.updateProgressCircle();
      
      // 检查是否结束
      if (this.timeLeft <= 0) {
        this.timerComplete();
      }
    }, 1000);
  }
  
  // 暂停计时
  pauseTimer() {
    if (!this.isRunning) return;
    
    this.isRunning = false;
    
    // 切换按钮显示
    this.startButton.style.display = 'flex';
    this.pauseButton.style.display = 'none';
    
    // 清除定时器
    clearInterval(this.interval);
  }
  
  // 重置计时器
  resetTimer() {
    // 暂停计时器
    if (this.isRunning) {
      this.pauseTimer();
    }
    
    // 根据当前模式重置时间
    switch (this.currentMode) {
      case 'pomodoro':
        this.timeLeft = this.pomodoroTime * 60;
        break;
      case 'shortBreak':
        this.timeLeft = this.shortBreakTime * 60;
        break;
      case 'longBreak':
        this.timeLeft = this.longBreakTime * 60;
        break;
    }
    
    // 更新显示
    this.updateTimerDisplay();
    this.updateProgressCircle();
  }
  
  // 更新计时器显示
  updateTimerDisplay() {
    const minutes = Math.floor(this.timeLeft / 60);
    const seconds = this.timeLeft % 60;
    
    this.minutesDisplay.textContent = minutes.toString().padStart(2, '0');
    this.secondsDisplay.textContent = seconds.toString().padStart(2, '0');
  }
  
  // 更新圆形进度条
  updateProgressCircle() {
    let totalSeconds;
    switch (this.currentMode) {
      case 'pomodoro':
        totalSeconds = this.pomodoroTime * 60;
        break;
      case 'shortBreak':
        totalSeconds = this.shortBreakTime * 60;
        break;
      case 'longBreak':
        totalSeconds = this.longBreakTime * 60;
        break;
    }
    
    const fraction = this.timeLeft / totalSeconds;
    const dashoffset = this.totalPathLength * (1 - fraction);
    this.timerPathRemaining.style.strokeDashoffset = dashoffset;
  }
  
  // 计时完成
  timerComplete() {
    // 清除定时器
    clearInterval(this.interval);
    this.isRunning = false;
    
    // 切换按钮显示
    this.startButton.style.display = 'flex';
    this.pauseButton.style.display = 'none';
    
    // 播放提示音
    this.playAlarm();
    
    // 显示通知
    this.showNotification();
    
    // 如果是专注时间完成
    if (this.currentMode === 'pomodoro') {
      // 记录完成的番茄钟
      this.completedPomodoros++;
      this.totalFocusTime += this.pomodoroTime;
      
      // 更新统计数据
      this.updateStats();
      
      // 保存统计数据
      this.saveStats();
      
      // 自动切换到休息模式
      if (this.completedPomodoros % 4 === 0) {
        // 每四个番茄钟后进行长休息
        this.setMode('longBreak');
      } else {
        // 否则进行短休息
        this.setMode('shortBreak');
      }
    } else {
      // 如果是休息完成，自动切换到专注模式
      this.setMode('pomodoro');
    }
  }
  
  // 播放提示音
  playAlarm() {
    const audio = new Audio('/static/sound/pomodoro-complete.mp3');
    audio.play();
  }
  
  // 显示通知
  showNotification() {
    if ('Notification' in window && Notification.permission === 'granted') {
      let title, body;
      
      if (this.currentMode === 'pomodoro') {
        title = '专注时间结束！';
        body = '现在是休息时间。';
      } else {
        title = '休息时间结束！';
        body = '准备开始新的专注时间。';
      }
      
      new Notification(title, {
        body: body,
        icon: '/static/img/tomato.png'
      });
    }
  }
  
  // 加载统计数据
  loadStats() {
    const today = new Date().toDateString();
    const stats = JSON.parse(localStorage.getItem('pomodoroStats') || '{}');
    
    if (stats[today]) {
      this.completedPomodoros = stats[today].count || 0;
      this.totalFocusTime = stats[today].time || 0;
    } else {
      this.completedPomodoros = 0;
      this.totalFocusTime = 0;
    }
  }
  
  // 保存统计数据
  saveStats() {
    const today = new Date().toDateString();
    const stats = JSON.parse(localStorage.getItem('pomodoroStats') || '{}');
    
    stats[today] = {
      count: this.completedPomodoros,
      time: this.totalFocusTime
    };
    
    localStorage.setItem('pomodoroStats', JSON.stringify(stats));
  }
  
  // 更新统计显示
  updateStats() {
    this.focusCountDisplay.textContent = this.completedPomodoros;
    this.focusTimeDisplay.textContent = this.totalFocusTime;
  }
  
  // 保存任务
  saveTask() {
    this.currentTask = this.taskInput.value.trim();
    
    if (this.currentTask) {
      // 保存到本地存储
      localStorage.setItem('currentTask', this.currentTask);
      
      // 显示保存成功提示
      alert('任务已保存');
    }
  }
  
  // 加载任务
  loadTask() {
    const savedTask = localStorage.getItem('currentTask');
    if (savedTask) {
      this.taskInput.value = savedTask;
      this.currentTask = savedTask;
    }
  }
  
  // 请求通知权限
  requestNotificationPermission() {
    if ('Notification' in window && Notification.permission !== 'granted') {
      Notification.requestPermission();
    }
  }
}

// 页面加载完成后初始化番茄计时器
document.addEventListener('DOMContentLoaded', () => {
  const timer = new PomodoroTimer();
  timer.requestNotificationPermission();
  
  // 添加可爱的番茄动画
  const timerDisplay = document.querySelector('.timer-display');
  const tomatoAnimation = document.createElement('div');
  tomatoAnimation.className = 'pomodoro-animation';
  tomatoAnimation.innerHTML = `
    <div class="tomato">
      <div class="tomato-face">
        <div class="tomato-eye"></div>
        <div class="tomato-eye"></div>
      </div>
      <div class="tomato-smile"></div>
    </div>
  `;
  
  timerDisplay.prepend(tomatoAnimation);
}); 