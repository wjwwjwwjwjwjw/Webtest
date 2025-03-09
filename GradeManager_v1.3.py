# -*- coding: utf-8 -*-

"""
班级成绩管理系统
Version: 1.3
"""

import tkinter as tk
from tkinter import messagebox, filedialog, Menu
from tkinter import ttk
from PIL import Image, ImageTk
import pytesseract
import pandas as pd
import re
import os
import platform
import json
import webbrowser
from datetime import datetime

# 如果Tesseract没有添加到系统环境变量，请指定Tesseract的路径
# 例如：
# pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

class Student:
    """
    学生类，存储学生基本信息和成绩
    """
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
    
    def add_grade(self, course_name, course_type, credit, score, research, year):
        # 数据验证
        if not isinstance(course_name, str):
            raise ValueError("课程名称必须是字符串，例如：'数学'")
        if course_type not in ["必修", "选修"]:
            raise ValueError("课程性质必须是 '必修' 或 '选修'")
        if not isinstance(credit, float) or credit <= 0:
            raise ValueError("学分必须是正浮点型，例如：'3.0'")
        if not isinstance(score, int) or score < 0 or score > 100:
            raise ValueError("成绩必须是0到100之间的整型，例如：'85'")
        if research not in ["是", "否"]:
            raise ValueError("保研课程与否必须是 '是' 或 '否'")
        if year not in ["大一学年", "大二学年", "大三学年", "大四学年"]:
            raise ValueError("学年必须是 '大一学年', '大二学年', '大三学年' 或 '大四学年'")

        # 计算绩点
        gpa = round(self.calculate_gpa_from_score(score), 1)

        # 添加到成绩列表
        self.grades.append({
            "course_name": course_name,
            "course_type": course_type,
            "credit": credit,
            "gpa": gpa,
            "score": score,
            "research": research,
            "year": year
        })
        
    def calculate_gpa_from_score(self, score):
        if score >= 90:
            return 4.0 + (score - 90) / 10
        elif score >= 60:
            return 1.0 + (score - 60) / 30 * 3
        else:
            return 0.0
            
    def calculate_weighted_average_score(self, include_all=True, research=False, year=None):
        total_score = 0
        total_credits = 0

        for grade in self.grades:
            if (include_all or grade["course_type"] == "必修") and \
               (not research or grade["research"] == "是") and \
               (year is None or grade["year"] == year):
                total_score += grade["score"] * grade["credit"]
                total_credits += grade["credit"]

        return total_score / total_credits if total_credits > 0 else 0

    def calculate_weighted_gpa(self, include_all=True, research=False, year=None):
        total_gpa = 0
        total_credits = 0

        for grade in self.grades:
            if (include_all or grade["course_type"] == "必修") and \
               (not research or grade["research"] == "是") and \
               (year is None or grade["year"] == year):
                total_gpa += grade["gpa"] * grade["credit"]
                total_credits += grade["credit"]

        return total_gpa / total_credits if total_credits > 0 else 0
        
    def count_high_scores(self, year=None):
        count_95 = 0
        count_90 = 0

        for grade in self.grades:
            if year is None or grade["year"] == year:
                if grade["score"] >= 95:
                    count_95 += 1
                if grade["score"] >= 90:
                    count_90 += 1

        return count_90, count_95
        
    def calculate_total_credits(self):
        required_credits = sum(grade['credit'] for grade in self.grades if grade['course_type'] == '必修')
        total_credits = sum(grade['credit'] for grade in self.grades)
        return required_credits, total_credits
        
    def delete_grade(self, course_name):
        grade_to_delete = next((grade for grade in self.grades if grade["course_name"] == course_name), None)
        if grade_to_delete:
            self.grades.remove(grade_to_delete)
        else:
            raise ValueError(f"课程 '{course_name}' 不存在，无法删除。")
            
    def get_grades(self):
        return self.grades
        
    def sort_grades(self, by="course_name"):
        if by == "course_name":
            self.grades.sort(key=lambda x: x["course_name"], reverse=True)
        elif by == "credit":
            self.grades.sort(key=lambda x: x["credit"], reverse=True)
        elif by == "score":
            self.grades.sort(key=lambda x: x["score"], reverse=True)
        elif by == "year":
            self.grades.sort(key=lambda x: x["year"], reverse=True)
            
    def search_grades(self, course_name):
        return [grade for grade in self.grades if course_name in grade["course_name"]]
        
    def filter_grades(self, by, value):
        if by == "credit":
            return [grade for grade in self.grades if grade["credit"] == value]
        elif by == "course_type":
            return [grade for grade in self.grades if grade["course_type"] == value]
        elif by == "research":
            return [grade for grade in self.grades if grade["research"] == value]
        elif by == "year":
            return [grade for grade in self.grades if grade["year"] == value]


