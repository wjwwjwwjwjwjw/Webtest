# -*- coding: utf-8 -*-
from flask import Flask, render_template, request, redirect, url_for, flash, jsonify, send_file, send_from_directory
import os
import json
from models import Student, ClassManager, UserManager, DATA_DIR
import pandas as pd
from datetime import datetime, timedelta
from werkzeug.utils import secure_filename
from flask_login import LoginManager, UserMixin, login_user, logout_user, login_required, current_user
from werkzeug.security import generate_password_hash, check_password_hash
from functools import wraps
import requests
from bs4 import BeautifulSoup

app = Flask(__name__, static_folder='static')
app.secret_key = 'your_secret_key'  # 用于flash消息

# 添加上传文件夹配置
app.config['UPLOAD_FOLDER'] = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'uploads')
# 确保上传文件夹存在
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

# 初始化班级管理器
class_manager = ClassManager()

# 初始化Flask-Login
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'
login_manager.login_message = '请先登录'
login_manager.login_message_category = 'info'

# 初始化用户管理器
user_manager = UserManager()
user_manager.load_users()

# 数据文件路径
DEFAULT_CLASS_FILE = os.path.join(DATA_DIR, 'class_data.json')

# 如果存在默认班级文件，加载它
if os.path.exists(DEFAULT_CLASS_FILE):
    try:
        class_manager.load_from_file(DEFAULT_CLASS_FILE)
    except Exception as e:
        print(f"加载班级数据失败: {e}")

# 需要管理员权限的路由装饰器
def admin_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not current_user.is_authenticated or not current_user.user.is_admin:
            flash('需要管理员权限', 'danger')
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    return decorated_function

# 路由: 首页
@app.route('/')
@login_required
def index():
    # 获取最近的更新
    recent_updates = []
    
    # 使用正确的方法获取学生
    students = class_manager.get_all_students()
    
    # 确保 students 是可迭代的列表类型
    if students and isinstance(students, list):
        # 安全地获取最近添加的学生（最多5个）
        recent_students = students[-5:] if len(students) >= 5 else students[:]
        
        for student in recent_students:
            recent_updates.append({
                'type': '学生',
                'content': f'添加了学生 {student.name}',
                'time': '最近'
            })
        
        # 获取最近的成绩更新
        for student in students:
            if hasattr(student, 'grades') and student.grades:
                # 获取最近的成绩，避免使用切片
                recent_grades = []
                for grade in student.grades:
                    if len(recent_grades) < 3:  # 最多取3条
                        recent_grades.append(grade)
                
                for grade in recent_grades:
                    recent_updates.append({
                        'type': '成绩',
                        'content': f'{student.name} 添加了 {grade["course_name"]}',
                        'time': '最近'
                    })
    
    # 按时间排序并只保留最近的10条
    if len(recent_updates) > 10:
        recent_updates = sorted(recent_updates, key=lambda x: x['time'], reverse=True)[:10]
    
    return render_template('dashboard.html', recent_updates=recent_updates)

# 路由: 学生列表
@app.route('/students')
def student_list():
    students = class_manager.get_all_students()
    return render_template('student_list.html', students=students)

# 路由: 学生详情
@app.route('/student/<student_id>')
def student_detail(student_id):
    student = class_manager.get_student(student_id)
    if not student:
        flash('学生不存在', 'danger')
        return redirect(url_for('student_list'))
    
    # 计算学生统计数据
    stats = {
        'avg_score': student.calculate_weighted_average_score(),
        'avg_gpa': student.calculate_weighted_gpa(),
        'required_credits': student.calculate_total_credits()[0],
        'total_credits': student.calculate_total_credits()[1],
        'count_90': student.count_high_scores()[0],
        'count_95': student.count_high_scores()[1]
    }
    
    return render_template('student_detail.html', student=student, stats=stats)

