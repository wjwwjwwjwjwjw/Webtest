// 成绩编辑功能
document.addEventListener('DOMContentLoaded', function() {
    // 获取模态框元素
    const editModal = new bootstrap.Modal(document.getElementById('editGradeModal'));
    
    // 监听编辑按钮点击事件
    document.querySelectorAll('.edit-grade-btn').forEach(button => {
        button.addEventListener('click', function() {
            // 获取成绩数据
            const courseName = this.dataset.courseName;
            const courseType = this.dataset.courseType;
            const credit = this.dataset.credit;
            const score = this.dataset.score;
            const research = this.dataset.research;
            const year = this.dataset.year;
            
            // 填充表单
            document.getElementById('original_course_name').value = courseName;
            document.getElementById('edit_course_name').value = courseName;
            document.getElementById('edit_course_type').value = courseType;
            document.getElementById('edit_credit').value = credit;
            document.getElementById('edit_score').value = score;
            document.getElementById('edit_research').value = research;
            document.getElementById('edit_year').value = year;
            
            // 显示模态框
            editModal.show();
        });
    });
    
    // 保存按钮点击事件
    document.getElementById('saveGradeChanges').addEventListener('click', function() {
        const form = document.getElementById('editGradeForm');
        const formData = new FormData(form);
        
        // 获取当前学生ID
        const studentId = window.location.pathname.split('/').pop();
        
        // 发送AJAX请求
        fetch(`/student/${studentId}/edit_grade`, {
            method: 'POST',
            body: formData
        })
        .then(response => response.json())
        .then(data => {
            if (data.status === 'success') {
                // 关闭模态框
                editModal.hide();
                
                // 显示成功消息
                showAlert('success', data.message);
                
                // 刷新页面显示更新后的数据
                setTimeout(() => window.location.reload(), 1000);
            } else {
                // 显示错误消息
                showAlert('danger', data.message);
            }
        })
        .catch(error => {
            showAlert('danger', '请求失败：' + error);
        });
    });
    
    // 显示提示消息
    function showAlert(type, message) {
        const alertDiv = document.createElement('div');
        alertDiv.className = `alert alert-${type} alert-dismissible fade show`;
        alertDiv.innerHTML = `
            ${message}
            <button type="button" class="btn-close" data-bs-dismiss="alert"></button>
        `;
        
        document.querySelector('.main-content').insertAdjacentElement('afterbegin', alertDiv);
        
        // 5秒后自动移除
        setTimeout(() => alertDiv.remove(), 5000);
    }
}); 