class ClassManager:
    """
    班级管理类，用于管理班级信息和学生
    """
    def __init__(self, class_name=""):
        self.class_name = class_name
        self.students = {}  # 学号作为键，Student对象作为值
        
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
        
    def get_all_students(self):
        """获取所有学生列表"""
        return list(self.students.values())
        
    def get_student_ids(self):
        """获取所有学生学号列表"""
        return list(self.students.keys())
        
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
                
    def import_from_excel(self, filepath):
        """从Excel文件导入学生成绩"""
        try:
            df = pd.read_excel(filepath)
            # 检查必要的列
            required_columns = ["学号", "姓名", "课程名称", "课程性质", "学分", "成绩", "保研课程", "学年"]
            missing_columns = [col for col in required_columns if col not in df.columns]
            if missing_columns:
                raise ValueError(f"Excel文件缺少必要列: {', '.join(missing_columns)}")
                
            # 按学号分组
            for student_id, group in df.groupby("学号"):
                # 获取学生信息
                student_row = group.iloc[0]
                name = student_row["姓名"]
                gender = student_row.get("性别", "未知")
                major = student_row.get("专业", "未知")
                admission_year = student_row.get("入学年份", "")
                
                # 检查学生是否已存在
                student = self.get_student(student_id)
                if not student:
                    student = Student(student_id, name, gender, major, admission_year)
                    self.add_student(student)
                
                # 添加成绩
                for _, row in group.iterrows():
                    course_name = row["课程名称"]
                    course_type = row["课程性质"]
                    credit = float(row["学分"])
                    score = int(row["成绩"])
                    research = row["保研课程"]
                    year = row["学年"]
                    
                    # 检查课程是否已存在
                    existing_grade = next((g for g in student.grades if g["course_name"] == course_name), None)
                    if existing_grade:
                        # 这里应该向用户请求确认，但由于这是批量导入，我们默认跳过已存在的课程
                        continue
                    
                    student.add_grade(course_name, course_type, credit, score, research, year)
                    
            return True
            
        except Exception as e:
            raise ValueError(f"导入Excel文件失败: {str(e)}")
            
    def export_to_excel(self, filepath):
        """导出班级数据到Excel文件"""
        try:
            data = []
            for student_id, student in self.students.items():
                for grade in student.grades:
                    data.append({
                        "学号": student_id,
                        "姓名": student.name,
                        "性别": student.gender,
                        "专业": student.major,
                        "入学年份": student.admission_year,
                        "课程名称": grade["course_name"],
                        "课程性质": grade["course_type"],
                        "学分": grade["credit"],
                        "绩点": grade["gpa"],
                        "成绩": grade["score"],
                        "保研课程": grade["research"],
                        "学年": grade["year"]
                    })
            
            if not data:
                raise ValueError("没有数据可导出")
                
            df = pd.DataFrame(data)
            df.to_excel(filepath, index=False)
            return True
            
        except Exception as e:
            raise ValueError(f"导出Excel文件失败: {str(e)}")
            
    def generate_html_report(self, filepath, title="班级成绩报告"):
        """生成HTML报表"""
        try:
            # 创建HTML内容
            html_content = f"""
            <!DOCTYPE html>
            <html lang="zh-CN">
            <head>
                <meta charset="UTF-8">
                <meta name="viewport" content="width=device-width, initial-scale=1.0">
                <title>{title}</title>
                <style>
                    body {{
                        font-family: 'Microsoft YaHei', 'SimHei', sans-serif;
                        margin: 0;
                        padding: 20px;
                        background-color: #f5f5f5;
                    }}
                    .container {{
                        max-width: 1200px;
                        margin: 0 auto;
                        background-color: white;
                        padding: 20px;
                        box-shadow: 0 0 10px rgba(0,0,0,0.1);
                        border-radius: 5px;
                    }}
                    h1, h2, h3 {{
                        color: #333;
                    }}
                    .class-info {{
                        margin-bottom: 30px;
                        padding-bottom: 10px;
                        border-bottom: 1px solid #eee;
                    }}
                    .student-card {{
                        margin-bottom: 30px;
                        padding: 15px;
                        border: 1px solid #ddd;
                        border-radius: 5px;
                        background-color: #f9f9f9;
                    }}
                    .student-info {{
                        margin-bottom: 15px;
                    }}
                    .student-stats {{
                        margin: 15px 0;
                        padding: 10px;
                        background-color: #e9f7ef;
                        border-radius: 5px;
                    }}
                    table {{
                        width: 100%;
                        border-collapse: collapse;
                        margin-top: 10px;
                    }}
                    th, td {{
                        border: 1px solid #ddd;
                        padding: 8px;
                        text-align: center;
                    }}
                    th {{
                        background-color: #f2f2f2;
                    }}
                    tr:nth-child(even) {{
                        background-color: #f9f9f9;
                    }}
                    .fail {{
                        color: red;
                    }}
                    .class-stats {{
                        margin-top: 30px;
                        padding: 15px;
                        background-color: #edf7ff;
                        border-radius: 5px;
                    }}
                    .timestamp {{
                        text-align: right;
                        color: #888;
                        font-size: 0.8em;
                        margin-top: 30px;
                    }}
                </style>
            </head>
            <body>
                <div class="container">
                    <div class="class-info">
                        <h1>{title}</h1>
                        <p>班级名称: {self.class_name}</p>
                        <p>学生总数: {len(self.students)}</p>
                    </div>
            """
            
            # 班级统计信息
            class_stats = self.calculate_class_statistics()
            html_content += f"""
                <div class="class-stats">
                    <h2>班级统计</h2>
                    <p>平均绩点: {class_stats['avg_gpa']:.2f}</p>
                    <p>平均分数: {class_stats['avg_score']:.2f}</p>
                    <p>及格率: {class_stats['pass_rate']:.2f}%</p>
                    <p>优秀率(90分以上): {class_stats['excellent_rate']:.2f}%</p>
                </div>
            """
            
            # 按学生分别显示成绩
            for student_id, student in sorted(self.students.items()):
                html_content += f"""
                <div class="student-card">
                    <div class="student-info">
                        <h2>{student.name} ({student_id})</h2>
                        <p>性别: {student.gender} | 专业: {student.major} | 入学年份: {student.admission_year}</p>
                    </div>
                    
                    <div class="student-stats">
                        <h3>个人统计</h3>
                """
                
                # 计算个人统计数据
                avg_score = student.calculate_weighted_average_score()
                avg_gpa = student.calculate_weighted_gpa()
                required_credits, total_credits = student.calculate_total_credits()
                count_90, count_95 = student.count_high_scores()
                
                html_content += f"""
                        <p>加权平均分: {avg_score:.2f} | 加权绩点: {avg_gpa:.2f}</p>
                        <p>已修必修学分: {required_credits} | 总学分: {total_credits}</p>
                        <p>90分以上课程数: {count_90} | 95分以上课程数: {count_95}</p>
                    </div>
                    
                    <h3>成绩列表</h3>
                    <table>
                        <tr>
                            <th>课程名称</th>
                            <th>课程性质</th>
                            <th>学分</th>
                            <th>绩点</th>
                            <th>成绩</th>
                            <th>保研课程</th>
                            <th>学年</th>
                        </tr>
                """
                
                # 显示成绩
                for grade in sorted(student.grades, key=lambda x: x['score'], reverse=True):
                    fail_class = ' class="fail"' if grade['score'] < 60 else ''
                    gpa_display = f"{grade['gpa']:.1f}" if grade['score'] >= 60 else "未及格"
                    
                    html_content += f"""
                        <tr{fail_class}>
                            <td>{grade['course_name']}</td>
                            <td>{grade['course_type']}</td>
                            <td>{grade['credit']}</td>
                            <td>{gpa_display}</td>
                            <td>{grade['score']}</td>
                            <td>{grade['research']}</td>
                            <td>{grade['year']}</td>
                        </tr>
                    """
                
                html_content += """
                    </table>
                </div>
                """
            
            # 添加时间戳
            timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            html_content += f"""
                <div class="timestamp">
                    报告生成时间: {timestamp}
                </div>
            </div>
            </body>
            </html>
            """
            
            # 写入文件
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(html_content)
                
            return True
            
        except Exception as e:
            raise ValueError(f"生成HTML报表失败: {str(e)}")
            
    def calculate_class_statistics(self):
        """计算班级统计数据"""
        if not self.students:
            return {
                "avg_gpa": 0,
                "avg_score": 0,
                "pass_rate": 0,
                "excellent_rate": 0,
                "total_students": 0,
                "total_courses": 0
            }
            
        total_gpa = 0
        total_score = 0
        total_courses = 0
        passed_courses = 0
        excellent_courses = 0
        
        for student in self.students.values():
            for grade in student.grades:
                total_gpa += grade["gpa"]
                total_score += grade["score"]
                total_courses += 1
                
                if grade["score"] >= 60:
                    passed_courses += 1
                    
                if grade["score"] >= 90:
                    excellent_courses += 1
        
        return {
            "avg_gpa": total_gpa / total_courses if total_courses > 0 else 0,
            "avg_score": total_score / total_courses if total_courses > 0 else 0,
            "pass_rate": (passed_courses / total_courses * 100) if total_courses > 0 else 0,
            "excellent_rate": (excellent_courses / total_courses * 100) if total_courses > 0 else 0,
            "total_students": len(self.students),
            "total_courses": total_courses
        }