# 路由: 添加学生表单
@app.route('/add_student', methods=['GET', 'POST'])
@admin_required
def add_student():
    if request.method == 'POST':
        try:
            student_id = request.form['student_id'].strip()
            name = request.form['name'].strip()
            gender = request.form['gender']
            major = request.form['major'].strip()
            admission_year = request.form['admission_year'].strip()
            
            if not student_id or not name:
                flash('学号和姓名不能为空', 'danger')
                return redirect(url_for('add_student'))
            
            if student_id in class_manager.students:
                flash('该学号已存在', 'danger')
                return redirect(url_for('add_student'))
                
            student = Student(student_id, name, gender, major, admission_year)
            class_manager.add_student(student)
            
            # 保存班级数据
            class_manager.save_to_file(DEFAULT_CLASS_FILE)
            
            flash('学生添加成功', 'success')
            return redirect(url_for('student_list'))
        except Exception as e:
            flash(f'添加失败: {str(e)}', 'danger')
            return redirect(url_for('add_student'))
    
    return render_template('add_student.html')

# 路由: 添加成绩
@app.route('/student/<student_id>/add_grade', methods=['GET', 'POST'])
@admin_required
def add_grade(student_id):
    student = class_manager.get_student(student_id)
    if not student:
        flash('学生不存在', 'danger')
        return redirect(url_for('student_list'))
    
    if request.method == 'POST':
        try:
            course_name = request.form['course_name'].strip()
            course_type = request.form['course_type']
            credit = float(request.form['credit'])
            score = int(request.form['score'])
            research = request.form['research']
            year = request.form['year']
            
            student.add_grade(course_name, course_type, credit, score, research, year)
            class_manager.save_to_file(DEFAULT_CLASS_FILE)
            
            flash('成绩添加成功', 'success')
            return redirect(url_for('student_detail', student_id=student_id))
        except Exception as e:
            flash(f'添加失败: {str(e)}', 'danger')
    
    return render_template('add_grade.html', student=student)

# 路由: 删除成绩
@app.route('/student/<student_id>/delete_grade/<course_name>', methods=['POST'])
@admin_required
def delete_grade(student_id, course_name):
    student = class_manager.get_student(student_id)
    if not student:
        flash('学生不存在', 'danger')
        return redirect(url_for('student_list'))
    
    try:
        student.delete_grade(course_name)
        class_manager.save_to_file(DEFAULT_CLASS_FILE)
        flash('成绩删除成功', 'success')
    except Exception as e:
        flash(f'删除失败: {str(e)}', 'danger')
    
    return redirect(url_for('student_detail', student_id=student_id))

# 路由: 设置班级名称
@app.route('/set_class_name', methods=['GET', 'POST'])
@admin_required
def set_class_name():
    if request.method == 'POST':
        class_name = request.form['class_name'].strip()
        class_manager.class_name = class_name
        class_manager.save_to_file(DEFAULT_CLASS_FILE)
        flash('班级名称设置成功', 'success')
        return redirect(url_for('index'))
    
    return render_template('set_class_name.html', class_name=class_manager.class_name)

# 路由: 班级统计报告
@app.route('/reports')
def reports():
    """显示班级统计报告"""
    students = class_manager.get_all_students()
    
    if not students:
        flash('暂无学生数据', 'info')
        return render_template('reports.html', 
                              class_name='未设置班级名称',
                              class_stats=[],
                              class_avg_score=0,
                              class_avg_gpa=0,
                              pass_rate=0)
    
    # 计算每个学生的统计数据
    class_stats = []
    
    # 班级汇总统计
    total_weighted_score = 0
    total_credits = 0
    total_gpa_weighted = 0
    pass_count = 0
    fail_count = 0
    
    for student in students:
        # 计算该学生的统计数据
        avg_score = student.calculate_weighted_average_score()
        avg_gpa = student.calculate_weighted_gpa()
        required_credits, total_student_credits = student.calculate_total_credits()
        count_90, count_95 = student.count_high_scores()
        
        # 判断是否及格
        if avg_score >= 60:
            pass_count += 1
        else:
            fail_count += 1
        
        # 累加班级统计数据
        if total_student_credits > 0:
            total_weighted_score += avg_score * total_student_credits
            total_gpa_weighted += avg_gpa * total_student_credits
            total_credits += total_student_credits
        
        # 添加到学生统计列表
        class_stats.append({
            'student_id': student.student_id,
            'name': student.name,
            'avg_score': avg_score,
            'avg_gpa': avg_gpa,
            'required_credits': required_credits,
            'total_credits': total_student_credits,
            'count_90': count_90,
            'count_95': count_95
        })
    
    # 按平均分排序
    class_stats.sort(key=lambda x: x['avg_score'], reverse=True)
    
    # 计算班级平均分和平均绩点
    class_avg_score = total_weighted_score / total_credits if total_credits > 0 else 0
    class_avg_gpa = total_gpa_weighted / total_credits if total_credits > 0 else 0
    
    # 计算及格率
    total_students = pass_count + fail_count
    pass_rate = pass_count / total_students if total_students > 0 else 0
    
    return render_template('reports.html', 
                          class_name=class_manager.class_name,
                          class_stats=class_stats,
                          class_avg_score=class_avg_score,
                          class_avg_gpa=class_avg_gpa,
                          pass_rate=pass_rate)

