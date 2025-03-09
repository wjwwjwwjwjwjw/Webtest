import os
import http.server
import socketserver
import webbrowser
from threading import Timer

# 设置端口
PORT = 8000

# 创建简单的 HTTP 服务器
Handler = http.server.SimpleHTTPRequestHandler

def open_browser():
    """在默认浏览器中打开测试页面"""
    webbrowser.open(f'http://localhost:{PORT}')

if __name__ == '__main__':
    # 切换到静态文件目录
    os.chdir('static')
    
    # 启动浏览器
    Timer(1.5, open_browser).start()
    
    # 启动服务器
    with socketserver.TCPServer(("", PORT), Handler) as httpd:
        print(f"服务器运行在 port {PORT}")
        httpd.serve_forever() 