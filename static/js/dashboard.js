/**
 * 班级成绩管理系统 - 仪表盘脚本
 * 用于首页数据可视化和交互效果
 */

document.addEventListener('DOMContentLoaded', function() {
    // 初始化图表
    initCharts();
    
    // 初始化数据卡片动画
    initStatCards();
    
    // 初始化日历视图
    initCalendarView();
});

/**
 * 初始化统计卡片动画效果
 */
function initStatCards() {
    const statCards = document.querySelectorAll('.stat-card');
    
    statCards.forEach((card, index) => {
        // 添加延迟动画效果
        setTimeout(() => {
            card.classList.add('show');
        }, 100 * index);
        
        // 添加鼠标悬停效果
        card.addEventListener('mouseenter', function() {
            this.classList.add('hover');
        });
        
        card.addEventListener('mouseleave', function() {
            this.classList.remove('hover');
        });
    });
}

/**
 * 初始化所有图表
 */
function initCharts() {
    // 初始化成绩分布图表
    initGradeDistributionChart();
    
    // 初始化学年成绩趋势图
    initGradeTrendChart();
    
    // 初始化课程类型分布图
    initCourseTypeChart();
}

/**
 * 初始化成绩分布图表
 */
function initGradeDistributionChart() {
    const ctx = document.getElementById('gradeDistributionChart');
    
    if (!ctx) return;
    
    // 模拟数据 - 实际应用中应从后端获取
    const data = {
        labels: ['优秀(90-100)', '良好(80-89)', '中等(70-79)', '及格(60-69)', '不及格(<60)'],
        datasets: [{
            label: '学生人数',
            data: [15, 25, 12, 8, 2],
            backgroundColor: [
                'rgba(76, 201, 240, 0.7)',
                'rgba(67, 97, 238, 0.7)',
                'rgba(58, 12, 163, 0.7)',
                'rgba(114, 9, 183, 0.7)',
                'rgba(247, 37, 133, 0.7)'
            ],
            borderColor: [
                'rgba(76, 201, 240, 1)',
                'rgba(67, 97, 238, 1)',
                'rgba(58, 12, 163, 1)',
                'rgba(114, 9, 183, 1)',
                'rgba(247, 37, 133, 1)'
            ],
            borderWidth: 1
        }]
    };
    
    new Chart(ctx, {
        type: 'doughnut',
        data: data,
        options: {
            responsive: true,
            maintainAspectRatio: false,
            plugins: {
                legend: {
                    position: 'right',
                }
            },
            cutout: '70%',
            animation: {
                animateScale: true,
                animateRotate: true
            }
        }
    });
}

/**
 * 初始化学年成绩趋势图
 */
function initGradeTrendChart() {
    const ctx = document.getElementById('gradeTrendChart');
    
    if (!ctx) return;
    
    // 模拟数据 - 实际应用中应从后端获取
    const data = {
        labels: ['大一上学期', '大一下学期', '大二上学期', '大二下学期', '大三上学期', '大三下学期'],
        datasets: [{
            label: '平均分',
            data: [82, 85, 83, 87, 89, 91],
            borderColor: 'rgba(67, 97, 238, 1)',
            backgroundColor: 'rgba(67, 97, 238, 0.1)',
            tension: 0.4,
            fill: true
        }, {
            label: '最高分',
            data: [95, 97, 94, 98, 99, 100],
            borderColor: 'rgba(76, 201, 240, 1)',
            backgroundColor: 'rgba(76, 201, 240, 0.0)',
            borderDash: [5, 5],
            tension: 0.4,
            fill: false
        }]
    };
    
    new Chart(ctx, {
        type: 'line',
        data: data,
        options: {
            responsive: true,
            maintainAspectRatio: false,
            plugins: {
                legend: {
                    position: 'top',
                }
            },
            scales: {
                y: {
                    min: 60,
                    max: 100
                }
            },
            animation: {
                duration: 2000,
                easing: 'easeOutQuart'
            }
        }
    });
}

/**
 * 初始化课程类型分布图
 */
function initCourseTypeChart() {
    const ctx = document.getElementById('courseTypeChart');
    
    if (!ctx) return;
    
    // 模拟数据 - 实际应用中应从后端获取
    const data = {
        labels: ['必修课', '选修课', '实验课', '实践课'],
        datasets: [{
            label: '学分占比',
            data: [65, 20, 10, 5],
            backgroundColor: [
                'rgba(67, 97, 238, 0.7)',
                'rgba(76, 201, 240, 0.7)',
                'rgba(58, 12, 163, 0.7)',
                'rgba(114, 9, 183, 0.7)'
            ],
            borderWidth: 0
        }]
    };
    
    new Chart(ctx, {
        type: 'bar',
        data: data,
        options: {
            responsive: true,
            maintainAspectRatio: false,
            plugins: {
                legend: {
                    display: false
                }
            },
            scales: {
                y: {
                    beginAtZero: true,
                    title: {
                        display: true,
                        text: '学分'
                    }
                },
                x: {
                    title: {
                        display: true,
                        text: '课程类型'
                    }
                }
            },
            animation: {
                delay: function(context) {
                    return context.dataIndex * 100;
                }
            }
        }
    });
}

/**
 * 初始化日历视图
 */
