// 创建 static/js/forms.js 文件
class FormHandler {
    static async handleSubmit(form, event) {
        event.preventDefault();

        const formData = new FormData(form);
        const data = Object.fromEntries(formData.entries());

        try {
            if (navigator.onLine) {
                // 在线模式：直接提交到服务器
                const response = await fetch(form.action, {
                    method: form.method,
                    body: formData
                });

                if (!response.ok) {
                    throw new Error('提交失败');
                }
            } else {
                // 离线模式：保存到 IndexedDB
                if (form.id === 'addGradeForm') {
                    await gradeDB.saveGrade(data.student_id, {
                        course_name: data.course_name,
                        course_type: data.course_type,
                        credit: parseFloat(data.credit),
                        score: parseInt(data.score),
                        research: data.research,
                        year: data.year
                    });
                } else if (form.id === 'addStudentForm') {
                    await gradeDB.saveStudent({
                        student_id: data.student_id,
                        name: data.name,
                        gender: data.gender,
                        major: data.major,
                        admission_year: data.admission_year
                    });
                }
            }

            // 显示成功消息
            const message = navigator.onLine ? '提交成功' : '数据已保存，将在恢复网络连接后同步';
            dataSync.showStatus(message, 'success');

            // 重置表单
            form.reset();
        } catch (error) {
            dataSync.showStatus('操作失败：' + error.message, 'danger');
        }
    }
}

// 表单处理
document.addEventListener('DOMContentLoaded', () => {
    // 添加学生表单处理
    const addStudentForm = document.getElementById('add-student-form');
    if (addStudentForm) {
        addStudentForm.addEventListener('submit', async (e) => {
            e.preventDefault();
            
            const formData = new FormData(addStudentForm);
            const studentData = {
                student_id: formData.get('student_id'),
                name: formData.get('name'),
                gender: formData.get('gender'),
                major: formData.get('major'),
                admission_year: formData.get('admission_year')
            };
            
            try {
                // 保存到本地数据库
                await gradeDB.addStudent(studentData);
                
                // 添加到同步队列
                await gradeDB.addToSyncQueue({
                    type: 'student',
                    data: studentData
                });
                
                // 如果在线，立即同步
                if (navigator.onLine) {
                    await dataSync.sync();
                }
                
                // 提交表单
                addStudentForm.submit();
            } catch (error) {
                console.error('保存学生数据失败:', error);
                alert('保存失败，请重试');
            }
        });
    }
    
    // 添加成绩表单处理
    const addGradeForm = document.getElementById('add-grade-form');
    if (addGradeForm) {
        addGradeForm.addEventListener('submit', async (e) => {
            e.preventDefault();
            
            const formData = new FormData(addGradeForm);
            const gradeData = {
                student_id: formData.get('student_id'),
                course_name: formData.get('course_name'),
                course_type: formData.get('course_type'),
                credit: parseFloat(formData.get('credit')),
                score: parseInt(formData.get('score')),
                research: formData.get('research'),
                year: formData.get('year')
            };
            
            try {
                // 保存到本地数据库
                await gradeDB.addGrade(gradeData);
                
                // 添加到同步队列
                await gradeDB.addToSyncQueue({
                    type: 'grade',
                    data: gradeData
                });
                
                // 如果在线，立即同步
                if (navigator.onLine) {
                    await dataSync.sync();
                }
                
                // 提交表单
                addGradeForm.submit();
            } catch (error) {
                console.error('保存成绩数据失败:', error);
                alert('保存失败，请重试');
            }
        });
    }
    
    // 添加同步状态显示
    const navbarNav = document.querySelector('.navbar-nav');
    if (navbarNav) {
        const statusElement = document.createElement('li');
        statusElement.className = 'nav-item';
        statusElement.innerHTML = `
            <span class="nav-link">
                <i class="fas fa-sync"></i>
                <span id="sync-status">同步状态: 正在检查...</span>
            </span>
        `;
        navbarNav.appendChild(statusElement);
    }
}); 