// 初始化插件
chrome.runtime.onInstalled.addListener(function() {
  console.log('日历提醒插件已安装');
  
  // 创建右键菜单
  chrome.contextMenus.create({
    id: 'addTodo',
    title: '添加为待办事项',
    contexts: ['selection']
  });
});

// 处理右键菜单点击
chrome.contextMenus.onClicked.addListener(function(info, tab) {
  if (info.menuItemId === 'addTodo') {
    // 获取选中的文本
    const selectedText = info.selectionText;
    
    // 添加为待办事项
    addTodoFromSelection(selectedText);
  }
});

// 处理消息
chrome.runtime.onMessage.addListener(function(request, sender, sendResponse) {
  if (request.action === 'setReminder') {
    // 设置提醒
    setReminder(request.todo);
    sendResponse({ status: 'success' });
  }
  
  return true;
});

// 处理提醒
chrome.alarms.onAlarm.addListener(function(alarm) {
  // 检查是否是待办事项提醒
  if (alarm.name.startsWith('todo-reminder-')) {
    const todoId = alarm.name.replace('todo-reminder-', '');
    
    // 获取待办事项
    chrome.storage.local.get(['todos'], function(result) {
      const todos = result.todos || [];
      const todo = todos.find(t => t.id.toString() === todoId);
      
      if (todo) {
        // 显示通知
        chrome.notifications.create('', {
          type: 'basic',
          iconUrl: 'icons/icon128.png',
          title: '待办事项提醒',
          message: todo.title,
          buttons: [
            { title: '完成' },
            { title: '稍后提醒' }
          ],
          requireInteraction: true
        });
      }
    });
  }
});

// 处理通知按钮点击
chrome.notifications.onButtonClicked.addListener(function(notificationId, buttonIndex) {
  // 获取通知数据
  chrome.notifications.getAll(function(notifications) {
    const notification = notifications[notificationId];
    
    if (notification) {
      // 根据按钮索引处理
      if (buttonIndex === 0) {
        // 完成按钮
        markTodoAsCompleted(notification.todo.id);
      } else if (buttonIndex === 1) {
        // 稍后提醒按钮
        snoozeReminder(notification.todo.id);
      }
      
      // 关闭通知
      chrome.notifications.clear(notificationId);
    }
  });
});

// 从选中文本添加待办事项
function addTodoFromSelection(text) {
  if (!text) return;
  
  // 获取当前日期
  const today = new Date();
  const todayStr = `${today.getFullYear()}-${today.getMonth() + 1}-${today.getDate()}`;
  
  // 创建新待办事项
  const newTodo = {
    id: Date.now(),
    title: text,
    date: todayStr,
    time: '',
    completed: false
  };
  
  // 保存到存储
  chrome.storage.local.get(['todos'], function(result) {
    const todos = result.todos || [];
    todos.push(newTodo);
    
    chrome.storage.local.set({ todos: todos }, function() {
      // 显示通知
      chrome.notifications.create('', {
        type: 'basic',
        iconUrl: 'icons/icon128.png',
        title: '已添加待办事项',
        message: text
      });
    });
  });
}

// 设置提醒
function setReminder(todo) {
  if (!todo.time) return;
  
  // 解析日期和时间
  const [year, month, day] = todo.date.split('-').map(Number);
  const [hours, minutes] = todo.time.split(':').map(Number);
  
  // 创建提醒时间
  const reminderTime = new Date(year, month - 1, day, hours, minutes);
  
  // 如果时间已过，不设置提醒
  if (reminderTime < new Date()) return;
  
  // 计算提醒时间（毫秒）
  const alarmTime = reminderTime.getTime();
  
  // 创建提醒
  chrome.alarms.create(`todo-reminder-${todo.id}`, {
    when: alarmTime
  });
}

// 标记待办事项为已完成
function markTodoAsCompleted(todoId) {
  chrome.storage.local.get(['todos'], function(result) {
    const todos = result.todos || [];
    
    // 更新完成状态
    const updatedTodos = todos.map(todo => {
      if (todo.id === todoId) {
        return { ...todo, completed: true };
      }
      return todo;
    });
    
    // 保存到存储
    chrome.storage.local.set({ todos: updatedTodos });
  });
}

// 稍后提醒
function snoozeReminder(todoId) {
  // 设置15分钟后再次提醒
  const snoozeTime = Date.now() + 15 * 60 * 1000;
  
  // 创建提醒
  chrome.alarms.create(`todo-reminder-${todoId}`, {
    when: snoozeTime
  });
} 