# 路由: 导出Excel
@app.route('/export_excel')
def export_excel():
    """导出Excel格式的成绩单"""
    try:
        if not os.path.exists(app.config['UPLOAD_FOLDER']):
            os.makedirs(app.config['UPLOAD_FOLDER'])
            
        filename = f'班级成绩_{datetime.now().strftime("%Y%m%d%H%M%S")}.xlsx'
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        
        # 导出数据
        class_manager.export_to_excel(filepath)
        
        # 发送文件
        return send_file(
            filepath,
            as_attachment=True,
            download_name=f'{class_manager.class_name}成绩表.xlsx'
        )
    except Exception as e:
        flash(f'导出失败: {str(e)}', 'danger')
        return redirect(url_for('reports'))

# 路由: 成绩分析
@app.route('/student/<student_id>/analysis')
def grade_analysis(student_id):
    """显示学生成绩分析"""
    student = class_manager.get_student(student_id)
    if not student:
        flash('学生不存在', 'danger')
        return redirect(url_for('student_list'))
    
    # 计算基础统计数据
    stats = {
        'avg_score': student.calculate_weighted_average_score(),
        'avg_gpa': student.calculate_weighted_gpa(),
        'required_credits': student.calculate_total_credits()[0],
        'total_credits': student.calculate_total_credits()[1],
        'count_90': student.count_high_scores()[0],
        'count_95': student.count_high_scores()[1]
    }
    
    # 生成详细分析数据
    analysis = {
        'weighted_average': stats['avg_score'],
        'weighted_gpa': stats['avg_gpa'],
        'total_credits': stats['total_credits'],
        'course_count': len(student.grades) if hasattr(student, 'grades') else 0,
        
        # 成绩分布
        'grade_dist': [0, 0, 0, 0, 0],  # <60, 60-69, 70-79, 80-89, 90-100
        
        # 课程类型统计
        'course_type_stats': {
            'required': 0,  # 必修课程数
            'elective': 0,  # 选修课程数
            'research': 0,  # 研究课程数
        },
        
        # 成绩趋势
        'trend': {
            'semesters': [],
            'scores': []
        },
        
        # 学分-成绩关系数据
        'credit_score_data': [],
        
        # 各类课程统计
        'stats': {
            'required': {'mean': 0, 'std': 0, 'max': 0, 'min': 100},
            'elective': {'mean': 0, 'std': 0, 'max': 0, 'min': 100},
            'research': {'mean': 0, 'std': 0, 'max': 0, 'min': 100},
            'lab': {'mean': 0, 'std': 0, 'max': 0, 'min': 100},
            'theory': {'mean': 0, 'std': 0, 'max': 0, 'min': 100},
            'all': {'mean': 0, 'std': 0, 'max': 0, 'min': 100}
        }
    }
    
    # 如果没有成绩记录，直接返回
    if not hasattr(student, 'grades') or not student.grades:
        return render_template('grade_analysis.html', student=student, stats=stats, analysis=analysis)
    
    # 统计各类数据
    required_scores = []
    elective_scores = []
    research_scores = []
    lab_scores = []
    theory_scores = []
    all_scores = []
    semester_score_map = {}  # 用于学期-平均分统计
    
    for grade in student.grades:
        score = float(grade['score'])
        credit = float(grade['credit'])
        course_type = grade['course_type']
        is_research = grade.get('research', '否') == '是'
        year = grade.get('year', '未知学期')
        
        # 添加到学分-成绩数据
        analysis['credit_score_data'].append({
            'x': credit,
            'y': score
        })
        
        # 成绩分布统计
        if score < 60:
            analysis['grade_dist'][0] += 1
        elif score < 70:
            analysis['grade_dist'][1] += 1
        elif score < 80:
            analysis['grade_dist'][2] += 1
        elif score < 90:
            analysis['grade_dist'][3] += 1
        else:
            analysis['grade_dist'][4] += 1
        
        # 课程类型统计
        if '必修' in course_type:
            analysis['course_type_stats']['required'] += 1
            required_scores.append(score)
        elif '选修' in course_type:
            analysis['course_type_stats']['elective'] += 1
            elective_scores.append(score)
        
        # 研究课程统计
        if is_research:
            analysis['course_type_stats']['research'] += 1
            research_scores.append(score)
        
        # 实验与理论课程分类
        if '实验' in course_type:
            lab_scores.append(score)
        else:
            theory_scores.append(score)
        
        # 所有课程成绩
        all_scores.append(score)
        
        # 学期成绩统计
        if year not in semester_score_map:
            semester_score_map[year] = []
        semester_score_map[year].append(score)
    
    # 计算各类课程的统计数据
    def calculate_stats(scores):
        if not scores:
            return {'mean': 0, 'std': 0, 'max': 0, 'min': 0}
        
        mean = sum(scores) / len(scores)
        variance = sum((x - mean) ** 2 for x in scores) / len(scores)
        std = variance ** 0.5
        
        return {
            'mean': mean,
            'std': std,
            'max': max(scores),
            'min': min(scores)
        }
    
    # 更新统计数据
    if required_scores:
        analysis['stats']['required'] = calculate_stats(required_scores)
    if elective_scores:
        analysis['stats']['elective'] = calculate_stats(elective_scores)
    if research_scores:
        analysis['stats']['research'] = calculate_stats(research_scores)
    if lab_scores:
        analysis['stats']['lab'] = calculate_stats(lab_scores)
    if theory_scores:
        analysis['stats']['theory'] = calculate_stats(theory_scores)
    if all_scores:
        analysis['stats']['all'] = calculate_stats(all_scores)
    
    # 学期成绩趋势
    semesters = sorted(semester_score_map.keys())
    analysis['trend']['semesters'] = semesters
    
    for semester in semesters:
        avg_score = sum(semester_score_map[semester]) / len(semester_score_map[semester])
        analysis['trend']['scores'].append(avg_score)
    
    return render_template('grade_analysis.html', student=student, stats=stats, analysis=analysis)

