from PyQt6.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, 
                             QPushButton, QTextEdit, QListWidget, QTabWidget, QLabel, 
                             QTableWidget, QTableWidgetItem, QComboBox, QStackedWidget,QLineEdit,QFormLayout,QSplitter)
from PyQt6.QtCore import Qt

from PyQt6.QtGui import QTextCursor, QTextCharFormat,QColor
from PyQt6.QtWidgets import QFileDialog, QMessageBox

from PyQt6.QtWidgets import QWidget, QCheckBox, QSizePolicy,QLabel, QLineEdit, QPushButton, QTextEdit, QHBoxLayout, QVBoxLayout, QFormLayout, QGroupBox
from PyQt6.QtCore import QTimer, QMutex, QMutexLocker
from collections import defaultdict
from PyQt6.QtWidgets import QSplitter
from PyQt6.QtCore import QThread, pyqtSignal
from concurrent.futures import ThreadPoolExecutor

import qdarktheme

import sys
import pandas as pd
import re
import requests
import httpx
import asyncio
import os

import platform
from selenium import webdriver
from selenium.webdriver.edge.service import Service
from selenium.webdriver.edge.options import Options
from selenium.common.exceptions import TimeoutException, WebDriverException

from urllib.parse import urlparse
from requests.exceptions import RequestException
from bs4 import BeautifulSoup
from typing import List, Dict


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("文本处理工具")
        self.setGeometry(100, 100, 1000, 800)   # 设置窗口的位置和大小（x坐标，y坐标，宽度，高度）

        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        main_layout = QVBoxLayout(central_widget)

        self.tab_widget = QTabWidget()
        main_layout.addWidget(self.tab_widget)

        self.page6 = Page_js()
        self.tab_widget.addTab(self.page6, "JS接口测试")

