import customtkinter as ctk
from tkinter import messagebox
import numpy as np
from datetime import datetime, timedelta
import pandas as pd

class TinhToan:
    def __init__(self, app):
        self.app = app

    def tinh_toan_don_gian(self):
        # Tạo cửa sổ tính toán đơn giản
        window = ctk.CTkToplevel(self.app.root)
        window.title("Tính toán đơn giản")
        window.geometry("600x700")
        window.transient(self.app.root)
        window.grab_set()
        window.focus_force()

        # Configure grid for the window
        window.grid_columnconfigure(0, weight=1)
        window.grid_rowconfigure(0, weight=1)

        # Frame chứa các trường nhập liệu
        input_frame = ctk.CTkFrame(window)
        input_frame.grid(row=0, column=0, pady=10, padx=10, sticky="nsew")
        input_frame.grid_columnconfigure(1, weight=1) # Make the input column expandable

        row_idx = 0

        # Tạo các trường nhập liệu
        ctk.CTkLabel(input_frame, text="Số thứ nhất:").grid(row=row_idx, column=0, pady=5, padx=10, sticky="w")
        num1_entry = ctk.CTkEntry(input_frame)
        num1_entry.grid(row=row_idx, column=1, pady=5, padx=10, sticky="ew")
        row_idx += 1
        
        ctk.CTkLabel(input_frame, text="Số thứ hai:").grid(row=row_idx, column=0, pady=5, padx=10, sticky="w")
        num2_entry = ctk.CTkEntry(input_frame)
        num2_entry.grid(row=row_idx, column=1, pady=5, padx=10, sticky="ew")
        row_idx += 1
        
        # Tạo nút tính toán
        def calculate():
            try:
                num1 = float(num1_entry.get())
                num2 = float(num2_entry.get())
                result = num1 + num2
                messagebox.showinfo("Kết quả", f"Tổng: {result}")
            except ValueError:
                messagebox.showerror("Lỗi", "Vui lòng nhập số hợp lệ")
        
        ctk.CTkButton(window, text="Tính tổng", command=calculate).grid(row=1, column=0, pady=20)

    def chuyen_doi_tien_te(self):
        # Tạo cửa sổ chuyển đổi tiền tệ
        window = ctk.CTkToplevel(self.app.root)
        window.title("Chuyển đổi tiền tệ")
        window.geometry("600x700")
        window.transient(self.app.root)
        window.grab_set()
        window.focus_force()
        
        # Tỷ giá (có thể lấy từ API)
        rates = {
            "USD": 24500,
            "EUR": 26500,
            "GBP": 31000,
            "JPY": 165
        }
        
        # Configure grid for the window
        window.grid_columnconfigure(0, weight=1)
        window.grid_rowconfigure(0, weight=1)

        # Frame chứa các trường nhập liệu
        input_frame = ctk.CTkFrame(window)
        input_frame.grid(row=0, column=0, pady=10, padx=10, sticky="nsew")
        input_frame.grid_columnconfigure(1, weight=1) # Make the input column expandable

        row_idx = 0
        
        # Tạo các trường nhập liệu
        ctk.CTkLabel(input_frame, text="Số tiền:").grid(row=row_idx, column=0, pady=5, padx=10, sticky="w")
        amount_entry = ctk.CTkEntry(input_frame)
        amount_entry.grid(row=row_idx, column=1, pady=5, padx=10, sticky="ew")
        row_idx += 1
        
        ctk.CTkLabel(input_frame, text="Từ:").grid(row=row_idx, column=0, pady=5, padx=10, sticky="w")
        from_currency = ctk.CTkComboBox(input_frame, values=["VND"] + list(rates.keys()))
        from_currency.grid(row=row_idx, column=1, pady=5, padx=10, sticky="ew")
        row_idx += 1
        
        ctk.CTkLabel(input_frame, text="Sang:").grid(row=row_idx, column=0, pady=5, padx=10, sticky="w")
        to_currency = ctk.CTkComboBox(input_frame, values=["VND"] + list(rates.keys()))
        to_currency.grid(row=row_idx, column=1, pady=5, padx=10, sticky="ew")
        row_idx += 1
        
        # Tạo nút chuyển đổi
        def convert():
            try:
                amount = float(amount_entry.get())
                from_curr = from_currency.get()
                to_curr = to_currency.get()
                
                # Chuyển đổi sang VND
                if from_curr != "VND":
                    amount = amount * rates[from_curr]
                
                # Chuyển đổi từ VND sang đơn vị đích
                if to_curr != "VND":
                    amount = amount / rates[to_curr]
                
                messagebox.showinfo("Kết quả", f"{amount:.2f} {to_curr}")
            except ValueError:
                messagebox.showerror("Lỗi", "Vui lòng nhập số hợp lệ")
        
        ctk.CTkButton(window, text="Chuyển đổi", command=convert).grid(row=1, column=0, pady=20)

    def de_xuat_toiuu(self):
        # Tạo cửa sổ đề xuất tối ưu
        window = ctk.CTkToplevel(self.app.root)
        window.title("Đề xuất tối ưu chi tiêu")
        window.geometry("600x700")
        window.transient(self.app.root)
        window.grab_set()
        window.focus_force()
        
        # Tạo DataFrame từ dữ liệu giao dịch
        df = pd.DataFrame(self.app.transactions)
        if df.empty:
            messagebox.showinfo("Thông báo", "Không có dữ liệu để phân tích")
            window.destroy()
            return
        
        # Phân tích chi tiêu
        expenses = df[df['type'] == 'expense']
        total_expense = expenses['amount'].sum()
        avg_expense = expenses['amount'].mean()
        
        # Phân tích theo danh mục
        category_expenses = expenses.groupby('category')['amount'].sum()
        category_percentages = category_expenses / total_expense * 100
        
        # Tạo frame kết quả
        result_frame = ctk.CTkFrame(window)
        result_frame.grid(row=0, column=0, pady=10, padx=10, sticky="nsew")
        result_frame.grid_columnconfigure(0, weight=1) # Center content in result_frame

        # Hiển thị kết quả phân tích
        ctk.CTkLabel(result_frame, text="Phân tích chi tiêu:", font=("Arial", 14, "bold")).pack(pady=5)
        ctk.CTkLabel(result_frame, text=f"Tổng chi tiêu: {total_expense:,.0f} VNĐ").pack(pady=2)
        ctk.CTkLabel(result_frame, text=f"Chi tiêu trung bình: {avg_expense:,.0f} VNĐ").pack(pady=2)
        
        ctk.CTkLabel(result_frame, text="\nPhân bố theo danh mục:", font=("Arial", 14, "bold")).pack(pady=5)
        for category, percentage in category_percentages.items():
            ctk.CTkLabel(result_frame, 
                text=f"{category}: {percentage:.1f}%").pack(pady=2)
        
        # Đề xuất tối ưu
        ctk.CTkLabel(result_frame, text="\nĐề xuất tối ưu:", font=("Arial", 14, "bold")).pack(pady=5)
        
        # Kiểm tra các danh mục chi tiêu cao
        high_expense_categories = category_percentages[category_percentages > 30]
        if not high_expense_categories.empty:
            ctk.CTkLabel(result_frame, 
                text="Các danh mục chi tiêu cao cần kiểm soát:").pack(pady=2)
            for category in high_expense_categories.index:
                ctk.CTkLabel(result_frame, text=f"- {category}").pack(pady=2)
        
        # Kiểm tra chi tiêu so với thu nhập
        monthly_income = self.app.get_monthly_income()
        if monthly_income > 0:
            expense_ratio = total_expense / monthly_income * 100
            if expense_ratio > 80:
                ctk.CTkLabel(result_frame, 
                    text="\nCảnh báo: Chi tiêu đang vượt quá 80% thu nhập!").pack(pady=2)
            elif expense_ratio > 60:
                ctk.CTkLabel(result_frame, 
                    text="\nLưu ý: Chi tiêu đang ở mức cao (>60% thu nhập)").pack(pady=2)
        
        # Đề xuất tiết kiệm
        if monthly_income > 0:
            suggested_saving = monthly_income * 0.2  # Đề xuất tiết kiệm 20% thu nhập
            ctk.CTkLabel(result_frame, 
                text=f"\nĐề xuất tiết kiệm mỗi tháng: {suggested_saving:,.0f} VNĐ").pack(pady=2)

    def tinh_tyle_danhmuc(self):
        """Tính toán tỷ lệ chi tiêu theo danh mục"""
        try:
            # Lấy dữ liệu giao dịch
            giao_dich = self.app.xu_ly_du_lieu.doc_du_lieu()
            danh_muc = self.app.xu_ly_du_lieu.doc_danh_muc()
            
            # Lọc giao dịch chi tiêu
            chi_tieu = [g for g in giao_dich if g['loai'] == 'chi']
            
            # Tính tổng chi tiêu
            tong_chi = sum(g['so_tien'] for g in chi_tieu)
            
            # Tính tỷ lệ theo danh mục
            ty_le = {}
            for dm in danh_muc:
                if dm['loai'] == 'Chi':
                    chi_dm = sum(g['so_tien'] for g in chi_tieu if g['danh_muc'] == dm['ten'])
                    ty_le[dm['ten']] = (chi_dm / tong_chi * 100) if tong_chi > 0 else 0
            
            return ty_le
        except Exception as e:
            print(f"Lỗi khi tính tỷ lệ danh mục: {str(e)}")
            return {}

    def du_bao_theo_mua(self):
        """Dự báo chi tiêu theo mùa"""
        try:
            # Lấy dữ liệu giao dịch
            giao_dich = self.app.xu_ly_du_lieu.doc_du_lieu()
            
            # Lọc giao dịch chi tiêu
            chi_tieu = [g for g in giao_dich if g['loai'] == 'chi']
            
            # Chuyển đổi dữ liệu thành DataFrame
            df = pd.DataFrame(chi_tieu)
            df['ngay'] = pd.to_datetime(df['ngay'])
            
            # Nhóm dữ liệu theo tháng
            df_thang = df.groupby(df['ngay'].dt.to_period('M'))['so_tien'].sum()
            
            # Tính trung bình theo mùa
            mua_xuan = df_thang[df_thang.index.month.isin([1, 2, 3])].mean()
            mua_ha = df_thang[df_thang.index.month.isin([4, 5, 6])].mean()
            mua_thu = df_thang[df_thang.index.month.isin([7, 8, 9])].mean()
            mua_dong = df_thang[df_thang.index.month.isin([10, 11, 12])].mean()
            
            # Dự báo cho năm tiếp theo
            nam_hien_tai = datetime.now().year
            du_bao = {
                f'Mùa xuân {nam_hien_tai + 1}': mua_xuan,
                f'Mùa hạ {nam_hien_tai + 1}': mua_ha,
                f'Mùa thu {nam_hien_tai + 1}': mua_thu,
                f'Mùa đông {nam_hien_tai + 1}': mua_dong
            }
            
            return du_bao
        except Exception as e:
            print(f"Lỗi khi dự báo theo mùa: {str(e)}")
            return {}

    def phan_tich_xuhuong_theo_mua(self):
        """Phân tích xu hướng chi tiêu theo mùa"""
        try:
            # Lấy dữ liệu giao dịch
            giao_dich = self.app.xu_ly_du_lieu.doc_du_lieu()
            
            # Lọc giao dịch chi tiêu
            chi_tieu = [g for g in giao_dich if g['loai'] == 'chi']
            
            # Chuyển đổi dữ liệu thành DataFrame
            df = pd.DataFrame(chi_tieu)
            df['ngay'] = pd.to_datetime(df['ngay'])
            
            # Nhóm dữ liệu theo tháng và danh mục
            df_thang_dm = df.groupby([df['ngay'].dt.to_period('M'), 'danh_muc'])['so_tien'].sum().unstack()
            
            # Tính hệ số tương quan theo mùa
            he_so = {}
            for dm in df_thang_dm.columns:
                # Tính trung bình theo mùa
                mua_xuan = df_thang_dm[dm][df_thang_dm.index.month.isin([1, 2, 3])].mean()
                mua_ha = df_thang_dm[dm][df_thang_dm.index.month.isin([4, 5, 6])].mean()
                mua_thu = df_thang_dm[dm][df_thang_dm.index.month.isin([7, 8, 9])].mean()
                mua_dong = df_thang_dm[dm][df_thang_dm.index.month.isin([10, 11, 12])].mean()
                
                # Tính hệ số biến động
                trung_binh = (mua_xuan + mua_ha + mua_thu + mua_dong) / 4
                he_so[dm] = {
                    'Mùa xuân': mua_xuan / trung_binh if trung_binh > 0 else 1,
                    'Mùa hạ': mua_ha / trung_binh if trung_binh > 0 else 1,
                    'Mùa thu': mua_thu / trung_binh if trung_binh > 0 else 1,
                    'Mùa đông': mua_dong / trung_binh if trung_binh > 0 else 1
                }
            
            return he_so
        except Exception as e:
            print(f"Lỗi khi phân tích xu hướng theo mùa: {str(e)}")
            return {} 