ALLOWED_EXTENSIONS = {'txt', 'xlsx'}

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/student/<student_id>/import_grades', methods=['POST'])
def import_grades(student_id):
    """导入成绩文件"""
    student = class_manager.get_student(student_id)
    if not student:
        flash('学生不存在', 'danger')
        return redirect(url_for('student_list'))
    
    if 'grade_file' not in request.files:
        flash('没有选择文件', 'danger')
        return redirect(url_for('add_grade', student_id=student_id))
    
    file = request.files['grade_file']
    if file.filename == '':
        flash('没有选择文件', 'danger')
        return redirect(url_for('add_grade', student_id=student_id))
    
    if file and allowed_file(file.filename):
        try:
            filename = secure_filename(file.filename)
            ext = filename.rsplit('.', 1)[1].lower()
            
            if ext == 'txt':
                # 处理txt文件
                grades = []
                for line in file:
                    line = line.decode('utf-8').strip()
                    if line:
                        # 概率与统计A,必修,3.0,5.0,100,是,大二学年
                        parts = line.split(',')
                        if len(parts) == 7:  # 确保格式正确
                            course_name, course_type, credit, _, score, research, year = parts
                            grades.append({
                                'course_name': course_name.strip(),
                                'course_type': course_type.strip(),
                                'credit': float(credit),
                                'score': int(score),
                                'research': research.strip(),
                                'year': year.strip()
                            })
            else:  # xlsx文件
                # 读取Excel文件
                df = pd.read_excel(file)
                grades = []
                for _, row in df.iterrows():
                    grades.append({
                        'course_name': str(row['课程名称']).strip(),
                        'course_type': str(row['课程性质']).strip(),
                        'credit': float(row['学分']),
                        'score': int(row['成绩']),
                        'research': str(row['是否保研课程']).strip(),
                        'year': str(row['学年']).strip()
                    })
            
            # 添加成绩记录
            success_count = 0
            error_messages = []
            for grade in grades:
                try:
                    student.add_grade(
                        grade['course_name'],
                        grade['course_type'],
                        grade['credit'],
                        grade['score'],
                        grade['research'],
                        grade['year']
                    )
                    success_count += 1
                except Exception as e:
                    error_messages.append(f"课程 '{grade['course_name']}' 导入失败：{str(e)}")
            
            # 保存更新
            class_manager.save_to_file(DEFAULT_CLASS_FILE)
            
            # 显示结果
            if success_count > 0:
                flash(f'成功导入 {success_count} 条成绩记录', 'success')
            if error_messages:
                for msg in error_messages:
                    flash(msg, 'warning')
                    
        except Exception as e:
            flash(f'文件处理失败: {str(e)}', 'danger')
    else:
        flash('不支持的文件格式', 'danger')
    
    return redirect(url_for('student_detail', student_id=student_id))

