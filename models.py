# -*- coding: utf-8 -*-
import json
import pandas as pd
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash
import os

# 定义数据目录
DATA_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'data')
if not os.path.exists(DATA_DIR):
    os.makedirs(DATA_DIR)

class Student:
    """学生类，存储学生基本信息和成绩"""
    def __init__(self, student_id, name, gender="未知", major="未知", admission_year=""):
        self.student_id = student_id
        self.name = name
        self.gender = gender
        self.major = major
        self.admission_year = admission_year
        self.grades = []
        
    def to_dict(self):
        """将学生信息转换为字典格式"""
        return {
            "student_id": self.student_id,
            "name": self.name,
            "gender": self.gender,
            "major": self.major,
            "admission_year": self.admission_year,
            "grades": self.grades
        }
    
    @staticmethod
    def from_dict(data):
        """从字典创建学生对象"""
        student = Student(
            data["student_id"],
            data["name"],
            data.get("gender", "未知"),
            data.get("major", "未知"),
            data.get("admission_year", "")
        )
        student.grades = data.get("grades", [])
        return student
    
    def add_grade(self, course_name, course_type, credit, score, research="否", year=""):
        """添加一条成绩记录"""
        # 检查是否已存在该课程
        for grade in self.grades:
            if grade['course_name'] == course_name:
                raise ValueError(f"课程 '{course_name}' 已存在")
        
        # 计算绩点
        gpa = self.calculate_gpa_from_score(score)
        
        # 添加成绩记录
        self.grades.append({
            'course_name': course_name,
            'course_type': course_type,
            'credit': credit,
            'score': score,
            'gpa': gpa,
            'research': research,
            'year': year
        })
    
    def calculate_weighted_average_score(self):
        """计算加权平均分"""
        if not self.grades:
            return 0.0
        
        total_weighted_score = 0.0
        total_credits = 0.0
        
        for grade in self.grades:
            total_weighted_score += grade['score'] * grade['credit']
            total_credits += grade['credit']
        
        return total_weighted_score / total_credits if total_credits > 0 else 0.0
    
    def calculate_weighted_gpa(self):
        """计算加权平均绩点"""
        if not self.grades:
            return 0.0
        
        total_weighted_gpa = 0.0
        total_credits = 0.0
        
        for grade in self.grades:
            total_weighted_gpa += grade['gpa'] * grade['credit']
            total_credits += grade['credit']
        
        return total_weighted_gpa / total_credits if total_credits > 0 else 0.0
    
    def calculate_total_credits(self):
        """计算总学分和必修学分"""
        required_credits = 0.0
        total_credits = 0.0
        
        for grade in self.grades:
            total_credits += grade['credit']
            if grade['course_type'] == '必修':
                required_credits += grade['credit']
        
        return required_credits, total_credits
    
    def count_high_scores(self):
        """统计90分和95分以上的课程数量"""
        count_90 = 0
        count_95 = 0
        
        for grade in self.grades:
            score = grade['score']
            if score >= 95:
                count_95 += 1
                count_90 += 1
            elif score >= 90:
                count_90 += 1
        
        return count_90, count_95
    
    @staticmethod
    def calculate_gpa_from_score(score):
        """根据百分制分数计算绩点"""
        if score >= 90:
            return 4.0
        elif score >= 85:
            return 3.7
        elif score >= 82:
            return 3.3
        elif score >= 78:
            return 3.0
        elif score >= 75:
            return 2.7
        elif score >= 72:
            return 2.3
        elif score >= 68:
            return 2.0
        elif score >= 65:
            return 1.7
        elif score >= 64:
            return 1.5
        elif score >= 60:
            return 1.0
        else:
            return 0.0
    
    def analyze_grades(self):
        """分析学生成绩数据"""
        if not self.grades:
            return None
            
        # 基础统计
        total_credits = sum(float(grade['credit']) for grade in self.grades)
        weighted_sum = sum(float(grade['credit']) * float(grade['score']) for grade in self.grades)
        weighted_average = weighted_sum / total_credits if total_credits > 0 else 0
        
        # 计算加权GPA
        weighted_gpa = self.calculate_weighted_gpa()
        
        # 课程数量统计
        course_count = len(self.grades)
        
        # 成绩分布统计
        grade_dist = [0] * 5  # [<60, 60-69, 70-79, 80-89, 90-100]
        for grade in self.grades:
            score = float(grade['score'])
            if score < 60:
                grade_dist[0] += 1
            elif score < 70:
                grade_dist[1] += 1
            elif score < 80:
                grade_dist[2] += 1
            elif score < 90:
                grade_dist[3] += 1
            else:
                grade_dist[4] += 1
        
        # 课程类型统计
        course_types = {
            'required': [],
            'elective': [],
            'research': [],
            'lab': [],
            'theory': []
        }
        
        for grade in self.grades:
            if grade['course_type'] == '必修':
                course_types['required'].append(float(grade['score']))
            elif grade['course_type'] == '选修':
                course_types['elective'].append(float(grade['score']))
            if grade['research'] == '是':
                course_types['research'].append(float(grade['score']))
            
            # 根据课程名称判断是否为实验课
            if '实验' in grade['course_name'] or '实践' in grade['course_name']:
                course_types['lab'].append(float(grade['score']))
            else:
                course_types['theory'].append(float(grade['score']))
        
        # 计算各类课程统计数据
        stats = {
            'required': self._calculate_stats(course_types['required']),
            'elective': self._calculate_stats(course_types['elective']),
            'research': self._calculate_stats(course_types['research']),
            'lab': self._calculate_stats(course_types['lab']),
            'theory': self._calculate_stats(course_types['theory']),
            'all': self._calculate_stats([float(grade['score']) for grade in self.grades])
        }
        
        # 学期成绩趋势
        semesters = sorted(set(grade['year'] for grade in self.grades))
        semester_scores = []
        for semester in semesters:
            semester_grades = [g for g in self.grades if g['year'] == semester]
            if semester_grades:
                total_credits = sum(float(g['credit']) for g in semester_grades)
                weighted_sum = sum(float(g['credit']) * float(g['score']) for g in semester_grades)
                semester_scores.append(weighted_sum / total_credits if total_credits > 0 else 0)
        
        # 课程类型占比
        course_type_stats = {
            'required': len([g for g in self.grades if g['course_type'] == '必修']),
            'elective': len([g for g in self.grades if g['course_type'] == '选修']),
            'research': len([g for g in self.grades if g['research'] == '是'])
        }
        
        # 学分-成绩散点图数据
        credit_score_data = [
            {'x': float(grade['credit']), 'y': float(grade['score'])}
            for grade in self.grades
        ]
        
        # 课程相关性分析
        correlation_data = self._calculate_correlation()
        
        return {
            'weighted_average': weighted_average,
            'weighted_gpa': weighted_gpa,
            'total_credits': total_credits,
            'course_count': course_count,
            'grade_dist': grade_dist,
            'stats': stats,
            'trend': {
                'semesters': semesters,
                'scores': semester_scores
            },
            'course_type_stats': course_type_stats,
            'credit_score_data': credit_score_data,
            'correlation': correlation_data
        }
    
    def _calculate_stats(self, scores):
        """计算描述性统计数据"""
        if not scores:
            return {
                'mean': 0,
                'std': 0,
                'max': 0,
                'min': 0
            }
        
        import numpy as np
        return {
            'mean': np.mean(scores),
            'std': np.std(scores),
            'max': max(scores),
            'min': min(scores)
        }
    
    def _calculate_correlation(self):
        """计算课程类型间的相关性"""
        import numpy as np
        
        # 定义课程类型
        course_types = ['必修课程', '选修课程', '保研课程']
        
        # 获取各类型课程的成绩列表
        type_scores = {
            '必修课程': [float(g['score']) for g in self.grades if g['course_type'] == '必修'],
            '选修课程': [float(g['score']) for g in self.grades if g['course_type'] == '选修'],
            '保研课程': [float(g['score']) for g in self.grades if g['research'] == '是']
        }
        
        # 初始化相关系数矩阵
        correlation_matrix = []
        
        # 计算每种类型与其他类型的相关系数
        for type1 in course_types:
            scores1 = type_scores[type1]
            correlations = []
            
            for type2 in course_types:
                scores2 = type_scores[type2]
                
                if not scores1 or not scores2:
                    # 如果任一类型没有成绩，相关系数设为0
                    correlations.append(0)
                elif type1 == type2:
                    # 同一类型的相关系数为1
                    correlations.append(1)
                else:
                    try:
                        # 确保两个数组长度相同
                        min_len = min(len(scores1), len(scores2))
                        if min_len > 1:
                            # 计算皮尔逊相关系数
                            correlation = np.corrcoef(
                                scores1[:min_len],
                                scores2[:min_len]
                            )[0, 1]
                            # 处理无效值
                            correlations.append(
                                float(correlation) if not np.isnan(correlation) else 0
                            )
                        else:
                            correlations.append(0)
                    except Exception as e:
                        print(f"计算相关系数时出错 ({type1} vs {type2}): {e}")
                        correlations.append(0)
            
            correlation_matrix.append({
                'label': type1,
                'data': correlations
            })
        
        return {
            'labels': course_types,
            'datasets': correlation_matrix
        }
    
    def import_grades_from_file(self, filepath):
        """从文件导入成绩"""
        ext = filepath.rsplit('.', 1)[1].lower()
        
        if ext == 'txt':
            with open(filepath, 'r', encoding='utf-8') as f:
                for line in f:
                    line = line.strip()
                    if line:
                        course_name, course_type, credit, score, year, research = line.split(',')
                        self.add_grade(
                            course_name.strip(),
                            course_type.strip(),
                            float(credit),
                            int(score),
                            research.strip(),
                            year.strip()
                        )
        elif ext == 'xlsx':
            df = pd.read_excel(filepath)
            for _, row in df.iterrows():
                self.add_grade(
                    str(row['课程名称']).strip(),
                    str(row['课程性质']).strip(),
                    float(row['学分']),
                    int(row['成绩']),
                    str(row['是否保研课程']).strip(),
                    str(row['学年']).strip()
                )