function initCalendarView() {
    const calendarEl = document.getElementById('calendarView');
    
    if (!calendarEl) return;
    
    // 模拟数据 - 实际应用中应从后端获取
    const events = [
        {
            title: '期中考试',
            start: '2023-11-15',
            end: '2023-11-20',
            color: '#4361ee'
        },
        {
            title: '数学作业截止',
            start: '2023-11-10',
            color: '#f72585'
        },
        {
            title: '物理实验',
            start: '2023-11-05',
            color: '#4cc9f0'
        },
        {
            title: '班会',
            start: '2023-11-25',
            color: '#3f37c9'
        }
    ];
    
    // 如果有FullCalendar库，则初始化日历
    if (typeof FullCalendar !== 'undefined') {
        const calendar = new FullCalendar.Calendar(calendarEl, {
            initialView: 'dayGridMonth',
            headerToolbar: {
                left: 'prev,next today',
                center: 'title',
                right: 'dayGridMonth,timeGridWeek'
            },
            events: events,
            eventClick: function(info) {
                alert('事件: ' + info.event.title);
            },
            height: 350
        });
        
        calendar.render();
    } else {
        // 如果没有FullCalendar库，则显示简单的事件列表
        calendarEl.innerHTML = '<div class="p-3"><h5>近期事件</h5><ul class="list-group"></ul></div>';
        const eventList = calendarEl.querySelector('ul');
        
        events.forEach(event => {
            const li = document.createElement('li');
            li.className = 'list-group-item d-flex justify-content-between align-items-center';
            li.innerHTML = `
                ${event.title}
                <span class="badge" style="background-color: ${event.color}">${event.start}</span>
            `;
            eventList.appendChild(li);
        });
    }
}

/**
 * 更新在线用户数量
 */
function updateOnlineUsers() {
    const onlineUsersEl = document.getElementById('onlineUsers');
    
    if (!onlineUsersEl) return;
    
    // 模拟数据 - 实际应用中应从后端获取
    const onlineUsers = Math.floor(Math.random() * 20) + 10;
    onlineUsersEl.textContent = onlineUsers;
}

// 定期更新在线用户数量
setInterval(updateOnlineUsers, 5000);

/**
 * 班级成绩管理系统 - 首页功能
 * 包含iOS风格的日历、天气和专注时钟功能
 */

document.addEventListener('DOMContentLoaded', function() {
    // 初始化iOS风格日历
    initIOSCalendar();
    
    // 初始化iOS风格天气
    initIOSWeather();
    
    // 初始化番茄时钟
    initPomodoroTimer();
});

/**
 * 初始化iOS风格日历
 */