class UserLogin(UserMixin):
    def __init__(self, user):
        self.user = user
        self.id = user.username

@login_manager.user_loader
def load_user(username):
    user = user_manager.users.get(username)
    if user:
        return UserLogin(user)
    return None

# 登录路由
@app.route('/login', methods=['GET', 'POST'])
def login():
    # 如果用户已登录，直接跳转到首页
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        remember = 'remember' in request.form
        
        user = user_manager.verify_user(username, password)
        if user:
            user_login = UserLogin(user)
            # 如果选择记住我，设置30天的cookie过期时间
            if remember:
                login_user(user_login, remember=True, duration=timedelta(days=30))
            else:
                login_user(user_login)
            
            # 获取下一个页面的 URL
            next_page = request.args.get('next')
            # 确保 next_page 是相对路径
            if not next_page or '//' in next_page or ':' in next_page:
                next_page = url_for('index')
            
            flash('登录成功！', 'success')
            return redirect(next_page)
        
        flash('用户名或密码错误', 'danger')
    return render_template('login.html')

# 注册路由
@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        confirm_password = request.form['confirm_password']
        is_admin = 'is_admin' in request.form
        
        if password != confirm_password:
            flash('两次输入的密码不一致', 'danger')
            return render_template('register.html')
        
        try:
            user_manager.add_user(username, password, is_admin)
            flash('注册成功，请登录', 'success')
            return redirect(url_for('login'))
        except ValueError as e:
            flash(str(e), 'danger')
    
    return render_template('register.html')

# 登出路由
@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash('已退出登录', 'info')
    return redirect(url_for('login'))

# 添加图标路由
@app.route('/favicon.ico')
def favicon():
    return send_from_directory(os.path.join(app.root_path, 'static'),
                             'favicon.ico', mimetype='image/vnd.microsoft.icon')

# 添加离线访问清单
@app.route('/manifest.json')
def manifest():
    return send_from_directory(os.path.join(app.root_path, 'static'),
                             'manifest.json', mimetype='application/json')

# 添加服务工作线程
@app.route('/sw.js')
def service_worker():
    return send_from_directory(os.path.join(app.root_path, 'static'),
                             'sw.js', mimetype='application/javascript')

# 添加同步 API 路由
@app.route('/api/sync/student', methods=['POST'])
@login_required
def sync_student():
    try:
        if not request.is_xhr:
            return jsonify({'status': 'error', 'message': '无效的请求'}), 400
            
        data = request.json
        if not data:
            return jsonify({'status': 'error', 'message': '无效的数据'}), 400
            
        student = Student.from_dict(data)
        class_manager.add_student(student)
        class_manager.save_to_file(DEFAULT_CLASS_FILE)
        
        return jsonify({
            'status': 'success',
            'message': '学生数据同步成功'
        })
    except Exception as e:
        return jsonify({
            'status': 'error',
            'message': str(e)
        }), 400

@app.route('/api/sync/grade', methods=['POST'])
@login_required
def sync_grade():
    try:
        if not request.is_xhr:
            return jsonify({'status': 'error', 'message': '无效的请求'}), 400
            
        data = request.json
        if not data:
            return jsonify({'status': 'error', 'message': '无效的数据'}), 400
            
        student = class_manager.get_student(data['student_id'])
        if not student:
            return jsonify({
                'status': 'error',
                'message': '学生不存在'
            }), 404
            
        student.add_grade(
            data['course_name'],
            data['course_type'],
            data['credit'],
            data['score'],
            data['research'],
            data['year']
        )
        class_manager.save_to_file(DEFAULT_CLASS_FILE)
        
        return jsonify({
            'status': 'success',
            'message': '成绩数据同步成功'
        })
    except Exception as e:
        return jsonify({
            'status': 'error',
            'message': str(e)
        }), 400