class GradeManagementGUI:
    """班级成绩管理系统的图形用户界面"""
    def __init__(self, root):
        self.root = root
        self.root.title("班级成绩管理系统 v1.3")
        self.root.geometry("1200x700")
        
        # 初始化班级管理器
        self.class_manager = ClassManager()
        self.current_student_id = None
        self.last_report_path = None
        
        # 设置主题
        style = ttk.Style()
        style.theme_use('clam')
        
        # 创建主窗口布局
        self.create_menu()
        self.create_main_layout()
        
    def create_menu(self):
        """创建菜单栏"""
        menubar = Menu(self.root)
        self.root.config(menu=menubar)
        
        # 文件菜单
        file_menu = Menu(menubar, tearoff=0)
        menubar.add_cascade(label="文件", menu=file_menu)
        file_menu.add_command(label="新建班级", command=self.new_class)
        file_menu.add_command(label="打开班级文件", command=self.open_class_file)
        file_menu.add_command(label="保存班级文件", command=self.save_class_file)
        file_menu.add_separator()
        file_menu.add_command(label="从Excel导入班级", command=self.import_class_from_excel)
        file_menu.add_command(label="导出班级到Excel", command=self.export_class_to_excel)
        file_menu.add_separator()
        file_menu.add_command(label="退出", command=self.root.quit)
        
        # 班级菜单
        class_menu = Menu(menubar, tearoff=0)
        menubar.add_cascade(label="班级", menu=class_menu)
        class_menu.add_command(label="修改班级名称", command=self.rename_class)
        class_menu.add_command(label="班级统计", command=self.show_class_statistics)
        class_menu.add_command(label="生成班级报表", command=self.generate_class_report)
        
        # 帮助菜单
        help_menu = Menu(menubar, tearoff=0)
        menubar.add_cascade(label="帮助", menu=help_menu)
        help_menu.add_command(label="使用说明", command=self.show_help)
        help_menu.add_command(label="关于", command=self.show_about)
        
    def create_main_layout(self):
        """创建主窗口布局"""
        # 创建左右分割的面板
        paned = ttk.PanedWindow(self.root, orient=tk.HORIZONTAL)
        paned.pack(fill=tk.BOTH, expand=True)
        
        # 左侧面板
        left_frame = ttk.Frame(paned)
        paned.add(left_frame, weight=1)
        
        # 右侧面板
        self.right_frame = ttk.Frame(paned)
        paned.add(self.right_frame, weight=3)
        
        # 在左侧创建标签页
        self.notebook = ttk.Notebook(left_frame)
        self.notebook.pack(fill=tk.BOTH, expand=True)
        
        # 创建各个标签页
        self.student_tab = ttk.Frame(self.notebook)
        self.add_grade_tab = ttk.Frame(self.notebook)
        self.stats_tab = ttk.Frame(self.notebook)
        self.sort_search_tab = ttk.Frame(self.notebook)
        self.file_tab = ttk.Frame(self.notebook)
        self.report_tab = ttk.Frame(self.notebook)
        
        self.notebook.add(self.student_tab, text="学生管理")
        self.notebook.add(self.add_grade_tab, text="添加成绩")
        self.notebook.add(self.stats_tab, text="统计信息")
        self.notebook.add(self.sort_search_tab, text="排序/查找")
        self.notebook.add(self.file_tab, text="文件操作")
        self.notebook.add(self.report_tab, text="网页报表")
        
        # 创建各个标签页的内容
        self.create_student_tab()
        self.create_add_grade_tab()
        self.create_stats_tab()
        self.create_sort_search_tab()
        self.create_file_tab()
        self.create_report_tab()
        self.create_right_frame()
        
        # 初始禁用依赖学生选择的控件
        self.disable_student_dependent_widgets()

    def get_chinese_font(self):
        """
        根据操作系统选择合适的中文字体
        """
        system = platform.system()
        if system == "Windows":
            return ("Microsoft YaHei", 10)
        elif system == "Darwin":  # macOS
            return ("Heiti SC", 10)
        else:  # Linux或其他
            return ("SimHei", 10)  # 确保SimHei已安装
            
    def create_student_tab(self):
        """创建学生管理标签页"""
        # 学生列表框架
        list_frame = ttk.LabelFrame(self.student_tab, text="学生列表")
        list_frame.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        # 学生列表
        self.student_listbox = tk.Listbox(list_frame, font=self.get_chinese_font())
        self.student_listbox.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        self.student_listbox.bind('<<ListboxSelect>>', self.on_student_selected)
        
        # 学生操作按钮
        button_frame = ttk.Frame(self.student_tab)
        button_frame.pack(fill=tk.X, padx=5, pady=5)
        
        add_student_button = ttk.Button(button_frame, text="添加学生", command=self.add_student)
        add_student_button.pack(side=tk.LEFT, padx=5, pady=5)
        
        edit_student_button = ttk.Button(button_frame, text="编辑学生", command=self.edit_student)
        edit_student_button.pack(side=tk.LEFT, padx=5, pady=5)
        
        delete_student_button = ttk.Button(button_frame, text="删除学生", command=self.delete_student)
        delete_student_button.pack(side=tk.LEFT, padx=5, pady=5)

    def create_add_grade_tab(self):
        # 使用Grid布局，减少垂直空间
        for i in range(6):
            self.add_grade_tab.columnconfigure(i, weight=1)

        # 学生选择
        student_label = ttk.Label(self.add_grade_tab, text="当前学生")
        student_label.grid(row=0, column=0, padx=5, pady=5, sticky=tk.E)
        
        self.current_student_label = ttk.Label(self.add_grade_tab, text="未选择学生")
        self.current_student_label.grid(row=0, column=1, padx=5, pady=5, sticky=tk.W)

        labels = ["课程名称", "课程性质", "学分", "成绩", "保研课程", "学年"]
        for idx, text in enumerate(labels):
            label = ttk.Label(self.add_grade_tab, text=text)
            label.grid(row=idx+1, column=0, padx=5, pady=5, sticky=tk.E)

        self.course_name_entry = ttk.Entry(self.add_grade_tab)
        self.course_name_entry.grid(row=1, column=1, padx=5, pady=5, sticky=tk.W)

        self.course_type_combo = ttk.Combobox(self.add_grade_tab, values=["必修", "选修"], state="readonly")
        self.course_type_combo.grid(row=2, column=1, padx=5, pady=5, sticky=tk.W)
        self.course_type_combo.current(0)

        self.credit_combo = ttk.Combobox(self.add_grade_tab, values=[0.5, 1.0, 1.5, 2.0, 2.5, 3.0, 3.5, 4.0, 4.5, 5.0, 5.5, 6.0], state="readonly")
        self.credit_combo.grid(row=3, column=1, padx=5, pady=5, sticky=tk.W)
        self.credit_combo.current(5)  # 默认3.0

        self.score_entry = ttk.Entry(self.add_grade_tab)
        self.score_entry.grid(row=4, column=1, padx=5, pady=5, sticky=tk.W)

        self.research_combo = ttk.Combobox(self.add_grade_tab, values=["是", "否"], state="readonly")
        self.research_combo.grid(row=5, column=1, padx=5, pady=5, sticky=tk.W)
        self.research_combo.current(1)

        self.year_combo = ttk.Combobox(self.add_grade_tab, values=["大一学年", "大二学年", "大三学年", "大四学年"], state="readonly")
        self.year_combo.grid(row=6, column=1, padx=5, pady=5, sticky=tk.W)
        self.year_combo.current(0)

        self.add_button = ttk.Button(self.add_grade_tab, text="添加成绩", command=self.add_grade)
        self.add_button.grid(row=7, column=0, columnspan=2, pady=10)

    def create_stats_tab(self):
        # 使用Frame分组统计控件
        frame = ttk.Frame(self.stats_tab)
        frame.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)

        # 上部选择区域
        selection_frame = ttk.Frame(frame)
        selection_frame.pack(fill=tk.X, padx=5, pady=5)

        # 学生选择
        student_label = ttk.Label(selection_frame, text="当前学生:")
        student_label.grid(row=0, column=0, padx=5, pady=5, sticky=tk.E)
        
        self.stats_student_label = ttk.Label(selection_frame, text="未选择学生")
        self.stats_student_label.grid(row=0, column=1, padx=5, pady=5, sticky=tk.W)

        # 数据选择
        stats_label = ttk.Label(selection_frame, text="统计类别:")
        stats_label.grid(row=1, column=0, padx=5, pady=5, sticky=tk.E)

        self.stats_options_combo = ttk.Combobox(selection_frame, values=["所有学科", "必修学科", "保研课程"], state="readonly")
        self.stats_options_combo.grid(row=1, column=1, padx=5, pady=5, sticky=tk.W)
        self.stats_options_combo.current(0)
        self.stats_options_combo.bind("<<ComboboxSelected>>", self.update_stats_label)

        # 学年筛选
        year_filter_label = ttk.Label(selection_frame, text="学年:")
        year_filter_label.grid(row=1, column=2, padx=5, pady=5, sticky=tk.E)

        self.year_filter_combo = ttk.Combobox(selection_frame, values=["总学年", "大一学年", "大二学年", "大三学年", "大四学年"], state="readonly")
        self.year_filter_combo.grid(row=1, column=3, padx=5, pady=5, sticky=tk.W)
        self.year_filter_combo.current(0)
        self.year_filter_combo.bind("<<ComboboxSelected>>", self.update_stats_label)

        # 中部显示区域
        self.stats_text = tk.Text(frame, height=15, state='disabled', wrap='word')
        self.stats_text.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)

    def create_sort_search_tab(self):
        # 使用 Notebook 分页
        sub_notebook = ttk.Notebook(self.sort_search_tab)
        sub_notebook.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)

        # 排序页
        sort_tab = ttk.Frame(sub_notebook)
        sub_notebook.add(sort_tab, text="排序")
        
        # 学生选择
        student_label = ttk.Label(sort_tab, text="当前学生:")
        student_label.grid(row=0, column=0, padx=5, pady=5, sticky=tk.E)
        
        self.sort_student_label = ttk.Label(sort_tab, text="未选择学生")
        self.sort_student_label.grid(row=0, column=1, padx=5, pady=5, sticky=tk.W)

        sort_label = ttk.Label(sort_tab, text="排序方式")
        sort_label.grid(row=1, column=0, padx=5, pady=5, sticky=tk.E)

        self.sort_combo = ttk.Combobox(sort_tab, values=["按课程名称降序", "按学分降序", "按成绩降序", "按学年降序"], state="readonly")
        self.sort_combo.grid(row=1, column=1, padx=5, pady=5, sticky=tk.W)
        self.sort_combo.current(0)

        sort_button = ttk.Button(sort_tab, text="排序", command=self.sort_grades)
        sort_button.grid(row=2, column=0, columnspan=2, pady=10)

        # 查找页
        search_tab = ttk.Frame(sub_notebook)
        sub_notebook.add(search_tab, text="查找")
        
        # 学生选择
        student_label = ttk.Label(search_tab, text="当前学生:")
        student_label.grid(row=0, column=0, padx=5, pady=5, sticky=tk.E)
        
        self.search_student_label = ttk.Label(search_tab, text="未选择学生")
        self.search_student_label.grid(row=0, column=1, padx=5, pady=5, sticky=tk.W)

        search_label = ttk.Label(search_tab, text="课程名称")
        search_label.grid(row=1, column=0, padx=5, pady=5, sticky=tk.E)

        self.search_entry = ttk.Entry(search_tab)
        self.search_entry.grid(row=1, column=1, padx=5, pady=5, sticky=tk.W)

        search_button = ttk.Button(search_tab, text="查找", command=self.search_grades)
        search_button.grid(row=2, column=0, columnspan=2, pady=10)

        show_all_button = ttk.Button(search_tab, text="显示所有课程", command=self.update_grades_listbox)
        show_all_button.grid(row=3, column=0, columnspan=2, pady=5)
        
    def create_file_tab(self):
        frame = ttk.Frame(self.file_tab)
        frame.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)

        # 个人成绩文件操作
        personal_frame = ttk.LabelFrame(frame, text="个人成绩文件")
        personal_frame.pack(fill=tk.X, padx=5, pady=5)
        
        # 学生选择
        student_label = ttk.Label(personal_frame, text="当前学生:")
        student_label.grid(row=0, column=0, padx=5, pady=5, sticky=tk.E)
        
        self.file_student_label = ttk.Label(personal_frame, text="未选择学生")
        self.file_student_label.grid(row=0, column=1, padx=5, pady=5, sticky=tk.W, columnspan=2)
        
        save_button = ttk.Button(personal_frame, text="保存成绩到文件", command=self.save_grades)
        save_button.grid(row=1, column=0, padx=5, pady=5)

        save_excel_button = ttk.Button(personal_frame, text="保存成绩到Excel文件", command=self.save_grades_to_excel)
        save_excel_button.grid(row=1, column=1, padx=5, pady=5)

        load_button = ttk.Button(personal_frame, text="导入成绩文件", command=self.load_grades)
        load_button.grid(row=2, column=0, padx=5, pady=5)

        load_excel_button = ttk.Button(personal_frame, text="从Excel导入成绩", command=self.load_grades_from_excel)
        load_excel_button.grid(row=2, column=1, padx=5, pady=5)

        ocr_button = ttk.Button(personal_frame, text="从截图导入成绩", command=self.import_grades_from_screenshot)
        ocr_button.grid(row=3, column=0, padx=5, pady=5, columnspan=2)
        
        # 班级文件操作
        class_frame = ttk.LabelFrame(frame, text="班级文件操作")
        class_frame.pack(fill=tk.X, padx=5, pady=5)
        
        save_class_button = ttk.Button(class_frame, text="保存班级数据", command=self.save_class_file)
        save_class_button.pack(fill=tk.X, padx=5, pady=5)
        
        load_class_button = ttk.Button(class_frame, text="导入班级数据", command=self.open_class_file)
        load_class_button.pack(fill=tk.X, padx=5, pady=5)
        
        import_excel_button = ttk.Button(class_frame, text="从Excel导入班级", command=self.import_class_from_excel)
        import_excel_button.pack(fill=tk.X, padx=5, pady=5)
        
        export_excel_button = ttk.Button(class_frame, text="导出班级到Excel", command=self.export_class_to_excel)
        export_excel_button.pack(fill=tk.X, padx=5, pady=5)

    def create_report_tab(self):
        """创建网页报表标签页"""
        frame = ttk.Frame(self.report_tab)
        frame.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        # 报表标题
        title_label = ttk.Label(frame, text="报表标题:")
        title_label.grid(row=0, column=0, padx=5, pady=5, sticky=tk.E)
        
        self.report_title_entry = ttk.Entry(frame, width=40)
        self.report_title_entry.grid(row=0, column=1, padx=5, pady=5, sticky=tk.W)
        self.report_title_entry.insert(0, "班级成绩报告")
        
        # 生成报表按钮
        generate_button = ttk.Button(frame, text="生成HTML报表", command=self.generate_html_report)
        generate_button.grid(row=1, column=0, padx=5, pady=5)
        
        # 查看报表按钮
        view_button = ttk.Button(frame, text="查看最近生成的报表", command=self.view_html_report)
        view_button.grid(row=1, column=1, padx=5, pady=5)
        
        # 说明文本
        info_text = ttk.Label(frame, text="注意: 报表将包含所有学生的成绩和统计数据")
        info_text.grid(row=2, column=0, columnspan=2, padx=5, pady=5)
        
        self.last_report_path = None  # 存储最近生成的报表路径

    def create_right_frame(self):
        # 成绩列表
        self.grades_treeview = ttk.Treeview(self.right_frame, columns=(
            "course_name", "course_type", "credit", "gpa", "score", "research", "year"), show="headings")
        self.grades_treeview.heading("course_name", text="课程名称")
        self.grades_treeview.heading("course_type", text="课程性质")
        self.grades_treeview.heading("credit", text="学分")
        self.grades_treeview.heading("gpa", text="绩点")
        self.grades_treeview.heading("score", text="成绩")
        self.grades_treeview.heading("research", text="保研课程")
        self.grades_treeview.heading("year", text="学年")

        for col in self.grades_treeview["columns"]:
            self.grades_treeview.column(col, anchor=tk.CENTER, stretch=True)

        self.grades_treeview.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)

        # 绑定事件
        self.grades_treeview.bind("<Double-1>", self.on_double_click)
        self.grades_treeview.bind("<Button-3>", self.show_context_menu)

        # 创建右键菜单
        self.context_menu = Menu(self.grades_treeview, tearoff=0)
        self.context_menu.add_command(label="删除", command=self.delete_grade)
        
    def disable_student_dependent_widgets(self):
        """禁用依赖于学生选择的控件"""
        self.add_button.config(state="disabled")
        # 可以根据需要禁用更多控件
        
    def enable_student_dependent_widgets(self):
        """启用依赖于学生选择的控件"""
        self.add_button.config(state="normal")
        # 可以根据需要启用更多控件
    
    def on_student_selected(self, event):
        """当学生列表中选择学生时触发"""
        selection = self.student_listbox.curselection()
        if not selection:
            return
            
        index = selection[0]
        student_display = self.student_listbox.get(index)
        # 假设格式为 "姓名 (学号)"
        student_id = student_display.split("(")[1].split(")")[0]
        
        self.current_student_id = student_id
        student = self.class_manager.get_student(student_id)
        
        if student:
            # 更新所有标签
            student_text = f"{student.name} ({student_id})"
            self.current_student_label.config(text=student_text)
            self.stats_student_label.config(text=student_text)
            self.sort_student_label.config(text=student_text)
            self.search_student_label.config(text=student_text)
            self.file_student_label.config(text=student_text)
            
            # 启用依赖学生的控件
            self.enable_student_dependent_widgets()
            
            # 更新成绩显示
            self.update_grades_listbox()
            
            # 更新统计信息
            self.update_stats_label()
    
    def add_student(self):
        """添加新学生"""
        dialog = StudentInputDialog(self.root)
        self.root.wait_window(dialog.top)
        
        if dialog.result:
            try:
                # 创建新学生
                student = Student(
                    dialog.result.get('student_id', ''),
                    dialog.result.get('name', ''),
                    dialog.result.get('gender', '未知'),
                    dialog.result.get('major', '未知'),
                    dialog.result.get('admission_year', '')
                )
                
                # 添加到班级
                self.class_manager.add_student(student)
                
                # 更新学生列表
                self.update_student_listbox()
                
                messagebox.showinfo("成功", "学生添加成功！")
                
            except ValueError as e:
                self.show_error(str(e))
    
    def edit_student(self):
        """编辑选中的学生"""
        if not self.current_student_id:
            messagebox.showwarning("警告", "请先选择一个学生")
            return
            
        student = self.class_manager.get_student(self.current_student_id)
        if not student:
            return
            
        dialog = StudentInputDialog(self.root, {
            'student_id': student.student_id,
            'name': student.name,
            'gender': student.gender,
            'major': student.major,
            'admission_year': student.admission_year
        })
        
        self.root.wait_window(dialog.top)
        
        if dialog.result:
            # 更新学生信息
            student.name = dialog.result.get('name', student.name)
            student.gender = dialog.result.get('gender', student.gender)
            student.major = dialog.result.get('major', student.major)
            student.admission_year = dialog.result.get('admission_year', student.admission_year)
            
            # 更新学生列表和标签
            self.update_student_listbox()
            self.on_student_selected(None)  # 刷新标签
            
            messagebox.showinfo("成功", "学生信息已更新！")
    
    def delete_student(self):
        """删除选中的学生"""
        if not self.current_student_id:
            messagebox.showwarning("警告", "请先选择一个学生")
            return
            
        confirm = messagebox.askyesno("确认", "确定要删除这个学生及其所有成绩记录吗？此操作不可撤销。")
        if confirm:
            if self.class_manager.remove_student(self.current_student_id):
                self.current_student_id = None
                self.update_student_listbox()
                self.update_grades_listbox([])  # 清空成绩显示
                
                # 重置所有学生标签
                self.current_student_label.config(text="未选择学生")
                self.stats_student_label.config(text="未选择学生")
                self.sort_student_label.config(text="未选择学生")
                self.search_student_label.config(text="未选择学生")
                self.file_student_label.config(text="未选择学生")
                
                # 禁用依赖学生的控件
                self.disable_student_dependent_widgets()
                
                messagebox.showinfo("成功", "学生已删除")
    
    def update_student_listbox(self):
        """更新学生列表显示"""
        self.student_listbox.delete(0, tk.END)
        for student_id, student in sorted(self.class_manager.students.items()):
            self.student_listbox.insert(tk.END, f"{student.name} ({student_id})")
            
        # 如果当前选中的学生已被删除，清除选择
        if self.current_student_id and self.current_student_id not in self.class_manager.students:
            self.current_student_id = None
    
    def add_grade(self):
        """为当前选中的学生添加成绩"""
        if not self.current_student_id:
            messagebox.showwarning("警告", "请先选择一个学生")
            return
            
        student = self.class_manager.get_student(self.current_student_id)
        if not student:
            return
            
        try:
            course_name = self.course_name_entry.get().strip()
            course_type = self.course_type_combo.get()
            credit = float(self.credit_combo.get())
            score = int(self.score_entry.get())
            research = self.research_combo.get()
            year = self.year_combo.get()

            student.add_grade(course_name, course_type, credit, score, research, year)
            messagebox.showinfo("成功", "成绩添加成功！")
            self.update_grades_listbox()
            self.clear_input_fields()
            self.update_stats_label()
        except ValueError as e:
            self.show_error(str(e))

    def clear_input_fields(self):
        """清空输入字段"""
        self.course_name_entry.delete(0, tk.END)
        self.score_entry.delete(0, tk.END)
        self.course_type_combo.current(0)
        self.credit_combo.current(5)
        self.research_combo.current(1)
        self.year_combo.current(0)

    def delete_grade(self):
        """删除选中的成绩"""
        if not self.current_student_id:
            messagebox.showwarning("警告", "请先选择一个学生")
            return
            
        selected_item = self.grades_treeview.selection()
        if not selected_item:
            return
            
        student = self.class_manager.get_student(self.current_student_id)
        if not student:
            return
            
        values = self.grades_treeview.item(selected_item[0], "values")
        course_name = values[0]
        try:
            student.delete_grade(course_name)
            messagebox.showinfo("成功", "课程删除成功！")
            self.update_grades_listbox()
            self.update_stats_label()
        except ValueError as e:
            self.show_error(str(e))

    def sort_grades(self):
        """按指定方式排序成绩"""
        if not self.current_student_id:
            messagebox.showwarning("警告", "请先选择一个学生")
            return
            
        student = self.class_manager.get_student(self.current_student_id)
        if not student:
            return
            
        sort_by = self.sort_combo.get()
        if sort_by == "按课程名称降序":
            student.sort_grades(by="course_name")
        elif sort_by == "按学分降序":
            student.sort_grades(by="credit")
        elif sort_by == "按成绩降序":
            student.sort_grades(by="score")
        elif sort_by == "按学年降序":
            student.sort_grades(by="year")
            
        self.update_grades_listbox()

    def search_grades(self):
        """搜索课程名称"""
        if not self.current_student_id:
            messagebox.showwarning("警告", "请先选择一个学生")
            return
            
        student = self.class_manager.get_student(self.current_student_id)
        if not student:
            return
            
        course_name = self.search_entry.get().strip()
        if not course_name:
            self.show_error("请输入要搜索的课程名称。")
            return
            
        filtered_grades = student.search_grades(course_name)
        if not filtered_grades:
            messagebox.showinfo("未找到", f"未找到包含 '{course_name}' 的课程。")
            
        self.update_grades_listbox(filtered_grades)


