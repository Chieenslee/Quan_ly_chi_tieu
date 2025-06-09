import customtkinter as ctk
import darkdetect
import pandas as pd
from giao_dien import GiaoDien
from xuly_du_lieu import XuLyDuLieu
from bao_cao import BaoCao
from tinh_nang import TinhNang
from bao_mat import BaoMat
from bieu_do import BieuDo
from chatbot import Chatbot
from cai_dat import CaiDat
from thong_bao import ThongBao
from tinh_toan import TinhToan
from tkinter import messagebox
from datetime import datetime
import json
import os
import sys

class QuanLyChiTieu:
    def __init__(self, root):
        self.root = root
        # print(f"Type of self.root before setting title: {type(self.root)}")
        self.root.title("Quản Lý Chi Tiêu Cá Nhân Pro")
        self.root.geometry("1600x800")
        
        # Khởi tạo thuộc tính biểu đồ để tránh lỗi
        self.pie_chart = None
        self.trend_chart = None
        
        # Khởi tạo thuộc tính giao diện để tránh lỗi
        self.giao_dien = None
        
        # Thiết lập theme
        self.setup_theme()
        
        # Khởi tạo biến
        self.init_variables()
        
        # Khởi tạo các module
        self.init_modules()

        # Tạo giao diện
        self.tao_giaodien()
        
        # Khởi động các dịch vụ nền
        self.start_background_services()

    def setup_theme(self):
        if darkdetect.isDark():
            ctk.set_appearance_mode("dark")
            self.theme = "dark"
        else:
            ctk.set_appearance_mode("light")
            self.theme = "light"
        
        # Thiết lập màu sắc
        self.colors = {
            "light": {
                "bg": "#ffffff",
                "fg": "#000000",
                "accent": "#007bff",
                "success": "#28a745",
                "warning": "#ffc107",
                "danger": "#dc3545"
            },
            "dark": {
                "bg": "#2b2b2b",
                "fg": "#ffffff",
                "accent": "#0d6efd",
                "success": "#198754",
                "warning": "#ffc107",
                "danger": "#dc3545"
            }
        }

    def init_variables(self):
        # Khởi tạo các biến toàn cục
        self.transactions = []
        self.categories = {
            'income': ['Lương', 'Thưởng', 'Đầu tư', 'Khác'],
            'expense': ['Ăn uống', 'Di chuyển', 'Mua sắm', 'Giải trí', 'Khác']
        }
        self.settings = {
            'currency': 'VND',
            'language': 'vi',
            'theme': self.theme,
            'auto_backup': True,
            'backup_interval': 24,  # hours
            'last_backup': None,
            'budget_limit': 0
        }
        self.goals = []
        self.reminders = []

    def init_modules(self):
        # Khởi tạo các module
        self.xu_ly_du_lieu = XuLyDuLieu(self)
        self.bao_cao = BaoCao(self)
        self.tinh_nang = TinhNang(self)
        self.bao_mat = BaoMat(self)
        self.bieu_do = BieuDo(self)
        self.giao_dien = GiaoDien(self.root, self)
        self.chatbot = Chatbot(self.root)
        self.cai_dat = CaiDat(self)
        self.thong_bao = ThongBao(self)
        self.tinh_toan = TinhToan(self)

    def tao_giaodien(self):
        # Tạo giao diện chính
        self.giao_dien.tao_giaodien()
        
        # Create and display charts after UI is set up
        if self.giao_dien and hasattr(self.giao_dien, 'pie_chart_frame') and hasattr(self.giao_dien, 'trend_chart_frame'):
             self.bieu_do.create_and_display_charts(self.giao_dien.pie_chart_frame, self.giao_dien.trend_chart_frame)
             
        # Load transaction data and update summary/stats after charts are created
        self.xu_ly_du_lieu.load_transaction_data()
        self.update_financial_summary()
        self.update_category_stats()
        
        # Update budget display and reminders
        total_expense = sum(t['amount'] for t in self.transactions if t['type'] == 'expense')
        self.giao_dien.update_budget_display(self.settings.get('budget_limit', 0), total_expense)
        self.giao_dien.update_reminders()  # Ensure reminders are updated on startup

    def start_background_services(self):
        # Khởi động các dịch vụ nền
        self.update_charts() # This will now update the charts managed by BieuDo
        self.auto_backup_service()
        self.notification_service()

    def update_charts(self):
        # Cập nhật biểu đồ
        self.bieu_do.update_pie_chart()
        self.bieu_do.update_trend_chart()
        self.root.after(60000, self.update_charts)  # Cập nhật mỗi phút

    def auto_backup_service(self):
        # Dịch vụ sao lưu tự động
        if self.settings['auto_backup']:
            last_backup = self.settings['last_backup']
            if last_backup:
                last_backup = datetime.strptime(last_backup, "%Y%m%d_%H%M%S")
                hours_since_backup = (datetime.now() - last_backup).total_seconds() / 3600
                if hours_since_backup >= self.settings['backup_interval']:
                    self.xu_ly_du_lieu.backup_database()
            else:
                self.xu_ly_du_lieu.backup_database()
        
        self.root.after(3600000, self.auto_backup_service)  # Kiểm tra mỗi giờ

    def notification_service(self):
        # Dịch vụ thông báo
        # Kiểm tra các nhắc nhở
        current_time = datetime.now()
        for reminder in self.reminders:
            try:
                # Sử dụng trường 'datetime' mới
                reminder_datetime_str = reminder.get('datetime')
                if not reminder_datetime_str:
                    print(f"Cảnh báo: Nhắc nhở thiếu trường datetime: {reminder.get('title', 'Không tiêu đề')}")
                    continue

                reminder_time_obj = datetime.strptime(reminder_datetime_str, "%Y-%m-%d %H:%M")

                if reminder_time_obj <= current_time and not reminder.get('notified', False):
                    messagebox.showinfo(reminder.get('title', 'Nhắc nhở'), reminder.get('content', ''))
                    reminder['notified'] = True
                    self.xu_ly_du_lieu.save_database()
            except Exception as e:
                print(f"Lỗi khi kiểm tra reminder: {reminder.get('title', '')} - {e}")
                continue
        
        # Kiểm tra các mục tiêu
        for goal in self.goals:
            try:
                deadline = goal['deadline']
                if isinstance(deadline, str):
                    try:
                        deadline = datetime.strptime(deadline, "%d/%m/%Y")
                    except Exception:
                        deadline = datetime.strptime(deadline, "%Y-%m-%d") # Fallback to YYYY-MM-DD if DMY fails
                if deadline <= current_time and not goal['completed']:
                    messagebox.showinfo("Mục tiêu", f"Mục tiêu '{goal.get('title', '')}' đã đến hạn!")
                    goal['completed'] = True
                    self.xu_ly_du_lieu.save_database()
            except Exception as e:
                print(f"Lỗi khi kiểm tra goal: {goal.get('deadline', '')} - {e}")
                continue
        
        self.root.after(60000, self.notification_service)  # Kiểm tra mỗi phút
        self.giao_dien.update_reminders() # Cập nhật nhắc nhở trên giao diện chính

    def update_financial_summary(self):
        # Cập nhật thông tin tài chính
        total_income = sum(t['amount'] for t in self.transactions if t['type'] == 'income')
        total_expense = sum(t['amount'] for t in self.transactions if t['type'] == 'expense')
        balance = total_income - total_expense
        
        # Cập nhật giao diện
        self.giao_dien.update_summary(total_income, total_expense, balance)
        self.giao_dien.update_budget_display(self.settings.get('budget_limit', 0), total_expense)
        self.giao_dien.update_reminders() # Cập nhật nhắc nhở trên giao diện chính

    def update_category_stats(self):
        # Cập nhật thống kê theo danh mục
        df = pd.DataFrame(self.transactions)
        if not df.empty:
            # Lấy dữ liệu tháng hiện tại
            current_month = datetime.now().strftime("%Y-%m")
            # Chỉ định rõ định dạng khi chuyển cột date sang datetime
            df['date'] = pd.to_datetime(df['date'], format='%d/%m/%Y', errors='coerce')
            # Loại bỏ các dòng có ngày không hợp lệ sau chuyển đổi
            df.dropna(subset=['date'], inplace=True)
            df['month'] = df['date'].dt.strftime("%Y-%m")
            monthly_data = df[df['month'] == current_month]
            
            # Tính toán thống kê
            category_stats = monthly_data.groupby('category')['amount'].agg(['sum', 'count'])
            
            # Cập nhật giao diện
            self.giao_dien.update_category_stats(category_stats)

    def doi_theme(self):
        # Chuyển đổi theme
        if self.theme == "light":
            ctk.set_appearance_mode("dark")
            self.theme = "dark"
        else:
            ctk.set_appearance_mode("light")
            self.theme = "light"
        
        self.settings['theme'] = self.theme
        self.xu_ly_du_lieu.save_database()
        self.update_colors()

    def update_colors(self):
        # Cập nhật màu sắc dựa trên theme
        colors = self.colors[self.theme]
        self.giao_dien.update_colors(colors)

    def mo_caidat(self):
        # Gọi hàm mở cài đặt từ module CaiDat
        self.cai_dat.mo_caidat()

    def dong_bo_du_lieu(self):
        # Tạo cửa sổ đồng bộ dữ liệu
        window = ctk.CTkToplevel(self.root)
        window.title("Đồng Bộ Dữ Liệu")
        window.geometry("400x200")
        window.transient(self.root)
        window.grab_set()
        window.focus_force()
        
        # Tạo các tùy chọn
        ctk.CTkLabel(window, text="Chọn phương thức đồng bộ:").pack(pady=10)
        
        sync_type = ctk.StringVar(value="local")
        ctk.CTkRadioButton(window, text="Đồng bộ cục bộ", variable=sync_type, value="local").pack()
        ctk.CTkRadioButton(window, text="Đồng bộ đám mây", variable=sync_type, value="cloud").pack()
        
        def sync():
            try:
                if sync_type.get() == "local":
                    # Đồng bộ cục bộ
                    self.xu_ly_du_lieu.backup_database()
                else:
                    # Đồng bộ đám mây (chưa triển khai)
                    messagebox.showinfo("Thông báo", "Tính năng đồng bộ đám mây đang được phát triển!")
                
                window.destroy()
            except Exception as e:
                messagebox.showerror("Lỗi", f"Không thể đồng bộ dữ liệu: {str(e)}")
        
        ctk.CTkButton(window, text="Đồng bộ", command=sync).pack(pady=20)

    def kiem_tra_capnhat(self):
        # Gọi hàm kiểm tra cập nhật từ module ThongBao
        self.thong_bao.kiem_tra_capnhat()

    def bao_loi(self):
        # Gọi hàm báo lỗi từ module ThongBao
        self.thong_bao.bao_loi()

    def xem_huongdan(self):
        # Tạo cửa sổ hướng dẫn chi tiết
        window = ctk.CTkToplevel(self.root)
        window.title("Hướng dẫn sử dụng")
        window.geometry("800x600")
        window.transient(self.root)
        window.grab_set()
        window.focus_force()

        # Tiêu đề
        ctk.CTkLabel(window, text="HƯỚNG DẪN SỬ DỤNG ỨNG DỤNG", font=("Arial", 20, "bold")).pack(pady=10)

        # Khung chứa nội dung cuộn được
        text_frame = ctk.CTkFrame(window)
        text_frame.pack(fill="both", expand=True, padx=20, pady=10)

        # Tạo Textbox để hiển thị nội dung hướng dẫn
        help_text_box = ctk.CTkTextbox(text_frame, wrap="word", font=("Arial", 12))
        help_text_box.pack(side="left", fill="both", expand=True)

        # Thanh cuộn cho Textbox
        scrollbar = ctk.CTkScrollbar(text_frame, command=help_text_box.yview)
        scrollbar.pack(side="right", fill="y")
        help_text_box.configure(yscrollcommand=scrollbar.set)

        # Nội dung hướng dẫn chi tiết
        help_content = """
HƯỚNG DẪN SỬ DỤNG ỨNG DỤNG QUẢN LÝ CHI TIÊU CÁ NHÂN

Chào mừng bạn đến với ứng dụng Quản lý chi tiêu cá nhân! Ứng dụng này giúp bạn theo dõi thu nhập, chi tiêu, quản lý ngân sách, đặt mục tiêu tài chính và nhận nhắc nhở.

1.  Màn hình chính:
    *   Hiển thị tổng quan về thu nhập, chi tiêu và số dư của bạn.
    *   Bao gồm các biểu đồ trực quan giúp bạn dễ dàng theo dõi xu hướng tài chính.
    *   Phần "Nhắc nhở & Thống kê" sẽ hiển thị các nhắc nhở quan trọng và tóm tắt tình hình tài chính.

2.  Thêm Giao dịch:
    *   Nhấn vào nút "➕ Thêm giao dịch" trên thanh công cụ.
    *   Chọn loại giao dịch là "Thu nhập" hoặc "Chi tiêu".
    *   Nhập đầy đủ các thông tin: Ngày, Số tiền, Danh mục và Ghi chú.
    *   Nhấn "Lưu" để thêm giao dịch.

3.  Quản lý Giao dịch:
    *   Bạn có thể xem danh sách các giao dịch trong bảng.
    *   Sử dụng thanh tìm kiếm và bộ lọc để tìm kiếm và sắp xếp giao dịch.
    *   Chọn một giao dịch và nhấn "Sửa" để chỉnh sửa thông tin.
    *   Chọn một giao dịch và nhấn "Xóa" để loại bỏ giao dịch đó.

4.  Quản lý Nhắc nhở:
    *   Vào menu "Tính năng" -> "🔔 Quản lý nhắc nhở" để xem và quản lý các nhắc nhở.
    *   Nhấn "➕ Thêm nhắc nhở" để tạo nhắc nhở mới với Tiêu đề, Nội dung, Ngày và Giờ cụ thể.
    *   Các nhắc nhở sẽ hiển thị thông báo khi đến hạn.

5.  Quản lý Mục tiêu:
    *   Vào menu "Tính năng" -> "🎯 Quản lý mục tiêu" (nếu có).
    *   Thêm các mục tiêu tài chính của bạn với tên, số tiền và thời hạn.
    *   Ứng dụng sẽ nhắc nhở bạn khi mục tiêu sắp đến hạn.

6.  Quản lý Ngân sách:
    *   Nhấn vào biểu tượng "💲" trên thanh công cụ hoặc vào "Công cụ" -> "Ngân sách tháng".
    *   Nhập hoặc sửa ngân sách giới hạn cho tháng.
    *   Ứng dụng sẽ cảnh báo khi chi tiêu của bạn vượt quá 80% hoặc vượt ngân sách.

7.  Cài đặt:
    *   Vào menu "Cài đặt" để tùy chỉnh theme, tiền tệ, ngôn ngữ, và cài đặt sao lưu tự động.
    *   Quản lý các danh mục thu nhập và chi tiêu của bạn.

8.  Sao lưu & Khôi phục:
    *   Vào menu "Bảo mật" -> "📦 Sao lưu bảo mật" để tạo bản sao lưu dữ liệu của bạn.
    *   Vào menu "Bảo mật" -> "↩️ Khôi phục bảo mật" để khôi phục dữ liệu từ bản sao lưu.
    *   Ứng dụng cũng có tính năng sao lưu tự động (có thể cấu hình trong Cài đặt).

9.  Kiểm tra cập nhật:
    *   Vào menu "Trợ giúp" -> "Kiểm tra cập nhật" để xem có phiên bản mới của ứng dụng không.

Cảm ơn bạn đã sử dụng chương trình!
        """
        help_text_box.insert("1.0", help_content)
        help_text_box.configure(state="disabled") # Ngăn người dùng chỉnh sửa nội dung

    def xem_gioithieu(self):
        # Hiển thị thông tin về phần mềm
        messagebox.showinfo("Giới thiệu", """
        Quản Lý Chi Tiêu Cá Nhân Pro
        Phiên bản: 1.0.0
        Phát triển bởi: Lê Trọng Chiến
        
        Một ứng dụng quản lý tài chính cá nhân đơn giản và hiệu quả.
        """)

    def mo_chatbot(self):
        # Mở cửa sổ chatbot
        self.chatbot.create_chatbot_window()

    def nhap_sua_ngansach(self):
        # Tạo cửa sổ nhập/sửa ngân sách tháng
        window = ctk.CTkToplevel(self.root)
        window.title("Ngân sách tháng")
        window.geometry("300x300")
        window.transient(self.root)
        window.grab_set()
        window.focus_force()

        current_budget = self.settings.get('budget_limit', 0)

        ctk.CTkLabel(window, text=f"Ngân sách hiện tại: {current_budget:,.0f} VNĐ").pack(pady=5)
        
        ctk.CTkLabel(window, text="Nhập ngân sách mới:").pack(pady=5)
        budget_entry = ctk.CTkEntry(window)
        budget_entry.insert(0, str(current_budget))
        budget_entry.pack(pady=5)

        def save_budget():
            try:
                new_budget = float(budget_entry.get())
                if new_budget < 0:
                    messagebox.showwarning("Cảnh báo", "Ngân sách không thể là số âm!")
                    return
                
                self.settings['budget_limit'] = new_budget
                self.xu_ly_du_lieu.save_database()
                # Cập nhật hiển thị ngân sách sau khi lưu
                total_expense = sum(t['amount'] for t in self.transactions if t['type'] == 'expense')
                self.giao_dien.update_budget_display(new_budget, total_expense)
                messagebox.showinfo("Thành công", f"Đã cập nhật ngân sách thành: {new_budget:,.0f} VNĐ")
                window.destroy()
            except ValueError:
                messagebox.showerror("Lỗi", "Vui lòng nhập số hợp lệ cho ngân sách!")
            except Exception as e:
                messagebox.showerror("Lỗi", f"Không thể lưu ngân sách: {str(e)}")

        ctk.CTkButton(window, text="Lưu ngân sách", command=save_budget).pack(pady=10)

    def get_monthly_income(self):
        """Lấy tổng thu nhập trong tháng hiện tại"""
        current_month = datetime.now().month
        current_year = datetime.now().year
        monthly_income = 0
        transactions_data = self.xu_ly_du_lieu.doc_du_lieu()
        
        for transaction in transactions_data:
            try:
                # Check if transaction is a dictionary and has 'date' and 'type' keys
                if isinstance(transaction, dict) and 'date' in transaction and 'type' in transaction:
                    transaction_date = datetime.strptime(transaction['date'], "%Y-%m-%d")
                    if transaction['type'] == 'income' and transaction_date.month == current_month and transaction_date.year == current_year:
                        monthly_income += transaction['amount']
            except Exception as e:
                print(f"Lỗi khi xử lý giao dịch thu nhập: {transaction.get('date', '') if isinstance(transaction, dict) else str(transaction)} - {e}")
                continue
        return monthly_income

    def get_monthly_expense(self):
        """Lấy tổng chi tiêu trong tháng hiện tại"""
        current_month = datetime.now().month
        current_year = datetime.now().year
        monthly_expense = 0
        transactions_data = self.xu_ly_du_lieu.doc_du_lieu()

        for transaction in transactions_data:
            try:
                # Check if transaction is a dictionary and has 'date' and 'type' keys
                if isinstance(transaction, dict) and 'date' in transaction and 'type' in transaction:
                    transaction_date = datetime.strptime(transaction['date'], "%Y-%m-%d")
                    if transaction['type'] == 'expense' and transaction_date.month == current_month and transaction_date.year == current_year:
                        monthly_expense += transaction['amount']
            except Exception as e:
                print(f"Lỗi khi xử lý giao dịch chi tiêu: {transaction.get('date', '') if isinstance(transaction, dict) else str(transaction)} - {e}")
                continue
        return monthly_expense

if __name__ == "__main__":
    root = ctk.CTk()
    app = QuanLyChiTieu(root)
    root.mainloop() 