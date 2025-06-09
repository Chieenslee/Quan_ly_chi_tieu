import sys
import os
import importlib
import tkinter as tk
import customtkinter as ctk
from tkinter import messagebox

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
        'cryptography': 'cryptography'
    }
    
    missing_packages = []
    
    for package, import_name in required_packages.items():
        try:
            importlib.import_module(import_name)
        except ImportError:
            missing_packages.append(package)
    
    if missing_packages:
        print("Thiếu các package sau:")
        for package in missing_packages:
            print(f"- {package}")
        print("\nCài đặt bằng lệnh:")
        print(f"pip install {' '.join(missing_packages)}")
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
    
    for file in required_files:
        if not os.path.exists(file):
            missing_files.append(file)
    
    if missing_files:
        print("Thiếu các file sau:")
        for file in missing_files:
            print(f"- {file}")
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