# 代码补充方案
    def update_grades_listbox(self, grades=None):
        """更新成绩列表显示"""
        for item in self.grades_treeview.get_children():
            self.grades_treeview.delete(item)
            
        if not self.current_student_id:
            return
            
        student = self.class_manager.get_student(self.current_student_id)
        if not student:
            return
            
        grades = grades if grades is not None else student.get_grades()
        for grade in grades:
            gpa_display = f"{grade['gpa']:.1f}" if grade["score"] >= 60 else "未及格"
            tag = "pass" if grade["score"] >= 60 else "fail"
            self.grades_treeview.insert("", tk.END, values=(
                grade["course_name"], grade["course_type"], grade["credit"], gpa_display, grade["score"],
                grade["research"], grade["year"]), tags=(tag,))
        self.grades_treeview.tag_configure("fail", foreground="red")

    def update_stats_label(self, event=None):
        """更新统计信息显示"""
        if not self.current_student_id:
            return
            
        student = self.class_manager.get_student(self.current_student_id)
        if not student:
            return
            
        # 获取用户选择的统计类别
        stats_option = self.stats_options_combo.get()
        if stats_option == "所有学科":
            include_all = True
            research = False
        elif stats_option == "必修学科":
            include_all = False
            research = False
        elif stats_option == "保研课程":
            include_all = False
            research = True
        else:
            include_all = True
            research = False

        # 获取用户选择的学年
        year_option = self.year_filter_combo.get()
        year = None if year_option == "总学年" else year_option

        # 计算统计数据
        avg_score = student.calculate_weighted_average_score(include_all=include_all, research=research, year=year)
        avg_gpa = student.calculate_weighted_gpa(include_all=include_all, research=research, year=year)
        count_90, count_95 = student.count_high_scores(year=year)
        required_credits, total_credits = student.calculate_total_credits()

        # 准备显示文本
        stats_text = f"学生: {student.name} ({student.student_id})\n"
        stats_text += f"专业: {student.major}\n\n"
        stats_text += f"统计类别: {stats_option}\n"
        stats_text += f"学年: {year_option}\n\n"
        stats_text += f"加权平均分: {avg_score:.2f}\n"
        stats_text += f"加权绩点: {avg_gpa:.2f}\n"
        stats_text += f"必修课总学分: {required_credits}\n"
        stats_text += f"总学分: {total_credits}\n"
        stats_text += f"90分以上课程数目: {count_90}\n"
        stats_text += f"95分以上课程数目: {count_95}\n"

        # 更新Text控件
        self.stats_text.config(state='normal')
        self.stats_text.delete(1.0, tk.END)
        self.stats_text.insert(tk.END, stats_text)
        self.stats_text.config(state='disabled')

    def on_double_click(self, event):
        """双击成绩条目时编辑成绩"""
        if not self.current_student_id:
            return
            
        selected_item = self.grades_treeview.selection()
        if not selected_item:
            return
            
        student = self.class_manager.get_student(self.current_student_id)
        if not student:
            return
            
        item = selected_item[0]
        values = self.grades_treeview.item(item, "values")
        dialog = GradeInputDialog(self.root, {
            'course_name': values[0],
            'course_type': values[1],
            'credit': values[2],
            'score': values[4],
            'research': values[5],
            'year': values[6]
        })
        self.root.wait_window(dialog.top)
        if dialog.result:
            try:
                student.delete_grade(values[0])
            except ValueError:
                pass
            try:
                student.add_grade(
                    dialog.result.get('course_name', values[0]),
                    dialog.result.get('course_type', values[1]),
                    float(dialog.result.get('credit', values[2])),
                    int(dialog.result.get('score', values[4])),
                    dialog.result.get('research', values[5]),
                    dialog.result.get('year', values[6])
                )
                self.update_grades_listbox()
                self.update_stats_label()
            except ValueError as e:
                self.show_error(str(e))

    def show_context_menu(self, event):
        """显示右键菜单"""
        if not self.current_student_id:
            return
            
        selected_item = self.grades_treeview.identify_row(event.y)
        if selected_item:
            self.grades_treeview.selection_set(selected_item)
            self.context_menu.post(event.x_root, event.y_root)

    def save_grades(self):
        """保存当前学生成绩到文件"""
        if not self.current_student_id:
            messagebox.showwarning("警告", "请先选择一个学生")
            return
            
        student = self.class_manager.get_student(self.current_student_id)
        if not student:
            return
            
        filepath = filedialog.asksaveasfilename(defaultextension=".txt",
                                                filetypes=[("Text files", "*.txt")])
        if filepath:
            try:
                with open(filepath, 'w', encoding='utf-8') as f:
                    for grade in student.grades:
                        f.write(
                            f"{grade['course_name']},{grade['course_type']},{grade['credit']},{grade['gpa']},{grade['score']},{grade['research']},{grade['year']}\n")
                messagebox.showinfo("成功", "成绩已保存到文件！")
            except Exception as e:
                self.show_error(f"保存文件失败: {e}")

    def save_grades_to_excel(self):
        """保存当前学生成绩到Excel文件"""
        if not self.current_student_id:
            messagebox.showwarning("警告", "请先选择一个学生")
            return
            
        student = self.class_manager.get_student(self.current_student_id)
        if not student:
            return
            
        filepath = filedialog.asksaveasfilename(defaultextension=".xlsx",
                                                filetypes=[("Excel files", "*.xlsx")])
        if filepath:
            try:
                df = pd.DataFrame(student.grades)
                df.columns = ['课程名称', '课程性质', '学分', '绩点', '成绩', '保研课程', '学年']
                df.to_excel(filepath, index=False)
                messagebox.showinfo("成功", "成绩已保存到Excel文件！")
            except Exception as e:
                self.show_error(f"保存Excel文件失败: {e}")

    def load_grades(self):
        """从文件导入成绩到当前学生"""
        if not self.current_student_id:
            messagebox.showwarning("警告", "请先选择一个学生")
            return
            
        student = self.class_manager.get_student(self.current_student_id)
        if not student:
            return
            
        filepath = filedialog.askopenfilename(filetypes=[("Text files", "*.txt")])
        if filepath:
            try:
                with open(filepath, 'r', encoding='utf-8') as f:
                    for line in f:
                        course_name, course_type, credit, gpa, score, research, year = line.strip().split(',')
                        # 检查课程是否已存在
                        existing_grade = next((g for g in student.grades if g["course_name"] == course_name), None)
                        if existing_grade:
                            continue  # 跳过已存在的课程
                        student.add_grade(course_name, course_type, float(credit), int(score), research, year)
                messagebox.showinfo("成功", "成绩文件已导入！")
                self.update_grades_listbox()
                self.update_stats_label()
            except Exception as e:
                self.show_error(f"导入文件失败: {e}")

    def load_grades_from_excel(self):
        """从Excel文件导入成绩到当前学生"""
        if not self.current_student_id:
            messagebox.showwarning("警告", "请先选择一个学生")
            return
            
        student = self.class_manager.get_student(self.current_student_id)
        if not student:
            return
            
        filepath = filedialog.askopenfilename(filetypes=[("Excel files", "*.xlsx")])
        if filepath:
            try:
                df = pd.read_excel(filepath)
                for _, row in df.iterrows():
                    course_name = row['课程名称']
                    course_type = row['课程性质']
                    credit = row['学分']
                    score = row['成绩']
                    research = row['保研课程']
                    year = row['学年']
                    
                    # 检查课程是否已存在
                    existing_grade = next((g for g in student.grades if g["course_name"] == course_name), None)
                    if existing_grade:
                        continue  # 跳过已存在的课程
                        
                    student.add_grade(course_name, course_type, float(credit), int(score), research, year)
                messagebox.showinfo("成功", "Excel成绩文件已导入！")
                self.update_grades_listbox()
                self.update_stats_label()
            except Exception as e:
                self.show_error(f"导入Excel文件失败: {e}")

    def import_grades_from_screenshot(self):
        """从截图导入成绩"""
        if not self.current_student_id:
            messagebox.showwarning("警告", "请先选择一个学生")
            return
            
        student = self.class_manager.get_student(self.current_student_id)
        if not student:
            return
            
        filepath = filedialog.askopenfilename(filetypes=[("Image files", "*.png;*.jpg;*.jpeg;*.bmp;*.tiff")])
        if filepath:
            try:
                image = Image.open(filepath)
                ocr_result = pytesseract.image_to_string(image, lang='chi_sim+eng')
                grades_data = self.parse_ocr_result(ocr_result)
                if not grades_data:
                    messagebox.showwarning("警告", "未能识别到任何成绩信息。")
                    return
                for grade in grades_data:
                    dialog = GradeInputDialog(self.root, grade)
                    self.root.wait_window(dialog.top)
                    if dialog.result:
                        student.add_grade(
                            dialog.result.get('course_name', grade.get('course_name', '')),
                            dialog.result.get('course_type', grade.get('course_type', '必修')),
                            float(dialog.result.get('credit', grade.get('credit', 3.0))),
                            int(dialog.result.get('score', grade.get('score', 0))),
                            dialog.result.get('research', grade.get('research', '否')),
                            dialog.result.get('year', grade.get('year', '大一学年'))
                        )
                messagebox.showinfo("成功", "从截图导入的成绩已添加。")
                self.update_grades_listbox()
                self.update_stats_label()
            except Exception as e:
                self.show_error(f"从截图导入失败: {e}")

    def parse_ocr_result(self, text):
        """解析OCR结果"""
        grades = []
        lines = text.split('\n')
        for line in lines:
            if not line.strip():
                continue
            match = re.match(r'(?P<course_name>[\u4e00-\u9fa5a-zA-Z0-9]+)\s+(?P<course_type>必修|选修)\s+(?P<credit>\d+(\.\d+)?)\s+(?P<score>\d{1,3})', line)
            if match:
                grade = {
                    'course_name': match.group('course_name'),
                    'course_type': match.group('course_type'),
                    'credit': float(match.group('credit')),
                    'score': int(match.group('score')),
                    'research': '否',
                    'year': '大一学年'
                }
                grades.append(grade)
        return grades

    def new_class(self):
        """创建新班级"""
        dialog = ClassNameDialog(self.root)
        self.root.wait_window(dialog.top)
        
        if dialog.result:
            class_name = dialog.result.get('class_name', '')
            if class_name:
                self.class_manager = ClassManager(class_name)
                self.update_student_listbox()
                self.update_grades_listbox([])
                
                # 重置所有学生标签
                self.current_student_id = None
                self.current_student_label.config(text="未选择学生")
                self.stats_student_label.config(text="未选择学生")
                self.sort_student_label.config(text="未选择学生")
                self.search_student_label.config(text="未选择学生")
                self.file_student_label.config(text="未选择学生")
                
                # 禁用依赖学生的控件
                self.disable_student_dependent_widgets()
                
                messagebox.showinfo("成功", f"已创建新班级: {class_name}")
                
    def open_class_file(self):
        """打开班级文件"""
        filepath = filedialog.askopenfilename(filetypes=[("JSON files", "*.json")])
        if filepath:
            try:
                self.class_manager.load_from_file(filepath)
                self.update_student_listbox()
                self.update_grades_listbox([])
                
                # 重置所有学生标签
                self.current_student_id = None
                self.current_student_label.config(text="未选择学生")
                self.stats_student_label.config(text="未选择学生")
                self.sort_student_label.config(text="未选择学生")
                self.search_student_label.config(text="未选择学生")
                self.file_student_label.config(text="未选择学生")
                
                # 禁用依赖学生的控件
                self.disable_student_dependent_widgets()
                
                messagebox.showinfo("成功", f"已加载班级: {self.class_manager.class_name}")
            except Exception as e:
                self.show_error(f"加载班级文件失败: {e}")
                
    def save_class_file(self):
        """保存班级文件"""
        filepath = filedialog.asksaveasfilename(defaultextension=".json",
                                                filetypes=[("JSON files", "*.json")])
        if filepath:
            try:
                self.class_manager.save_to_file(filepath)
                messagebox.showinfo("成功", "班级数据已保存！")
            except Exception as e:
                self.show_error(f"保存班级文件失败: {e}")
                
    def import_class_from_excel(self):
        """从Excel导入班级数据"""
        filepath = filedialog.askopenfilename(filetypes=[("Excel files", "*.xlsx")])
        if filepath:
            try:
                self.class_manager.import_from_excel(filepath)
                self.update_student_listbox()
                messagebox.showinfo("成功", "班级数据已从Excel导入！")
            except Exception as e:
                self.show_error(f"导入班级数据失败: {e}")
                
    def export_class_to_excel(self):
        """导出班级数据到Excel"""
        filepath = filedialog.asksaveasfilename(defaultextension=".xlsx",
                                                filetypes=[("Excel files", "*.xlsx")])
        if filepath:
            try:
                self.class_manager.export_to_excel(filepath)
                messagebox.showinfo("成功", "班级数据已导出到Excel！")
            except Exception as e:
                self.show_error(f"导出班级数据失败: {e}")
                
    def rename_class(self):
        """重命名班级"""
        dialog = ClassNameDialog(self.root, {'class_name': self.class_manager.class_name})
        self.root.wait_window(dialog.top)
        
        if dialog.result:
            class_name = dialog.result.get('class_name', '')
            if class_name:
                self.class_manager.class_name = class_name
                messagebox.showinfo("成功", f"班级已重命名为: {class_name}")
                
    def show_class_statistics(self):
        """显示班级统计信息"""
        stats = self.class_manager.calculate_class_statistics()
        
        stats_text = f"班级名称: {self.class_manager.class_name}\n\n"
        stats_text += f"学生总数: {stats['total_students']}\n"
        stats_text += f"课程总数: {stats['total_courses']}\n\n"
        stats_text += f"平均绩点: {stats['avg_gpa']:.2f}\n"
        stats_text += f"平均分数: {stats['avg_score']:.2f}\n"
        stats_text += f"及格率: {stats['pass_rate']:.2f}%\n"
        stats_text += f"优秀率(90分以上): {stats['excellent_rate']:.2f}%\n"
        
        messagebox.showinfo("班级统计", stats_text)
                
    def generate_html_report(self):
        """生成HTML报表"""
        title = self.report_title_entry.get().strip()
        if not title:
            title = "班级成绩报告"
            
        filepath = filedialog.asksaveasfilename(defaultextension=".html",
                                                filetypes=[("HTML files", "*.html")])
        if filepath:
            try:
                self.class_manager.generate_html_report(filepath, title)
                self.last_report_path = filepath
                messagebox.showinfo("成功", "HTML报表已生成！")
            except Exception as e:
                self.show_error(f"生成HTML报表失败: {e}")
                
    def view_html_report(self):
        """查看最近生成的HTML报表"""
        if self.last_report_path and os.path.exists(self.last_report_path):
            webbrowser.open(self.last_report_path)
        else:
            messagebox.showwarning("警告", "没有可查看的报表，请先生成报表。")
                
    def generate_class_report(self):
        """从菜单生成班级报表"""
        self.notebook.select(self.report_tab)
        self.generate_html_report()
                
    def show_help(self):
        """显示帮助信息"""
        help_text = """
班级成绩管理系统使用说明：

1. 学生管理：
- 添加、编辑、删除学生信息
- 在左侧列表中选择学生进行操作

2. 成绩管理：
- 为选中的学生添加成绩
- 双击成绩可以编辑
- 右键点击成绩可以删除

3. 统计信息：
- 查看学生的加权平均分、绩点等统计数据
- 可按不同类别和学年筛选

4. 文件操作：
- 导入/导出单个学生的成绩
- 导入/导出整个班级的数据
- 支持从截图识别成绩

5. 网页报表：
- 生成包含所有学生成绩的HTML报表
- 可在浏览器中查看和打印
        """
        messagebox.showinfo("使用说明", help_text)
                
    def show_about(self):
        """显示关于信息"""
        about_text = """
班级成绩管理系统 v1.3

功能：
- 多学生成绩管理
- 成绩统计分析
- 文件导入导出
- HTML报表生成

Copyright © 2023
        """
        messagebox.showinfo("关于", about_text)
                
    def show_error(self, error_message):
        """显示错误信息"""
        # 提供可能的解决方案
        suggestions = {
            "课程名称必须是字符串": "请检查课程名称的输入，确保其为文本格式，例如：'数学'。",
            "课程性质必须是 '必修' 或 '选修'": "请检查课程性质的选择，只能为'必修'或'选修'。",
            "学分必须是正浮点型": "请检查学分的输入，确保其为正浮点数，例如：'3.0'。",
            "成绩必须是0到100之间的整型": "请检查成绩的输入，确保其为0到100之间的整数，例如：'85'。",
            "保研课程与否必须是 '是' 或 '否'": "请检查保研课程的选择，只能为'是'或'否'。",
            "学年必须是 '大一学年', '大二学年', '大三学年' 或 '大四学年'": "请检查学年的选择，只能为'大一学年', '大二学年', '大三学年' 或 '大四学年'。",
            "课程名称不能为空。": "课程名称不能为空，请输入有效的课程名称。",
            "学号不能为空": "学号不能为空，请输入有效的学号。",
            "姓名不能为空": "姓名不能为空，请输入有效的姓名。"
        }
        
        for key in suggestions:
            if key in error_message:
                suggestion = suggestions[key]
                break
        else:
            suggestion = "请检查输入的数据格式是否正确。"
            
        messagebox.showerror("错误", f"{error_message}\n\n可能的解决方案：\n{suggestion}")