function initIOSCalendar() {
    const calendarContainer = document.getElementById('ios-calendar-days');
    const yearMonthDisplay = document.getElementById('calendar-year-month');
    const selectedDateInfoDisplay = document.getElementById('selected-date-info');
    
    // 视图切换按钮
    const monthViewBtn = document.getElementById('monthViewBtn');
    const weekViewBtn = document.getElementById('weekViewBtn');
    const lunarViewBtn = document.getElementById('lunarViewBtn');
    
    let currentDate = new Date();
    let currentView = 'month'; // 'month', 'week', 'lunar'
    let selectedDate = new Date();
    
    // 农历数据和节日数据
    const lunarMonths = ['正月', '二月', '三月', '四月', '五月', '六月', '七月', '八月', '九月', '十月', '冬月', '腊月'];
    const lunarDays = ['初一', '初二', '初三', '初四', '初五', '初六', '初七', '初八', '初九', '初十', 
                      '十一', '十二', '十三', '十四', '十五', '十六', '十七', '十八', '十九', '二十', 
                      '廿一', '廿二', '廿三', '廿四', '廿五', '廿六', '廿七', '廿八', '廿九', '三十'];
    const chineseZodiac = ['鼠', '牛', '虎', '兔', '龙', '蛇', '马', '羊', '猴', '鸡', '狗', '猪'];
    const heavenlyStems = ['甲', '乙', '丙', '丁', '戊', '己', '庚', '辛', '壬', '癸'];
    const earthlyBranches = ['子', '丑', '寅', '卯', '辰', '巳', '午', '未', '申', '酉', '戌', '亥'];
    
    // 中国传统节日（简化版）
    const chineseHolidays = [
        {name: '春节', month: 1, day: 1, lunar: true},
        {name: '元宵节', month: 1, day: 15, lunar: true},
        {name: '清明节', month: 4, day: 5, lunar: false},
        {name: '端午节', month: 5, day: 5, lunar: true},
        {name: '中秋节', month: 8, day: 15, lunar: true},
        {name: '重阳节', month: 9, day: 9, lunar: true},
        {name: '元旦', month: 1, day: 1, lunar: false},
        {name: '劳动节', month: 5, day: 1, lunar: false},
        {name: '国庆节', month: 10, day: 1, lunar: false},
        {name: '植树节', month: 3, day: 12, lunar: false},
        {name: '教师节', month: 9, day: 10, lunar: false},
        {name: '儿童节', month: 6, day: 1, lunar: false}
    ];
    
    // 初始化
    renderCalendar();
    setupEventListeners();
    
    // 设置事件监听器
    function setupEventListeners() {
        // 月视图按钮
        monthViewBtn.addEventListener('click', function() {
            if (currentView !== 'month') {
                currentView = 'month';
                updateViewButtons();
                renderCalendar();
            }
        });
        
        // 周视图按钮
        weekViewBtn.addEventListener('click', function() {
            if (currentView !== 'week') {
                currentView = 'week';
                updateViewButtons();
                renderCalendar();
            }
        });
        
        // 农历视图按钮
        lunarViewBtn.addEventListener('click', function() {
            if (currentView !== 'lunar') {
                currentView = 'lunar';
                updateViewButtons();
                renderCalendar();
            }
        });
        
        // 添加左右滑动手势支持
        let touchStartX = 0;
        let touchEndX = 0;
        
        const calendarCard = document.querySelector('.ios-calendar-card');
        calendarCard.addEventListener('touchstart', function(e) {
            touchStartX = e.touches[0].clientX;
        });
        
        calendarCard.addEventListener('touchend', function(e) {
            touchEndX = e.changedTouches[0].clientX;
            handleSwipe();
        });
        
        function handleSwipe() {
            if (touchEndX < touchStartX - 50) {
                // 向左滑动 - 下一个月/周
                if (currentView === 'month') {
                    currentDate.setMonth(currentDate.getMonth() + 1);
                } else if (currentView === 'week') {
                    currentDate.setDate(currentDate.getDate() + 7);
                } else if (currentView === 'lunar') {
                    currentDate.setMonth(currentDate.getMonth() + 1);
                }
                renderCalendar();
            } else if (touchEndX > touchStartX + 50) {
                // 向右滑动 - 上一个月/周
                if (currentView === 'month') {
                    currentDate.setMonth(currentDate.getMonth() - 1);
                } else if (currentView === 'week') {
                    currentDate.setDate(currentDate.getDate() - 7);
                } else if (currentView === 'lunar') {
                    currentDate.setMonth(currentDate.getMonth() - 1);
                }
                renderCalendar();
            }
        }
    }
    
    // 更新视图按钮的状态
    function updateViewButtons() {
        monthViewBtn.classList.remove('active');
        weekViewBtn.classList.remove('active');
        lunarViewBtn.classList.remove('active');
        
        if (currentView === 'month') {
            monthViewBtn.classList.add('active');
        } else if (currentView === 'week') {
            weekViewBtn.classList.add('active');
        } else if (currentView === 'lunar') {
            lunarViewBtn.classList.add('active');
        }
    }
    
    // 渲染日历
    function renderCalendar() {
        calendarContainer.innerHTML = '';
        
        if (currentView === 'month') {
            renderMonthView();
        } else if (currentView === 'week') {
            renderWeekView();
        } else if (currentView === 'lunar') {
            renderLunarView();
        }
        
        // 更新年月显示
        yearMonthDisplay.textContent = `${currentDate.getFullYear()} / ${currentDate.getMonth() + 1}`;
        
        // 更新所选日期信息
        updateSelectedDateInfo(selectedDate);
        
        // 更新假日倒计时
        updateHolidayCountdown();
    }
    
    // 渲染月视图
    function renderMonthView() {
        const year = currentDate.getFullYear();
        const month = currentDate.getMonth();
        
        // 获取当前月的第一天
        const firstDayOfMonth = new Date(year, month, 1);
        
        // 获取当前月的最后一天
        const lastDayOfMonth = new Date(year, month + 1, 0);
        
        // 获取当前月第一天是星期几 (0-6)
        const firstDayOfWeek = firstDayOfMonth.getDay();
        
        // 获取当前月的总天数
        const daysInMonth = lastDayOfMonth.getDate();
        
        // 获取上个月的最后几天
        const prevMonthLastDay = new Date(year, month, 0).getDate();
        
        // 计算日历表格中的总单元格数 (6行 * 7列)
        const totalCells = 6 * 7;
        
        // 填充日历表格
        for (let i = 0; i < totalCells; i++) {
            let day;
            let cellDate;
            let className = 'calendar-day-wrapper';
            let lunarText = '';
            let holiday = '';
            
            // 上个月的最后几天
            if (i < firstDayOfWeek) {
                day = prevMonthLastDay - firstDayOfWeek + i + 1;
                cellDate = new Date(year, month - 1, day);
                className += ' other-month';
                lunarText = getLunarDay(cellDate);
            }
            // 当前月的天数
            else if (i < firstDayOfWeek + daysInMonth) {
                day = i - firstDayOfWeek + 1;
                cellDate = new Date(year, month, day);
                lunarText = getLunarDay(cellDate);
                
                // 检查是否为今天
                const today = new Date();
                if (day === today.getDate() && month === today.getMonth() && year === today.getFullYear()) {
                    className += ' today';
                }
                
                // 检查是否为所选日期
                if (day === selectedDate.getDate() && month === selectedDate.getMonth() && year === selectedDate.getFullYear()) {
                    className += ' selected';
                }
                
                // 检查是否为假日
                holiday = getHoliday(cellDate);
            }
            // 下个月的前几天
            else {
                day = i - firstDayOfWeek - daysInMonth + 1;
                cellDate = new Date(year, month + 1, day);
                className += ' other-month';
                lunarText = getLunarDay(cellDate);
            }
            
            // 创建并添加日历单元格
            addCalendarDay(day, className, lunarText, holiday, cellDate);
        }
    }
    
    // 渲染周视图
    function renderWeekView() {
        // 获取当前日期所在周的星期一
        const monday = getMonday(currentDate);
        
        // 添加周视图的7天
        for (let i = 0; i < 7; i++) {
            const day = new Date(monday);
            day.setDate(monday.getDate() + i);
            
            const dayOfMonth = day.getDate();
            let className = 'calendar-day-wrapper week-view';
            let lunarText = getLunarDay(day);
            let holiday = getHoliday(day);
            
            // 检查是否为今天
            const today = new Date();
            if (dayOfMonth === today.getDate() && day.getMonth() === today.getMonth() && day.getFullYear() === today.getFullYear()) {
                className += ' today';
            }
            
            // 检查是否为所选日期
            if (dayOfMonth === selectedDate.getDate() && day.getMonth() === selectedDate.getMonth() && day.getFullYear() === selectedDate.getFullYear()) {
                className += ' selected';
            }
            
            // 检查是否为当前月
            if (day.getMonth() !== currentDate.getMonth()) {
                className += ' other-month';
            }
            
            // 创建并添加日历单元格
            addCalendarDay(dayOfMonth, className, lunarText, holiday, day);
        }
    }
    
    // 渲染农历视图
    function renderLunarView() {
        // 农历视图与月视图类似，但更强调农历信息
        const year = currentDate.getFullYear();
        const month = currentDate.getMonth();
        
        // 获取当前月的第一天
        const firstDayOfMonth = new Date(year, month, 1);
        
        // 获取当前月的最后一天
        const lastDayOfMonth = new Date(year, month + 1, 0);
        
        // 获取当前月第一天是星期几 (0-6)
        const firstDayOfWeek = firstDayOfMonth.getDay();
        
        // 获取当前月的总天数
        const daysInMonth = lastDayOfMonth.getDate();
        
        // 获取上个月的最后几天
        const prevMonthLastDay = new Date(year, month, 0).getDate();
        
        // 计算日历表格中的总单元格数 (6行 * 7列)
        const totalCells = 6 * 7;
        
        // 填充日历表格
        for (let i = 0; i < totalCells; i++) {
            let day;
            let cellDate;
            let className = 'calendar-day-wrapper lunar-view';
            let lunarText = '';
            let holiday = '';
            
            // 上个月的最后几天
            if (i < firstDayOfWeek) {
                day = prevMonthLastDay - firstDayOfWeek + i + 1;
                cellDate = new Date(year, month - 1, day);
                className += ' other-month';
                lunarText = getLunarDay(cellDate);
            }
            // 当前月的天数
            else if (i < firstDayOfWeek + daysInMonth) {
                day = i - firstDayOfWeek + 1;
                cellDate = new Date(year, month, day);
                lunarText = getLunarDay(cellDate);
                
                // 检查是否为今天
                const today = new Date();
                if (day === today.getDate() && month === today.getMonth() && year === today.getFullYear()) {
                    className += ' today';
                }
                
                // 检查是否为所选日期
                if (day === selectedDate.getDate() && month === selectedDate.getMonth() && year === selectedDate.getFullYear()) {
                    className += ' selected';
                }
                
                // 检查是否为农历节日
                holiday = getHoliday(cellDate);
            }
            // 下个月的前几天
            else {
                day = i - firstDayOfWeek - daysInMonth + 1;
                cellDate = new Date(year, month + 1, day);
                className += ' other-month';
                lunarText = getLunarDay(cellDate);
            }
            
            // 创建并添加日历单元格，强调农历信息
            addCalendarDay(day, className, lunarText, holiday, cellDate, true);
        }
    }
    
    // 添加日历天
    function addCalendarDay(day, className = '', lunarDay = '', holiday = '', date = null, emphasizeLunar = false) {
        const dayElement = document.createElement('div');
        dayElement.className = className;
        
        // 创建日期数字
        const dayNumber = document.createElement('div');
        dayNumber.className = 'calendar-day-number';
        dayNumber.textContent = day;
        
        // 创建农历日期
        const lunarElement = document.createElement('div');
        lunarElement.className = 'calendar-day-lunar';
        lunarElement.textContent = lunarDay;
        
        // 如果强调农历，则调整样式
        if (emphasizeLunar) {
            lunarElement.style.fontSize = '12px';
            lunarElement.style.fontWeight = '600';
            lunarElement.style.color = '#ff3b30';
        }
        
        // 如果有节日，添加节日标记
        if (holiday) {
            const holidayElement = document.createElement('div');
            holidayElement.className = 'calendar-day-holiday';
            holidayElement.textContent = holiday;
            holidayElement.style.fontSize = '10px';
            holidayElement.style.color = '#ff9500';
            dayElement.appendChild(holidayElement);
            dayElement.classList.add('has-event');
        }
        
        dayElement.appendChild(dayNumber);
        dayElement.appendChild(lunarElement);
        
        // 添加点击事件，选择日期
        if (date) {
            dayElement.addEventListener('click', function() {
                selectedDate = new Date(date);
                updateSelectedDateInfo(selectedDate);
                
                // 如果点击的是当前月的日期，更新选中状态
                const allDays = document.querySelectorAll('.calendar-day-wrapper');
                allDays.forEach(el => el.classList.remove('selected'));
                this.classList.add('selected');
            });
        }
        
        calendarContainer.appendChild(dayElement);
    }
    
    // 更新所选日期信息
    function updateSelectedDateInfo(date) {
        const lunarInfo = getLunarInfo(date);
        const formattedDate = `${lunarMonths[lunarInfo.month - 1]}${lunarDays[lunarInfo.day - 1]}`;
        const zodiacYear = `${getChineseYear(date.getFullYear())}${chineseZodiac[(date.getFullYear() - 4) % 12]}年`;
        const heavenlyStem = heavenlyStems[(date.getFullYear() - 4) % 10];
        const earthlyBranch = earthlyBranches[(date.getFullYear() - 4) % 12];
        
        selectedDateInfoDisplay.innerHTML = `
            <h4>${formattedDate}</h4>
            <p>${zodiacYear} ${heavenlyStem}${earthlyBranch}月 ${getDayTerrestrialBranch(date)}日</p>
        `;
    }
    
    // 更新假日倒计时
    function updateHolidayCountdown() {
        const holidayContainer = document.querySelector('.holiday-reminder');
        if (!holidayContainer) return;
        
        holidayContainer.innerHTML = '';
        
        // 获取下一个假日
        const nextHoliday = getNextHoliday();
        
        if (nextHoliday) {
            const holidayItem = document.createElement('div');
            holidayItem.className = 'holiday-item';
            
            const holidayName = document.createElement('div');
            holidayName.className = 'holiday-name';
            holidayName.textContent = nextHoliday.name;
            
            const holidayDate = document.createElement('div');
            holidayDate.className = 'holiday-date';
            
            // 格式化日期
            const formattedDate = `${nextHoliday.date.getMonth() + 1}月${nextHoliday.date.getDate()}日`;
            holidayDate.textContent = formattedDate;
            
            const holidayCountdown = document.createElement('div');
            holidayCountdown.className = 'holiday-countdown';
            
            // 计算倒计时
            const today = new Date();
            today.setHours(0, 0, 0, 0);
            const timeDiff = nextHoliday.date.getTime() - today.getTime();
            const dayDiff = Math.ceil(timeDiff / (1000 * 3600 * 24));
            
            holidayCountdown.innerHTML = `${dayDiff}<span>天</span>`;
            
            holidayItem.appendChild(holidayName);
            holidayItem.appendChild(holidayDate);
            holidayItem.appendChild(holidayCountdown);
            
            holidayContainer.appendChild(holidayItem);
        }
    }
    
    // 获取下一个假日
    function getNextHoliday() {
        const today = new Date();
        today.setHours(0, 0, 0, 0);
        
        let nextHoliday = null;
        let minDiff = Infinity;
        
        chineseHolidays.forEach(holiday => {
            let holidayDate;
            
            if (holiday.lunar) {
                // 转换农历日期到公历日期（简化计算）
                holidayDate = new Date(today.getFullYear(), holiday.month - 1, holiday.day);
                // 注意：这里使用了简化版，实际应该使用更复杂的农历转公历算法
            } else {
                holidayDate = new Date(today.getFullYear(), holiday.month - 1, holiday.day);
            }
            
            // 如果今年的节日已经过了，计算明年的日期
            if (holidayDate < today) {
                if (holiday.lunar) {
                    holidayDate = new Date(today.getFullYear() + 1, holiday.month - 1, holiday.day);
                } else {
                    holidayDate = new Date(today.getFullYear() + 1, holiday.month - 1, holiday.day);
                }
            }
            
            const timeDiff = holidayDate.getTime() - today.getTime();
            const dayDiff = Math.ceil(timeDiff / (1000 * 3600 * 24));
            
            if (dayDiff > 0 && dayDiff < minDiff) {
                minDiff = dayDiff;
                nextHoliday = {
                    name: holiday.name,
                    date: holidayDate,
                    daysLeft: dayDiff
                };
            }
        });
        
        return nextHoliday;
    }
    
    // 获取星期一的日期
    function getMonday(date) {
        const day = date.getDay();
        const diff = date.getDate() - day + (day === 0 ? -6 : 1); // 调整星期天
        return new Date(date.setDate(diff));
    }
    
    // 获取农历日期（简化版）
    function getLunarDay(date) {
        // 这里是简化的计算方法，实际应该使用更准确的农历转换算法
        const day = date.getDate();
        const totalDays = new Date(date.getFullYear(), date.getMonth() + 1, 0).getDate();
        
        // 模拟农历日期 - 实际应使用专业农历算法库
        const lunarDayIndex = (day - 1) % 30; // 简化：假设农历月总是30天
        return lunarDays[lunarDayIndex];
    }
    
    // 获取农历信息（简化版）
    function getLunarInfo(date) {
        // 这里是简化的计算方法，实际应该使用更准确的农历转换算法
        const day = date.getDate();
        
        // 模拟农历月份 - 实际应使用专业农历算法库
        const month = ((date.getMonth() + 2) % 12) + 1; // 简化：假设农历月比公历月晚一个月
        const lunarDayIndex = (day - 1) % 30; // 简化：假设农历月总是30天
        
        return {
            year: date.getFullYear(),
            month: month,
            day: lunarDayIndex + 1
        };
    }
    
    // 获取中国农历年份
    function getChineseYear(year) {
        const stem = heavenlyStems[(year - 4) % 10];
        const branch = earthlyBranches[(year - 4) % 12];
        return stem + branch;
    }
    
    // 获取日干支
    function getDayTerrestrialBranch(date) {
        // 简化版，实际应使用更复杂的计算
        const day = date.getDate();
        const stem = heavenlyStems[day % 10];
        const branch = earthlyBranches[day % 12];
        return stem + branch;
    }
    
    // 获取节日
    function getHoliday(date) {
        let holidayName = '';
        
        chineseHolidays.forEach(holiday => {
            if (!holiday.lunar && holiday.month === date.getMonth() + 1 && holiday.day === date.getDate()) {
                holidayName = holiday.name;
            }
            // 注意：这里忽略了农历节日的判断，实际应转换农历后比较
        });
        
        return holidayName;
    }
}