class ClassManager:
    """班级管理类，用于管理班级信息和学生"""
    def __init__(self, class_name=""):
        self.class_name = class_name
        self.students = {}  # 学号作为键，Student对象作为值
        
    def get_all_students(self):
        """获取所有学生列表"""
        return list(self.students.values())
    
    def get_student_ids(self):
        """获取所有学生学号列表"""
        return list(self.students.keys())
        
    def add_student(self, student):
        """添加学生到班级"""
        if student.student_id in self.students:
            raise ValueError(f"学号 '{student.student_id}' 已存在")
        self.students[student.student_id] = student
        
    def remove_student(self, student_id):
        """从班级移除学生"""
        if student_id in self.students:
            del self.students[student_id]
            return True
        return False
        
    def get_student(self, student_id):
        """获取指定学号的学生"""
        return self.students.get(student_id)
        
    def save_to_file(self, filepath):
        """保存班级数据到文件"""
        data = {
            "class_name": self.class_name,
            "students": {id: student.to_dict() for id, student in self.students.items()}
        }
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
            
    def load_from_file(self, filepath):
        """从文件加载班级数据"""
        with open(filepath, 'r', encoding='utf-8') as f:
            data = json.load(f)
            self.class_name = data.get("class_name", "")
            self.students = {}
            for id, student_data in data.get("students", {}).items():
                self.students[id] = Student.from_dict(student_data)
        
    def export_to_excel(self, filepath):
        """导出班级成绩到Excel文件"""
        # 准备数据
        data = []
        for student in self.students.values():
            # 添加成绩信息
            for grade in student.grades:
                data.append({
                    '课程名称': grade['course_name'],
                    '课程性质': grade['course_type'],
                    '学分': grade['credit'],
                    '成绩': grade['score'],
                    '是否保研课程': grade['research'],
                    '学年': grade['year']
                })
        
        # 创建DataFrame并导出
        df = pd.DataFrame(data)
        # 调整列的顺序
        columns = ['课程名称', '课程性质', '学分', '成绩', '是否保研课程', '学年']
        df = df[columns]
        df.to_excel(filepath, index=False, engine='openpyxl')
        
    # ... 保留其他方法 (add_student, remove_student等) ... 