class StudentInputDialog:
    """学生信息输入对话框"""
    def __init__(self, parent, student_data=None):
        top = self.top = tk.Toplevel(parent)
        top.title("学生信息")
        top.grab_set()
        top.transient(parent)

        self.result = None
        
        # 使用Grid布局
        for i in range(5):
            top.columnconfigure(i, weight=1)
            
        # 学号
        student_id_label = ttk.Label(top, text="学号:")
        student_id_label.grid(row=0, column=0, padx=5, pady=5, sticky=tk.E)
        
        self.student_id_entry = ttk.Entry(top)
        self.student_id_entry.grid(row=0, column=1, padx=5, pady=5, sticky=tk.W)
        if student_data and 'student_id' in student_data:
            self.student_id_entry.insert(0, student_data['student_id'])
            self.student_id_entry.config(state='readonly')  # 学号不可修改
            
        # 姓名
        name_label = ttk.Label(top, text="姓名:")
        name_label.grid(row=1, column=0, padx=5, pady=5, sticky=tk.E)
        
        self.name_entry = ttk.Entry(top)
        self.name_entry.grid(row=1, column=1, padx=5, pady=5, sticky=tk.W)
        if student_data and 'name' in student_data:
            self.name_entry.insert(0, student_data['name'])
            
        # 性别
        gender_label = ttk.Label(top, text="性别:")
        gender_label.grid(row=2, column=0, padx=5, pady=5, sticky=tk.E)
        
        self.gender_combo = ttk.Combobox(top, values=["男", "女", "未知"], state="readonly")
        self.gender_combo.grid(row=2, column=1, padx=5, pady=5, sticky=tk.W)
        if student_data and 'gender' in student_data:
            if student_data['gender'] in ["男", "女", "未知"]:
                self.gender_combo.set(student_data['gender'])
            else:
                self.gender_combo.set("未知")
        else:
            self.gender_combo.set("未知")
            
        # 专业
        major_label = ttk.Label(top, text="专业:")
        major_label.grid(row=3, column=0, padx=5, pady=5, sticky=tk.E)
        
        self.major_entry = ttk.Entry(top)
        self.major_entry.grid(row=3, column=1, padx=5, pady=5, sticky=tk.W)
        if student_data and 'major' in student_data:
            self.major_entry.insert(0, student_data['major'])
            
        # 入学年份
        admission_year_label = ttk.Label(top, text="入学年份:")
        admission_year_label.grid(row=4, column=0, padx=5, pady=5, sticky=tk.E)
        
        self.admission_year_entry = ttk.Entry(top)
        self.admission_year_entry.grid(row=4, column=1, padx=5, pady=5, sticky=tk.W)
        if student_data and 'admission_year' in student_data:
            self.admission_year_entry.insert(0, student_data['admission_year'])
            
        # 按钮
        button_frame = ttk.Frame(top)
        button_frame.grid(row=5, column=0, columnspan=2, pady=10)
        
        self.ok_button = ttk.Button(button_frame, text="确定", command=self.on_ok)
        self.ok_button.pack(side=tk.LEFT, padx=5)
        
        self.cancel_button = ttk.Button(button_frame, text="取消", command=self.on_cancel)
        self.cancel_button.pack(side=tk.LEFT, padx=5)
        
    def on_ok(self):
        """确认按钮回调"""
        try:
            student_id = self.student_id_entry.get().strip()
            name = self.name_entry.get().strip()
            gender = self.gender_combo.get()
            major = self.major_entry.get().strip()
            admission_year = self.admission_year_entry.get().strip()
            
            if not student_id:
                raise ValueError("学号不能为空")
            if not name:
                raise ValueError("姓名不能为空")
                
            self.result = {
                'student_id': student_id,
                'name': name,
                'gender': gender,
                'major': major,
                'admission_year': admission_year
            }
            self.top.destroy()
        except ValueError as e:
            messagebox.showerror("错误", f"输入错误: {e}")
            
    def on_cancel(self):
        """取消按钮回调"""
        self.top.destroy()


