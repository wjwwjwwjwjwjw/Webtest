import os
import http.server
import socketserver
import webbrowser
from threading import Timer

# ���ö˿�
PORT = 8000

# �����򵥵� HTTP ������
Handler = http.server.SimpleHTTPRequestHandler

def open_browser():
    """��Ĭ��������д򿪲���ҳ��"""
    webbrowser.open(f'http://localhost:{PORT}')

if __name__ == '__main__':
    # �л�����̬�ļ�Ŀ¼
    os.chdir('static')
    
    # ���������
    Timer(1.5, open_browser).start()
    
    # ����������
    with socketserver.TCPServer(("", PORT), Handler) as httpd:
        print(f"������������ port {PORT}")
        httpd.serve_forever() 