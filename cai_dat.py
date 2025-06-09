import customtkinter as ctk
from tkinter import messagebox
import tkinter as tk
import json
import os
import darkdetect
from tkinter import ttk

class CaiDat:
    def __init__(self, app):
        self.app = app
        self.load_settings()
        self.income_categories = []  # Khởi tạo danh sách các StringVar cho danh mục thu nhập
        self.expense_categories = []  # Khởi tạo danh sách các StringVar cho danh mục chi tiêu
        
    def load_settings(self):
        # Tải cài đặt từ file
        try:
            with open("settings.json", "r", encoding="utf-8") as f:
                self.settings = json.load(f)
        except:
            # Cài đặt mặc định
            self.settings = {
                "theme": "system",
                "currency": "VNĐ",
                "language": "vi",
                "notifications": True,
                "auto_backup": True,
                "backup_interval": 24,
                "categories": {
                    "Thu nhập": ["Lương", "Thưởng", "Đầu tư", "Khác"],
                    "Chi tiêu": ["Ăn uống", "Di chuyển", "Nhà cửa", "Giải trí", "Mua sắm", "Y tế", "Giáo dục", "Khác"]
                }
            }
            self.save_settings()
    
    def save_settings(self):
        # Lưu cài đặt vào file
        try:
            with open("settings.json", "w", encoding="utf-8") as f:
                json.dump(self.settings, f, ensure_ascii=False, indent=4)
        except Exception as e:
            messagebox.showerror("Lỗi", f"Không thể lưu cài đặt: {str(e)}")
    
    def mo_caidat(self):
        # Tạo cửa sổ cài đặt
        window = ctk.CTkToplevel(self.app.root)
        window.title("Cài đặt")
        window.geometry("600x700")
        window.transient(self.app.root)
        window.grab_set()
        window.focus_force()
        
        # Configure grid for the window to allow notebook to expand
        window.grid_columnconfigure(0, weight=1)
        window.grid_rowconfigure(0, weight=1)
        window.grid_rowconfigure(1, weight=0) # For the save button

        # Tạo notebook (tabbed interface)
        notebook = ttk.Notebook(window)
        notebook.grid(row=0, column=0, padx=10, pady=10, sticky="nsew")
        
        # Tab Chung
        general_frame = ctk.CTkFrame(notebook)
        notebook.add(general_frame, text="Chung")
        self.tao_tab_chung(general_frame)
        
        # Tab Thông báo
        notification_frame = ctk.CTkFrame(notebook)
        notebook.add(notification_frame, text="Thông báo")
        self.tao_tab_thongbao(notification_frame)
        
        # Tab Sao lưu
        backup_frame = ctk.CTkFrame(notebook)
        notebook.add(backup_frame, text="Sao lưu")
        self.tao_tab_saoluu(backup_frame)
        
        # Tab Danh mục
        category_frame = ctk.CTkFrame(notebook)
        notebook.add(category_frame, text="Danh mục")
        self.tao_tab_danhmuc(category_frame)
        
        # Nút lưu
        ctk.CTkButton(window, text="Lưu", 
                     command=lambda: self.luu_caidat(window)).grid(row=1, column=0, pady=10)
    
    def tao_tab_chung(self, parent):
        parent.grid_columnconfigure(1, weight=1) # Make the second column expandable

        row_idx = 0

        # Theme
        ctk.CTkLabel(parent, text="Theme:").grid(row=row_idx, column=0, pady=5, padx=10, sticky="w")
        theme_frame = ctk.CTkFrame(parent)
        theme_frame.grid(row=row_idx, column=1, pady=5, padx=10, sticky="ew")
        self.theme_var = tk.StringVar(value=self.settings["theme"])
        
        ctk.CTkRadioButton(theme_frame, text="Hệ thống", 
                          variable=self.theme_var, value="system").pack(side=tk.LEFT, padx=5, expand=True)
        ctk.CTkRadioButton(theme_frame, text="Sáng", 
                          variable=self.theme_var, value="light").pack(side=tk.LEFT, padx=5, expand=True)
        ctk.CTkRadioButton(theme_frame, text="Tối", 
                          variable=self.theme_var, value="dark").pack(side=tk.LEFT, padx=5, expand=True)
        row_idx += 1
        
        # Tiền tệ
        ctk.CTkLabel(parent, text="Tiền tệ:").grid(row=row_idx, column=0, pady=5, padx=10, sticky="w")
        self.currency_entry = ctk.CTkEntry(parent)
        self.currency_entry.grid(row=row_idx, column=1, pady=5, padx=10, sticky="ew")
        self.currency_entry.insert(0, self.settings["currency"])
        row_idx += 1
        
        # Ngôn ngữ
        ctk.CTkLabel(parent, text="Ngôn ngữ:").grid(row=row_idx, column=0, pady=5, padx=10, sticky="w")
        language_frame = ctk.CTkFrame(parent)
        language_frame.grid(row=row_idx, column=1, pady=5, padx=10, sticky="ew")
        self.language_var = tk.StringVar(value=self.settings["language"])
        
        ctk.CTkRadioButton(language_frame, text="Tiếng Việt", 
                          variable=self.language_var, value="vi").pack(side=tk.LEFT, padx=5, expand=True)
        ctk.CTkRadioButton(language_frame, text="English", 
                          variable=self.language_var, value="en").pack(side=tk.LEFT, padx=5, expand=True)
        row_idx += 1
    
    def tao_tab_thongbao(self, parent):
        parent.grid_columnconfigure(0, weight=1) # Make column 0 expandable for better centering
        
        row_idx = 0

        # Bật/tắt thông báo
        notification_frame = ctk.CTkFrame(parent)
        notification_frame.grid(row=row_idx, column=0, pady=5, padx=10, sticky="ew")
        self.notification_var = tk.BooleanVar(value=self.settings["notifications"])
        ctk.CTkCheckBox(notification_frame, text="Bật thông báo", 
                       variable=self.notification_var).pack(padx=5, pady=5, anchor="w")
        row_idx += 1
        
        # Các loại thông báo
        types_frame = ctk.CTkFrame(parent)
        types_frame.grid(row=row_idx, column=0, pady=5, padx=10, sticky="ew")
        
        ctk.CTkLabel(types_frame, text="Loại thông báo:", font=("Arial", 12, "bold")).pack(padx=5, pady=5, anchor="w")
        
        self.reminder_var = tk.BooleanVar(value=True)
        ctk.CTkCheckBox(types_frame, text="Nhắc nhở", 
                       variable=self.reminder_var).pack(padx=5, pady=2, anchor="w")
        
        self.goal_var = tk.BooleanVar(value=True)
        ctk.CTkCheckBox(types_frame, text="Mục tiêu", 
                       variable=self.goal_var).pack(padx=5, pady=2, anchor="w")
        
        self.budget_var = tk.BooleanVar(value=True)
        ctk.CTkCheckBox(types_frame, text="Ngân sách", 
                       variable=self.budget_var).pack(padx=5, pady=2, anchor="w")
        row_idx += 1
    
    def tao_tab_saoluu(self, parent):
        parent.grid_columnconfigure(1, weight=1) # Make the second column expandable

        row_idx = 0

        # Tự động sao lưu
        ctk.CTkLabel(parent, text="Tự động sao lưu:").grid(row=row_idx, column=0, pady=5, padx=10, sticky="w")
        auto_backup_frame = ctk.CTkFrame(parent)
        auto_backup_frame.grid(row=row_idx, column=1, pady=5, padx=10, sticky="ew")
        self.auto_backup_var = tk.BooleanVar(value=self.settings["auto_backup"])
        ctk.CTkCheckBox(auto_backup_frame, text="Bật", 
                       variable=self.auto_backup_var).pack(padx=5, pady=5, anchor="w")
        row_idx += 1
        
        # Khoảng thời gian
        ctk.CTkLabel(parent, text="Khoảng thời gian (giờ):").grid(row=row_idx, column=0, pady=5, padx=10, sticky="w")
        self.interval_entry = ctk.CTkEntry(parent, width=100)
        self.interval_entry.grid(row=row_idx, column=1, pady=5, padx=10, sticky="ew")
        self.interval_entry.insert(0, str(self.settings["backup_interval"]))
        row_idx += 1
        
        # Nút sao lưu thủ công
        ctk.CTkButton(parent, text="Sao lưu ngay", 
                     command=self.app.bao_mat.sao_luu_baomat).grid(row=row_idx, column=0, columnspan=2, pady=10)
        row_idx += 1
        
        # Nút khôi phục
        ctk.CTkButton(parent, text="Khôi phục", 
                     command=self.app.bao_mat.khoi_phuc_baomat).grid(row=row_idx, column=0, columnspan=2, pady=5)
        row_idx += 1
    
    def tao_tab_danhmuc(self, parent):
        parent.grid_columnconfigure(0, weight=1) # Make column 0 expandable for centering

        row_idx = 0

        # Danh mục thu nhập
        income_frame = ctk.CTkFrame(parent)
        income_frame.grid(row=row_idx, column=0, pady=5, padx=10, sticky="ew")
        income_frame.grid_columnconfigure(0, weight=1)

        ctk.CTkLabel(income_frame, text="Danh mục thu nhập:", font=("Arial", 12, "bold")).grid(row=0, column=0, pady=5, padx=5, sticky="w")
        
        self.income_entries = [] # Store entry widgets for easy removal
        for i, category in enumerate(self.settings["categories"]["Thu nhập"]):
            var = tk.StringVar(value=category)
            self.income_categories.append(var)
            entry = ctk.CTkEntry(income_frame, textvariable=var)
            entry.grid(row=i + 1, column=0, padx=5, pady=2, sticky="ew")
            self.income_entries.append(entry)
        
        # Thêm/xóa danh mục thu nhập
        income_btn_frame = ctk.CTkFrame(income_frame)
        income_btn_frame.grid(row=len(self.settings["categories"]["Thu nhập"]) + 1, column=0, pady=5, padx=5, sticky="ew")
        income_btn_frame.grid_columnconfigure(0, weight=1)
        income_btn_frame.grid_columnconfigure(1, weight=1)

        ctk.CTkButton(income_btn_frame, text="Thêm", 
                     command=lambda: self.them_danhmuc(income_frame, "Thu nhập")).grid(row=0, column=0, padx=5, sticky="ew")
        ctk.CTkButton(income_btn_frame, text="Xóa", 
                     command=lambda: self.xoa_danhmuc(income_frame, "Thu nhập")).grid(row=0, column=1, padx=5, sticky="ew")
        row_idx += 1
        
        # Danh mục chi tiêu
        expense_frame = ctk.CTkFrame(parent)
        expense_frame.grid(row=row_idx, column=0, pady=5, padx=10, sticky="ew")
        expense_frame.grid_columnconfigure(0, weight=1)

        ctk.CTkLabel(expense_frame, text="Danh mục chi tiêu:", font=("Arial", 12, "bold")).grid(row=0, column=0, pady=5, padx=5, sticky="w")
        
        self.expense_entries = [] # Store entry widgets for easy removal
        for i, category in enumerate(self.settings["categories"]["Chi tiêu"]):
            var = tk.StringVar(value=category)
            self.expense_categories.append(var)
            entry = ctk.CTkEntry(expense_frame, textvariable=var)
            entry.grid(row=i + 1, column=0, padx=5, pady=2, sticky="ew")
            self.expense_entries.append(entry)
        
        # Thêm/xóa danh mục chi tiêu
        expense_btn_frame = ctk.CTkFrame(expense_frame)
        expense_btn_frame.grid(row=len(self.settings["categories"]["Chi tiêu"]) + 1, column=0, pady=5, padx=5, sticky="ew")
        expense_btn_frame.grid_columnconfigure(0, weight=1)
        expense_btn_frame.grid_columnconfigure(1, weight=1)

        ctk.CTkButton(expense_btn_frame, text="Thêm", 
                     command=lambda: self.them_danhmuc(expense_frame, "Chi tiêu")).grid(row=0, column=0, padx=5, sticky="ew")
        ctk.CTkButton(expense_btn_frame, text="Xóa", 
                     command=lambda: self.xoa_danhmuc(expense_frame, "Chi tiêu")).grid(row=0, column=1, padx=5, sticky="ew")
        row_idx += 1
    
    def them_danhmuc(self, parent, type):
        # Thêm danh mục mới
        var = tk.StringVar()
        if type == "Thu nhập":
            self.income_categories.append(var)
        else:
            self.expense_categories.append(var)
        
        entry = ctk.CTkEntry(parent, textvariable=var)
        entry.pack(fill=tk.X, padx=5, pady=2)
        entry.focus()
    
    def xoa_danhmuc(self, parent, type):
        # Xóa danh mục cuối cùng
        if type == "Thu nhập" and self.income_categories:
            self.income_categories.pop()
            parent.winfo_children()[-2].destroy()
        elif type == "Chi tiêu" and self.expense_categories:
            self.expense_categories.pop()
            parent.winfo_children()[-2].destroy()
    
    def luu_caidat(self, window):
        try:
            # Cập nhật cài đặt
            self.settings["theme"] = self.theme_var.get()
            self.settings["currency"] = self.currency_entry.get()
            self.settings["language"] = self.language_var.get()
            self.settings["notifications"] = self.notification_var.get()
            self.settings["auto_backup"] = self.auto_backup_var.get()
            self.settings["backup_interval"] = int(self.interval_entry.get())
            
            # Cập nhật danh mục
            self.settings["categories"]["Thu nhập"] = [var.get() for var in self.income_categories]
            self.settings["categories"]["Chi tiêu"] = [var.get() for var in self.expense_categories]
            
            # Lưu cài đặt
            self.save_settings()
            
            # Cập nhật giao diện
            self.app.doi_theme()
            
            # Đóng cửa sổ
            window.destroy()
            
            messagebox.showinfo("Thành công", "Đã lưu cài đặt!")
            
        except Exception as e:
            messagebox.showerror("Lỗi", f"Không thể lưu cài đặt: {str(e)}")
    
    # Removed: doi_theme, update_colors, update_ui_colors (functionality moved to quanlychitieu.py or its modules) 