/**
 * 初始化iOS风格天气
 */
function initIOSWeather() {
    const locationElement = document.getElementById('location-district');
    const temperatureElement = document.getElementById('temperature');
    const tempHighElement = document.getElementById('temp-high');
    const tempLowElement = document.getElementById('temp-low');
    const weatherDescElement = document.getElementById('weather-desc');
    const refreshButton = document.getElementById('refreshWeather');
    
    // 模拟天气数据(大连)
    const weatherData = {
        location: '甘井子区',
        currentTemp: 7,
        tempHigh: 8,
        tempLow: 0,
        description: '大雾',
        humidity: 65,
        wind: '南风 3级',
        pressure: '1016 hPa',
        feelsLike: 4,
        uvIndex: '中 4',
        forecast: {
            hourly: [
                { time: '16时', temp: 7, icon: 'sun' },
                { time: '17时', temp: 6, icon: 'sun' },
                { time: '17:54', temp: 5, icon: 'sunset' },
                { time: '18时', temp: 5, icon: 'moon' },
                { time: '19时', temp: 4, icon: 'moon' },
                { time: '20时', temp: 4, icon: 'moon' }
            ],
            daily: [
                { day: '周一', tempLow: 3, tempHigh: 12, icon: 'sun' },
                { day: '周二', tempLow: 5, tempHigh: 12, icon: 'cloud-sun' },
                { day: '周三', tempLow: 3, tempHigh: 12, icon: 'sun' },
                { day: '周四', tempLow: 2, tempHigh: 8, icon: 'sun' }
            ]
        }
    };
    
    // 更新天气显示
    function updateWeatherDisplay() {
        // 添加刷新按钮动画
        refreshButton.querySelector('i').classList.add('fa-spin');
        
        // 模拟API调用延迟
        setTimeout(() => {
            // 更新位置和当前天气
            locationElement.innerHTML = `${weatherData.location} <i class="fas fa-map-marker-alt"></i>`;
            temperatureElement.textContent = weatherData.currentTemp;
            tempHighElement.textContent = weatherData.tempHigh;
            tempLowElement.textContent = weatherData.tempLow;
            weatherDescElement.textContent = weatherData.description;
            
            // 更新湿度、风向等详细信息
            document.getElementById('humidity-detail').textContent = `${weatherData.humidity}% 舒适`;
            document.getElementById('wind-detail').textContent = weatherData.wind;
            document.getElementById('feels-like-detail').textContent = `${weatherData.feelsLike}° 冷`;
            document.getElementById('uv-index').textContent = weatherData.uvIndex;
            
            // 停止刷新按钮动画
            refreshButton.querySelector('i').classList.remove('fa-spin');
        }, 1000);
    }
    
    // 刷新按钮事件
    refreshButton.addEventListener('click', updateWeatherDisplay);
    
    // 初始更新
    updateWeatherDisplay();
}

