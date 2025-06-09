import matplotlib.pyplot as plt
import seaborn as sns
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import pandas as pd
from datetime import datetime
import customtkinter as ctk
from matplotlib.backends.backend_tkagg import NavigationToolbar2Tk
import numpy as np
import os
from tkinter import messagebox, filedialog
from sklearn.linear_model import LinearRegression
from matplotlib.figure import Figure
import tkinter as tk

class BieuDo:
    def __init__(self, app):
        self.app = app

    def tao_bieudo_tron(self, parent=None):
        # Tạo DataFrame
        df = pd.DataFrame(self.app.transactions)
        if df.empty:
            if parent:
                messagebox.showinfo("Thông báo", "Không có dữ liệu để vẽ biểu đồ")
            return
        
        # Tính toán dữ liệu
        expense_by_category = df[df['type'] == 'expense'].groupby('category')['amount'].sum()
        
        # Tạo biểu đồ
        fig, ax = plt.subplots(figsize=(5, 4))
        expense_by_category.plot(kind='pie', autopct='%1.1f%%', ax=ax)
        ax.set_title('Phân bố chi tiêu theo danh mục')
        ax.set_ylabel('') # Đặt rỗng sau khi vẽ để đảm bảo ẩn
        
        if parent:
            # Hiển thị biểu đồ trong frame được chỉ định
            canvas = FigureCanvasTkAgg(fig, parent)
            canvas.draw()
            canvas.get_tk_widget().pack(fill="both", expand=True)
        else:
            # Tạo cửa sổ mới nếu không có parent
            window = ctk.CTkToplevel(self.app.root)
            window.title("Biểu đồ phân bố chi tiêu")
            window.geometry("1200x800")
            window.transient(self.app.root)
            window.grab_set()
            window.focus_force()
            
            # Configure grid for the window
            window.grid_columnconfigure(0, weight=1)
            window.grid_rowconfigure(0, weight=1)
            window.grid_rowconfigure(1, weight=0) # For the toolbar frame

            canvas = FigureCanvasTkAgg(fig, window)
            canvas.draw()
            canvas.get_tk_widget().grid(row=0, column=0, sticky="nsew")
            
            # Thêm thanh công cụ trong một frame riêng
            toolbar_frame = ctk.CTkFrame(window) # Tạo một frame mới cho toolbar
            toolbar_frame.grid(row=1, column=0, sticky="ew") # Đặt frame này bằng grid
            toolbar_frame.grid_columnconfigure(0, weight=1) # Đảm bảo frame có thể mở rộng

            toolbar = NavigationToolbar2Tk(canvas, toolbar_frame)
            toolbar.update()
            toolbar.pack(side=tk.BOTTOM, fill=tk.X, expand=True) # Sử dụng pack bên trong toolbar_frame

    def tao_bieudo_xuhuong(self, parent=None):
        # Tạo cửa sổ biểu đồ xu hướng
        if parent:
            window = parent
        else:
            window = ctk.CTkToplevel(self.app.root)
            window.title("Biểu đồ xu hướng chi tiêu")
            window.geometry("1200x800")
            window.transient(self.app.root)
            window.grab_set()
            window.focus_force()
        
        # Configure grid for the window
        window.grid_columnconfigure(0, weight=1)
        window.grid_rowconfigure(0, weight=1)
        window.grid_rowconfigure(1, weight=0) # For the toolbar frame
        
        # Tạo DataFrame
        df = pd.DataFrame(self.app.transactions)
        if df.empty:
            messagebox.showinfo("Thông báo", "Không có dữ liệu để vẽ biểu đồ")
            if not parent:
                window.destroy()
            return
        
        # Chuyển đổi ngày
        df['date'] = pd.to_datetime(df['date'], format='%d/%m/%Y')
        df = df.sort_values('date')
        
        # Tính toán dữ liệu
        daily_expenses = df[df['type'] == 'expense'].groupby('date')['amount'].sum()
        
        # Tạo biểu đồ
        fig, ax = plt.subplots(figsize=(8, 6))
        daily_expenses.plot(kind='line', ax=ax)
        ax.set_title('Xu hướng chi tiêu theo thời gian')
        ax.set_xlabel('Ngày')
        ax.set_ylabel('Số tiền (VNĐ)')
        plt.xticks(rotation=0)
        
        # Hiển thị biểu đồ
        canvas = FigureCanvasTkAgg(fig, window)
        canvas.draw()
        canvas.get_tk_widget().grid(row=0, column=0, sticky="nsew")
        
        # Thêm thanh công cụ trong một frame riêng
        toolbar_frame = ctk.CTkFrame(window) # Tạo một frame mới cho toolbar
        toolbar_frame.grid(row=1, column=0, sticky="ew") # Đặt frame này bằng grid
        toolbar_frame.grid_columnconfigure(0, weight=1) # Đảm bảo frame có thể mở rộng

        toolbar = NavigationToolbar2Tk(canvas, toolbar_frame)
        toolbar.update()
        toolbar.pack(side=tk.BOTTOM, fill=tk.X, expand=True) # Sử dụng pack bên trong toolbar_frame

    def create_and_display_charts(self, pie_parent_frame, trend_parent_frame):
        # Tạo biểu đồ tròn
        self.pie_fig, self.pie_ax = plt.subplots(figsize=(1, 1), dpi=100) # Initial size, will expand
        self.pie_canvas = FigureCanvasTkAgg(self.pie_fig, master=pie_parent_frame)
        self.pie_canvas.get_tk_widget().pack(fill="both", expand=True)
        
        # Tạo biểu đồ xu hướng
        self.trend_fig, self.trend_ax = plt.subplots(figsize=(1, 1), dpi=100) # Initial size, will expand
        self.trend_canvas = FigureCanvasTkAgg(self.trend_fig, master=trend_parent_frame)
        self.trend_canvas.get_tk_widget().pack(fill="both", expand=True)

    def update_pie_chart(self):
        # Cập nhật biểu đồ tròn
        df = pd.DataFrame(self.app.transactions)
        if df.empty:
            self.pie_ax.clear()
            self.pie_ax.set_title('Phân bố chi tiêu theo danh mục (Không có dữ liệu)')
            self.pie_fig.canvas.draw()
            return
            
        expense_by_category = df[df['type'] == 'expense'].groupby('category')['amount'].sum()
        
        self.pie_ax.clear()
        if not expense_by_category.empty:
             expense_by_category.plot(kind='pie', autopct='%1.1f%%', ax=self.pie_ax, ylabel='') # Đặt rỗng sau khi vẽ để đảm bảo ẩn
        self.pie_ax.set_title('Phân bố chi tiêu theo danh mục')
        self.pie_ax.set_ylabel('') # Remove default y-label 'amount'
        self.pie_fig.canvas.draw()

    def update_trend_chart(self):
        # Cập nhật biểu đồ xu hướng
        df = pd.DataFrame(self.app.transactions)
        if df.empty:
            self.trend_ax.clear()
            self.trend_ax.set_title('Xu hướng chi tiêu theo thời gian (Không có dữ liệu)')
            self.trend_ax.set_xlabel('Ngày')
            self.trend_ax.set_ylabel('Số tiền (VNĐ)')
            self.trend_fig.canvas.draw()
            return

        try:
            df['date'] = pd.to_datetime(df['date'], format='%d/%m/%Y')
            df = df.sort_values('date')
            
            daily_expenses = df[df['type'] == 'expense'].groupby('date')['amount'].sum()
            
            self.trend_ax.clear()
            if not daily_expenses.empty:
                daily_expenses.plot(kind='line', ax=self.trend_ax)
            self.trend_ax.set_title('Xu hướng chi tiêu theo thời gian')
            self.trend_ax.set_xlabel('Ngày')
            self.trend_ax.set_ylabel('Số tiền (VNĐ)')
            plt.xticks(rotation=0)
            self.trend_fig.canvas.draw()
        except Exception as e:
            print(f"Error updating trend chart: {e}")
            self.trend_ax.clear()
            self.trend_ax.set_title('Xu hướng chi tiêu theo thời gian (Lỗi dữ liệu)')
            self.trend_ax.set_xlabel('Ngày')
            self.trend_ax.set_ylabel('Số tiền (VNĐ)')
            self.trend_fig.canvas.draw()

    def save_charts_as_image(self):
        # Lưu cả hai biểu đồ thành ảnh
        try:
            # Tạo thư mục charts nếu chưa tồn tại
            if not os.path.exists("charts"):
                os.makedirs("charts")
            
            # Mở hộp thoại lưu file
            filename = filedialog.asksaveasfilename(
                defaultextension=".png",
                filetypes=[("PNG files", "*.png"), ("All files", "*.*")],
                title="Lưu ảnh biểu đồ"
            )
            
            if filename:
                # Tạo một figure mới chứa cả hai biểu đồ
                combined_fig = Figure(figsize=(12, 8))
                ax1 = combined_fig.add_subplot(1, 2, 1) # 1 hàng, 2 cột, ô 1
                ax2 = combined_fig.add_subplot(1, 2, 2) # 1 hàng, 2 cột, ô 2

                # Copy nội dung biểu đồ tròn sang combined_fig
                if hasattr(self, 'pie_fig') and self.pie_fig is not None:
                     # sao chép axes
                    for artist in self.pie_ax.get_children():
                        ax1.add_artist(artist)
                    ax1.set_title(self.pie_ax.get_title())
                    ax1.set_xlabel(self.pie_ax.get_xlabel())
                    ax1.set_ylabel(self.pie_ax.get_ylabel())
                    ax1.autoscale() # Điều chỉnh tỷ lệ trục
                    # sao chép legend
                    if self.pie_ax.get_legend():
                         ax1.legend(*self.pie_ax.get_legend_handles_labels())

                # Copy nội dung biểu đồ xu hướng sang combined_fig
                if hasattr(self, 'trend_fig') and self.trend_fig is not None:
                    # sao chép axes
                    for artist in self.trend_ax.get_children():
                        ax2.add_artist(artist)
                    ax2.set_title(self.trend_ax.get_title())
                    ax2.set_xlabel(self.trend_ax.get_xlabel())
                    ax2.set_ylabel(self.trend_ax.get_ylabel())
                    ax2.autoscale() # Điều chỉnh tỷ lệ trục
                    # sao chép legend
                    if self.trend_ax.get_legend():
                         ax2.legend(*self.trend_ax.get_legend_handles_labels())

                # Điều chỉnh layout để tránh chồng chéo
                combined_fig.tight_layout()

                # Lưu ảnh
                combined_fig.savefig(filename, dpi=300)

                # Đóng figure kết hợp để giải phóng bộ nhớ
                plt.close(combined_fig)

                messagebox.showinfo("Thành công", f"Đã lưu ảnh biểu đồ vào {filename}")
            
        except Exception as e:
            messagebox.showerror("Lỗi", f"Không thể lưu ảnh biểu đồ: {str(e)}") 

    def tao_bieudo_so_sanh(self):
        # Tạo cửa sổ biểu đồ so sánh
        window = ctk.CTkToplevel(self.app.root)
        window.title("Biểu đồ so sánh thu chi")
        window.geometry("1200x800")
        window.transient(self.app.root)
        window.grab_set()
        window.focus_force()
        # Tạo DataFrame
        df = pd.DataFrame(self.app.transactions)
        if df.empty:
            messagebox.showinfo("Thông báo", "Không có dữ liệu để vẽ biểu đồ")
            window.destroy()
            return
        
        # Tính toán dữ liệu
        monthly_data = df.groupby(['date', 'type'])['amount'].sum().unstack()
        
        # Tạo biểu đồ
        fig, ax = plt.subplots(figsize=(10, 6))
        monthly_data.plot(kind='bar', ax=ax)
        ax.set_title('So sánh thu chi theo thời gian')
        ax.set_xlabel('Thời gian')
        ax.set_ylabel('Số tiền (VNĐ)')
        plt.xticks(rotation=45)
        
        # Hiển thị biểu đồ
        canvas = FigureCanvasTkAgg(fig, window)
        canvas.draw()
        canvas.get_tk_widget().pack(fill="both", expand=True)
        
        # Thêm thanh công cụ
        toolbar = NavigationToolbar2Tk(canvas, window)
        toolbar.update()

    def tao_bieudo_phan_tich(self):
        # Tạo cửa sổ biểu đồ phân tích
        window = ctk.CTkToplevel(self.app.root)
        window.title("Biểu đồ phân tích chi tiêu")
        window.geometry("1200x800")
        window.transient(self.app.root)
        window.grab_set()
        window.focus_force()
        
        # Tạo DataFrame
        df = pd.DataFrame(self.app.transactions)
        if df.empty:
            messagebox.showinfo("Thông báo", "Không có dữ liệu để vẽ biểu đồ")
            window.destroy()
            return
        
        # Chuyển đổi ngày
        df['date'] = pd.to_datetime(df['date'], format='%d/%m/%Y')
        df['month'] = df['date'].dt.strftime('%Y-%m')
        
        # Tạo biểu đồ
        fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 5))
        
        # Biểu đồ cột chi tiêu theo tháng
        monthly_expenses = df[df['type'] == 'expense'].groupby('month')['amount'].sum()
        monthly_expenses.plot(kind='bar', ax=ax1)
        ax1.set_title('Chi tiêu theo tháng')
        ax1.set_xlabel('Tháng')
        ax1.set_ylabel('Số tiền (VNĐ)')
        plt.setp(ax1.xaxis.get_majorticklabels(), rotation=1)
        
        # Biểu đồ tròn phân bố chi tiêu
        expense_by_category = df[df['type'] == 'expense'].groupby('category')['amount'].sum()
        expense_by_category.plot(kind='pie', autopct='%1.1f%%', ax=ax2)
        ax2.set_title('Phân bố chi tiêu theo danh mục')
        ax2.set_ylabel('')

        # Hiển thị biểu đồ
        canvas = FigureCanvasTkAgg(fig, window)
        canvas.draw()
        canvas.get_tk_widget().pack(fill="both", expand=True)
        
        # Thêm thanh công cụ
        toolbar = NavigationToolbar2Tk(canvas, window)
        toolbar.update()

    def tao_bieudo_thoiquen(self):
        # Tạo cửa sổ biểu đồ thói quen
        window = ctk.CTkToplevel(self.app.root)
        window.title("Biểu đồ thói quen chi tiêu")
        window.geometry("1200x800")
        window.transient(self.app.root)
        window.grab_set()
        window.focus_force()
        # Tạo DataFrame
        df = pd.DataFrame(self.app.transactions)
        if df.empty:
            messagebox.showinfo("Thông báo", "Không có dữ liệu để vẽ biểu đồ")
            window.destroy()
            return
        
        # Chuyển đổi ngày
        df['date'] = pd.to_datetime(df['date'], format='%d/%m/%Y')
        df['day_of_week'] = df['date'].dt.day_name()
        df['hour'] = df['date'].dt.hour
        
        # Tạo biểu đồ
        fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 5))
        
        # Biểu đồ cột chi tiêu theo ngày trong tuần
        daily_expenses = df[df['type'] == 'expense'].groupby('day_of_week')['amount'].mean()
        daily_expenses.plot(kind='bar', ax=ax1)
        ax1.set_title('Chi tiêu trung bình theo ngày trong tuần')
        ax1.set_xlabel('Ngày')
        ax1.set_ylabel('Số tiền (VNĐ)')
        plt.setp(ax1.xaxis.get_majorticklabels(), rotation=45)
        
        # Biểu đồ đường chi tiêu theo giờ
        hourly_expenses = df[df['type'] == 'expense'].groupby('hour')['amount'].mean()
        hourly_expenses.plot(kind='line', ax=ax2)
        ax2.set_title('Chi tiêu trung bình theo giờ')
        ax2.set_xlabel('Giờ')
        ax2.set_ylabel('Số tiền (VNĐ)')
        
        # Hiển thị biểu đồ
        canvas = FigureCanvasTkAgg(fig, window)
        canvas.draw()
        canvas.get_tk_widget().pack(fill="both", expand=True)
        
        # Thêm thanh công cụ
        toolbar = NavigationToolbar2Tk(canvas, window)
        toolbar.update()

    def tao_bieudo_muctieu(self):
        # Tạo cửa sổ biểu đồ mục tiêu
        window = ctk.CTkToplevel(self.app.root)
        window.title("Biểu đồ tiến độ mục tiêu")
        window.geometry("1200x900")
        window.transient(self.app.root)
        window.grab_set()
        window.focus_force()
        if not self.app.goals:
            messagebox.showinfo("Thông báo", "Không có mục tiêu để vẽ biểu đồ")
            window.destroy()
            return
        
        # Tạo biểu đồ
        fig, ax = plt.subplots(figsize=(10, 6))
        
        # Tính toán dữ liệu
        goals = []
        progress = []
        for goal in self.app.goals:
            goals.append(goal['title'])
            progress.append((goal['saved'] / goal['amount']) * 100)
        
        # Vẽ biểu đồ
        ax.bar(goals, progress)
        ax.set_title('Tiến độ các mục tiêu')
        ax.set_xlabel(' ')
        ax.set_ylabel('Tiến độ (%)')
        plt.xticks(rotation=25)
        
        # Thêm đường 100%
        ax.axhline(y=100, color='r', linestyle='--')
        
        # Hiển thị biểu đồ
        canvas = FigureCanvasTkAgg(fig, window)
        canvas.draw()
        canvas.get_tk_widget().pack(fill="both", expand=True)
        
        # Thêm thanh công cụ
        toolbar = NavigationToolbar2Tk(canvas, window)
        toolbar.update()

    def tao_bieudo_du_bao(self):
        # Tạo cửa sổ biểu đồ dự báo
        window = ctk.CTkToplevel(self.app.root)
        window.title("Biểu đồ dự báo chi tiêu")
        window.geometry("1200x800")
        window.transient(self.app.root)
        window.grab_set()
        window.focus_force()
        # Tạo DataFrame
        df = pd.DataFrame(self.app.transactions)
        if df.empty:
            messagebox.showinfo("Thông báo", "Không có dữ liệu để vẽ biểu đồ")
            window.destroy()
            return
        
        # Chuyển đổi ngày
        df['date'] = pd.to_datetime(df['date'], format='%d/%m/%Y')
        df['month'] = df['date'].dt.strftime('%Y-%m')
        
        # Tính toán dữ liệu
        monthly_expenses = df[df['type'] == 'expense'].groupby('month')['amount'].sum()
        
        if len(monthly_expenses) < 2:
            messagebox.showinfo("Thông báo", "Không đủ dữ liệu để dự báo")
            window.destroy()
            return
        
        # Chuẩn bị dữ liệu cho mô hình
        X = np.arange(len(monthly_expenses)).reshape(-1, 1)
        y = monthly_expenses.values
        
        # Huấn luyện mô hình
        model = LinearRegression()
        model.fit(X, y)
        
        # Dự đoán 3 tháng tiếp theo
        future_months = []
        last_month = pd.to_datetime(monthly_expenses.index[-1], format='%Y-%m')
        
        for i in range(1, 4):
            next_month = last_month + pd.DateOffset(months=i)
            future_months.append(next_month.strftime('%Y-%m'))
        
        X_future = np.arange(len(monthly_expenses), len(monthly_expenses) + 3).reshape(-1, 1)
        y_future = model.predict(X_future)
        
        # Tạo biểu đồ
        fig, ax = plt.subplots(figsize=(10, 6))
        
        # Vẽ dữ liệu thực tế
        ax.plot(monthly_expenses.index, monthly_expenses.values, 'b-', label='Thực tế')
        
        # Vẽ dự báo
        ax.plot(future_months, y_future, 'r--', label='Dự báo')
        
        ax.set_title('Dự báo chi tiêu')
        ax.set_xlabel('Tháng')
        ax.set_ylabel('Số tiền (VNĐ)')
        plt.xticks(rotation=1)
        ax.legend()
        
        # Hiển thị biểu đồ
        canvas = FigureCanvasTkAgg(fig, window)
        canvas.draw()
        canvas.get_tk_widget().pack(fill="both", expand=True)
        
        # Thêm thanh công cụ
        toolbar = NavigationToolbar2Tk(canvas, window)
        toolbar.update() 