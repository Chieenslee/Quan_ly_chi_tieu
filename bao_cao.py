import pandas as pd
from datetime import datetime, timedelta
import matplotlib.pyplot as plt
import seaborn as sns
import os
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.lib import colors
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
import numpy as np
from sklearn.linear_model import LinearRegression
import customtkinter as ctk
import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import darkdetect
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

class BaoCao:
    def __init__(self, app):
        self.app = app
        self.normal_font = 'Helvetica'  # Fallback font
        self.bold_font = 'Helvetica-Bold' # Fallback font

        font_dir = os.path.join(os.getcwd(), 'fonts')
        noto_regular_path = os.path.join(font_dir, 'NotoSans-Regular.ttf')
        noto_bold_path = os.path.join(font_dir, 'NotoSans-Bold.ttf')

        found_noto_font = False
        if os.path.exists(noto_regular_path) and os.path.exists(noto_bold_path):
            try:
                pdfmetrics.registerFont(TTFont('NotoSans', noto_regular_path))
                pdfmetrics.registerFont(TTFont('NotoSans-Bold', noto_bold_path))
                pdfmetrics.registerFontFamily('NotoSans', normal='NotoSans', bold='NotoSans-Bold')
                self.normal_font = 'NotoSans'
                self.bold_font = 'NotoSans-Bold'
                found_noto_font = True
            except Exception as e:
                print(f"Lỗi khi đăng ký font Noto Sans: {e}")
        
        if not found_noto_font:
            pass

    def _remove_vietnamese_accents(self, text):
        # Hàm này sẽ loại bỏ dấu tiếng Việt
        accents_mapping = {
            'á': 'a', 'à': 'a', 'ả': 'a', 'ạ': 'a', 'ã': 'a', 'ă': 'a', 'ằ': 'a', 'ắ': 'a', 'ẳ': 'a', 'ặ': 'a', 'ẵ': 'a', 'â': 'a', 'ầ': 'a', 'ấ': 'a', 'ẩ': 'a', 'ậ': 'a', 'ẫ': 'a',
            'Á': 'A', 'À': 'A', 'Ả': 'A', 'Ạ': 'A', 'Ã': 'A', 'Ă': 'A', 'Ằ': 'A', 'Ắ': 'A', 'Ẳ': 'A', 'Ặ': 'A', 'Ẵ': 'A', 'Â': 'A', 'Ầ': 'A', 'Ấ': 'A', 'Ẩ': 'A', 'Ậ': 'A', 'Ẫ': 'A',
            'é': 'e', 'è': 'e', 'ẻ': 'e', 'ẹ': 'e', 'ẽ': 'e', 'ê': 'e', 'ề': 'e', 'ế': 'e', 'ể': 'e', 'ệ': 'e', 'ễ': 'e',
            'É': 'E', 'È': 'E', 'Ẻ': 'E', 'Ẹ': 'E', 'Ẽ': 'E', 'Ê': 'E', 'Ề': 'E', 'Ế': 'E', 'Ể': 'E', 'Ệ': 'E', 'Ễ': 'E',
            'í': 'i', 'ì': 'i', 'ỉ': 'i', 'ị': 'i', 'ĩ': 'i',
            'Í': 'I', 'Ì': 'I', 'Ỉ': 'I', 'Ị': 'I', 'Ĩ': 'I',
            'ó': 'o', 'ò': 'o', 'ỏ': 'o', 'ọ': 'o', 'õ': 'o', 'ô': 'o', 'ồ': 'o', 'ố': 'o', 'ổ': 'o', 'ộ': 'o', 'ỗ': 'o', 'ơ': 'o', 'ờ': 'o', 'ớ': 'o', 'ở': 'o', 'ợ': 'o', 'ỡ': 'o',
            'Ó': 'O', 'Ò': 'O', 'Ỏ': 'O', 'Ọ': 'O', 'Õ': 'O', 'Ô': 'O', 'Ồ': 'O', 'Ố': 'O', 'Ổ': 'O', 'Ộ': 'O', 'Ỗ': 'O', 'Ơ': 'O', 'Ờ': 'O', 'Ớ': 'O', 'Ở': 'O', 'Ợ': 'O', 'Ỡ': 'O',
            'ú': 'u', 'ù': 'u', 'ủ': 'u', 'ụ': 'u', 'ũ': 'u', 'ư': 'u', 'ừ': 'u', 'ứ': 'u', 'ử': 'u', 'ự': 'u', 'ữ': 'u',
            'Ú': 'U', 'Ù': 'U', 'Ủ': 'U', 'Ụ': 'U', 'Ũ': 'U', 'Ư': 'U', 'Ừ': 'U', 'Ứ': 'U', 'Ử': 'U', 'Ự': 'U', 'Ữ': 'U',
            'ý': 'y', 'ỳ': 'y', 'ỷ': 'y', 'ỵ': 'y', 'ỹ': 'y',
            'Ý': 'Y', 'Ỳ': 'Y', 'Ỷ': 'Y', 'Ỵ': 'Y', 'Ỹ': 'Y',
            'đ': 'd', 'Đ': 'D'
        }
        for accent_char, normal_char in accents_mapping.items():
            text = text.replace(accent_char, normal_char)
        return text

    def xem_baocao(self):
        # Tạo cửa sổ xuất báo cáo
        window = ctk.CTkToplevel(self.app.root)
        window.title("Xuất báo cáo")
        window.geometry("600x700")
        window.transient(self.app.root)
        window.grab_set()
        window.focus_force()

        # Configure grid for the window
        window.grid_columnconfigure(0, weight=1)
        for i in range(4): # For report_frame, date_frame, format_frame, and button
            window.grid_rowconfigure(i, weight=1) 
        
        # Frame chọn loại báo cáo
        report_frame = ctk.CTkFrame(window)
        report_frame.grid(row=0, column=0, padx=10, pady=5, sticky="nsew")
        report_frame.grid_columnconfigure(0, weight=1)

        ctk.CTkLabel(report_frame, text="Chọn loại báo cáo:", font=("Arial", 14, "bold")).grid(row=0, column=0, pady=5)
        
        report_type = ctk.StringVar(value="summary")
        report_type_frame = ctk.CTkFrame(report_frame)
        report_type_frame.grid(row=1, column=0, pady=5)
        ctk.CTkRadioButton(report_type_frame, text="Báo cáo tổng hợp", 
                          variable=report_type, value="summary").pack(anchor="w", padx=10)
        ctk.CTkRadioButton(report_type_frame, text="Báo cáo chi tiết", 
                          variable=report_type, value="detail").pack(anchor="w", padx=10)
        ctk.CTkRadioButton(report_type_frame, text="Báo cáo xu hướng", 
                          variable=report_type, value="trend").pack(anchor="w", padx=10)
        ctk.CTkRadioButton(report_type_frame, text="Báo cáo phân tích", 
                          variable=report_type, value="analysis").pack(anchor="w", padx=10)
        
        # Frame chọn khoảng thời gian
        date_frame = ctk.CTkFrame(window)
        date_frame.grid(row=1, column=0, padx=10, pady=5, sticky="nsew")
        date_frame.grid_columnconfigure(0, weight=1)
        
        ctk.CTkLabel(date_frame, text="Khoảng thời gian:", font=("Arial", 14, "bold")).grid(row=0, column=0, pady=5)
        
        date_range = ctk.StringVar(value="month")
        date_range_frame = ctk.CTkFrame(date_frame)
        date_range_frame.grid(row=1, column=0, pady=5)
        ctk.CTkRadioButton(date_range_frame, text="Tháng này", 
                          variable=date_range, value="month").pack(anchor="w", padx=10)
        ctk.CTkRadioButton(date_range_frame, text="Quý này", 
                          variable=date_range, value="quarter").pack(anchor="w", padx=10)
        ctk.CTkRadioButton(date_range_frame, text="Năm nay", 
                          variable=date_range, value="year").pack(anchor="w", padx=10)
        ctk.CTkRadioButton(date_range_frame, text="Tùy chọn", 
                          variable=date_range, value="custom").pack(anchor="w", padx=10)
        
        # Frame chọn định dạng
        format_frame = ctk.CTkFrame(window)
        format_frame.grid(row=2, column=0, padx=10, pady=5, sticky="nsew")
        format_frame.grid_columnconfigure(0, weight=1)
        
        ctk.CTkLabel(format_frame, text="Định dạng:", font=("Arial", 14, "bold")).grid(row=0, column=0, pady=5)
        
        report_format = ctk.StringVar(value="pdf")
        format_type_frame = ctk.CTkFrame(format_frame)
        format_type_frame.grid(row=1, column=0, pady=5)
        ctk.CTkRadioButton(format_type_frame, text="PDF", 
                          variable=report_format, value="pdf").pack(anchor="w", padx=10)
        ctk.CTkRadioButton(format_type_frame, text="Excel", 
                          variable=report_format, value="excel").pack(anchor="w", padx=10)
        ctk.CTkRadioButton(format_type_frame, text="CSV", 
                          variable=report_format, value="csv").pack(anchor="w", padx=10)
        
        # Frame cho nút
        button_frame = ctk.CTkFrame(window)
        button_frame.grid(row=3, column=0, padx=10, pady=5, sticky="ew")
        button_frame.grid_columnconfigure(0, weight=1)
        button_frame.grid_columnconfigure(1, weight=1)

        # Nút xem báo cáo
        ctk.CTkButton(button_frame, text="Xem báo cáo", 
                     command=lambda: self.view_report(
                         report_type.get(),
                         date_range.get(),
                         report_format.get()
                     )).grid(row=0, column=0, padx=5, pady=5)

        # Nút xuất báo cáo
        ctk.CTkButton(button_frame, text="Xuất báo cáo", 
                     command=lambda: self.generate_report(
                         report_type.get(),
                         date_range.get(),
                         report_format.get()
                     )).grid(row=0, column=1, padx=5, pady=5)

    def generate_report(self, report_type, date_range, format):
        date_from, date_to = self._get_date_range(date_range)

        title = ""
        data = None

        if report_type == "summary":
            title, data = self._get_summary_report_data(date_from, date_to)
        elif report_type == "detail":
            title, data = self._get_detail_report_data(date_from, date_to)
        elif report_type == "trend":
            title, data = self._get_trend_report_data(date_from, date_to)
        elif report_type == "analysis":
            title, data = self._get_analysis_report_data(date_from, date_to)

        if data is None:
            messagebox.showwarning("Cảnh báo", "Không có dữ liệu trong khoảng thời gian này!")
            return

        # Xuất báo cáo
        if format == "pdf":
            self.create_pdf_report(title, data)
        elif format == "excel":
            if isinstance(data, dict):
                self.create_excel_report(title, pd.DataFrame(data.items(), columns=['Chỉ số', 'Giá trị']))
            else:
                self.create_excel_report(title, data)
        else:  # csv
            if isinstance(data, dict):
                self.create_csv_report(title, pd.DataFrame(data.items(), columns=['Chỉ số', 'Giá trị']))
            else:
                self.create_csv_report(title, data)

    def _get_date_range(self, date_range):
        today = datetime.now()
        if date_range == "month":
            date_from = today.replace(day=1)
            date_to = today
        elif date_range == "quarter":
            quarter = (today.month - 1) // 3
            date_from = today.replace(month=quarter * 3 + 1, day=1)
            date_to = today
        elif date_range == "year":
            date_from = today.replace(month=1, day=1)
            date_to = today
        else:  # custom
            # TODO: Thêm dialog chọn ngày
            date_from = today - timedelta(days=365) # Mặc định 1 năm trước
            date_to = today
        return date_from, date_to

    def _get_summary_report_data(self, date_from, date_to):
        df = self.app.xu_ly_du_lieu.get_transactions_dataframe(
            date_from.strftime("%Y-%m-%d"),
            date_to.strftime("%Y-%m-%d")
        )
        
        if df.empty:
            return f"Báo cáo tổng hợp ({date_from.strftime('%d/%m/%Y')} - {date_to.strftime('%d/%m/%Y')})", None
        
        total_income = df[df['type'] == 'income']['amount'].sum()
        total_expense = df[df['type'] == 'expense']['amount'].sum()
        net_income = total_income - total_expense
        
        title = f"Báo cáo tổng hợp ({date_from.strftime('%d/%m/%Y')} - {date_to.strftime('%d/%m/%Y')})"
        data = {
            "Tổng thu": f"{total_income:,.0f} VND",
            "Tổng chi": f"{total_expense:,.0f} VND",
            "Thu nhập ròng": f"{net_income:,.0f} VND",
            "Khoản chi lớn nhất": self.get_largest_expense(df),
            "Khoản thu lớn nhất": self.get_largest_income(df),
            "Danh mục phổ biến nhất": self.get_most_common_category(df)
        }
        return title, data

    def _get_detail_report_data(self, date_from, date_to):
        df = self.app.xu_ly_du_lieu.get_transactions_dataframe(
            date_from.strftime("%Y-%m-%d"),
            date_to.strftime("%Y-%m-%d")
        )
        
        if df.empty:
            return f"Báo cáo chi tiết ({date_from.strftime('%d/%m/%Y')} - {date_to.strftime('%d/%m/%Y')})", None
        
        # Map 'income' to 'Thu' and 'expense' to 'Chi' for display in detail report
        df['type'] = df['type'].map({'income': 'Thu', 'expense': 'Chi'})
        
        title = f"Báo cáo chi tiết ({date_from.strftime('%d/%m/%Y')} - {date_to.strftime('%d/%m/%Y')})"
        return title, df

    def _get_trend_report_data(self, date_from, date_to):
        df = self.app.xu_ly_du_lieu.get_transactions_dataframe(
            date_from.strftime("%Y-%m-%d"),
            date_to.strftime("%Y-%m-%d")
        )
        
        if df.empty:
            return f"Báo cáo xu hướng ({date_from.strftime('%d/%m/%Y')} - {date_to.strftime('%d/%m/%Y')})", None
        
        df['date'] = pd.to_datetime(df['date'])
        daily_data = df.groupby(['date', 'type'])['amount'].sum().unstack()
        
        future_expenses = self.predict_future_expenses(df)
        
        title = f"Báo cáo xu hướng ({date_from.strftime('%d/%m/%Y')} - {date_to.strftime('%d/%m/%Y')})"
        data = {
            "Xu hướng thu": "Tăng" if daily_data.get('income', pd.Series()).pct_change().mean() > 0 else "Giảm",
            "Xu hướng chi": "Tăng" if daily_data.get('expense', pd.Series()).pct_change().mean() > 0 else "Giảm",
            "Dự đoán chi tiêu tháng tới": f"{future_expenses:,.0f} VND"
        }
        return title, data

    def _get_analysis_report_data(self, date_from, date_to):
        df = self.app.xu_ly_du_lieu.get_transactions_dataframe(
            date_from.strftime("%Y-%m-%d"),
            date_to.strftime("%Y-%m-%d")
        )
        
        if df.empty:
            return f"Báo cáo phân tích ({date_from.strftime('%d/%m/%Y')} - {date_to.strftime('%d/%m/%Y')})", None
        
        expense_by_category = df[df['type'] == 'expense'].groupby('category')['amount'].sum()
        income_by_category = df[df['type'] == 'income'].groupby('category')['amount'].sum()
        
        total_income_amount = df[df['type'] == 'income']['amount'].sum()
        total_expense_amount = df[df['type'] == 'expense']['amount'].sum()
        
        saving_rate = 0
        if total_income_amount > 0:
            saving_rate = ((total_income_amount - total_expense_amount) / total_income_amount) * 100

        title = f"Báo cáo phân tích ({date_from.strftime('%d/%m/%Y')} - {date_to.strftime('%d/%m/%Y')})"
        data = {
            "Phân bố chi tiêu": expense_by_category.to_dict(),
            "Phân bố thu nhập": income_by_category.to_dict(),
            "Tỷ lệ tiết kiệm": f"{saving_rate:.1f}%"
        }
        return title, data

    def create_pdf_report(self, title, data):
        # Tạo tên file
        report_type_name = "Bao_cao_tong_hop" if isinstance(data, dict) else "Bao_cao_chi_tiet"
        date_str = datetime.now().strftime("%Y%m%d")
        filename = f"{report_type_name}_{date_str}.pdf"
        
        # Tạo file PDF
        filepath = filedialog.asksaveasfilename(
            defaultextension=".pdf",
            initialfile=filename,
            filetypes=[("PDF files", "*.pdf")]
        )
        
        if not filepath:
            return

        # Tạo document
        doc = SimpleDocTemplate(
            filepath,
            pagesize=A4,
            rightMargin=72,
            leftMargin=72,
            topMargin=72,
            bottomMargin=72
        )

        # Tạo styles
        styles = getSampleStyleSheet()
        
        title_style = ParagraphStyle(
            'CustomTitle',
            parent=styles['Heading1'],
            fontName=self.bold_font,
            fontSize=16,
            spaceAfter=30,
            alignment=1
        )

        normal_style = ParagraphStyle(
            'NormalVietnamese',
            parent=styles['Normal'],
            fontName=self.normal_font,
            fontSize=12
        )

        # Tạo nội dung
        elements = []
        
        # Thêm tiêu đề
        elements.append(Paragraph(self._remove_vietnamese_accents(title), title_style))
        
        if isinstance(data, dict):
            # Báo cáo tổng hợp
            for key, value in data.items():
                elements.append(Paragraph(f"{self._remove_vietnamese_accents(key)}: {self._remove_vietnamese_accents(str(value))}", normal_style))
                elements.append(Paragraph("<br/>", normal_style))
        else:
            # Báo cáo chi tiết
            # Tạo bảng
            headers = [self._remove_vietnamese_accents(h) for h in list(data[0].keys())]
            table_data = [headers]  # Header row
            
            # Thêm dữ liệu
            for row in data:
                table_data.append([self._remove_vietnamese_accents(str(value)) for value in row.values()])
            
            # Tạo table
            table = Table(table_data)
            
            # Style cho bảng
            table.setStyle(TableStyle([
                ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
                ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
                ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
                ('FONTNAME', (0, 0), (-1, 0), self.bold_font),
                ('FONTSIZE', (0, 0), (-1, 0), 12),
                ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
                ('BACKGROUND', (0, 1), (-1, -1), colors.white),
                ('TEXTCOLOR', (0, 1), (-1, -1), colors.black),
                ('FONTNAME', (0, 1), (-1, -1), self.normal_font),
                ('FONTSIZE', (0, 1), (-1, -1), 10),
                ('GRID', (0, 0), (-1, -1), 1, colors.black),
                ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
                ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
            ]))
            
            elements.append(table)

        # Build PDF
        doc.build(elements)
        messagebox.showinfo("Thông báo", "Đã xuất báo cáo PDF thành công!")

    def create_excel_report(self, title, df):
        # Tạo tên file
        report_type = "Bao_cao_tong_hop" if len(df.columns) == 2 else "Bao_cao_chi_tiet"
        date_str = datetime.now().strftime("%Y%m%d")
        filename = f"{report_type}_{date_str}.xlsx"
        
        # Tạo file Excel
        filepath = filedialog.asksaveasfilename(
            defaultextension=".xlsx",
            initialfile=filename,
            filetypes=[("Excel files", "*.xlsx")]
        )
        
        if not filepath:
            return
            
        with pd.ExcelWriter(filepath, engine='openpyxl') as writer:
            df.to_excel(writer, sheet_name='Báo cáo', index=False)
            
            # Điều chỉnh độ rộng cột
            worksheet = writer.sheets['Báo cáo']
            for idx, col in enumerate(df.columns):
                max_length = max(
                    df[col].astype(str).apply(len).max(),
                    len(str(col))
                )
                worksheet.column_dimensions[chr(65 + idx)].width = max_length + 2
        
        messagebox.showinfo("Thông báo", "Đã xuất báo cáo Excel thành công!")

    def create_csv_report(self, title, df):
        # Tạo tên file
        report_type = "Bao_cao_tong_hop" if len(df.columns) == 2 else "Bao_cao_chi_tiet"
        date_str = datetime.now().strftime("%Y%m%d")
        filename = f"{report_type}_{date_str}.csv"
        
        # Tạo file CSV
        filepath = filedialog.asksaveasfilename(
            defaultextension=".csv",
            initialfile=filename,
            filetypes=[("CSV files", "*.csv")]
        )
        
        if not filepath:
            return
            
        df.to_csv(filepath, index=False, encoding='utf-8-sig')
        messagebox.showinfo("Thông báo", "Đã xuất báo cáo CSV thành công!")

    def get_largest_expense(self, df):
        # Tìm khoản chi lớn nhất
        if df.empty or not (df['type'] == 'expense').any():
            return "Không có dữ liệu"
        largest = df[df['type'] == 'expense'].nlargest(1, 'amount').iloc[0]
        return f"{largest['category']}: {largest['amount']:,.0f} VND"

    def get_largest_income(self, df):
        # Tìm khoản thu lớn nhất
        if df.empty or not (df['type'] == 'income').any():
            return "Không có dữ liệu"
        largest = df[df['type'] == 'income'].nlargest(1, 'amount').iloc[0]
        return f"{largest['category']}: {largest['amount']:,.0f} VND"

    def get_most_common_category(self, df):
        # Tìm danh mục phổ biến nhất
        if df.empty:
            return "Không có dữ liệu"
        return df['category'].mode().iloc[0]

    def predict_future_expenses(self, df):
        # Phân tích xu hướng chi tiêu
        if df.empty or not (df['type'] == 'expense').any():
            return 0
        
        # Lấy dữ liệu chi tiêu
        expense_data = df[df['type'] == 'expense'].groupby('date')['amount'].sum()
        
        if len(expense_data) < 2:
            return expense_data.mean()
        
        # Chuẩn bị dữ liệu
        X = np.arange(len(expense_data)).reshape(-1, 1)
        y = expense_data.values
        
        # Huấn luyện mô hình
        model = LinearRegression()
        model.fit(X, y)
        
        # Dự đoán chi tiêu tháng tới
        next_month = len(expense_data)
        prediction = model.predict([[next_month]])[0]
        
        return max(0, prediction)  # Đảm bảo giá trị không âm 

    def preview_detail_report(self, date_from, date_to, format):
        # Tạo DataFrame từ dữ liệu
        df = self.app.xu_ly_du_lieu.get_transactions_dataframe(
            date_from.strftime("%Y-%m-%d"),
            date_to.strftime("%Y-%m-%d")
        )
        
        if df.empty:
            messagebox.showwarning("Cảnh báo", "Không có dữ liệu trong khoảng thời gian này!")
            return

        # Tạo cửa sổ preview
        preview_window = ctk.CTkToplevel(self.app.root)
        preview_window.title(f"Xem trước báo cáo chi tiết ({date_from.strftime('%d/%m/%Y')} - {date_to.strftime('%d/%m/%Y')})")
        preview_window.geometry("800x600")
        preview_window.transient(self.app.root)
        preview_window.grab_set()
        preview_window.focus_force()

        # Configure grid
        preview_window.grid_columnconfigure(0, weight=1)
        preview_window.grid_rowconfigure(0, weight=1)
        preview_window.grid_rowconfigure(1, weight=0)

        # Tạo frame cho bảng dữ liệu
        table_frame = ctk.CTkFrame(preview_window)
        table_frame.grid(row=0, column=0, padx=10, pady=5, sticky="nsew")
        table_frame.grid_columnconfigure(0, weight=1)
        table_frame.grid_rowconfigure(0, weight=1)

        # Tạo Treeview để hiển thị dữ liệu
        columns = list(df.columns)
        self.tree = ttk.Treeview(table_frame, columns=columns, show='headings')
        
        # Thêm thanh cuộn
        scrollbar_y = ttk.Scrollbar(table_frame, orient="vertical", command=self.tree.yview)
        scrollbar_x = ttk.Scrollbar(table_frame, orient="horizontal", command=self.tree.xview)
        self.tree.configure(yscrollcommand=scrollbar_y.set, xscrollcommand=scrollbar_x.set)

        # Đặt vị trí các thành phần
        self.tree.grid(row=0, column=0, sticky="nsew")
        scrollbar_y.grid(row=0, column=1, sticky="ns")
        scrollbar_x.grid(row=1, column=0, sticky="ew")

        # Đặt tên cột
        column_names = {
            'date': 'Ngày',
            'type': 'Loại',
            'category': 'Danh mục',
            'amount': 'Số tiền',
            'description': 'Mô tả'
        }
        for col in columns:
            self.tree.heading(col, text=column_names.get(col, col))
            self.tree.column(col, width=100)

        # Thêm dữ liệu
        for _, row in df.iterrows():
            self.tree.insert("", "end", values=list(row))

        # Frame cho nút xuất báo cáo
        button_frame = ctk.CTkFrame(preview_window)
        button_frame.grid(row=1, column=0, padx=10, pady=5, sticky="ew")
        button_frame.grid_columnconfigure(0, weight=1)
        button_frame.grid_columnconfigure(1, weight=1)

        # Nút xuất báo cáo
        ctk.CTkButton(button_frame, text="Xuất báo cáo", 
                     command=lambda: self.generate_detail_report(date_from, date_to, format)).grid(row=0, column=0, padx=5, pady=5)
        
        # Nút đóng
        ctk.CTkButton(button_frame, text="Đóng", 
                     command=preview_window.destroy).grid(row=0, column=1, padx=5, pady=5)

    def view_report(self, report_type, date_range, format):
        date_from, date_to = self._get_date_range(date_range)

        title = ""
        report_data = None

        if report_type == "summary":
            title, report_data = self._get_summary_report_data(date_from, date_to)
        elif report_type == "detail":
            title, report_data = self._get_detail_report_data(date_from, date_to)
        elif report_type == "trend":
            title, report_data = self._get_trend_report_data(date_from, date_to)
        elif report_type == "analysis":
            title, report_data = self._get_analysis_report_data(date_from, date_to)

        if report_data is None:
            messagebox.showwarning("Cảnh báo", "Không có dữ liệu trong khoảng thời gian này!")
            return

        # Tạo cửa sổ xem báo cáo
        view_window = ctk.CTkToplevel(self.app.root)
        view_window.title(title)
        view_window.geometry("800x600")
        view_window.transient(self.app.root)
        view_window.grab_set()
        view_window.focus_force()

        # Configure grid
        view_window.grid_columnconfigure(0, weight=1)
        view_window.grid_rowconfigure(0, weight=1)
        view_window.grid_rowconfigure(1, weight=0)

        # Tạo frame hiển thị dữ liệu
        # Use CTkScrollableFrame for dictionary-based reports
        if isinstance(report_data, pd.DataFrame):
            display_frame = ctk.CTkFrame(view_window) # Use regular frame for Treeview
            display_frame.grid(row=0, column=0, padx=10, pady=5, sticky="nsew")
            display_frame.grid_columnconfigure(0, weight=1)
            display_frame.grid_rowconfigure(0, weight=1)

            # Hiển thị dạng bảng (cho báo cáo chi tiết)
            columns = list(report_data.columns)
            self.tree = ttk.Treeview(display_frame, columns=columns, show='headings')
            
            scrollbar_y = ttk.Scrollbar(display_frame, orient="vertical", command=self.tree.yview)
            scrollbar_x = ttk.Scrollbar(display_frame, orient="horizontal", command=self.tree.xview)
            self.tree.configure(yscrollcommand=scrollbar_y.set, xscrollcommand=scrollbar_x.set)

            self.tree.grid(row=0, column=0, sticky="nsew")
            scrollbar_y.grid(row=0, column=1, sticky="ns")
            scrollbar_x.grid(row=1, column=0, sticky="ew")

            column_names = {
                'date': 'Ngày',
                'type': 'Loại',
                'category': 'Danh mục',
                'amount': 'Số tiền',
                'description': 'Mô tả'
            }
            for col in columns:
                self.tree.heading(col, text=column_names.get(col, col))
                self.tree.column(col, width=100)

            for _, row in report_data.iterrows():
                self.tree.insert("", "end", values=list(row))
        elif isinstance(report_data, dict):
            # Hiển thị dạng danh sách (cho báo cáo tổng hợp, xu hướng, phân tích)
            scrollable_frame = ctk.CTkScrollableFrame(view_window)
            scrollable_frame.grid(row=0, column=0, padx=10, pady=5, sticky="nsew")
            
            # Sử dụng pack để sắp xếp gọn gàng các labels
            for key, value in report_data.items():
                # Format dictionaries within dict (for analysis report categories)
                if isinstance(value, dict):
                    # For nested dictionaries (like in Analysis report for categories)
                    ctk.CTkLabel(scrollable_frame, text=f"{key}:", font=("Arial", 14, "bold")).pack(anchor="w", padx=5, pady=5)
                    for sub_key, sub_value in value.items():
                        ctk.CTkLabel(scrollable_frame, text=f"  - {sub_key}: {sub_value}", font=("Arial", 12)).pack(anchor="w", padx=15, pady=2)
                else:
                    ctk.CTkLabel(scrollable_frame, text=f"{key}: {value}", font=("Arial", 12)).pack(anchor="w", padx=5, pady=2)

        # Frame cho nút
        button_frame = ctk.CTkFrame(view_window)
        button_frame.grid(row=1, column=0, padx=10, pady=5, sticky="ew")
        button_frame.grid_columnconfigure(0, weight=1)
        button_frame.grid_columnconfigure(1, weight=1)

        # Nút xuất báo cáo (sử dụng lại logic generate_report)
        ctk.CTkButton(button_frame, text="Xuất báo cáo", 
                     command=lambda: self.generate_report(report_type, date_range, format)).grid(row=0, column=0, padx=5, pady=5)
        
        # Nút đóng
        ctk.CTkButton(button_frame, text="Đóng", 
                     command=view_window.destroy).grid(row=0, column=1, padx=5, pady=5)

    def xem_thongke(self):
        # Tạo cửa sổ thống kê
        window = ctk.CTkToplevel(self.app.root)
        window.title("Thống kê chi tiết")
        window.geometry("800x800")
        window.transient(self.app.root)
        window.grab_set()
        window.focus_force()
        
        # Frame chọn khoảng thời gian
        date_frame = ctk.CTkFrame(window)
        date_frame.pack(fill=tk.X, padx=10, pady=5)
        
        ctk.CTkLabel(date_frame, text="Khoảng thời gian:").pack(pady=5)
        
        date_range = ctk.StringVar(value="month")
        ctk.CTkRadioButton(date_frame, text="Tháng này", 
                          variable=date_range, value="month").pack()
        ctk.CTkRadioButton(date_frame, text="Quý này", 
                          variable=date_range, value="quarter").pack()
        ctk.CTkRadioButton(date_frame, text="Năm nay", 
                          variable=date_range, value="year").pack()
        ctk.CTkRadioButton(date_frame, text="Tùy chọn", 
                          variable=date_range, value="custom").pack()
        
        # Frame hiển thị thống kê
        stats_frame = ctk.CTkFrame(window)
        stats_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)
        
        # Tạo các tab cho các loại thống kê khác nhau
        tabview = ctk.CTkTabview(stats_frame)
        tabview.pack(fill=tk.BOTH, expand=True)
        
        # Tab tổng quan
        tabview.add("Tổng quan")
        overview_frame = ctk.CTkFrame(tabview.tab("Tổng quan"))
        overview_frame.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        # Tab theo danh mục
        tabview.add("Theo danh mục")
        category_frame = ctk.CTkFrame(tabview.tab("Theo danh mục"))
        category_frame.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        # Tab xu hướng
        tabview.add("Xu hướng")
        trend_frame = ctk.CTkFrame(tabview.tab("Xu hướng"))
        trend_frame.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        def update_stats(*args):
            # Xác định khoảng thời gian
            today = datetime.now()
            if date_range.get() == "month":
                date_from = today.replace(day=1)
                date_to = today
            elif date_range.get() == "quarter":
                quarter = (today.month - 1) // 3
                date_from = today.replace(month=quarter * 3 + 1, day=1)
                date_to = today
            elif date_range.get() == "year":
                date_from = today.replace(month=1, day=1)
                date_to = today
            else:  # custom
                # TODO: Thêm dialog chọn ngày
                date_from = today - timedelta(days=365) # Mặc định 1 năm trước
                date_to = today
            
            # Lấy dữ liệu
            df = self.app.xu_ly_du_lieu.get_transactions_dataframe(
                date_from.strftime("%Y-%m-%d"),
                date_to.strftime("%Y-%m-%d")
            )
            
            if df.empty:
                messagebox.showwarning("Cảnh báo", "Không có dữ liệu trong khoảng thời gian này!")
                return
            
            # Cập nhật tab tổng quan
            self.update_overview_tab(overview_frame, df)
            
            # Cập nhật tab theo danh mục
            self.update_category_tab(category_frame, df)
            
            # Cập nhật tab xu hướng
            self.update_trend_tab(trend_frame, df)
        
        # Gắn sự kiện cập nhật
        date_range.trace_add("write", update_stats)
        
        # Nút cập nhật
        ctk.CTkButton(window, text="Cập nhật", command=update_stats).pack(pady=10)
        
        # Cập nhật lần đầu
        update_stats()
    
    def update_overview_tab(self, frame, df):
        # Xóa các widget cũ
        for widget in frame.winfo_children():
            widget.destroy()
        
        # Tính toán các chỉ số
        total_income = df[df['type'] == 'income']['amount'].sum()
        total_expense = df[df['type'] == 'expense']['amount'].sum()
        net_income = total_income - total_expense
        
        # Hiển thị các chỉ số
        ctk.CTkLabel(frame, text="Tổng quan tài chính", 
                    font=("Arial", 16, "bold")).pack(pady=10)
        
        stats = [
            ("Tổng thu", f"{total_income:,.0f} VND"),
            ("Tổng chi", f"{total_expense:,.0f} VND"),
            ("Thu nhập ròng", f"{net_income:,.0f} VND"),
            ("Khoản chi lớn nhất", self.get_largest_expense(df)),
            ("Khoản thu lớn nhất", self.get_largest_income(df)),
            ("Danh mục phổ biến nhất", self.get_most_common_category(df))
        ]
        
        for label, value in stats:
            stat_frame = ctk.CTkFrame(frame)
            stat_frame.pack(fill=tk.X, padx=5, pady=2)
            ctk.CTkLabel(stat_frame, text=label).pack(side=tk.LEFT, padx=5)
            ctk.CTkLabel(stat_frame, text=value).pack(side=tk.RIGHT, padx=5)
    
    def update_category_tab(self, frame, df):
        # Xóa các widget cũ
        for widget in frame.winfo_children():
            widget.destroy()
        
        # Tính toán thống kê theo danh mục
        category_stats = df.groupby(['type', 'category'])['amount'].agg(['sum', 'count'])
        
        # Hiển thị thống kê
        ctk.CTkLabel(frame, text="Thống kê theo danh mục", 
                    font=("Arial", 16, "bold")).pack(pady=10)
        
        # Tạo bảng
        columns = ("Loại", "Danh mục", "Tổng tiền", "Số giao dịch")
        self.tree = ttk.Treeview(frame, columns=columns, show="headings")
        
        for col in columns:
            self.tree.heading(col, text=col)
            self.tree.column(col, width=100)
        
        # Thêm dữ liệu
        for (type_, category), stats in category_stats.iterrows():
            display_type = 'Thu' if type_ == 'income' else 'Chi'
            self.tree.insert("", "end", values=(
                display_type,
                category,
                f"{stats['sum']:,.0f} VND",
                stats['count']
            ))
        
        self.tree.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
    
    def update_trend_tab(self, frame, df):
        # Xóa các widget cũ
        for widget in frame.winfo_children(): 
            widget.destroy()
        
        # Tính toán xu hướng
        df['date'] = pd.to_datetime(df['date'])
        daily_data = df.groupby(['date', 'type'])['amount'].sum().unstack()
        
        # Dự đoán xu hướng
        future_expenses = self.predict_future_expenses(df)
        
        # Hiển thị xu hướng
        ctk.CTkLabel(frame, text="Phân tích xu hướng", 
                    font=("Arial", 16, "bold")).pack(pady=10)
        
        # Tạo biểu đồ
        fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(10, 8))  # Tăng kích thước biểu đồ
        
        # Điều chỉnh khoảng cách giữa các subplot
        plt.subplots_adjust(hspace=0.5)  # Tăng khoảng cách giữa các subplot
        
        # Biểu đồ xu hướng thu chi
        daily_data.plot(ax=ax1)
        ax1.set_title("Xu hướng thu chi & Phân bố chi tiêu theo danh mục", fontsize=14)  # Điều chỉnh kích thước chữ
        ax1.set_xlabel(" ", fontsize=12)  # Điều chỉnh kích thước chữ
        ax1.set_ylabel("Số tiền (VND)", fontsize=12)  # Điều chỉnh kích thước chữ
        ax1.grid(True)  # Thêm đường lưới để dễ đọc hơn
        ax1.tick_params(axis='x', rotation=0)  # Điều chỉnh góc của nhãn trục x

        
        # Biểu đồ phân bố chi tiêu theo danh mục
        df[df['type'] == 'expense'].groupby('category')['amount'].sum().plot(
            kind='pie', ax=ax2, autopct='%1.1f%%', colors=['#ff9999','#66b3ff','#99ff99','#ffcc99']
        )
        ax2.set_title(" ", fontsize=20)  # Điều chỉnh kích thước chữ
        ax2.set_ylabel('')  # Ẩn chữ "amount"

        # Hiển thị dự đoán
        ctk.CTkLabel(frame, 
                    text=f"Dự đoán chi tiêu tháng tới: {future_expenses:,.0f} VND",
                    font=("Arial", 12, "bold")).pack(pady=5)
        
        # Hiển thị biểu đồ
        canvas = FigureCanvasTkAgg(fig, master=frame)
        canvas.draw()
        canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
    def xem_lichsu(self):
        # Tạo cửa sổ lịch sử
        window = ctk.CTkToplevel(self.app.root)
        window.title("Lịch sử giao dịch")
        window.geometry("1000x600")
        window.transient(self.app.root)
        window.grab_set()
        window.focus_force()
        
        # Frame chọn khoảng thời gian
        date_frame = ctk.CTkFrame(window)
        date_frame.pack(fill=tk.X, padx=10, pady=5)
        
        ctk.CTkLabel(date_frame, text="Khoảng thời gian:").pack(pady=5)
        
        date_range = ctk.StringVar(value="month")
        ctk.CTkRadioButton(date_frame, text="Tháng này", 
                          variable=date_range, value="month").pack()
        ctk.CTkRadioButton(date_frame, text="Quý này", 
                          variable=date_range, value="quarter").pack()
        ctk.CTkRadioButton(date_frame, text="Năm nay", 
                          variable=date_range, value="year").pack()
        ctk.CTkRadioButton(date_frame, text="Tùy chọn", 
                          variable=date_range, value="custom").pack()
        
        # Frame tìm kiếm và lọc
        filter_frame = ctk.CTkFrame(window)
        filter_frame.pack(fill=tk.X, padx=10, pady=5)
        
        ctk.CTkLabel(filter_frame, text="Tìm kiếm:").pack(side=tk.LEFT, padx=5)
        search_entry = ctk.CTkEntry(filter_frame)
        search_entry.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=5)

        ctk.CTkLabel(filter_frame, text="Loại:").pack(side=tk.LEFT, padx=5)
        type_var = ctk.StringVar(value="Tất cả")
        type_combo = ctk.CTkComboBox(filter_frame, 
                                   values=["Tất cả", "Thu", "Chi"],
                                   variable=type_var)
        type_combo.pack(side=tk.LEFT, padx=5)
        
        ctk.CTkLabel(filter_frame, text="Danh mục:").pack(side=tk.LEFT, padx=5)
        category_var = ctk.StringVar(value="Tất cả")
        category_combo = ctk.CTkComboBox(filter_frame, 
                                       values=["Tất cả"] + 
                                             self.app.categories['income'] + 
                                             self.app.categories['expense'],
                                       variable=category_var)
        category_combo.pack(side=tk.LEFT, padx=5)
        
        # Frame hiển thị lịch sử
        history_frame = ctk.CTkFrame(window)
        history_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)
        
        # Tạo bảng
        columns = ("Ngày", "Loại", "Danh mục", "Số tiền", "Ghi chú")
        self.tree = ttk.Treeview(history_frame, columns=columns, show="headings")
        
        # Định dạng cột
        for col in columns:
            self.tree.heading(col, text=col)
            self.tree.column(col, width=100)
        
        # Thêm thanh cuộn
        scrollbar = ttk.Scrollbar(history_frame, orient=tk.VERTICAL, command=self.tree.yview)
        self.tree.configure(yscrollcommand=scrollbar.set)
        
        # Sắp xếp layout
        self.tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        # Định nghĩa update_history_local SAU KHI tree được tạo
        def update_history_local(*args):
            # Xóa dữ liệu cũ
            for item in self.tree.get_children():
                self.tree.delete(item)
            
            # Xác định khoảng thời gian
            today = datetime.now()
            if date_range.get() == "month":
                date_from = today.replace(day=1)
                date_to = today
            elif date_range.get() == "quarter":
                quarter = (today.month - 1) // 3
                date_from = today.replace(month=quarter * 3 + 1, day=1)
                date_to = today
            elif date_range.get() == "year":
                date_from = today.replace(month=1, day=1)
                date_to = today
            else:  # custom
                # TODO: Thêm dialog chọn ngày
                date_from = today - timedelta(days=365) # Mặc định 1 năm trước
                date_to = today
            
            # Lấy dữ liệu
            df = self.app.xu_ly_du_lieu.get_transactions_dataframe(
                date_from.strftime("%Y-%m-%d"),
                date_to.strftime("%Y-%m-%d")
            )
            
            if df.empty:
                messagebox.showwarning("Cảnh báo", "Không có dữ liệu trong khoảng thời gian này!")
                return
            
            # Lọc dữ liệu
            if type_var.get() != "Tất cả":
                # Ánh xạ loại giao dịch từ hiển thị sang dữ liệu
                mapped_type_filter = type_var.get()
                if mapped_type_filter == "Thu":
                    mapped_type_filter = "income"
                elif mapped_type_filter == "Chi":
                    mapped_type_filter = "expense"
                df = df[df['type'] == mapped_type_filter]
            
            if category_var.get() != "Tất cả":
                df = df[df['category'] == category_var.get()]
            
            search_text = search_entry.get().lower()
            if search_text:
                df = df[df['note'].str.lower().str.contains(search_text, na=False)]
            
            # Sắp xếp theo ngày
            df = df.sort_values('date', ascending=False)
            
            # Hiển thị dữ liệu
            for _, row in df.iterrows():
                display_type = 'Thu' if row['type'] == 'income' else 'Chi'
                self.tree.insert("", "end", values=(
                    row['date'].strftime("%d/%m/%Y"),
                    display_type,
                    row['category'],
                    f"{row['amount']:,.0f} VND",
                    row['note']
                ))
        
        # Nút cập nhật và Gắn sự kiện cập nhật (Moved here after update_history_local definition)
        ctk.CTkButton(filter_frame, text="Cập nhật", command=update_history_local).pack(side=tk.LEFT, padx=5)
        date_range.trace_add("write", update_history_local)
        type_var.trace_add("write", update_history_local)
        category_var.trace_add("write", update_history_local)
        search_entry.bind("<KeyRelease>", update_history_local)
        
        # Cập nhật lần đầu
        update_history_local()