class ClassNameDialog:
    """班级名称输入对话框"""
    def __init__(self, parent, data=None):
        top = self.top = tk.Toplevel(parent)
        top.title("班级名称")
        top.grab_set()
        top.transient(parent)

        self.result = None
        
        # 班级名称
        name_label = ttk.Label(top, text="班级名称:")
        name_label.grid(row=0, column=0, padx=5, pady=5, sticky=tk.E)
        
        self.name_entry = ttk.Entry(top, width=30)
        self.name_entry.grid(row=0, column=1, padx=5, pady=5, sticky=tk.W)
        if data and 'class_name' in data:
            self.name_entry.insert(0, data['class_name'])
        # ... 现有代码 ...
        
        # 按钮
        button_frame = ttk.Frame(top)
        button_frame.grid(row=1, column=0, columnspan=2, pady=10)
        
        self.ok_button = ttk.Button(button_frame, text="确定", command=self.on_ok)
        self.ok_button.pack(side=tk.LEFT, padx=5)
        
        self.cancel_button = ttk.Button(button_frame, text="取消", command=self.on_cancel)
        self.cancel_button.pack(side=tk.LEFT, padx=5)
        
    def on_ok(self):
        """确认按钮回调"""
        class_name = self.name_entry.get().strip()
        if class_name:
            self.result = {'class_name': class_name}
            self.top.destroy()
        else:
            messagebox.showerror("错误", "班级名称不能为空")
            
    def on_cancel(self):
        """取消按钮回调"""
        self.top.destroy()


