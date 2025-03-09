// 日历功能
let currentDate = new Date();

// 初始化日历
function initCalendar() {
    updateCalendarHeader();
    renderCalendar();
}

// 更新日历标题
function updateCalendarHeader() {
    const monthNames = ['一月', '二月', '三月', '四月', '五月', '六月', 
                        '七月', '八月', '九月', '十月', '十一月', '十二月'];
    document.querySelector('.month-display h3').textContent = 
        `${monthNames[currentDate.getMonth()]} ${currentDate.getFullYear()}`;
}

// 渲染日历
function renderCalendar() {
    const daysGrid = document.querySelector('.days-grid');
    daysGrid.innerHTML = '';
    
    const year = currentDate.getFullYear();
    const month = currentDate.getMonth();
    
    // 获取当月第一天
    const firstDay = new Date(year, month, 1);
    // 获取当月天数
    const daysInMonth = new Date(year, month + 1, 0).getDate();
    
    // 获取上个月天数
    const daysInPrevMonth = new Date(year, month, 0).getDate();
    
    // 当月第一天是星期几 (0-6，0=星期日)
    let firstDayIndex = firstDay.getDay();
    if (firstDayIndex === 0) firstDayIndex = 7; // 调整为周一为一周的第一天
    
    // 计算需要显示的日期总数 (上月剩余 + 当月 + 下月开始)
    const totalCells = 42; // 6行7列
    
    // 当前日期
    const today = new Date();
    const currentYear = today.getFullYear();
    const currentMonth = today.getMonth();
    const currentDay = today.getDate();
    
    // 生成日历网格
    let date = 1;
    let prevMonthDate = daysInPrevMonth - firstDayIndex + 2;
    let nextMonthDate = 1;
    
    for (let row = 0; row < 6; row++) {
        const weekEl = document.createElement('div');
        weekEl.className = 'week';
        
        for (let col = 0; col < 7; col++) {
            const dayCell = document.createElement('div');
            dayCell.className = 'day-cell';
            
            if (row === 0 && col < firstDayIndex - 1) {
                // 上月的日期
                dayCell.textContent = prevMonthDate;
                dayCell.classList.add('other-month');
                prevMonthDate++;
            } else if (date > daysInMonth) {
                // 下月的日期
                dayCell.textContent = nextMonthDate;
                dayCell.classList.add('other-month');
                nextMonthDate++;
            } else {
                // 当月的日期
                dayCell.textContent = date;
                
                // 标记今天
                if (year === currentYear && month === currentMonth && date === currentDay) {
                    dayCell.classList.add('today');
                }
                
                date++;
            }
            
            weekEl.appendChild(dayCell);
        }
        
        daysGrid.appendChild(weekEl);
        
        // 如果已经显示完当月所有日期，且下月日期也超过了一行，就不再生成后续行
        if (date > daysInMonth && row >= 4) break;
    }
}

// 切换到上个月
function prevMonth() {
    currentDate.setMonth(currentDate.getMonth() - 1);
    updateCalendarHeader();
    renderCalendar();
}

// 切换到下个月
function nextMonth() {
    currentDate.setMonth(currentDate.getMonth() + 1);
    updateCalendarHeader();
    renderCalendar();
}

// 回到今天
function goToToday() {
    currentDate = new Date();
    updateCalendarHeader();
    renderCalendar();
}

// 切换视图模式 (月/周)
function switchView(mode) {
    const monthBtn = document.querySelector('.btn-month');
    const weekBtn = document.querySelector('.btn-week');
    
    if (mode === 'month') {
        monthBtn.classList.add('btn-active');
        weekBtn.classList.remove('btn-active');
        document.querySelector('.days-grid').classList.remove('week-view');
    } else {
        weekBtn.classList.add('btn-active');
        monthBtn.classList.remove('btn-active');
        document.querySelector('.days-grid').classList.add('week-view');
    }
}

// 初始化日历
document.addEventListener('DOMContentLoaded', initCalendar); 