/**
 * 初始化番茄时钟
 */
function initPomodoroTimer() {
    // 时钟元素
    const pomodoroTimeElem = document.getElementById('pomodoroTime');
    const startTimerBtn = document.getElementById('startTimer');
    const shortBreakBtn = document.getElementById('shortBreak');
    const longBreakBtn = document.getElementById('longBreak');
    const focusCountElem = document.getElementById('focusCount');
    const totalFocusTimeElem = document.getElementById('totalFocusTime');
    const focusEfficiencyElem = document.getElementById('focusEfficiency');
    
    // 番茄模式元素
    const enableTomatoMode = document.getElementById('enableTomatoMode');
    const clockIcon = document.getElementById('clockIcon');
    const tomatoImg = document.getElementById('tomatoImg');
    const tomatoIcon = document.getElementById('tomatoIcon');
    
    // 时间设置元素
    const customHoursInput = document.getElementById('customHours');
    const customMinutesInput = document.getElementById('customMinutes');
    const customSecondsInput = document.getElementById('customSeconds');
    const decreaseHoursBtn = document.getElementById('decreaseHours');
    const increaseHoursBtn = document.getElementById('increaseHours');
    const decreaseMinutesBtn = document.getElementById('decreaseMinutes');
    const increaseMinutesBtn = document.getElementById('increaseMinutes');
    const decreaseSecondsBtn = document.getElementById('decreaseSeconds');
    const increaseSecondsBtn = document.getElementById('increaseSeconds');
    const presetButtons = document.querySelectorAll('.preset-btn');
    
    // 计时器状态
    let timerInterval = null;
    let hours = parseInt(customHoursInput.value) || 0;
    let minutes = parseInt(customMinutesInput.value) || 25;
    let seconds = parseInt(customSecondsInput.value) || 0;
    let isRunning = false;
    let focusSessions = 0;
    let totalFocusMinutes = 0;
    let startTime = null;
    let endTime = null;
    let pausedTime = 0;
    let isTomatoMode = false;
    
    // 从本地存储加载数据
    loadStats();
    
    // 初始化显示
    updateTimeDisplay();
    
    // 自定义时间按钮和输入事件
    decreaseHoursBtn.addEventListener('click', () => {
        if (hours > 0) hours--;
        customHoursInput.value = hours;
        updateTimeDisplay();
    });
    
    increaseHoursBtn.addEventListener('click', () => {
        if (hours < 12) hours++;
        customHoursInput.value = hours;
        updateTimeDisplay();
    });
    
    decreaseMinutesBtn.addEventListener('click', () => {
        if (minutes > 0) minutes--;
        else if (hours > 0) {
            hours--;
            minutes = 59;
            customHoursInput.value = hours;
        }
        customMinutesInput.value = minutes;
        updateTimeDisplay();
    });
    
    increaseMinutesBtn.addEventListener('click', () => {
        if (minutes < 59) minutes++;
        else {
            if (hours < 12) {
                hours++;
                minutes = 0;
                customHoursInput.value = hours;
            } else {
                minutes = 59;
            }
        }
        customMinutesInput.value = minutes;
        updateTimeDisplay();
    });
    
    decreaseSecondsBtn.addEventListener('click', () => {
        if (seconds > 0) seconds--;
        else if (minutes > 0) {
            minutes--;
            seconds = 59;
            customMinutesInput.value = minutes;
        } else if (hours > 0) {
            hours--;
            minutes = 59;
            seconds = 59;
            customHoursInput.value = hours;
            customMinutesInput.value = minutes;
        }
        customSecondsInput.value = seconds;
        updateTimeDisplay();
    });
    
    increaseSecondsBtn.addEventListener('click', () => {
        if (seconds < 59) seconds++;
        else {
            seconds = 0;
            if (minutes < 59) {
                minutes++;
            } else {
                minutes = 0;
                if (hours < 12) {
                    hours++;
                    customHoursInput.value = hours;
                }
            }
            customMinutesInput.value = minutes;
        }
        customSecondsInput.value = seconds;
        updateTimeDisplay();
    });
    
    // 输入框变化事件
    customHoursInput.addEventListener('change', () => {
        hours = parseInt(customHoursInput.value) || 0;
        if (hours < 0) hours = 0;
        if (hours > 12) hours = 12;
        customHoursInput.value = hours;
        updateTimeDisplay();
    });
    
    customMinutesInput.addEventListener('change', () => {
        minutes = parseInt(customMinutesInput.value) || 0;
        if (minutes < 0) minutes = 0;
        if (minutes > 59) minutes = 59;
        customMinutesInput.value = minutes;
        updateTimeDisplay();
    });
    
    customSecondsInput.addEventListener('change', () => {
        seconds = parseInt(customSecondsInput.value) || 0;
        if (seconds < 0) seconds = 0;
        if (seconds > 59) seconds = 59;
        customSecondsInput.value = seconds;
        updateTimeDisplay();
    });
    
    // 预设按钮事件
    presetButtons.forEach(btn => {
        btn.addEventListener('click', () => {
            hours = parseInt(btn.dataset.hours) || 0;
            minutes = parseInt(btn.dataset.minutes) || 0;
            seconds = parseInt(btn.dataset.seconds) || 0;
            
            customHoursInput.value = hours;
            customMinutesInput.value = minutes;
            customSecondsInput.value = seconds;
            
            updateTimeDisplay();
            
            // 添加动画效果
            btn.classList.add('animate__animated', 'animate__pulse');
            setTimeout(() => {
                btn.classList.remove('animate__animated', 'animate__pulse');
            }, 1000);
        });
    });
    
    // 番茄模式切换
    enableTomatoMode.addEventListener('change', () => {
        isTomatoMode = enableTomatoMode.checked;
        
        if (isTomatoMode) {
            clockIcon.classList.add('d-none');
            tomatoImg.classList.remove('d-none');
            tomatoIcon.classList.add('tomato-mode');
        } else {
            clockIcon.classList.remove('d-none');
            tomatoImg.classList.add('d-none');
            tomatoIcon.classList.remove('tomato-mode');
        }
    });
    
    // 开始/暂停计时器
    startTimerBtn.addEventListener('click', () => {
        if (isRunning) {
            pauseTimer();
        } else {
            startTimer();
        }
    });
    
    // 短休息按钮 (5分钟)
    shortBreakBtn.addEventListener('click', () => {
        resetTimer(0, 5, 0);
        shortBreakBtn.classList.add('animate__animated', 'animate__pulse');
        setTimeout(() => {
            shortBreakBtn.classList.remove('animate__animated', 'animate__pulse');
        }, 1000);
    });
    
    // 长休息按钮 (15分钟)
    longBreakBtn.addEventListener('click', () => {
        resetTimer(0, 15, 0);
        longBreakBtn.classList.add('animate__animated', 'animate__pulse');
        setTimeout(() => {
            longBreakBtn.classList.remove('animate__animated', 'animate__pulse');
        }, 1000);
    });
    
    // 更新时间显示
    function updateTimeDisplay() {
        pomodoroTimeElem.textContent = 
            `${hours.toString().padStart(2, '0')}:${minutes.toString().padStart(2, '0')}:${seconds.toString().padStart(2, '0')}`;
    }
    
    // 开始计时器
    function startTimer() {
        if (!isRunning) {
            if (hours === 0 && minutes === 0 && seconds === 0) {
                // 如果时间为0，恢复默认值
                minutes = 25;
                customMinutesInput.value = minutes;
                updateTimeDisplay();
            }
            
            if (!startTime) {
                startTime = new Date();
            }
            
            startTimerBtn.textContent = '暂停';
            startTimerBtn.classList.remove('btn-primary');
            startTimerBtn.classList.add('btn-warning');
            isRunning = true;
            
            // 添加动画到计时器
            pomodoroTimeElem.classList.add('pulsate');
            
            timerInterval = setInterval(() => {
                if (seconds === 0) {
                    if (minutes === 0) {
                        if (hours === 0) {
                            // 计时结束
                            timerComplete();
                            return;
                        }
                        hours--;
                        minutes = 59;
                    } else {
                        minutes--;
                    }
                    seconds = 59;
                } else {
                    seconds--;
                }
                
                customHoursInput.value = hours;
                customMinutesInput.value = minutes;
                customSecondsInput.value = seconds;
                
                updateTimeDisplay();
            }, 1000);
        }
    }
    
    // 暂停计时器
    function pauseTimer() {
        if (isRunning) {
            clearInterval(timerInterval);
            startTimerBtn.textContent = '继续';
            startTimerBtn.classList.remove('btn-warning');
            startTimerBtn.classList.add('btn-primary');
            isRunning = false;
            
            // 更新暂停时间
            pausedTime += (new Date()) - startTime;
            startTime = new Date();
            
            // 移除计时器动画
            pomodoroTimeElem.classList.remove('pulsate');
        }
    }
    
    // 重置计时器
    function resetTimer(h, m, s) {
        clearInterval(timerInterval);
        hours = h;
        minutes = m;
        seconds = s;
        
        customHoursInput.value = hours;
        customMinutesInput.value = minutes;
        customSecondsInput.value = seconds;
        
        updateTimeDisplay();
        isRunning = false;
        startTimerBtn.textContent = '开始专注';
        startTimerBtn.classList.remove('btn-warning');
        startTimerBtn.classList.add('btn-primary');
        
        // 重置时间记录
        startTime = null;
        endTime = null;
        pausedTime = 0;
        
        // 移除计时器动画
        pomodoroTimeElem.classList.remove('pulsate');
    }
    
    // 计时结束
    function timerComplete() {
        clearInterval(timerInterval);
        endTime = new Date();
        
        // 播放声音提醒
        playAlarm();
        
        // 显示通知
        showNotification('专注时间结束！', '休息一下吧！');
        
        isRunning = false;
        startTimerBtn.textContent = '开始专注';
        startTimerBtn.classList.remove('btn-warning');
        startTimerBtn.classList.add('btn-primary');
        
        // 移除计时器动画
        pomodoroTimeElem.classList.remove('pulsate');
        
        // 添加完成动画
        pomodoroTimeElem.classList.add('animate__animated', 'animate__rubberBand');
        setTimeout(() => {
            pomodoroTimeElem.classList.remove('animate__animated', 'animate__rubberBand');
        }, 1000);
        
        // 更新统计数据
        updateStats();
        
        // 重置为之前的设置时间
        resetTimer(
            parseInt(customHoursInput.getAttribute('data-original') || 0),
            parseInt(customMinutesInput.getAttribute('data-original') || 25),
            parseInt(customSecondsInput.getAttribute('data-original') || 0)
        );
    }
    
    // 更新统计数据
    function updateStats() {
        // 增加专注次数
        focusSessions++;
        
        // 计算专注总时长(分钟)
        const originalHours = parseInt(customHoursInput.getAttribute('data-original') || 0);
        const originalMinutes = parseInt(customMinutesInput.getAttribute('data-original') || 25);
        const originalSeconds = parseInt(customSecondsInput.getAttribute('data-original') || 0);
        
        const totalMinutes = originalHours * 60 + originalMinutes + originalSeconds / 60;
        totalFocusMinutes += Math.round(totalMinutes);
        
        // 计算专注效率
        let efficiency = 100;
        if (endTime && startTime) {
            const totalTimeMs = endTime - startTime;
            const activeTimeMs = totalTimeMs - pausedTime;
            efficiency = Math.round((activeTimeMs / totalTimeMs) * 100);
        }
        
        // 更新显示
        focusCountElem.textContent = focusSessions;
        totalFocusTimeElem.textContent = totalFocusMinutes;
        focusEfficiencyElem.textContent = `${efficiency}%`;
        
        // 保存到本地存储
        saveStats();
        
        // 储存原始时间设置
        customHoursInput.setAttribute('data-original', originalHours);
        customMinutesInput.setAttribute('data-original', originalMinutes);
        customSecondsInput.setAttribute('data-original', originalSeconds);
    }
    
    // 播放提醒声音
    function playAlarm() {
        try {
            const audio = new Audio('https://soundbible.com/grab.php?id=1746&type=mp3');
            audio.volume = 0.5;
            audio.play();
        } catch (e) {
            console.log('无法播放声音提醒:', e);
        }
    }
    
    // 显示通知
    function showNotification(title, body) {
        if (Notification.permission === 'granted') {
            new Notification(title, {
                body,
                icon: isTomatoMode ? '/static/img/tomato.png' : null
            });
        } else if (Notification.permission !== 'denied') {
            Notification.requestPermission().then(permission => {
                if (permission === 'granted') {
                    new Notification(title, {
                        body,
                        icon: isTomatoMode ? '/static/img/tomato.png' : null
                    });
                }
            });
        }
    }
    
    // 从本地存储加载统计数据
    function loadStats() {
        const savedStats = localStorage.getItem('pomodoroStats');
        if (savedStats) {
            const stats = JSON.parse(savedStats);
            focusSessions = stats.sessions || 0;
            totalFocusMinutes = stats.totalMinutes || 0;
            
            focusCountElem.textContent = focusSessions;
            totalFocusTimeElem.textContent = totalFocusMinutes;
            focusEfficiencyElem.textContent = stats.efficiency || '0%';
        }
    }
    
    // 保存统计数据到本地存储
    function saveStats() {
        const stats = {
            sessions: focusSessions,
            totalMinutes: totalFocusMinutes,
            efficiency: focusEfficiencyElem.textContent,
            lastUpdated: new Date().toISOString()
        };
        localStorage.setItem('pomodoroStats', JSON.stringify(stats));
    }
    
    // 储存原始时间设置
    customHoursInput.setAttribute('data-original', hours);
    customMinutesInput.setAttribute('data-original', minutes);
    customSecondsInput.setAttribute('data-original', seconds);
}