class GradeInputDialog:
    """成绩输入对话框"""
    def __init__(self, parent, grade_data=None):
        top = self.top = tk.Toplevel(parent)
        top.title("成绩信息")
        top.grab_set()
        top.transient(parent)

        self.result = None
        
        # 使用Grid布局
        for i in range(6):
            top.columnconfigure(i, weight=1)

        labels = ["课程名称", "课程性质", "学分", "成绩", "保研课程", "学年"]
        for idx, text in enumerate(labels):
            label = ttk.Label(top, text=text)
            label.grid(row=idx, column=0, padx=5, pady=5, sticky=tk.E)

        self.course_name_entry = ttk.Entry(top)
        self.course_name_entry.grid(row=0, column=1, padx=5, pady=5, sticky=tk.W)
        if grade_data and 'course_name' in grade_data:
            self.course_name_entry.insert(0, grade_data['course_name'])

        self.course_type_combo = ttk.Combobox(top, values=["必修", "选修"], state="readonly")
        self.course_type_combo.grid(row=1, column=1, padx=5, pady=5, sticky=tk.W)
        if grade_data and 'course_type' in grade_data:
            if grade_data['course_type'] in ["必修", "选修"]:
                self.course_type_combo.set(grade_data['course_type'])
            else:
                self.course_type_combo.set("必修")
        else:
            self.course_type_combo.set("必修")

        self.credit_combo = ttk.Combobox(top, values=[0.5, 1.0, 1.5, 2.0, 2.5, 3.0, 3.5, 4.0, 4.5, 5.0, 5.5, 6.0], state="readonly")
        self.credit_combo.grid(row=2, column=1, padx=5, pady=5, sticky=tk.W)
        if grade_data and 'credit' in grade_data:
            self.credit_combo.set(grade_data['credit'])
        else:
            self.credit_combo.set(3.0)

        self.score_entry = ttk.Entry(top)
        self.score_entry.grid(row=3, column=1, padx=5, pady=5, sticky=tk.W)
        if grade_data and 'score' in grade_data:
            self.score_entry.insert(0, grade_data['score'])

        self.research_combo = ttk.Combobox(top, values=["是", "否"], state="readonly")
        self.research_combo.grid(row=4, column=1, padx=5, pady=5, sticky=tk.W)
        if grade_data and 'research' in grade_data:
            if grade_data['research'] in ["是", "否"]:
                self.research_combo.set(grade_data['research'])
            else:
                self.research_combo.set("否")
        else:
            self.research_combo.set("否")

        self.year_combo = ttk.Combobox(top, values=["大一学年", "大二学年", "大三学年", "大四学年"], state="readonly")
        self.year_combo.grid(row=5, column=1, padx=5, pady=5, sticky=tk.W)
        if grade_data and 'year' in grade_data:
            if grade_data['year'] in ["大一学年", "大二学年", "大三学年", "大四学年"]:
                self.year_combo.set(grade_data['year'])
            else:
                self.year_combo.set("大一学年")
        else:
            self.year_combo.set("大一学年")

        button_frame = ttk.Frame(top)
        button_frame.grid(row=6, column=0, columnspan=2, pady=10)
        
        self.ok_button = ttk.Button(button_frame, text="确定", command=self.on_ok)
        self.ok_button.pack(side=tk.LEFT, padx=5)
        
        self.cancel_button = ttk.Button(button_frame, text="取消", command=self.on_cancel)
        self.cancel_button.pack(side=tk.LEFT, padx=5)
        
    def on_ok(self):
        """确认按钮回调"""
        try:
            course_name = self.course_name_entry.get().strip()
            course_type = self.course_type_combo.get()
            credit = float(self.credit_combo.get())
            score = int(self.score_entry.get())
            research = self.research_combo.get()
            year = self.year_combo.get()
            
            if not course_name:
                raise ValueError("课程名称不能为空")
                
            self.result = {
                'course_name': course_name,
                'course_type': course_type,
                'credit': credit,
                'score': score,
                'research': research,
                'year': year
            }
            self.top.destroy()
        except ValueError as e:
            messagebox.showerror("错误", f"输入错误: {e}")
            
    def on_cancel(self):
        """取消按钮回调"""
        self.top.destroy()


if __name__ == "__main__":
    root = tk.Tk()
    app = GradeManagementGUI(root)
    root.mainloop()
                
