import sys
import os
import importlib
import tkinter as tk
import customtkinter as ctk
from tkinter import messagebox
import subprocess

def check_dependencies():
    required_packages = {
        'customtkinter': 'customtkinter',
        'pandas': 'pandas',
        'matplotlib': 'matplotlib',
        'numpy': 'numpy',
        'fpdf': 'fpdf',
        'darkdetect': 'darkdetect',
        'pillow': 'PIL',
        'openpyxl': 'openpyxl',
        'cryptography': 'cryptography',
        'tkcalendar': 'tkcalendar',
        'seaborn': 'seaborn',
        'reportlab': 'reportlab',
        'scikit-learn': 'sklearn',
        'google-generativeai': 'google.generativeai',
        'requests': 'requests',
        'python-dateutil': 'dateutil',
        'unidecode': 'unidecode',
        'secure-smtplib': 'secure_smtplib',
        'python-dotenv': 'dotenv'
    }
    
    missing_packages = []
    
    for package, import_name in required_packages.items():
        try:
            importlib.import_module(import_name)
        except ImportError:
            missing_packages.append(package)
    
    if missing_packages:
        print("Đang cài đặt các package còn thiếu...")
        try:
            subprocess.check_call([sys.executable, "-m", "pip", "install"] + missing_packages)
            print("Đã cài đặt thành công các package còn thiếu!")
            return True
        except subprocess.CalledProcessError as e:
            print(f"Lỗi khi cài đặt packages: {str(e)}")
            return False
    return True

def check_files():
    required_files = [
        'giao_dien.py',
        'bao_mat.py',
        'bieu_do.py',
        'bao_cao.py',
        'tinh_nang.py',
        'tinh_toan.py',
        'thong_bao.py',
        'xuly_du_lieu.py',
        'cai_dat.py',
        'quanlychitieu.py'
    ]
    
    missing_files = []
    current_dir = os.path.dirname(os.path.abspath(__file__))
    
    for file in required_files:
        file_path = os.path.join(current_dir, file)
        if not os.path.exists(file_path):
            missing_files.append(file)
            print(f"Không tìm thấy file: {file_path}")
    
    if missing_files:
        print("\nDanh sách các file còn thiếu:")
        for file in missing_files:
            print(f"- {file}")
        print("\nVui lòng đảm bảo tất cả các file trên đều tồn tại trong thư mục chương trình.")
        return False
    return True

def create_data_directories():
    directories = ['data', 'backup', 'reports', 'temp']
    for directory in directories:
        if not os.path.exists(directory):
            os.makedirs(directory)
            print(f"Đã tạo thư mục {directory}")

def main():
    print("Kiểm tra dependencies...")
    if not check_dependencies():
        return
    
    print("\nKiểm tra files...")
    if not check_files():
        return
    
    print("\nTạo thư mục dữ liệu...")
    create_data_directories()
    
    print("\nKhởi động ứng dụng...")
    try:
        from quanlychitieu import QuanLyChiTieu
        
        root = ctk.CTk()
        app = QuanLyChiTieu(root)
        root.mainloop()
        
    except Exception as e:
        print(f"\nLỗi khi khởi động ứng dụng: {str(e)}")
        messagebox.showerror("Lỗi", f"Không thể khởi động ứng dụng:\n{str(e)}")

if __name__ == "__main__":
    main() 