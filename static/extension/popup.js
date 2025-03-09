document.addEventListener('DOMContentLoaded', function() {
  // 显示当前日期
  const dateDisplay = document.getElementById('date-display');
  const today = new Date();
  const options = { weekday: 'long', year: 'numeric', month: 'long', day: 'numeric' };
  dateDisplay.textContent = today.toLocaleDateString('zh-CN', options);
  
  // 获取待办事项列表元素
  const todoList = document.getElementById('todo-list');
  
  // 加载今日待办事项
  loadTodayTodos();
  
  // 绑定添加待办事项按钮点击事件
  document.getElementById('add-todo-btn').addEventListener('click', addTodo);
  document.getElementById('new-todo').addEventListener('keypress', function(e) {
    if (e.key === 'Enter') {
      addTodo();
    }
  });
  
  // 绑定打开日历按钮点击事件
  document.getElementById('open-calendar').addEventListener('click', function() {
    chrome.tabs.create({ url: chrome.runtime.getURL('calendar.html') });
  });
  
  // 绑定同步数据按钮点击事件
  document.getElementById('sync-todos').addEventListener('click', syncTodos);
  
  // 加载今日待办事项
  function loadTodayTodos() {
    // 清空待办事项列表
    todoList.innerHTML = '';
    
    // 从存储中获取待办事项
    chrome.storage.local.get(['todos'], function(result) {
      const todos = result.todos || [];
      
      // 过滤出今日待办事项
      const todayStr = `${today.getFullYear()}-${today.getMonth() + 1}-${today.getDate()}`;
      const todayTodos = todos.filter(todo => todo.date === todayStr);
      
      // 如果没有今日待办事项，显示空状态
      if (todayTodos.length === 0) {
        const emptyState = document.createElement('div');
        emptyState.className = 'empty-state';
        emptyState.textContent = '今日暂无待办事项';
        todoList.appendChild(emptyState);
        return;
      }
      
      // 渲染今日待办事项
      todayTodos.forEach(todo => {
        const todoItem = document.createElement('div');
        todoItem.className = `todo-item ${todo.completed ? 'todo-completed' : ''}`;
        todoItem.dataset.id = todo.id;
        
        // 创建复选框
        const checkbox = document.createElement('input');
        checkbox.type = 'checkbox';
        checkbox.className = 'todo-checkbox';
        checkbox.checked = todo.completed;
        checkbox.addEventListener('change', function() {
          toggleTodoComplete(todo.id, this.checked);
        });
        
        // 创建标题
        const title = document.createElement('div');
        title.className = 'todo-title';
        title.textContent = todo.title;
        
        // 创建时间（如果有）
        let timeElement = '';
        if (todo.time) {
          const time = document.createElement('div');
          time.className = 'todo-time';
          time.textContent = todo.time;
          timeElement = time;
        }
        
        // 添加元素到待办事项
        todoItem.appendChild(checkbox);
        todoItem.appendChild(title);
        if (timeElement) todoItem.appendChild(timeElement);
        
        // 添加到待办事项列表
        todoList.appendChild(todoItem);
      });
    });
  }
  
  // 添加新待办事项
  function addTodo() {
    const input = document.getElementById('new-todo');
    const title = input.value.trim();
    
    if (!title) return;
    
    // 从存储中获取现有待办事项
    chrome.storage.local.get(['todos'], function(result) {
      const todos = result.todos || [];
      
      // 创建新待办事项
      const newTodo = {
        id: Date.now(),
        title: title,
        date: `${today.getFullYear()}-${today.getMonth() + 1}-${today.getDate()}`,
        time: '',
        completed: false
      };
      
      // 添加到待办事项列表
      todos.push(newTodo);
      
      // 保存到存储
      chrome.storage.local.set({ todos: todos }, function() {
        // 清空输入
        input.value = '';
        
        // 重新加载待办事项
        loadTodayTodos();
        
        // 设置提醒
        chrome.runtime.sendMessage({ 
          action: 'setReminder', 
          todo: newTodo 
        });
      });
    });
  }
  
  // 切换待办事项完成状态
  function toggleTodoComplete(id, completed) {
    // 从存储中获取待办事项
    chrome.storage.local.get(['todos'], function(result) {
      const todos = result.todos || [];
      
      // 更新完成状态
      const updatedTodos = todos.map(todo => {
        if (todo.id === id) {
          return { ...todo, completed: completed };
        }
        return todo;
      });
      
      // 保存到存储
      chrome.storage.local.set({ todos: updatedTodos }, function() {
        // 更新UI
        const todoItem = document.querySelector(`.todo-item[data-id="${id}"]`);
        if (todoItem) {
          todoItem.classList.toggle('todo-completed', completed);
        }
      });
    });
  }
  
  // 同步待办事项
  function syncTodos() {
    // 显示同步中...
    const syncButton = document.getElementById('sync-todos');
    const originalText = syncButton.textContent;
    syncButton.textContent = '同步中...';
    
    // 与主应用同步数据
    fetch('https://example.com/api/sync-todos', {
      method: 'GET',
      credentials: 'include'
    })
    .then(response => response.json())
    .then(data => {
      // 保存同步的待办事项
      chrome.storage.local.set({ todos: data.todos }, function() {
        // 重新加载待办事项
        loadTodayTodos();
        
        // 恢复按钮文本
        syncButton.textContent = originalText;
        
        // 显示成功消息
        alert('同步成功');
      });
    })
    .catch(error => {
      console.error('同步失败:', error);
      
      // 恢复按钮文本
      syncButton.textContent = originalText;
      
      // 显示错误消息
      alert('同步失败，请稍后重试');
    });
  }
}); 