class User:
    def __init__(self, username, password_hash, is_admin=False):
        self.username = username
        self.password_hash = password_hash
        self.is_admin = is_admin
    
    def to_dict(self):
        return {
            'username': self.username,
            'password_hash': self.password_hash,
            'is_admin': self.is_admin
        }
    
    @staticmethod
    def from_dict(data):
        return User(
            data['username'],
            data['password_hash'],
            data.get('is_admin', False)
        )

class UserManager:
    def __init__(self):
        self.users = {}  # username -> User
        self.users_file = os.path.join(DATA_DIR, 'users.json')
    
    def add_user(self, username, password, is_admin=False):
        if username in self.users:
            raise ValueError('用户名已存在')
        
        password_hash = generate_password_hash(password)
        user = User(username, password_hash, is_admin)
        self.users[username] = user
        self.save_users()
    
    def verify_user(self, username, password):
        user = self.users.get(username)
        if user and check_password_hash(user.password_hash, password):
            return user
        return None
    
    def save_users(self):
        data = {username: user.to_dict() for username, user in self.users.items()}
        with open(self.users_file, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
    
    def load_users(self):
        try:
            with open(self.users_file, 'r', encoding='utf-8') as f:
                data = json.load(f)
                self.users = {username: User.from_dict(user_data) 
                            for username, user_data in data.items()}
        except FileNotFoundError:
            self.users = {} 