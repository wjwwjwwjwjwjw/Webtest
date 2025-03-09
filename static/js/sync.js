// 数据同步管理
const dataSync = {
    syncInterval: 5000, // 同步间隔（毫秒）
    isOnline: navigator.onLine,
    syncTimer: null,
    
    init() {
        // 监听在线状态变化
        window.addEventListener('online', () => {
            this.isOnline = true;
            this.showSyncStatus('在线');
            this.sync();
        });
        
        window.addEventListener('offline', () => {
            this.isOnline = false;
            this.showSyncStatus('离线');
        });
        
        // 启动定期同步
        this.startSync();
        
        // 显示初始状态
        this.showSyncStatus(this.isOnline ? '在线' : '离线');
    },
    
    startSync() {
        this.syncTimer = setInterval(() => {
            if (this.isOnline) {
                this.sync();
            }
        }, this.syncInterval);
    },
    
    stopSync() {
        if (this.syncTimer) {
            clearInterval(this.syncTimer);
            this.syncTimer = null;
        }
    },
    
    async sync() {
        try {
            const queue = await gradeDB.getSyncQueue();
            if (queue.length === 0) return;
            
            for (const item of queue) {
                try {
                    await this.syncItem(item);
                    await gradeDB.removeSyncItem(item.id);
                } catch (error) {
                    console.error('同步失败:', error);
                    this.showSyncError(error.message);
                }
            }
        } catch (error) {
            console.error('获取同步队列失败:', error);
            this.showSyncError('获取同步队列失败');
        }
    },
    
    async syncItem(item) {
        const endpoint = item.type === 'student' ? '/api/sync/student' : '/api/sync/grade';
        
        const response = await fetch(endpoint, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'X-Requested-With': 'XMLHttpRequest'
            },
            body: JSON.stringify(item.data)
        });
        
        if (!response.ok) {
            const error = await response.json();
            throw new Error(error.message || '同步失败');
        }
        
        return response.json();
    },
    
    showSyncStatus(status) {
        const statusElement = document.getElementById('sync-status');
        if (statusElement) {
            statusElement.textContent = `同步状态: ${status}`;
            statusElement.className = status === '在线' ? 'text-success' : 'text-warning';
        }
    },
    
    showSyncError(message) {
        const errorElement = document.createElement('div');
        errorElement.className = 'alert alert-danger alert-dismissible fade show';
        errorElement.innerHTML = `
            <strong>同步错误:</strong> ${message}
            <button type="button" class="btn-close" data-bs-dismiss="alert"></button>
        `;
        
        const container = document.querySelector('.main-content');
        if (container) {
            container.insertBefore(errorElement, container.firstChild);
        }
    }
}; 