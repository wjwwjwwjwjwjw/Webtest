// IndexedDB 数据库管理
const gradeDB = {
    db: null,
    
    async init() {
        return new Promise((resolve, reject) => {
            const request = indexedDB.open('GradeManagerDB', 1);
            
            request.onerror = () => reject(request.error);
            
            request.onsuccess = () => {
                this.db = request.result;
                resolve();
            };
            
            request.onupgradeneeded = (event) => {
                const db = event.target.result;
                
                // 创建学生表
                if (!db.objectStoreNames.contains('students')) {
                    db.createObjectStore('students', { keyPath: 'student_id' });
                }
                
                // 创建成绩表
                if (!db.objectStoreNames.contains('grades')) {
                    const gradeStore = db.createObjectStore('grades', { keyPath: ['student_id', 'course_name'] });
                    gradeStore.createIndex('student_id', 'student_id');
                }
                
                // 创建待同步队列
                if (!db.objectStoreNames.contains('syncQueue')) {
                    db.createObjectStore('syncQueue', { keyPath: 'id', autoIncrement: true });
                }
            };
        });
    },
    
    async addStudent(student) {
        return new Promise((resolve, reject) => {
            const transaction = this.db.transaction(['students'], 'readwrite');
            const store = transaction.objectStore('students');
            
            const request = store.add(student);
            
            request.onsuccess = () => resolve();
            request.onerror = () => reject(request.error);
        });
    },
    
    async addGrade(grade) {
        return new Promise((resolve, reject) => {
            const transaction = this.db.transaction(['grades'], 'readwrite');
            const store = transaction.objectStore('grades');
            
            const request = store.add(grade);
            
            request.onsuccess = () => resolve();
            request.onerror = () => reject(request.error);
        });
    },
    
    async addToSyncQueue(item) {
        return new Promise((resolve, reject) => {
            const transaction = this.db.transaction(['syncQueue'], 'readwrite');
            const store = transaction.objectStore('syncQueue');
            
            const request = store.add({
                ...item,
                timestamp: new Date().getTime()
            });
            
            request.onsuccess = () => resolve();
            request.onerror = () => reject(request.error);
        });
    },
    
    async getSyncQueue() {
        return new Promise((resolve, reject) => {
            const transaction = this.db.transaction(['syncQueue'], 'readonly');
            const store = transaction.objectStore('syncQueue');
            
            const request = store.getAll();
            
            request.onsuccess = () => resolve(request.result);
            request.onerror = () => reject(request.error);
        });
    },
    
    async removeSyncItem(id) {
        return new Promise((resolve, reject) => {
            const transaction = this.db.transaction(['syncQueue'], 'readwrite');
            const store = transaction.objectStore('syncQueue');
            
            const request = store.delete(id);
            
            request.onsuccess = () => resolve();
            request.onerror = () => reject(request.error);
        });
    }
}; 