class Page_js(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()
        self.the_number_of_objectives_for_multi_tasking = 0
        self.the_target_of_objectives_for_multi_tasking = []

    def initUI(self):
        layout = QVBoxLayout(self)

        # 定制该页面样式表
        nested_tab_widget = QTabWidget()
        nested_tab_widget.setStyleSheet("""
            QTabWidget::pane { 
                border: none;
                top: 0px;
            }
            QTabWidget::tab-bar {
                left: 5px;
            }
            QTabBar::tab {
                background: qlineargradient(x1: 0, y1: 0, x2: 0, y2: 1,
                                            stop: 0 #e6e6e6, stop: 0.4 #d9d9d9,
                                            stop: 0.5 #d3d3d3, stop: 1.0 #c7c7c7);
                border: 1px solid #c4c4c4;
                border-bottom-color: #c2c7cb;
                border-top-left-radius: 4px;
                border-top-right-radius: 4px;
                min-width: 8ex;
                padding: 2px;
                color: #333333;
            }
            QTabBar::tab:selected, QTabBar::tab:hover {
                background: #ffffff;
                color: #000000;
            }
            QTabBar::tab:selected {
                border-color: #9b9b9b;
                border-bottom-color: #ffffff;
            }
        """)
        layout.addWidget(nested_tab_widget)

        # 创建第一个嵌套页面
        page_js_1 = self.create_page1()
        nested_tab_widget.addTab(page_js_1, "JS接口发现")

        # 创建第二个嵌套页面
        page_js_3 = self.create_page3()
        nested_tab_widget.addTab(page_js_3, "测试接口状态")

        # 创建第三个嵌套页面
        page_js_2 = self.create_page2()
        nested_tab_widget.addTab(page_js_2, "请求信息配置")

        # 创建第三个嵌套页面
        page_js_4 = self.create_page4()
        nested_tab_widget.addTab(page_js_4, "多目标扫描")

        page_js_5 = self.create_page5()
        nested_tab_widget.addTab(page_js_5, "目录深度扫描")

        self.setStyleSheet("""
            QWidget {
                background-color: #333333; /* 浅灰色背景 */
                font-family: 'Arial', sans-serif; /* 设置字体 */
                font-size: 14px; /* 设置字体大小 */
            }
                        

            QLineEdit, QTextEdit {
                background-color: #010101;
                border: 1px solid white;
                border-radius: 3px;
                padding: 5px;
            }
            QPushButton {
                padding: 6px 15px;
                background-color: #4CAF50;
                color: white;
            }
            
            QCheckBox {
                margin-top: 0px;  
                margin-bottom: 0px;  
            }

        """)

    def create_page1(self):
        page = QWidget()
        layout = QVBoxLayout(page)

        # 顶部正则选项卡
        top_regular_mode = QHBoxLayout()
        top_regular_mode.setAlignment(Qt.AlignmentFlag.AlignRight) 
        top_regular_mode_label = QLabel("使用的正则匹配模块:")
        self.checkbox_findsomething = QCheckBox('findsomething', self)
        self.checkbox_JSFinder = QCheckBox('JSFinder', self)
        # 设置复选框的初始状态
        self.checkbox_findsomething.setChecked(True)  # findsomething 初始为选中状态
        self.checkbox_JSFinder.setChecked(False)  # JSFinder 初始为未选中状态
        top_regular_mode.addWidget(top_regular_mode_label)
        top_regular_mode.addWidget(self.checkbox_findsomething)
        top_regular_mode.addWidget(self.checkbox_JSFinder)
        layout.addLayout(top_regular_mode)

        # 顶部输入URL和获取按钮
        top_layout = QHBoxLayout()
        self.page1_url_input = QLineEdit()
        get_button = QPushButton("获取")
        top_layout.addWidget(self.page1_url_input)
        top_layout.addWidget(get_button)
        layout.addLayout(top_layout)

        # 中间部分，分为左右两列
        mid_layout = QHBoxLayout()

        # 左侧布局
        left_layout = QVBoxLayout()
        
        # JS路径部分
        js_path_label = QLabel("获取的JS路径:")
        left_layout.addWidget(js_path_label)
        self.page1_js_path_output = QTextEdit()
        left_layout.addWidget(self.page1_js_path_output)

        # 域名部分
        domain_label = QLabel("扫描进度信息:")
        left_layout.addWidget(domain_label)
        self.page1_domain_output = QTextEdit()
        left_layout.addWidget(self.page1_domain_output)

        # 设置比例
        left_layout.setStretchFactor(self.page1_js_path_output, 3)  # 1.5比例
        left_layout.setStretchFactor(self.page1_domain_output, 2)  # 1比例

        mid_layout.addLayout(left_layout)


        # 右侧布局
        right_layout = QVBoxLayout()
        self.page1_api_list_output = QTextEdit()
        right_layout.addWidget(QLabel("接口列表:"))
        right_layout.addWidget(self.page1_api_list_output)
        mid_layout.addLayout(right_layout)

        # 将左右布局添加到主布局
        layout.addLayout(mid_layout)

        # 设置一些基本样式
        page.setStyleSheet("""
            QLineEdit, QTextEdit {
                border: 1px solid white;
                border-radius: 3px;
                padding: 5px;
            }
            QPushButton {
                padding: 6px 15px;
                background-color: #4CAF50;
                color: white;
            }
            QCheckBox {
                margin-top: 0px;  
                margin-bottom: 0px;  
            }
        """)
        # layout.setSpacing(1)
        # 连接按钮信号到槽函数
        get_button.clicked.connect(self.process_js1)

        return page

    def process_js1(self):
        self.thread = None
        self.page1_api_list_output.clear()
        self.page1_js_path_output.clear()

        def displayResult(result):
            self.page1_js_path_output.append(result)

        def displayResult_path(result):
            self.page1_api_list_output.append(result)

        def displayError(error):
            self.page1_domain_output.append(f"-{error}")
            # self.page1_api_list_output.append(f"Error occurred: {error}")



        # 这里可以添加获取URL、JS路径、域名和接口列表的逻辑
        url = self.page1_url_input.text()

        if not url:
            self.page1_api_list_output.setText("请输入一个url")
            return
        
        if self.thread and self.thread.isRunning():
            self.page1_api_list_output.setText("一个目标正在运行中，请等待...")
            return
        
        options = {
            'findsomething': self.checkbox_findsomething.isChecked(),
            'JSFinder': self.checkbox_JSFinder.isChecked(),
        }

        self.page1_domain_output.setText("开始扫描...")
        self.thread = JSFinderThread(url,options)
        self.thread.resultSignal.connect(displayResult)
        self.thread.resultSignal_path.connect(displayResult_path)
        self.thread.errorSignal.connect(displayError)
        self.thread.start()

    def create_page3(self):
        page = QWidget()
        layout = QVBoxLayout(page)

        # 顶部配置选项卡
        top_regular_mode = QHBoxLayout()

        top_text_filtering_label = QLabel("是否启用文本过滤:")
        self.checkbox_text_filtering = QCheckBox('启用', self)
        top_regular_mode.setAlignment(Qt.AlignmentFlag.AlignRight)
        top_regular_mode_label = QLabel("选择显示状态码范围:")
        self.status_code_range_299 = QCheckBox('200~299',self)
        self.status_code_range_399 = QCheckBox('300~399',self) 
        # 设置复选框的初始状态
        self.status_code_range_299.setChecked(True)  # 200~299 初始为选中状态
        self.status_code_range_399.setChecked(False)  # 300~399 初始为未选中状态
        self.checkbox_text_filtering.setChecked(False)  # 启用 初始为选中状态
        top_regular_mode.addWidget(top_text_filtering_label)
        top_regular_mode.addWidget(self.checkbox_text_filtering)
        top_regular_mode.addStretch()
        top_regular_mode.addWidget(top_regular_mode_label)
        top_regular_mode.addWidget(self.status_code_range_299)
        top_regular_mode.addWidget(self.status_code_range_399)
        layout.addLayout(top_regular_mode)

        # 顶部域名输入框
        top_layout = QHBoxLayout()
        top_target_domain_label = QLabel("目标域名:")
        self.page3_domain_input = QLineEdit()
        top_layout.addWidget(top_target_domain_label)
        top_layout.addWidget(self.page3_domain_input)
        layout.addLayout(top_layout)

        # 下面布局，需要分三列
        tail_layout = QHBoxLayout()

        # 左侧接口输入框
        left_layout = QVBoxLayout()
        self.page3_api_text_input = QTextEdit()
        left_layout.addWidget(QLabel("接口列表:"))
        left_layout.addWidget(self.page3_api_text_input)
        # tail_layout.addLayout(left_layout)

        # 中间部分
        mid_layout = QVBoxLayout()
        self.page3_mid_api_input = QLineEdit()
        add_to_directory_button = QPushButton("添加前置目录")
        add_to_directory_button.clicked.connect(self.process3_add_front_loaded_directory)
        replace_the_directory_button = QPushButton("替换./目录")
        replace_the_directory_button.clicked.connect(self.process3_replace_the_directory)
        self.checkbox_GET = QCheckBox('GET', self)
        self.checkbox_POST = QCheckBox('POST', self)
        obtain_the_interface_status_button = QPushButton("获取接口状态")
        obtain_the_interface_status_button.clicked.connect(self.process3_api_httpx)  
        self.directions_for_use_line_edit = QTextEdit()
        self.directions_for_use_line_edit.setText("使用说明\n\n1、可输入接口前置目录\n2、左侧输入接口地址\n3、选择请求方式\n4、获取接口状态") #使用说明文本框的初始内容
        self.directions_for_use_line_edit.setStyleSheet("color: yellow;")
        self.directions_for_use_line_edit.setReadOnly(True)

        # 增加控件间距和间隔
        mid_layout.addSpacing(70)  # 在顶部增加一些空间
        mid_layout.addWidget(self.page3_mid_api_input)
        mid_layout.addWidget(add_to_directory_button)
        mid_layout.addWidget(replace_the_directory_button)
        mid_layout.addSpacing(50)  # 在按钮和标签之间增加空间
        mid_layout.addWidget(QLabel("请求方式:"))
        mid_layout.addWidget(self.checkbox_GET)
        mid_layout.addWidget(self.checkbox_POST)
        mid_layout.addSpacing(10)  # 在复选框和按钮之间增加空间
        mid_layout.addWidget(obtain_the_interface_status_button)
        mid_layout.addSpacing(20)  # 在按钮和说明文本之间增加空间
        mid_layout.addWidget(self.directions_for_use_line_edit)
        mid_layout.addStretch(1)  # 将剩余空间推到最底部
        # tail_layout.addLayout(mid_layout)






        # 右侧显示部分
        right_layout = QVBoxLayout()
        self.page3_request_result_output = QTextEdit()
        right_layout.addWidget(QLabel("请求结果:"))
        right_layout.addWidget(self.page3_request_result_output)
        # tail_layout.addLayout(right_layout)


        left_widget = QWidget()
        left_widget.setLayout(left_layout)
        mid_widget = QWidget()
        mid_widget.setLayout(mid_layout)
        right_widget = QWidget()
        right_widget.setLayout(right_layout)

        tail_layout.addWidget(left_widget)
        tail_layout.addWidget(mid_widget)
        tail_layout.addWidget(right_widget)

        tail_layout.setStretchFactor(left_widget, 4)
        tail_layout.setStretchFactor(mid_widget, 3)
        tail_layout.setStretchFactor(right_widget, 6)

        # 然后将splitter添加到布局中

        layout.addLayout(tail_layout)

        page.setStyleSheet("""
            QLineEdit, QTextEdit {
                border-radius: 3px;
                padding: 5px;
            }
            QPushButton {
                padding: 6px 15px;
                background-color: #4CAF50;
                color: white;
            }
            QCheckBox {
                margin-top: 0px;  
                margin-bottom: 0px;  
            }
        """)



        return page

    def process3_add_front_loaded_directory(self):
        api_text = self.page3_api_text_input.toPlainText()
        front_directory = self.page3_mid_api_input.text()
        if front_directory and front_directory.strip():  # 检查输入是否为空或仅包含空白字符
            # self.page3_request_result_output.setPlainText("进去啦")
            if not front_directory.startswith('/'):
                front_directory = '/' + front_directory
            if front_directory.endswith('/'):
                front_directory = front_directory[:-1]

        front_directory_api_lists = []
        if not api_text:
            return
        split_lists = [line.strip() for line in api_text.split('\n') if line.strip()]
        self.page3_api_text_input.clear()
        for api_list in split_lists:
            if api_list[0:2] == "//":
                api_list_complete = front_directory+"/" +api_list[2:]
            elif api_list[0:1] == "/":
                api_list_complete = front_directory + api_list
            else:
                api_list_complete = front_directory + "/" +api_list

            front_directory_api_lists.append(api_list_complete)

        self.page3_api_text_input.setPlainText('\n'.join(front_directory_api_lists))

    def process3_replace_the_directory(self):
        api_text = self.page3_api_text_input.toPlainText()
        front_directory = self.page3_mid_api_input.text()
        if front_directory and front_directory.strip():  # 检查输入是否为空或仅包含空白字符
            # self.page3_request_result_output.setPlainText("进去啦")
            if not front_directory.startswith('/'):
                front_directory = '/' + front_directory
            if front_directory.endswith('/'):
                front_directory = front_directory[:-1]
        
        front_directory_api_lists = []
        if not api_text:
            return
        split_lists = [line.strip() for line in api_text.split('\n') if line.strip()]
        self.page3_api_text_input.clear()
        for api_list in split_lists:
            if api_list[0:2] == "//":
                api_list_complete = "/" + api_list[2:]
                # api_list_complete = api_list[2:]
            elif api_list[0:1] == "/":
                api_list_complete = api_list
            elif api_list[0:3] == "../":
                # api_list_complete = api_list
                URL = self.page3_domain_input.text()
                URL_raw = urlparse(URL)
                path_URL = URL_raw.path   # 初始路径
                # ab_URL = URL_raw.netloc   # 域名
                # host_URL = URL_raw.scheme # 协议
                path_URL = '/'.join(path_URL.split('/')[:-1]) + '/'
                full_path = os.path.normpath(os.path.join(path_URL, api_list))
                api_list_complete = f"{full_path}"
            elif api_list[0:2] == "./":
                    if front_directory and front_directory.strip(): # 检查输入是否为空或仅包含空白字符
                        api_list_complete = front_directory + "/" + api_list[2:]
                    else:
                        api_list_complete = api_list

            else:
                api_list_complete = "/" + api_list
                

            front_directory_api_lists.append(api_list_complete)

        self.page3_api_text_input.setPlainText('\n'.join(front_directory_api_lists))

    def process3_api_httpx(self):
        self.thread_httpx = None
        target_domain_url = self.page3_domain_input.text()


        target_api = self.page3_api_text_input.toPlainText()
        self.page3_request_result_output.clear()


        def displayResult(result):
            self.page3_request_result_output.append(result)


        def displayError(error):
            self.page3_request_result_output.append(f"Error occurred: {error}")


        if not target_domain_url:
            self.page3_request_result_output.setText("请输入目标域名")
            return

        target_domain_raw = urlparse(target_domain_url)
        target_domain = target_domain_raw.scheme + "://" + target_domain_raw.netloc

        if target_domain.endswith('/'):
            target_domain = target_domain[:-1]
        
        if not target_api:
            self.page3_request_result_output.setText("请输入需要测试的接口")
            return
        
        # if self.thread_httpx and self.thread_httpx.isRunning():
        #     self.page3_request_result_output.setText("一个目标正在运行中，请等待...")
        #     return
        if self.thread_httpx and (self.thread_httpx.isRunning() or not self.thread_httpx.isFinished()):
            self.page3_request_result_output.setText("一个目标正在运行中，请等待...")
            return

        
        options = {
            'GET': self.checkbox_GET.isChecked(),
            'POST': self.checkbox_POST.isChecked(),
        }


        self.page3_request_result_output.setText("开始扫描接口，请等待...")
        self.thread_httpx = apihttpxThread(target_domain,target_api,options)
        self.thread_httpx.resultSignal.connect(displayResult)
        self.thread_httpx.errorSignal.connect(displayError)
        self.thread_httpx.start()

    def create_page2(self):
        page = QWidget()
        layout = QVBoxLayout(page)






        return page

    def create_page4(self):
        page = QWidget()
        layout = QVBoxLayout(page)

        self.page4_text_edits = {}

        # 顶部正则选项卡
        top_regular_mode = QHBoxLayout()
        top_regular_mode.setAlignment(Qt.AlignmentFlag.AlignRight) 
        top_regular_input_label = QLabel("请输入多个目标，每行一个:")
        top_regular_mode_label = QLabel("使用的正则匹配模块:")
        self.page4_checkbox_findsomething = QCheckBox('findsomething', self)
        self.page4_checkbox_JSFinder = QCheckBox('JSFinder', self)
        # 设置复选框的初始状态
        self.page4_checkbox_findsomething.setChecked(True)  # findsomething 初始为选中状态
        self.page4_checkbox_JSFinder.setChecked(False)  # JSFinder 初始为未选中状态
        top_regular_mode.addWidget(top_regular_input_label)
        top_regular_mode.addStretch()
        top_regular_mode.addWidget(top_regular_mode_label)
        top_regular_mode.addWidget(self.page4_checkbox_findsomething)
        top_regular_mode.addWidget(self.page4_checkbox_JSFinder)
        layout.addLayout(top_regular_mode)



        self.page4_url_target_input = QTextEdit(self)  # 使用QTextEdit支持多行输入
        self.page4_url_target_input.setFixedHeight(100)
        scan_button = QPushButton("开始扫描", self)
        scan_button.clicked.connect(self.create_page4_start_scan)

        layout.addWidget(self.page4_url_target_input)
        layout.addWidget(scan_button)

        self.page4_tab_widget = QTabWidget(self)
        layout.addWidget(self.page4_tab_widget)

        page.setStyleSheet("""
            QLineEdit, QTextEdit {
                border: 1px solid gray;
                border-radius: 3px;
                padding: 5px;
            }
            QPushButton {
                padding: 6px 15px;
                background-color: #4CAF50;
                color: white;
            }
            QCheckBox {
                margin-top: 0px;  
                margin-bottom: 0px;  
            }
        """)


        return page


    def create_page4_start_scan(self):
        try:
            """
            多目标扫描
            生成多个扫描结果页面和扫描线程
            """
            def extract_domain(url):
                # 检查是否是一个合法的URL
                try:
                    result = urlparse(url)
                    # 筛选过滤掉不包含协议的URl
                    if result.scheme and result.netloc:
                        # 使用正则表达式提取域名
                        match = re.search(r'^(?:www\.)?([a-zA-Z0-9.-]+)', result.netloc)
                        if match:
                            return match.group(1)
                except ValueError:
                    pass  # 如果不是合法的URL，urlparse会抛出ValueError异常
                return None


            targets = [] # 存放处理后的目标
            # 获取目标，去重和去除空白行
            raw_targets = self.page4_url_target_input.toPlainText().split('\n')
            targets_starts = list(dict.fromkeys([line.strip() for line in raw_targets if line.strip()]))

            # 创建页面名称
            for target in targets_starts:
                target_domain = extract_domain(target)
                if target_domain:
                    number_of_occurrences = 0
                    for domain in self.the_target_of_objectives_for_multi_tasking:
                        domain = re.sub(r'_(\d+)$', '', domain)
                        if target_domain == domain:
                            number_of_occurrences += 1
                    if number_of_occurrences == 0:
                        targets.append(target)
                        self.the_target_of_objectives_for_multi_tasking.append(target_domain)
                    else:
                        targets.append(target)
                        target_domain  = f"{target_domain}_{number_of_occurrences}"
                        self.the_target_of_objectives_for_multi_tasking.append(target_domain)

        




            # 目标计数
            new_target_num = 0
            for i, target in enumerate(targets):
                target = target.strip()
                if target:
                    # 创建新的页面并使用封装的函数来构造页面
                    new_tab = QWidget()
                    target_num = i+self.the_number_of_objectives_for_multi_tasking
                    self.create_page4_zi(new_tab, target, target_num)
                    self.page4_tab_widget.addTab(new_tab, f"{self.the_target_of_objectives_for_multi_tasking[target_num]}")
                new_target_num += 1

            target_num = 0
            # 一对一创建扫描线程
            for i, target in enumerate(targets):
                target = target.strip()
                if target:
                    target_num = i+self.the_number_of_objectives_for_multi_tasking
                    self.process_js4_zi(target, target_num)

            # 多目标扫描全局计数
            self.the_number_of_objectives_for_multi_tasking += new_target_num
        except Exception as e:
            pass

    def create_page4_zi(self,page,target,target_num):

        layout = QVBoxLayout(page)




        # 中间部分，分为左右两列
        mid_layout = QHBoxLayout()
        # 左侧布局
        left_layout = QVBoxLayout()
        
        # JS路径部分
        js_path_label = QLabel("获取的JS路径:")
        left_layout.addWidget(js_path_label)

        attr_name_js_path = f"page4_js_path_output_{target_num}"
        self.page4_text_edits[attr_name_js_path] = QTextEdit()
        left_layout.addWidget(self.page4_text_edits[attr_name_js_path])
        # self.page1_js_path_output = QTextEdit()
        # left_layout.addWidget(self.page1_js_path_output)

        # 域名部分
        domain_label = QLabel("获取的域名:")
        left_layout.addWidget(domain_label)
        attr_name_domain = f"page4_domain_output_{target_num}"
        self.page4_text_edits[attr_name_domain] = QTextEdit()
        left_layout.addWidget(self.page4_text_edits[attr_name_domain])

        # 设置比例
        left_layout.setStretchFactor(self.page4_text_edits[attr_name_js_path], 3)  # 1.5比例
        left_layout.setStretchFactor(self.page4_text_edits[attr_name_domain], 2)  # 1比例

        mid_layout.addLayout(left_layout)


        # 右侧布局
        right_layout = QVBoxLayout()
        attr_name_api = f"page4_api_list_output_{target_num}"
        self.page4_text_edits[attr_name_api] = QTextEdit()
        right_layout.addWidget(QLabel("接口列表:"))
        right_layout.addWidget(self.page4_text_edits[attr_name_api])
        mid_layout.addLayout(right_layout)

        # 将左右布局添加到主布局
        layout.addLayout(mid_layout)

        # 设置一些基本样式
        page.setStyleSheet("""
            QLineEdit, QTextEdit {
                border: 1px solid gray;
                border-radius: 3px;
                padding: 5px;
            }
            QPushButton {
                padding: 6px 15px;
                background-color: #4CAF50;
                color: white;
            }
            QCheckBox {
                margin-top: 0px;  
                margin-bottom: 0px;  
            }
        """)
        # layout.setSpacing(1)
        # 连接按钮信号到槽函数

        return page
    
    def process_js4_zi(self,url,target_num):


        attr_name_js_path = f"page4_js_path_output_{target_num}"
        attr_name_domain = f"page4_domain_output_{target_num}"
        attr_name_api = f"page4_api_list_output_{target_num}"
        attr_name_thread = f"page4_thread_{target_num}"
        self.page4_text_edits[attr_name_thread] = None
        # self.thread = None
        self.page4_text_edits[attr_name_js_path].clear()
        self.page4_text_edits[attr_name_api].clear()
        self.page4_text_edits[attr_name_domain].clear()

        def displayResult(result):
            self.page4_text_edits[attr_name_js_path].append(result)

        def displayResult_path(result):
            self.page4_text_edits[attr_name_api].append(result)

        def displayError(error):
            self.page4_text_edits[attr_name_domain].append(f"Error occurred: {error}")


        # 这里可以添加获取URL、JS路径、域名和接口列表的逻辑
        # url = self.page1_url_input.text()

        # if not url:
        #     self.page1_api_list_output.setText("请输入一个url")
        #     return
        
        # if self.thread and self.thread.isRunning():
        #     self.page1_api_list_output.setText("一个目标正在运行中，请等待...")
        #     return
        
        options = {
            'findsomething': self.page4_checkbox_findsomething.isChecked(),
            'JSFinder': self.page4_checkbox_JSFinder.isChecked(),
        }

        self.page4_text_edits[attr_name_domain].setText("开始扫描...")
        self.page4_text_edits[attr_name_thread] = JSFinderThread(url,options)
        self.page4_text_edits[attr_name_thread].resultSignal.connect(displayResult)
        self.page4_text_edits[attr_name_thread].resultSignal_path.connect(displayResult_path)
        self.page4_text_edits[attr_name_thread].errorSignal.connect(displayError)
        self.page4_text_edits[attr_name_thread].start()

    def create_page5(self):
        page = QWidget()
        layout = QVBoxLayout(page)
        # 整体布局


        # 顶部配置选项卡
        top_regular_mode = QHBoxLayout()
        layout.addLayout(top_regular_mode)

        # 顶部域名输入框
        top_layout = QHBoxLayout()
        top_target_domain_label = QLabel("目标域名:")
        self.page5_domain_input = QLineEdit()
        start_scanning_directory_button = QPushButton("扫描目录", self)
        start_scanning_directory_button.clicked.connect(self.process5_directory_scan)
        top_layout.addWidget(top_target_domain_label)
        top_layout.addWidget(self.page5_domain_input)
        top_layout.addWidget(start_scanning_directory_button)
        layout.addLayout(top_layout)


        tail_layout = QHBoxLayout()

        left_layout = QVBoxLayout()
        self.page5_api_text_input = QTextEdit(self)
        left_layout.addWidget(QLabel("扫描接口列表:"))
        left_layout.addWidget(self.page5_api_text_input)

        self.page5_dictionary_text_input = QTextEdit(self)
        left_layout.addWidget(QLabel("字典列表:"))
        left_layout.addWidget(self.page5_dictionary_text_input)

        mid_layout = QVBoxLayout()
        get_the_first_level_directory_button = QPushButton("获取第一级目录", self)
        get_the_first_level_directory_button.clicked.connect(self.process5)
        get_the_second_level_directory_button = QPushButton("获取第二级目录", self)
        get_the_second_level_directory_button.clicked.connect(self.process5)
        self.page5_dictionary_comboBox = QComboBox(self)
        dictionary_update_button = QPushButton('更新列表', self)
        dictionary_update_button.clicked.connect(self.process5)
        dictionary_write_button = QPushButton('使用字典', self)
        dictionary_write_button.clicked.connect(self.process5)

        mid_layout.addSpacing(30)
        mid_layout.addWidget(get_the_first_level_directory_button)
        mid_layout.addWidget(get_the_second_level_directory_button)
        mid_layout.addSpacing(190)
        mid_layout.addWidget(self.page5_dictionary_comboBox)
        mid_layout.addWidget(dictionary_update_button)
        mid_layout.addWidget(dictionary_write_button)
        mid_layout.addSpacing(80)

        right_layout = QVBoxLayout()
        self.page5_request_result_output = QTextEdit(self)
        self.page5_request_progress_output = QLineEdit(self)
        right_layout.addWidget(QLabel("扫描进度:"))
        right_layout.addWidget(self.page5_request_progress_output)
        right_layout.addWidget(QLabel("扫描结果:"))
        right_layout.addWidget(self.page5_request_result_output)


        left_widget = QWidget()
        left_widget.setLayout(left_layout)
        mid_widget = QWidget()
        mid_widget.setLayout(mid_layout)
        right_widget = QWidget()
        right_widget.setLayout(right_layout)

        tail_layout.addWidget(left_widget)
        tail_layout.addWidget(mid_widget)
        tail_layout.addWidget(right_widget)

        tail_layout.setStretchFactor(left_widget, 4)
        tail_layout.setStretchFactor(mid_widget, 3)
        tail_layout.setStretchFactor(right_widget, 6)

        # 然后将splitter添加到布局中

        layout.addLayout(tail_layout)

        return page


    def process5(self):
        print("1")

    def process5_directory_scan(self):
        self.thread_directory_httpx = None
        target_domain_url = self.page5_domain_input.text()
        target_api = self.page5_api_text_input.toPlainText()
        use_dictionary = self.page5_dictionary_text_input.toPlainText()
        self.page5_request_result_output.clear()

        def displayResult(result):
            self.page5_request_result_output.append(result)

        def displayError(error):
            self.page5_request_result_output.append(f"Error occurred: {error}")

        def displayProgress(progress):
            self.page5_request_progress_output.setText(progress)
        
        if not target_domain_url:
            self.page5_request_result_output.setText("请输入目标域名")
            return

        if not target_api:
            self.page5_request_result_output.setText("请输入需要测试的接口")
            return
        
        target_domain_raw = urlparse(target_domain_url)
        target_domain = target_domain_raw.scheme + "://" + target_domain_raw.netloc

        if target_domain.endswith('/'):
            target_domain = target_domain[:-1]

        if self.thread_directory_httpx and (self.thread_directory_httpx.isRunning() or not self.thread_directory_httpx.isFinished()):
            self.page5_request_result_output.append("一个目标正在运行中，请等待...")
            return

        self.page5_request_result_output.setText("开始目录探测，请等待...")
        self.thread_directory_httpx = directoryhttpxThread(target_domain,target_api,use_dictionary)
        self.thread_directory_httpx.resultSignal.connect(displayResult)
        self.thread_directory_httpx.errorSignal.connect(displayError)
        self.thread_directory_httpx.progressSignal.connect(displayProgress)
        self.thread_directory_httpx.start()




class apihttpxThread(QThread):
    resultSignal = pyqtSignal(str)
    errorSignal = pyqtSignal(str)

    def __init__(self, target_domain, target_api,options):
        QThread.__init__(self)
        self.target_domain = target_domain
        self.target_apis = [line.strip() for line in target_api.split('\n') if line.strip()]
        self.options = options
        self.target_urls = []

        self.requests_header_UA = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.108 Safari/537.36"
        self.requests_header_Cookie = ""

        self.requests_header = {"User-Agent": self.requests_header_UA,
                                "Cookie": self.requests_header_Cookie
                                }

    def run(self):
        try:
            self.target_urls = self.target_process(self.target_domain,self.target_apis)
            self.test_the_status_of_the_interface(self.target_urls)

            print("")
        except Exception as e:
            self.errorSignal.emit(str(e))



    def target_process(self,target_domain,target_apis):
        target_url = []
        for target_api in target_apis:
            if target_api[0:4] == "http":
                target_url.append(target_api)
            elif target_api[0:2] == "//":
                target_api = target_domain + "/"+ target_api[3:]
                target_url.append(target_api)
            elif target_api[0:1] == "/":
                target_api = target_domain + target_api
                target_url.append(target_api)
            else:
                target_api = target_domain + "/"+ target_api
                target_url.append(target_api)
        return target_url
    

# -- 用于对url发起自定义请求
# @param 无
# @out 无
# @return 无
# --
    def requests_url(self,url):
        max_retries = 2
        for attempt in range(max_retries):
            try:
                response = requests.get(url, headers=self.requests_header, timeout=3, verify=False)
                response.raise_for_status()  # 状态码不在200到299之间
                content_length = response.headers.get('Content-Length', 'Unknown')
                # print(response.text)
                # for key, value in response.request.headers.items():
                #     print(f"{key}: {value}")
                return {
                    'body': response.text,
                    'status_code': response.status_code,
                    'content_length': content_length
                }
            except requests.exceptions.RequestException as e:
                # 捕获所有与请求相关的异常
                if attempt >= max_retries - 1:
                    if isinstance(e, requests.exceptions.HTTPError):
                        content_length = response.headers.get('Content-Length', 'Unknown')
                        # self.errorSignal.emit(f"目标:{url} \n 访问不到，状态码：{e.response.status_code}")
                        if 300 <= e.response.status_code < 400:
                            return {
                                'body': response.text,
                                'status_code': response.status_code,
                                'content_length': content_length
                            }
                        else:
                            return {
                                'body': "wu",
                                'status_code': e.response.status_code,
                                'content_length': "wu"
                            }
                    else:
                        # self.errorSignal.emit(f"目标:{url} \n 无法访问")
                        return
            except Exception as e:
                # 捕获其他未预料到的异常
                # self.errorSignal.emit(f"目标:{url} \n 发生未知错误：{str(e)}")
                return
            
    def test_the_status_of_the_interface(self,target_urls):
        interface_status_result = {}
        for target_url in target_urls:
            interface_status_result = self.requests_url(target_url)
            if interface_status_result:
                if interface_status_result['body'] == "wu":
                    request_a_display_of_results = (
                        f"<span style='color:red;'>404  ---   {target_url}</span>"
                    )
                    # request_a_display_of_results = (
                    #     f"------------------------------------\n"
                    #     f"[出货]   ---   {target_url}\n"
                    #     f"状态码: {interface_status_result['status_code']}\n"
                    #     f"Content-Length: {interface_status_result['content_length']}\n"
                    #     f"响应内容: {interface_status_result['body']}\n"
                    #     f"------------------------------------\n"
                    # )
                else:
                    body_preview = interface_status_result['body'][:120] + "..." if len(interface_status_result['body']) > 120 else interface_status_result['body']
                    request_a_display_of_results = (
                        f"------------------------------------\n"
                        f"[出货]   ---   {target_url}\n"
                        f"状态码: {interface_status_result['status_code']}\n"
                        f"Content-Length: {interface_status_result['content_length']}\n"
                        f"响应内容: {body_preview}\n"
                        f"------------------------------------"
                    )
                
            else:
                request_a_display_of_results = (
                    f"<span style='color:red;'>404  ---   {target_url}</span>"
                )

            self.resultSignal.emit(request_a_display_of_results)


class JSFinderThread(QThread):
    """
    创建子线程用于JS文件中接口发现扫描
    """
    resultSignal = pyqtSignal(str)
    errorSignal = pyqtSignal(str)
    resultSignal_path = pyqtSignal(str)

    def __init__(self, url, options):
        QThread.__init__(self)
        self.options = options
        self.url = url
        self.target_url_js = []  # 存放目标网站的js路径
        self.target_url_js_path = [] # 存放目标网站的js里包含的接口

        

        self.requests_header_UA = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.108 Safari/537.36"
        self.requests_header_Cookie = ""

        self.requests_header = {"User-Agent": self.requests_header_UA,
                                "Cookie": self.requests_header_UA
                                }
    # 路径黑名单
        self.strings_to_remove = ['//', '/', '/.', '/./','/ ','../../..','../../']
    # 从渲染页面二次提取html页面
        self.html_iframe = r'<iframe[^>]*?src="([^"]+)"'


    # 从html页面发现js路径使用的正则
        self.js_href = r'href=[\'"]?([^\'">]+)'
        self.js_src = r'src=[\'"]?([^\'">]+)'
        self.js_script = r'<script [^><]*?src=[\'"]?([^\'">]+)'

    # 从js文件发现路径使用的正则
        self.path_findsomething = r"['\"](?:/|\.\./|\./)[^\/>\\< \)\(\{\}\,\'\"\\]([^\>\< \)\(\{\}\,\'\"\\])*?['\"]"
        self.path_JSFinder = r"""
      (?:"|')                               # Start newline delimiter
      (
        ((?:[a-zA-Z]{1,10}://|//)           # Match a scheme [a-Z]*1-10 or //
        [^"'/]{1,}\.                        # Match a domainname (any character + dot)
        [a-zA-Z]{2,}[^"']{0,})              # The domainextension and/or path
        |
        ((?:/|\.\./|\./)                    # Start with /,../,./
        [^"'><,;| *()(%%$^/\\\[\]]          # Next character can't be...
        [^"'><,;|()]{1,})                   # Rest of the characters can't be
        |
        ([a-zA-Z0-9_\-/]{1,}/               # Relative endpoint with /
        [a-zA-Z0-9_\-/]{1,}                 # Resource name
        \.(?:[a-zA-Z]{1,4}|action)          # Rest + extension (length 1-4 or action)
        (?:[\?|/][^"|']{0,}|))              # ? mark with parameters
        |
        ([a-zA-Z0-9_\-]{1,}                 # filename
        \.(?:php|asp|aspx|jsp|json|
             action|html|js|txt|xml)             # . + extension
        (?:\?[^"|']{0,}|))                  # ? mark with parameters
      )
      (?:"|')                               # End newline delimiter
    """


    def run(self):
        try:
            if not self.options['JSFinder'] and not self.options['findsomething']:
                self.errorSignal.emit("没有选择正则模块")
                return
            parsed_url = urlparse(self.url)
            url_path = parsed_url.path
            if not url_path.lower().endswith('.js') or url_path == '/' or url_path == '':
                self.target_url_js = self.discover_js_via_html(self.url)
                if not self.target_url_js:
                    self.errorSignal.emit("没找到js文件")
                else:
                    self.resultSignal.emit('\n'.join(self.target_url_js))
                # self.resultSignal.emit('\n'.join(self.target_url_js))
            else:
                self.target_url_js = [self.url]
                self.resultSignal.emit("单独js文件扫描:\n"+self.url)

            self.target_url_js_path = self.discover_path_via_js(self.target_url_js)
            if not self.target_url_js_path:
                self.errorSignal.emit("没找到接口路径")
            else:
                self.resultSignal_path.emit('\n'.join(self.target_url_js_path))

        except Exception as e:
            self.errorSignal.emit(str(e))
        self.errorSignal.emit("接口扫描已完成")








# -- 用于对url发起自定义请求
# @param 无
# @out 无
# @return 无
# --
    def requests_url(self,url):
        max_retries = 2
        for attempt in range(max_retries):
            try:
                response = requests.get(url, headers=self.requests_header, timeout=5, verify=False)
                response.raise_for_status()  # 状态码不在200到299之间
                return response.text  # 请求成功，返回响应
            except requests.exceptions.RequestException as e:
                # 捕获所有与请求相关的异常
                if attempt >= max_retries - 1:
                    if isinstance(e, requests.exceptions.HTTPError):
                        self.errorSignal.emit(f"目标:{url} \n 访问不到，状态码：{e.response.status_code}")
                    else:
                        # self.errorSignal.emit(f"网站:{url} \n 无法访问：{str(e)}")
                        self.errorSignal.emit(f"目标:{url} \n 无法访问")
                        # self.errorSignal.emit(f"{response.request.headers}")
                        # self.errorSignal.emit(f"{e}")

                    return f""
            except Exception as e:
                # 捕获其他未预料到的异常
                # self.errorSignal.emit(f"网站:{url} \n 发生未知错误：{str(e)}")
                self.errorSignal.emit(f"目标:{url} \n 发生未知错误：{str(e)}")
                return f""
            
    def deep_requests_url(self,url):
        system = platform.system()  
        print(system)
        if system == "Windows":
            # 指定Edge浏览器可执行文件路径
            edge_binary_path = "edgedriver_arm64/Edge/msedge.exe"
            # 初始化Edge浏览器
            service = Service(executable_path='edgedriver_arm64/msedgedriver.exe')
        elif system == "Darwin":
            # 指定Edge浏览器可执行文件路径
            edge_binary_path = "edgedriver_mac64/Edge/Microsoft Edge.app/Contents/MacOS/Microsoft Edge"
            # 初始化Edge浏览器
            service = Service(executable_path='edgedriver_mac64/msedgedriver')
# 创建浏览器选项
        opt = Options()
        opt.binary_location = edge_binary_path
        opt.add_argument("--disable-blink-features=AutomationControlled")  # 禁用自动化检测
        opt.add_argument("--start-maximized")  # 启动时最大化窗口
        opt.add_argument("--incognito")        # 无痕模式
        opt.add_argument("--headless")         # 无头模式（可选）
        opt.add_argument("--ignore-certificate-errors")  # 忽略 SSL 证书错误


        try:
            driver = webdriver.Edge(service=service, options=opt)
            driver.set_page_load_timeout(30)
            # driver.get("http://106.39.13.42/sstms_common/page/NewDoorPage/page/index.html?admin=")
            driver.get(url)
            # 获取页面源代码
            page_content = driver.page_source

        except TimeoutException:
            page_content = ""

        except WebDriverException as e:
            page_content = ""

        finally:
            # 确保浏览器关闭
            try:
                driver.quit()
            except:
                pass
        # 打印获取内容
        return page_content
    
    def page_depth_extracts_html(self,url):
        page_html = []
        page_home_html_api = []
        page_home_html=self.deep_requests_url(url)
        page_html.append(page_home_html)
        page_home_html_api_initial = re.findall(self.html_iframe,page_home_html)
        

        for path in page_home_html_api_initial:
            url_html = self.process_url(url,path)
            parsed_url = urlparse(url_html)
            url_path = parsed_url.path
            if url_path.lower().endswith('.html'):
            # if '.html' in url_html.lower():
                page_home_html_api.append(url_html)
        
        if page_home_html_api:
            for path in page_home_html_api:
                page_sub_html = self.deep_requests_url(path)
                page_html.append(page_sub_html)
        
        return page_html





# -- 用于对发现的url进行处理
# @param 无
# @out 无
# @return 无
# --
    def process_url(self,URL, re_URL):
        black_url = ["javascript:"]	# Add some keyword for filter url.
        URL_raw = urlparse(URL)
        path_URL = URL_raw.path   # 初始路径
        ab_URL = URL_raw.netloc   # 域名
        host_URL = URL_raw.scheme # 协议
        path_URL = '/'.join(path_URL.split('/')[:-1]) + '/'


        if re_URL[0:2] == "//":
            result = host_URL  + ":" + re_URL
        elif re_URL[0:4] == "http":
            result = re_URL
        elif re_URL[0:2] != "//" and re_URL not in black_url:
            if re_URL[0:1] == "/":
                result = host_URL + "://" + ab_URL + re_URL
            else:
                if re_URL[0:1] == ".":
                    # 处理相对路径
                    # 将当前路径和相对路径进行拼接并规范化
                    full_path = os.path.normpath(os.path.join(path_URL, re_URL))
                    result = f"{host_URL}://{ab_URL}{full_path}"
                    # if re_URL[0:2] == "..":
                    #     result = host_URL + "://" + ab_URL + re_URL[2:]
                    # else:
                    #     result = host_URL + "://" + ab_URL +path_URL+re_URL[2:]
                else:
                    result = host_URL + "://" + ab_URL + path_URL + re_URL
        else:
            result = URL
        return result
    
    def discover_js_via_html(self, url):
        html_js_path = []
        html_js = []
        html_raw_list = []
        # html_raw_list.append(str(self.requests_url(url)))
        html_raw_list.extend(self.page_depth_extracts_html(url))

        if html_raw_list is None or not html_raw_list:
            return None
        
        for html_raw in html_raw_list:
            html_js_href = re.findall(self.js_href,html_raw)
            html_js_src = re.findall(self.js_src,html_raw)
            html_js_script = re.findall(self.js_script,html_raw)

            html_js_path.extend(html_js_href)
            html_js_path.extend(html_js_src)
            html_js_path.extend(html_js_script)
            html_js_path = list(set(html_js_path))

        # if not html_js_path:
        #     self.resultSignal.emit("kong")
        # else:
        #     self.resultSignal.emit('\n'.join(html_js_path))

        for path in html_js_path:
            url_js = self.process_url(url,path)
            parsed_url = urlparse(url_js)
            url_path = parsed_url.path
            if url_path.lower().endswith('.js'):
                html_js.append(url_js)


        html_js = list(set(html_js))
        



        return html_js
    
    def discover_path_via_js(self,html_js):
        js_path = []
        if not html_js:
            return None
        
        for url_js in html_js:
            js_raw = self.requests_url(url_js)
            if js_raw == None: 
                return None
            js_raw = str(js_raw)

        # 使用findsomething的正则筛选接口
            if self.options['findsomething']:
                js_path_findsomething = [match.group()[1:-1] for match in re.finditer(self.path_findsomething,js_raw)]
                js_path.extend(js_path_findsomething)

        # 使用JSFinder的正则筛选接口
            if self.options['JSFinder']:
                pattern =re.compile(self.path_JSFinder, re.VERBOSE)
                js_path_JSFinder = [match.group().strip('"').strip("'") for match in re.finditer(pattern, js_raw)]
                js_path_JSFinder = [path for path in js_path_JSFinder if not path.startswith('http')]
                js_path.extend(js_path_JSFinder)


            # if not js_path_JSFinder:
            #     self.resultSignal_path.emit("kong")
            # else:
            #     # self.resultSignal_path.emit(js_raw)
            #     self.resultSignal_path.emit('\n'.join(js_path_JSFinder))

    # 删除重复目录
        js_path = list(set(js_path))

    # 移除黑名单目录
        # strings_to_remove_set = set(self.strings_to_remove)
        # js_path = [item for item in js_path if item not in strings_to_remove_set]

        # 假设 self.strings_to_remove 已经定义为一个列表
        strings_to_remove_set = set(self.strings_to_remove)
        # 使用列表推导式去除空白字符并过滤黑名单内容
        js_path = [item.strip() for item in js_path if item.strip() and item.strip() not in strings_to_remove_set]

        return js_path

class directoryhttpxThread(QThread):
    resultSignal = pyqtSignal(str)  # 用于发送成功结果的信号
    errorSignal = pyqtSignal(str)   # 用于发送错误信息的信号
    progressSignal = pyqtSignal(str)  # 用于发送进度信息的信号

    def __init__(self, target_domain,target_api,use_dictionary):
        QThread.__init__(self)
        self.target_domain = target_domain
        self.target_apis = [line.strip() for line in target_api.split('\n') if line.strip()]
        self.use_dictionarys = [line.strip() for line in use_dictionary.split('\n') if line.strip()]
        self.max_concurrency = 15        # max_concurrency  # 最大并发任务数量

        # 用于存储进度信息的队列
        self.progress_queue = []
        self.progress_mutex = QMutex()  # 用于线程安全的互斥锁

        # 用于记录已完成的任务数量
        self.completed_tasks =  0 # 1+len(self.target_apis)
        self.total_tasks = len(self.use_dictionarys) * len(self.target_apis)

        # 初始化 QTimer
        self.timer = QTimer()
        self.timer.timeout.connect(self.emit_progress_signal)
        self.timer.start(100)  # 每 100 毫秒（0.1 秒）触发一次


    def emit_progress_signal(self):
        """
        定时器触发时，从队列中取出进度信息并发送信号
        """
        with QMutexLocker(self.progress_mutex):  # 加锁，确保线程安全
            if self.progress_queue:
                progress_info = self.progress_queue.pop(0)
                self.progressSignal.emit(progress_info)

    async def progress_timer_task(self):
        """
        定时器任务：每 0.1 秒计算一次进度并添加到队列
        """
        while self.completed_tasks < self.total_tasks:
            with QMutexLocker(self.progress_mutex):  # 加锁，确保线程安全
                # progress = self.completed_tasks / self.total_tasks * 100
                self.progress_queue.append(f"Scanning {self.completed_tasks}/{self.total_tasks}")
            await asyncio.sleep(0.1)  # 每 0.1 秒执行一次

        with QMutexLocker(self.progress_mutex):
            self.progress_queue.append(f"Scanning {self.completed_tasks}/{self.total_tasks}")

    async def scan_directory(self, client: httpx.AsyncClient, api: str, word: str) -> str:
        """
        扫描单个目录
        :param client: httpx 异步客户端
        :param api: 目标接口
        :param word: 字典中的单词
        :return: 扫描结果（如果成功）
        """
        url = f"{self.target_domain}/{api}/{word}"  # 构造完整的 URL
        try:
            response = await client.get(url)
            if 200 <= response.status_code <= 400:  # 如果状态码为 200，表示成功
                return f"{response.status_code} --- {url}"
        except Exception as e:
            # self.errorSignal.emit(f"Error scanning {url}: {str(e)}")
            pass
        return None
    
    async def run_scan(self) -> None:
        """
        异步运行目录扫描
        """
        semaphore = asyncio.Semaphore(self.max_concurrency)  # 限制并发任务数量

        async def limited_scan(client: httpx.AsyncClient, api: str, word: str) -> str:
            async with semaphore:  # 限制并发
                result = await self.scan_directory(client, api, word)
                with QMutexLocker(self.progress_mutex):  # 加锁，确保线程安全
                    self.completed_tasks += 1  # 更新已完成的任务数量
                    # self.progressSignal.emit(str(self.completed_tasks))
                return result
            

        progress_task = asyncio.create_task(self.progress_timer_task())


        async with httpx.AsyncClient() as client:
            for api in self.target_apis:  # 遍历每个接口
                self.resultSignal.emit(f"Results for API: {api}\n")
                results = []  # 存储当前接口的扫描结果
                tasks = [limited_scan(client, api, word) for  word  in self.use_dictionarys]
                for future in asyncio.as_completed(tasks):  # 按完成顺序获取结果
                    result = await future
                    if result:
                        self.resultSignal.emit(f"{result}")
                #         results.append(result)

                # # 将当前接口的扫描结果整理并发送到主线程
                # if results:
                #     result_message = f"Results for API: {api}\n" + "\n".join(results) + "\n"
                #     self.resultSignal.emit(result_message)

        await progress_task

        # with QMutexLocker(self.progress_mutex):
        if self.progress_queue:
            self.emit_progress_signal()  # 手动触发信号

    def run(self) -> None:
        """
        重写 QThread 的 run 方法，启动异步扫描
        """
        try:
            asyncio.run(self.run_scan())
        except Exception as e:
            self.errorSignal.emit(f"Error in run_scan: {str(e)}")
        finally:
            self.timer.stop()  # 扫描完成后停止定时器






if __name__ == "__main__":
    qdarktheme.enable_hi_dpi()
    app = QApplication(sys.argv)
    qdarktheme.setup_theme('dark') # dark 黑  light 白   auto 自动
    window = MainWindow()
    window.show()
    sys.exit(app.exec())
