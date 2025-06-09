import customtkinter as ctk
from tkinter import messagebox, ttk, filedialog
import tkinter as tk
from datetime import datetime
import pandas as pd
import numpy as np
from sklearn.linear_model import LinearRegression
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.backends.backend_tkagg import NavigationToolbar2Tk
import matplotlib.ticker as mticker
import matplotlib.dates as mdates
import matplotlib.pyplot as plt
import json

class TinhNang:
    def __init__(self, app):
        self.app = app

    def xem_nhacnho(self):
        # Tạo cửa sổ xem và quản lý nhắc nhở
        window = ctk.CTkToplevel(self.app.root)
        window.title("Quản lý nhắc nhở")
        window.geometry("800x600")
        window.transient(self.app.root)
        window.grab_set()
        window.focus_force()

        # Frame tìm kiếm và lọc
        filter_frame = ctk.CTkFrame(window)
        filter_frame.pack(fill=tk.X, padx=10, pady=5)
        
        ctk.CTkLabel(filter_frame, text="Tìm kiếm:").pack(side=tk.LEFT, padx=5)
        search_entry = ctk.CTkEntry(filter_frame)
        search_entry.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=5)

        ctk.CTkLabel(filter_frame, text="Trạng thái:").pack(side=tk.LEFT, padx=5)
        status_var = ctk.StringVar(value="Tất cả")
        status_combo = ctk.CTkComboBox(filter_frame, 
                                   values=["Tất cả", "Chưa thông báo", "Đã thông báo"],
                                   variable=status_var)
        status_combo.pack(side=tk.LEFT, padx=5)
        
        # Frame bảng nhắc nhở
        table_frame = ctk.CTkFrame(window)
        table_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)
        
        # Tạo bảng
        columns = ("id", "title", "content", "datetime", "notified")
        self.reminder_tree = ttk.Treeview(table_frame, columns=columns, show="headings")

        # Định dạng cột
        self.reminder_tree.heading("id", text="ID")
        self.reminder_tree.heading("title", text="Tiêu đề")
        self.reminder_tree.heading("content", text="Nội dung")
        self.reminder_tree.heading("datetime", text="Thời gian")
        self.reminder_tree.heading("notified", text="Đã thông báo")
        
        self.reminder_tree.column("id", width=50)
        self.reminder_tree.column("title", width=200)
        self.reminder_tree.column("content", width=300)
        self.reminder_tree.column("datetime", width=150)
        self.reminder_tree.column("notified", width=100)

        # Thêm thanh cuộn
        scrollbar = ttk.Scrollbar(table_frame, orient=tk.VERTICAL, command=self.reminder_tree.yview)
        self.reminder_tree.configure(yscrollcommand=scrollbar.set)

        # Đặt vị trí
        self.reminder_tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        # Nút làm mới, sửa, xóa
        button_frame = ctk.CTkFrame(window)
        button_frame.pack(pady=10)
        
        ctk.CTkButton(button_frame, text="Làm mới", 
                     command=lambda: load_reminders_data()).pack(side=tk.LEFT, padx=5)
        ctk.CTkButton(button_frame, text="Sửa", 
                     command=self.sua_nhacnho).pack(side=tk.LEFT, padx=5)
        ctk.CTkButton(button_frame, text="Xóa", 
                     command=self.xoa_nhacnho).pack(side=tk.LEFT, padx=5)

        def load_reminders_data():
            # Xóa dữ liệu cũ
            for item in self.reminder_tree.get_children():
                self.reminder_tree.delete(item)
            
            # Lọc dữ liệu
            filtered_reminders = []
            search_text = search_entry.get().lower()
            status_filter = status_var.get()
            
            for i, reminder in enumerate(self.app.reminders):
                # Thêm ID nếu chưa có
                if 'id' not in reminder:
                    reminder['id'] = i + 1
                
                # Kiểm tra tìm kiếm
                if search_text and search_text not in reminder.get('title', '').lower() and search_text not in reminder.get('content', '').lower():
                    continue
                
                # Kiểm tra trạng thái
                if status_filter == "Chưa thông báo" and reminder.get('notified', False):
                    continue
                elif status_filter == "Đã thông báo" and not reminder.get('notified', False):
                    continue
                
                filtered_reminders.append(reminder)
            
            # Thêm dữ liệu mới
            for reminder in filtered_reminders:
                self.reminder_tree.insert("", tk.END, values=(
                    reminder.get('id', ''),
                    reminder.get('title', ''),
                    reminder.get('content', ''),
                    reminder.get('datetime', ''),
                    "Có" if reminder.get('notified', False) else "Không"
                ))
        
        # Gắn sự kiện cập nhật
        search_entry.bind("<KeyRelease>", lambda e: load_reminders_data())
        status_var.trace_add("write", lambda *args: load_reminders_data())
        
        # Tải dữ liệu lần đầu
        load_reminders_data()

    def tinh_laisuat(self):
        # Tạo cửa sổ tính lãi suất
        window = ctk.CTkToplevel(self.app.root)
        window.title("Tính lãi suất")
        window.geometry("400x400")
        window.transient(self.app.root)
        window.grab_set()
        window.focus_force()
        
        # Lãi suất ban đầu
        ctk.CTkLabel(window, text="Số tiền ban đầu:").pack(pady=5)
        initial_amount_entry = ctk.CTkEntry(window)
        initial_amount_entry.pack(pady=5)
        
        # Lãi suất hàng năm
        ctk.CTkLabel(window, text="Lãi suất hàng năm (%):").pack(pady=5)
        interest_rate_entry = ctk.CTkEntry(window)
        interest_rate_entry.pack(pady=5)
        
        # Số năm
        ctk.CTkLabel(window, text="Số năm:").pack(pady=5)
        years_entry = ctk.CTkEntry(window)
        years_entry.pack(pady=5)
        
        # Kết quả
        result_label = ctk.CTkLabel(window, text="Kết quả:")
        result_label.pack(pady=10)
        
        def calculate():
            try:
                initial_amount = float(initial_amount_entry.get())
                interest_rate = float(interest_rate_entry.get()) / 100
                years = int(years_entry.get())
                
                final_amount = initial_amount * (1 + interest_rate)**years
                result_label.configure(text=f"Số tiền cuối cùng: {final_amount:,.0f} VND")
            except ValueError:
                messagebox.showerror("Lỗi", "Vui lòng nhập số hợp lệ!")
            except Exception as e:
                messagebox.showerror("Lỗi", f"Đã xảy ra lỗi: {str(e)}")
        
        ctk.CTkButton(window, text="Tính toán", command=calculate).pack(pady=20)

    def tinh_thue(self):
        # Tạo cửa sổ tính thuế
        window = ctk.CTkToplevel(self.app.root)
        window.title("Tính thuế")
        window.geometry("400x300")
        window.transient(self.app.root)
        window.grab_set()
        window.focus_force()
        
        # Thu nhập chịu thuế
        ctk.CTkLabel(window, text="Thu nhập chịu thuế (VNĐ):").pack(pady=5)
        income_entry = ctk.CTkEntry(window)
        income_entry.pack(pady=5)
        
        # Loại thuế
        ctk.CTkLabel(window, text="Loại thuế:").pack(pady=5)
        tax_type_var = ctk.StringVar(value="Thu nhập cá nhân")
        tax_type_optionmenu = ctk.CTkOptionMenu(window, variable=tax_type_var,
                                               values=["Thu nhập cá nhân", "Thuế VAT"])
        tax_type_optionmenu.pack(pady=5)
        
        # Kết quả
        result_label = ctk.CTkLabel(window, text="Kết quả:")
        result_label.pack(pady=10)
        
        def calculate():
            try:
                income = float(income_entry.get())
                tax_type = tax_type_var.get()
                tax_amount = 0
                
                if tax_type == "Thu nhập cá nhân":
                    if income <= 9000000:
                        tax_amount = income * 0.05
                    elif income <= 15000000:
                        tax_amount = income * 0.1 - 0.25 * 1000000
                    elif income <= 30000000:
                        tax_amount = income * 0.15 - 750000
                    else:
                        tax_amount = income * 0.2 - 1650000
                elif tax_type == "Thuế VAT":
                    tax_amount = income * 0.1 # 10% VAT
                
                result_label.configure(text=f"Số tiền thuế phải trả: {tax_amount:,.0f} VNĐ")
            except ValueError:
                messagebox.showerror("Lỗi", "Vui lòng nhập số hợp lệ cho thu nhập!")
            except Exception as e:
                messagebox.showerror("Lỗi", f"Đã xảy ra lỗi: {str(e)}")
        
        ctk.CTkButton(window, text="Tính toán", command=calculate).pack(pady=20)

    def lap_kehoach(self):
        # Tạo cửa sổ lập kế hoạch
        window = ctk.CTkToplevel(self.app.root)
        window.title("Lập kế hoạch")
        window.geometry("500x500")
        window.transient(self.app.root)
        window.grab_set()
        window.focus_force()
        
        # Thu nhập dự kiến
        ctk.CTkLabel(window, text="Thu nhập dự kiến (VNĐ/tháng):").pack(pady=5)
        income_entry = ctk.CTkEntry(window)
        income_entry.pack(pady=5)
        
        # Chi tiêu dự kiến
        ctk.CTkLabel(window, text="Chi tiêu dự kiến (VNĐ/tháng):").pack(pady=5)
        expense_entry = ctk.CTkEntry(window)
        expense_entry.pack(pady=5)
        
        # Mục tiêu tiết kiệm
        ctk.CTkLabel(window, text="Mục tiêu tiết kiệm (VNĐ/tháng):").pack(pady=5)
        saving_target_entry = ctk.CTkEntry(window)
        saving_target_entry.pack(pady=5)
        
        # Thời gian (tháng)
        ctk.CTkLabel(window, text="Thời gian (tháng):").pack(pady=5)
        months_entry = ctk.CTkEntry(window)
        months_entry.pack(pady=5)
        
        # Kết quả
        result_label = ctk.CTkLabel(window, text="Kết quả:")
        result_label.pack(pady=10)
        
        def calculate():
            try:
                income_per_month = float(income_entry.get())
                expense_per_month = float(expense_entry.get())
                saving_target_per_month = float(saving_target_entry.get())
                months = int(months_entry.get())
                
                total_income = income_per_month * months
                total_expense = expense_per_month * months
                total_savings = (income_per_month - expense_per_month) * months
                
                if total_savings >= saving_target_per_month * months:
                    message = f"Kế hoạch của bạn khả thi!\nTổng thu: {total_income:,.0f} VNĐ\nTổng chi: {total_expense:,.0f} VNĐ\nTổng tiết kiệm: {total_savings:,.0f} VNĐ"
                else:
                    message = f"Kế hoạch của bạn cần điều chỉnh.\nBạn cần tiết kiệm thêm {saving_target_per_month * months - total_savings:,.0f} VNĐ.\nTổng thu: {total_income:,.0f} VNĐ\nTổng chi: {total_expense:,.0f} VNĐ\nTổng tiết kiệm: {total_savings:,.0f} VNĐ"
                
                result_label.configure(text=message)
            except ValueError:
                messagebox.showerror("Lỗi", "Vui lòng nhập số hợp lệ!")
            except Exception as e:
                messagebox.showerror("Lỗi", f"Đã xảy ra lỗi: {str(e)}")
        
        ctk.CTkButton(window, text="Tính toán", command=calculate).pack(pady=20)

    def theo_doi_muctieu(self):
        # Tạo cửa sổ theo dõi mục tiêu
        window = ctk.CTkToplevel(self.app.root)
        window.title("Theo dõi mục tiêu")
        window.geometry("1000x700")
        window.transient(self.app.root)
        window.grab_set()
        window.focus_force()
        
        # Thanh tìm kiếm và lọc
        filter_frame = ctk.CTkFrame(window)
        filter_frame.pack(fill=tk.X, padx=10, pady=5)
        
        ctk.CTkLabel(filter_frame, text="Tìm kiếm:").pack(side=tk.LEFT, padx=5)
        search_entry = ctk.CTkEntry(filter_frame, width=200)
        search_entry.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=5)

        ctk.CTkLabel(filter_frame, text="Trạng thái:").pack(side=tk.LEFT, padx=5)
        status_var = ctk.StringVar(value="Tất cả")
        status_combo = ctk.CTkComboBox(filter_frame, 
                                   values=["Tất cả", "Chưa hoàn thành", "Đã hoàn thành"],
                                   variable=status_var)
        status_combo.pack(side=tk.LEFT, padx=5)
        
        # Frame bảng mục tiêu
        table_frame = ctk.CTkFrame(window)
        table_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)
        
        # Tạo bảng
        columns = ("title", "amount", "saved", "progress", "deadline", "completed")
        self.goal_tree = ttk.Treeview(table_frame, columns=columns, show="headings")
        
        # Định dạng cột
        self.goal_tree.heading("title", text="Tên mục tiêu")
        self.goal_tree.heading("amount", text="Số tiền mục tiêu")
        self.goal_tree.heading("saved", text="Đã tiết kiệm")
        self.goal_tree.heading("progress", text="Tiến độ (%)")
        self.goal_tree.heading("deadline", text="Hạn chót")
        self.goal_tree.heading("completed", text="Hoàn thành")
        
        self.goal_tree.column("title", width=200)
        self.goal_tree.column("amount", width=120)
        self.goal_tree.column("saved", width=120)
        self.goal_tree.column("progress", width=100)
        self.goal_tree.column("deadline", width=100)
        self.goal_tree.column("completed", width=80)
        
        # Thêm thanh cuộn
        scrollbar = ttk.Scrollbar(table_frame, orient=tk.VERTICAL, command=self.goal_tree.yview)
        self.goal_tree.configure(yscrollcommand=scrollbar.set)
        
        # Đặt vị trí
        self.goal_tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        # Nút làm mới, sửa, xóa, thêm
        button_frame = ctk.CTkFrame(window)
        button_frame.pack(pady=10)
        
        ctk.CTkButton(button_frame, text="Làm mới", 
                     command=lambda: refresh()).pack(side=tk.LEFT, padx=5)
        ctk.CTkButton(button_frame, text="Sửa", 
                     command=lambda: edit_goal()).pack(side=tk.LEFT, padx=5)
        ctk.CTkButton(button_frame, text="Xóa", 
                     command=lambda: delete_goal()).pack(side=tk.LEFT, padx=5)
        ctk.CTkButton(button_frame, text="Thêm", 
                     command=lambda: add_goal()).pack(side=tk.LEFT, padx=5)
        
        def refresh():
            # Xóa dữ liệu cũ
            for item in self.goal_tree.get_children():
                self.goal_tree.delete(item)
            
            # Lọc dữ liệu
            filtered_goals = []
            search_text = search_entry.get().lower()
            status_filter = status_var.get()
            
            for goal in self.app.goals:
                if search_text and search_text not in goal['title'].lower():
                    continue
                
                if status_filter == "Chưa hoàn thành" and goal['completed']:
                    continue
                elif status_filter == "Đã hoàn thành" and not goal['completed']:
                    continue
                
                # Tính toán tiến độ
                progress_value = self.calculate_goal_progress(goal)
                
                filtered_goals.append(goal)
            
            # Thêm dữ liệu mới
            for goal in filtered_goals:
                progress_value = self.calculate_goal_progress(goal) # Recalculate for display
                self.goal_tree.insert("", tk.END, values=(
                    goal['title'],
                    f"{goal['amount']:,.0f}",
                    f"{goal['saved']:,.0f}",
                    f"{progress_value:.1f}%",
                    goal['deadline'],
                    "Có" if goal['completed'] else "Không"
                ))
        
        def edit_goal():
            selected_item = self.goal_tree.selection()
            if not selected_item:
                messagebox.showwarning("Cảnh báo", "Vui lòng chọn mục tiêu cần sửa!")
                return
            
            # Lấy thông tin mục tiêu từ Treeview
            item_values = self.goal_tree.item(selected_item[0])['values']
            original_title = item_values[0]
            
            # Tìm mục tiêu gốc trong self.app.goals
            goal_to_edit = next((g for g in self.app.goals if g['title'] == original_title), None)
            if not goal_to_edit:
                messagebox.showerror("Lỗi", "Không tìm thấy mục tiêu này!")
                return
            
            window = ctk.CTkToplevel(self.app.root)
            window.title("Sửa mục tiêu")
            window.geometry("400x400")
            
            ctk.CTkLabel(window, text="Tên mục tiêu:").pack(pady=5)
            title_entry = ctk.CTkEntry(window)
            title_entry.insert(0, goal_to_edit['title'])
            title_entry.pack(pady=5)
            
            ctk.CTkLabel(window, text="Số tiền mục tiêu (VNĐ):").pack(pady=5)
            amount_entry = ctk.CTkEntry(window)
            amount_entry.insert(0, str(goal_to_edit['amount']))
            amount_entry.pack(pady=5)
            
            ctk.CTkLabel(window, text="Đã tiết kiệm (VNĐ):").pack(pady=5)
            saved_entry = ctk.CTkEntry(window)
            saved_entry.insert(0, str(goal_to_edit['saved']))
            saved_entry.pack(pady=5)
            
            ctk.CTkLabel(window, text="Hạn chót (DD/MM/YYYY):").pack(pady=5)
            deadline_entry = ctk.CTkEntry(window)
            deadline_entry.insert(0, goal_to_edit['deadline'])
            deadline_entry.pack(pady=5)
            
            ctk.CTkLabel(window, text="Hoàn thành:").pack(pady=5)
            completed_var = ctk.BooleanVar(value=goal_to_edit['completed'])
            ctk.CTkCheckBox(window, text="Đã hoàn thành", variable=completed_var).pack(pady=5)
            
            def save_changes():
                try:
                    new_title = title_entry.get()
                    new_amount = float(amount_entry.get())
                    new_saved = float(saved_entry.get())
                    new_deadline = deadline_entry.get()
                    new_completed = completed_var.get()
                    
                    # Validate data
                    datetime.strptime(new_deadline, "%d/%m/%Y")

                    # Update the original goal object
                    goal_to_edit['title'] = new_title
                    goal_to_edit['amount'] = new_amount
                    goal_to_edit['saved'] = new_saved
                    goal_to_edit['deadline'] = new_deadline
                    goal_to_edit['completed'] = new_completed
                    
                    self.app.xu_ly_du_lieu.save_database()
                    refresh()
                    window.destroy()
                except ValueError as ve:
                    messagebox.showerror("Lỗi", f"Dữ liệu không hợp lệ: {ve}")
                except Exception as e:
                    messagebox.showerror("Lỗi", f"Không thể lưu thay đổi: {e}")
            
            ctk.CTkButton(window, text="Lưu thay đổi", command=save_changes).pack(pady=20)

        def delete_goal():
            selected_item = self.goal_tree.selection()
            if not selected_item:
                messagebox.showwarning("Cảnh báo", "Vui lòng chọn mục tiêu cần xóa!")
                return
            
            if not messagebox.askyesno("Xác nhận", "Bạn có chắc chắn muốn xóa mục tiêu này?"):
                return
            
            item_values = self.goal_tree.item(selected_item[0])['values']
            title_to_delete = item_values[0]
            
            self.app.goals = [g for g in self.app.goals if g['title'] != title_to_delete]
            self.app.xu_ly_du_lieu.save_database()
            refresh()
            messagebox.showinfo("Thành công", "Đã xóa mục tiêu!")
        
        def add_goal():
            # Tạo cửa sổ thêm mục tiêu mới
            window = ctk.CTkToplevel(self.app.root)
            window.title("Thêm mục tiêu mới")
            window.geometry("400x400")
            
            ctk.CTkLabel(window, text="Tên mục tiêu:").pack(pady=5)
            title_entry = ctk.CTkEntry(window)
            title_entry.pack(pady=5)
            
            ctk.CTkLabel(window, text="Số tiền mục tiêu (VNĐ):").pack(pady=5)
            amount_entry = ctk.CTkEntry(window)
            amount_entry.pack(pady=5)
            
            ctk.CTkLabel(window, text="Đã tiết kiệm (VNĐ):").pack(pady=5)
            saved_entry = ctk.CTkEntry(window)
            saved_entry.insert(0, "0") # Default to 0 saved
            saved_entry.pack(pady=5)
            
            ctk.CTkLabel(window, text="Hạn chót (DD/MM/YYYY):").pack(pady=5)
            deadline_entry = ctk.CTkEntry(window)
            deadline_entry.insert(0, datetime.now().strftime("%d/%m/%Y"))
            deadline_entry.pack(pady=5)
            
            def save_goal():
                try:
                    title = title_entry.get()
                    amount = float(amount_entry.get())
                    saved = float(saved_entry.get())
                    deadline = deadline_entry.get()
                    
                    if not title or not amount or not deadline:
                        messagebox.showwarning("Cảnh báo", "Vui lòng điền đầy đủ thông tin!")
                        return
                    
                    # Validate date format
                    datetime.strptime(deadline, "%d/%m/%Y")

                    new_goal = {
                        'title': title,
                        'amount': amount,
                        'saved': saved,
                        'deadline': deadline,
                        'completed': False
                    }
                    
                    self.app.goals.append(new_goal)
                    self.app.xu_ly_du_lieu.save_database()
                    refresh()
                    window.destroy()
                    messagebox.showinfo("Thành công", "Đã thêm mục tiêu mới!")
                except ValueError as ve:
                    messagebox.showerror("Lỗi", f"Dữ liệu không hợp lệ: {ve}")
                except Exception as e:
                    messagebox.showerror("Lỗi", f"Không thể thêm mục tiêu: {e}")
            
            ctk.CTkButton(window, text="Lưu mục tiêu", command=save_goal).pack(pady=20)
        
        # Gắn sự kiện cập nhật
        search_entry.bind("<KeyRelease>", lambda e: refresh())
        status_var.trace_add("write", lambda *args: refresh())
        
        # Tải dữ liệu lần đầu
        refresh()

    def calculate_goal_progress(self, goal):
        # Tính tiến độ mục tiêu
        if goal['amount'] == 0:
            return 0
        return (goal['saved'] / goal['amount']) * 100

    def phan_tich_xuhuong(self):
        # Tạo cửa sổ phân tích xu hướng
        window = ctk.CTkToplevel(self.app.root)
        window.title("Phân tích xu hướng")
        window.geometry("800x600")
        window.transient(self.app.root)
        window.grab_set()
        window.focus_force()
        
        # Tạo DataFrame
        df = pd.DataFrame(self.app.transactions)
        if df.empty:
            messagebox.showinfo("Thông báo", "Không có dữ liệu để phân tích")
            window.destroy()
            return
        
        # Chuyển đổi ngày
        df['date'] = pd.to_datetime(df['date'], format='%d/%m/%Y')
        df['month'] = df['date'].dt.to_period('M')
        
        # Tính toán dữ liệu
        monthly_income = df[df['type'] == 'income'].groupby('month')['amount'].sum()
        monthly_expense = df[df['type'] == 'expense'].groupby('month')['amount'].sum()
        
        # Tạo biểu đồ
        fig, ax = plt.subplots(figsize=(10, 6))
        
        monthly_income.plot(ax=ax, label='Thu nhập', marker='o')
        monthly_expense.plot(ax=ax, label='Chi tiêu', marker='o')
        
        ax.set_title('Xu hướng thu nhập và chi tiêu hàng tháng')
        ax.set_xlabel('Tháng')
        ax.set_ylabel('Số tiền (VNĐ)')
        ax.legend()
        ax.grid(True)
        
        # Định dạng trục x
        ax.xaxis.set_major_formatter(plt.matplotlib.dates.DateFormatter('%Y-%m'))
        plt.xticks(rotation=45)
        
        # Hiển thị biểu đồ
        canvas = FigureCanvasTkAgg(fig, window)
        canvas.draw()
        canvas.get_tk_widget().pack(fill="both", expand=True)
        
        # Thêm thanh công cụ
        toolbar = NavigationToolbar2Tk(canvas, window)
        toolbar.update()

    def currency_formatter(self, x, pos):
        # Định dạng tiền tệ cho biểu đồ
        return f"{x:,.0f} VND"

    def phan_tich_thoiquen(self):
        # Tạo cửa sổ phân tích thói quen
        window = ctk.CTkToplevel(self.app.root)
        window.title("Phân tích thói quen chi tiêu")
        window.geometry("800x600")
        window.transient(self.app.root)
        window.grab_set()
        window.focus_force()
        
        # Tạo DataFrame
        df = pd.DataFrame(self.app.transactions)
        if df.empty:
            messagebox.showinfo("Thông báo", "Không có dữ liệu để phân tích")
            window.destroy()
            return
        
        # Chuyển đổi ngày
        df['date'] = pd.to_datetime(df['date'], format='%d/%m/%Y')
        df['day_of_week'] = df['date'].dt.day_name()
        df['hour_of_day'] = df['date'].dt.hour
        
        # Tính toán dữ liệu
        expense_by_day = df[df['type'] == 'expense'].groupby('day_of_week')['amount'].sum()
        expense_by_hour = df[df['type'] == 'expense'].groupby('hour_of_day')['amount'].sum()
        
        # Tạo biểu đồ
        fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 5))
        
        expense_by_day.plot(kind='bar', ax=ax1)
        ax1.set_title('Tổng chi tiêu theo ngày trong tuần')
        ax1.set_xlabel('Ngày trong tuần')
        ax1.set_ylabel('Số tiền (VNĐ)')
        plt.xticks(rotation=45)
        
        expense_by_hour.plot(kind='line', ax=ax2, marker='o')
        ax2.set_title('Tổng chi tiêu theo giờ trong ngày')
        ax2.set_xlabel('Giờ trong ngày')
        ax2.set_ylabel('Số tiền (VNĐ)')
        ax2.set_xticks(range(24)) # Đặt nhãn cho tất cả các giờ
        
        # Hiển thị biểu đồ
        canvas = FigureCanvasTkAgg(fig, window)
        canvas.draw()
        canvas.get_tk_widget().pack(fill="both", expand=True)
        
        # Thêm thanh công cụ
        toolbar = NavigationToolbar2Tk(canvas, window)
        toolbar.update() 

    def xuat_baocao(self):
        """Xuất báo cáo chi tiêu"""
        window = ctk.CTkToplevel(self.app.root)
        window.title("Xuất báo cáo")
        window.geometry("500x400")
        window.transient(self.app.root)
        window.grab_set()
        window.focus_force()
        
        # Chọn loại báo cáo
        ctk.CTkLabel(window, text="Loại báo cáo:").pack(pady=5)
        report_type_var = ctk.StringVar(value="Báo cáo tổng hợp")
        report_type_optionmenu = ctk.CTkOptionMenu(window, variable=report_type_var,
                                                 values=["Báo cáo tổng hợp", "Báo cáo chi tiết", "Báo cáo theo danh mục"])
        report_type_optionmenu.pack(pady=5)
        
        # Chọn thời gian
        ctk.CTkLabel(window, text="Thời gian:").pack(pady=5)
        time_frame_var = ctk.StringVar(value="Tháng này")
        time_frame_optionmenu = ctk.CTkOptionMenu(window, variable=time_frame_var,
                                                values=["Tháng này", "Quý này", "Năm nay", "Tùy chọn"])
        time_frame_optionmenu.pack(pady=5)
        
        # Chọn định dạng
        ctk.CTkLabel(window, text="Định dạng:").pack(pady=5)
        format_var = ctk.StringVar(value="PDF")
        format_optionmenu = ctk.CTkOptionMenu(window, variable=format_var,
                                            values=["PDF", "Excel", "CSV"])
        format_optionmenu.pack(pady=5)
        
        def export_report():
            try:
                # Lấy thông tin báo cáo
                report_type = report_type_var.get()
                time_frame = time_frame_var.get()
                export_format = format_var.get()
                
                # Tạo tên file
                timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                filename = f"baocao_{report_type}_{time_frame}_{timestamp}.{export_format.lower()}"
                
                # Xuất báo cáo
                if export_format == "PDF":
                    self.xuat_baocao_pdf(report_type, time_frame, filename)
                elif export_format == "Excel":
                    self.xuat_baocao_excel(report_type, time_frame, filename)
                else:  # CSV
                    self.xuat_baocao_csv(report_type, time_frame, filename)
                
                messagebox.showinfo("Thành công", f"Đã xuất báo cáo thành công: {filename}")
            except Exception as e:
                messagebox.showerror("Lỗi", f"Không thể xuất báo cáo: {str(e)}")
        
        ctk.CTkButton(window, text="Xuất báo cáo", command=export_report).pack(pady=20)

    def saoluu_khoiphuc(self):
        """Sao lưu và khôi phục dữ liệu"""
        window = ctk.CTkToplevel(self.app.root)
        window.title("Sao lưu và khôi phục")
        window.geometry("400x300")
        window.transient(self.app.root)
        window.grab_set()
        window.focus_force()
        
        def backup_data():
            try:
                # Tạo tên file backup
                timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                filename = f"backup_{timestamp}.json"
                
                # Sao lưu dữ liệu
                data = {
                    'transactions': self.app.xu_ly_du_lieu.doc_du_lieu(),
                    'categories': self.app.xu_ly_du_lieu.doc_danh_muc(),
                    'goals': self.app.xu_ly_du_lieu.doc_muc_tieu(),
                    'reminders': self.app.reminders
                }
                
                with open(filename, 'w', encoding='utf-8') as f:
                    json.dump(data, f, ensure_ascii=False, indent=4)
                
                messagebox.showinfo("Thành công", f"Đã sao lưu dữ liệu thành công: {filename}")
            except Exception as e:
                messagebox.showerror("Lỗi", f"Không thể sao lưu dữ liệu: {str(e)}")
        
        def restore_data():
            try:
                # Chọn file backup
                filename = filedialog.askopenfilename(
                    title="Chọn file backup",
                    filetypes=[("JSON files", "*.json"), ("All files", "*.*")]
                )
                
                if filename:
                    # Đọc dữ liệu từ file
                    with open(filename, 'r', encoding='utf-8') as f:
                        data = json.load(f)
                    
                    # Khôi phục dữ liệu
                    self.app.xu_ly_du_lieu.luu_du_lieu(data['transactions'])
                    self.app.xu_ly_du_lieu.luu_danh_muc(data['categories'])
                    self.app.xu_ly_du_lieu.luu_muc_tieu(data['goals'])
                    self.app.reminders = data['reminders']
                    
                    messagebox.showinfo("Thành công", "Đã khôi phục dữ liệu thành công")
            except Exception as e:
                messagebox.showerror("Lỗi", f"Không thể khôi phục dữ liệu: {str(e)}")
        
        # Nút sao lưu và khôi phục
        ctk.CTkButton(window, text="Sao lưu dữ liệu", command=backup_data).pack(pady=10)
        ctk.CTkButton(window, text="Khôi phục dữ liệu", command=restore_data).pack(pady=10)

    def quanly_danhmuc(self):
        """Quản lý danh mục chi tiêu"""
        window = ctk.CTkToplevel(self.app.root)
        window.title("Quản lý danh mục")
        window.geometry("600x400")
        window.transient(self.app.root)
        window.grab_set()
        window.focus_force()
        
        # Frame danh sách danh mục
        list_frame = ctk.CTkFrame(window)
        list_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)
        
        # Tạo bảng
        columns = ("id", "ten", "loai", "mota")
        self.category_tree = ttk.Treeview(list_frame, columns=columns, show="headings")
        
        # Định dạng cột
        self.category_tree.heading("id", text="ID")
        self.category_tree.heading("ten", text="Tên danh mục")
        self.category_tree.heading("loai", text="Loại")
        self.category_tree.heading("mota", text="Mô tả")
        
        self.category_tree.column("id", width=50)
        self.category_tree.column("ten", width=150)
        self.category_tree.column("loai", width=100)
        self.category_tree.column("mota", width=200)
        
        # Thêm thanh cuộn
        scrollbar = ttk.Scrollbar(list_frame, orient=tk.VERTICAL, command=self.category_tree.yview)
        self.category_tree.configure(yscrollcommand=scrollbar.set)
        
        # Đặt vị trí
        self.category_tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        # Frame thêm/sửa danh mục
        edit_frame = ctk.CTkFrame(window)
        edit_frame.pack(fill=tk.X, padx=10, pady=5)
        
        ctk.CTkLabel(edit_frame, text="Tên danh mục:").pack(side=tk.LEFT, padx=5)
        name_entry = ctk.CTkEntry(edit_frame)
        name_entry.pack(side=tk.LEFT, padx=5)
        
        ctk.CTkLabel(edit_frame, text="Loại:").pack(side=tk.LEFT, padx=5)
        type_var = ctk.StringVar(value="Chi")
        type_optionmenu = ctk.CTkOptionMenu(edit_frame, variable=type_var,
                                          values=["Chi", "Thu"])
        type_optionmenu.pack(side=tk.LEFT, padx=5)
        
        ctk.CTkLabel(edit_frame, text="Mô tả:").pack(side=tk.LEFT, padx=5)
        desc_entry = ctk.CTkEntry(edit_frame)
        desc_entry.pack(side=tk.LEFT, padx=5)
        
        # Nút thêm, sửa, xóa
        button_frame = ctk.CTkFrame(window)
        button_frame.pack(pady=10)
        
        def add_category():
            try:
                name = name_entry.get()
                category_type = type_var.get()
                description = desc_entry.get()
                
                if not name:
                    messagebox.showerror("Lỗi", "Vui lòng nhập tên danh mục!")
                    return
                
                # Thêm danh mục mới
                categories = self.app.xu_ly_du_lieu.doc_danh_muc()
                new_category = {
                    'id': len(categories) + 1,
                    'ten': name,
                    'loai': category_type,
                    'mota': description
                }
                categories.append(new_category)
                self.app.xu_ly_du_lieu.luu_danh_muc(categories)
                
                # Cập nhật bảng
                refresh_categories()
                
                # Xóa nội dung nhập
                name_entry.delete(0, tk.END)
                desc_entry.delete(0, tk.END)
                
                messagebox.showinfo("Thành công", "Đã thêm danh mục mới!")
            except Exception as e:
                messagebox.showerror("Lỗi", f"Không thể thêm danh mục: {str(e)}")
        
        def edit_category():
            try:
                selected = self.category_tree.selection()
                if not selected:
                    messagebox.showerror("Lỗi", "Vui lòng chọn danh mục cần sửa!")
                    return
                
                # Lấy thông tin danh mục được chọn
                item = self.category_tree.item(selected[0])
                category_id = int(item['values'][0])
                
                # Cập nhật danh mục
                categories = self.app.xu_ly_du_lieu.doc_danh_muc()
                for category in categories:
                    if category['id'] == category_id:
                        category['ten'] = name_entry.get()
                        category['loai'] = type_var.get()
                        category['mota'] = desc_entry.get()
                        break
                
                self.app.xu_ly_du_lieu.luu_danh_muc(categories)
                
                # Cập nhật bảng
                refresh_categories()
                
                messagebox.showinfo("Thành công", "Đã cập nhật danh mục!")
            except Exception as e:
                messagebox.showerror("Lỗi", f"Không thể cập nhật danh mục: {str(e)}")
        
        def delete_category():
            try:
                selected = self.category_tree.selection()
                if not selected:
                    messagebox.showerror("Lỗi", "Vui lòng chọn danh mục cần xóa!")
                    return
                
                if not messagebox.askyesno("Xác nhận", "Bạn có chắc muốn xóa danh mục này?"):
                    return
                
                # Xóa danh mục
                item = self.category_tree.item(selected[0])
                category_id = int(item['values'][0])
                
                categories = self.app.xu_ly_du_lieu.doc_danh_muc()
                categories = [c for c in categories if c['id'] != category_id]
                self.app.xu_ly_du_lieu.luu_danh_muc(categories)
                
                # Cập nhật bảng
                refresh_categories()
                
                messagebox.showinfo("Thành công", "Đã xóa danh mục!")
            except Exception as e:
                messagebox.showerror("Lỗi", f"Không thể xóa danh mục: {str(e)}")
        
        def refresh_categories():
            # Xóa dữ liệu cũ
            for item in self.category_tree.get_children():
                self.category_tree.delete(item)
            
            # Thêm dữ liệu mới
            categories = self.app.xu_ly_du_lieu.doc_danh_muc()
            for category in categories:
                self.category_tree.insert("", tk.END, values=(
                    category['id'],
                    category['ten'],
                    category['loai'],
                    category['mota']
                ))
        
        ctk.CTkButton(button_frame, text="Thêm", command=add_category).pack(side=tk.LEFT, padx=5)
        ctk.CTkButton(button_frame, text="Sửa", command=edit_category).pack(side=tk.LEFT, padx=5)
        ctk.CTkButton(button_frame, text="Xóa", command=delete_category).pack(side=tk.LEFT, padx=5)
        ctk.CTkButton(button_frame, text="Làm mới", command=refresh_categories).pack(side=tk.LEFT, padx=5)
        
        # Tải dữ liệu lần đầu
        refresh_categories() 

    def sua_nhacnho(self):
        """Sửa nhắc nhở đã chọn"""
        selected = self.reminder_tree.selection()
        if not selected:
            messagebox.showwarning("Cảnh báo", "Vui lòng chọn nhắc nhở cần sửa")
            return
            
        # Lấy thông tin nhắc nhở
        item = self.reminder_tree.item(selected[0])
        reminder_id = int(item['values'][0])
        
        # Tìm nhắc nhở trong danh sách
        reminder = None
        for r in self.app.reminders:
            if r.get('id') == reminder_id:
                reminder = r
                break
                
        if not reminder:
            messagebox.showerror("Lỗi", "Không tìm thấy nhắc nhở")
            return
            
        # Tạo cửa sổ sửa
        window = ctk.CTkToplevel(self.app.root)
        window.title("Sửa nhắc nhở")
        window.geometry("400x300")
        window.transient(self.app.root)
        window.grab_set()
        window.focus_force()
        
        # Tạo các trường nhập liệu
        ctk.CTkLabel(window, text="Tiêu đề:").pack(pady=5)
        title_entry = ctk.CTkEntry(window)
        title_entry.insert(0, reminder.get('title', ''))
        title_entry.pack(pady=5)
        
        ctk.CTkLabel(window, text="Nội dung:").pack(pady=5)
        content_entry = ctk.CTkEntry(window)
        content_entry.insert(0, reminder.get('content', ''))
        content_entry.pack(pady=5)
        
        ctk.CTkLabel(window, text="Ngày:").pack(pady=5)
        date_entry = ctk.CTkEntry(window)
        date_entry.insert(0, reminder.get('date', datetime.now().strftime("%Y-%m-%d")))
        date_entry.pack(pady=5)
        
        ctk.CTkLabel(window, text="Giờ:").pack(pady=5)
        time_entry = ctk.CTkEntry(window)
        time_entry.insert(0, reminder.get('time', datetime.now().strftime("%H:%M")))
        time_entry.pack(pady=5)
        
        def save_changes():
            try:
                # Cập nhật thông tin
                reminder['title'] = title_entry.get()
                reminder['content'] = content_entry.get()
                reminder['date'] = date_entry.get()
                reminder['time'] = time_entry.get()
                reminder['notified'] = False  # Reset trạng thái thông báo
                
                # Lưu vào database
                self.app.xu_ly_du_lieu.save_database()
                
                messagebox.showinfo("Thành công", "Đã cập nhật nhắc nhở")
                window.destroy()
                
                # Cập nhật lại danh sách
                self.xem_nhacnho()
                
            except Exception as e:
                messagebox.showerror("Lỗi", f"Không thể cập nhật nhắc nhở: {str(e)}")
        
        ctk.CTkButton(window, text="Lưu", command=save_changes).pack(pady=20) 

    def xoa_nhacnho(self):
        """Xóa nhắc nhở đã chọn"""
        selected = self.reminder_tree.selection()
        if not selected:
            messagebox.showwarning("Cảnh báo", "Vui lòng chọn nhắc nhở cần xóa")
            return
            
        # Xác nhận xóa
        if not messagebox.askyesno("Xác nhận", "Bạn có chắc muốn xóa nhắc nhở này?"):
            return
            
        try:
            # Lấy thông tin nhắc nhở
            item = self.reminder_tree.item(selected[0])
            reminder_id = int(item['values'][0])
            
            # Tìm và xóa nhắc nhở
            for i, reminder in enumerate(self.app.reminders):
                if reminder.get('id') == reminder_id:
                    self.app.reminders.pop(i)
                    break
            
            # Lưu vào database
            self.app.xu_ly_du_lieu.save_database()
            
            messagebox.showinfo("Thành công", "Đã xóa nhắc nhở")
            
            # Cập nhật lại danh sách
            self.xem_nhacnho()
            
        except Exception as e:
            messagebox.showerror("Lỗi", f"Không thể xóa nhắc nhở: {str(e)}") 