@app.route('/student/<student_id>/fetch_grades', methods=['GET', 'POST'])
@admin_required
def fetch_grades(student_id):
    student = class_manager.get_student(student_id)
    if not student:
        flash('学生不存在', 'danger')
        return redirect(url_for('student_list'))
    
    if request.method == 'POST':
        try:
            # 获取表单数据
            website_url = request.form['website_url']
            username = request.form['username']
            password = request.form['password']
            
            # 获取成绩数据
            grades = fetch_grades_from_website(website_url, username, password)
            
            # 检查重复课程并添加新课程
            added_count = 0
            duplicates = []
            
            for grade in grades:
                # 检查是否已存在该课程
                existing_grade = next((g for g in student.grades if g['course_name'] == grade['course_name']), None)
                
                if existing_grade:
                    duplicates.append(grade['course_name'])
                else:
                    # 添加新课程
                    student.add_grade(
                        grade['course_name'],
                        grade['course_type'],
                        grade['credit'],
                        grade['score'],
                        grade.get('research', '否'),
                        grade.get('year', '大一学年')
                    )
                    added_count += 1
            
            # 保存更新
            class_manager.save_to_file(DEFAULT_CLASS_FILE)
            
            # 显示结果
            if added_count > 0:
                flash(f'成功导入 {added_count} 条成绩', 'success')
            if duplicates:
                flash(f'发现 {len(duplicates)} 门重复课程: {", ".join(duplicates)}', 'warning')
                
            return redirect(url_for('student_detail', student_id=student_id))
            
        except Exception as e:
            flash(f'获取成绩失败: {str(e)}', 'danger')
    
    return render_template('fetch_grades.html', student=student)

def fetch_grades_from_website(url, username, password):
    """从指定网站获取成绩数据"""
    try:
        # 登录并获取成绩页面
        session = requests.Session()
        
        # 登录
        login_data = {
            'username': username,
            'password': password
        }
        response = session.post(f"{url}/login", data=login_data)
        response.raise_for_status()
        
        # 获取成绩页面
        grades_page = session.get(f"{url}/grades")
        grades_page.raise_for_status()
        
        # 解析HTML
        soup = BeautifulSoup(grades_page.text, 'html.parser')
        
        # 解析成绩表格
        grades = []
        grade_rows = soup.select('table.grades-table tr')[1:]  # 跳过表头
        
        for row in grade_rows:
            cols = row.select('td')
            if len(cols) >= 6:
                grade = {
                    'course_name': cols[0].text.strip(),
                    'course_type': cols[1].text.strip(),
                    'credit': float(cols[2].text.strip()),
                    'score': int(cols[3].text.strip()),
                    'research': '是' if '是' in cols[4].text.strip() else '否',
                    'year': cols[5].text.strip()
                }
                grades.append(grade)
        
        return grades
    except Exception as e:
        raise Exception(f"获取成绩失败: {str(e)}")

@app.route('/student/<student_id>/edit_grade', methods=['POST'])
@admin_required
def edit_grade(student_id):
    student = class_manager.get_student(student_id)
    if not student:
        return jsonify({'status': 'error', 'message': '学生不存在'})
    
    try:
        # 获取表单数据
        original_course_name = request.form['original_course_name']
        course_name = request.form['course_name']
        course_type = request.form['course_type']
        credit = float(request.form['credit'])
        score = int(request.form['score'])
        research = request.form['research']
        year = request.form['year']
        
        # 删除原有课程
        student.delete_grade(original_course_name)
        
        # 添加修改后的课程
        student.add_grade(course_name, course_type, credit, score, research, year)
        
        # 保存更新
        class_manager.save_to_file(DEFAULT_CLASS_FILE)
        
        return jsonify({'status': 'success', 'message': '成绩修改成功'})
    except Exception as e:
        return jsonify({'status': 'error', 'message': str(e)})

# 路由: 天气详情页面
@app.route('/weather')
def weather_detail():
    """显示天气详情页面"""
    return render_template('weather_detail.html')

if __name__ == '__main__':
    app.run(debug=True) 