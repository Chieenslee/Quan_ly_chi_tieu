import customtkinter as ctk
from tkinter import ttk, messagebox, Menu, filedialog
import tkinter as tk
from datetime import datetime
import pandas as pd
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.pyplot as plt
import darkdetect
import platform
from tkcalendar import Calendar, DateEntry

class GiaoDien:
    def __init__(self, root, app):
        self.root = root
        self.app = app

    def tao_giaodien(self):
        # Tạo menu chính
        self.tao_menu()
        
        # Tạo thanh công cụ
        self.tao_thanh_congcu()
        
        # Tạo khung chính
        self.main_frame = ctk.CTkFrame(self.root)
        self.main_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Tạo layout chính
        self.tao_layout_chinh()
        
        # Tạo thanh trạng thái
        self.tao_thanh_trangthai()

    def tao_menu(self):
        # Tạo menu chính
        menubar = Menu(self.root)
        self.root.config(menu=menubar)
        
        # Menu File
        file_menu = Menu(menubar, tearoff=0)
        menubar.add_cascade(label="📁 File", menu=file_menu)
        file_menu.add_command(label="📥 Nhập dữ liệu", command=self.app.xu_ly_du_lieu.nhap_dulieu)
        file_menu.add_command(label="📤 Xuất dữ liệu", command=self.app.xu_ly_du_lieu.xuat_dulieu)
        file_menu.add_separator()
        file_menu.add_command(label="🔄 Đồng bộ dữ liệu", command=self.app.dong_bo_du_lieu)
        file_menu.add_command(label="↩️ Khôi phục dữ liệu", command=self._select_backup_file_and_restore)
        file_menu.add_separator()
        file_menu.add_command(label="⚙️ Cài đặt", command=self.app.mo_caidat)
        file_menu.add_separator()
        file_menu.add_command(label="🚪 Thoát", command=self.root.quit)
        
        # Menu Giao dịch
        transaction_menu = Menu(menubar, tearoff=0)
        menubar.add_cascade(label="💰 Giao dịch", menu=transaction_menu)
        transaction_menu.add_command(label="➕ Thêm thu", command=lambda: self.tao_cua_so_them_giao_dich(transaction_type='income'))
        transaction_menu.add_command(label="➖ Thêm chi", command=lambda: self.tao_cua_so_them_giao_dich(transaction_type='expense'))
        transaction_menu.add_separator()
        transaction_menu.add_command(label="🔍 Tìm kiếm", command=self.app.xu_ly_du_lieu.tim_kiem)
        transaction_menu.add_command(label="🔎 Tìm kiếm nâng cao", command=self.app.xu_ly_du_lieu.tim_kiem_nang_cao)
        
        # Menu Báo cáo
        report_menu = Menu(menubar, tearoff=0)
        menubar.add_cascade(label="📊 Báo cáo", menu=report_menu)
        report_menu.add_command(label="📈 Báo cáo tổng hợp", command=self.app.bao_cao.xem_baocao)
        report_menu.add_command(label="📊 Thống kê", command=self.app.bao_cao.xem_thongke)
        report_menu.add_command(label="📅 Lịch sử", command=self.app.bao_cao.xem_lichsu)
        
        # Menu Biểu đồ
        chart_menu = Menu(menubar, tearoff=0)
        menubar.add_cascade(label="📈 Biểu đồ", menu=chart_menu)
        chart_menu.add_command(label="📊 Biểu đồ tròn", command=self.app.bieu_do.tao_bieudo_tron)
        chart_menu.add_command(label="📈 Biểu đồ xu hướng", command=self.app.bieu_do.tao_bieudo_xuhuong)
        chart_menu.add_command(label="🆚 Biểu đồ so sánh thu chi", command=self.app.bieu_do.tao_bieudo_so_sanh)
        chart_menu.add_command(label="📊 Biểu đồ phân tích chi tiêu", command=self.app.bieu_do.tao_bieudo_phan_tich)
        chart_menu.add_command(label="📉 Biểu đồ thói quen chi tiêu", command=self.app.bieu_do.tao_bieudo_thoiquen)
        chart_menu.add_command(label="🎯 Biểu đồ tiến độ mục tiêu", command=self.app.bieu_do.tao_bieudo_muctieu)
        chart_menu.add_command(label="🔮 Biểu đồ dự báo chi tiêu", command=self.app.bieu_do.tao_bieudo_du_bao)
        
        # Menu Tính năng
        feature_menu = Menu(menubar, tearoff=0)
        menubar.add_cascade(label="🛠️ Tính năng", menu=feature_menu)
        feature_menu.add_command(label="💹 Tính lãi suất", command=self.app.tinh_nang.tinh_laisuat)
        feature_menu.add_command(label="💰 Tính thuế", command=self.app.tinh_nang.tinh_thue)
        feature_menu.add_command(label="📋 Lập kế hoạch", command=self.app.tinh_nang.lap_kehoach)
        feature_menu.add_command(label="🎯 Theo dõi mục tiêu", command=self.app.tinh_nang.theo_doi_muctieu)
        feature_menu.add_command(label="📈 Phân tích xu hướng", command=self.app.tinh_nang.phan_tich_xuhuong)
        feature_menu.add_command(label="📊 Phân tích thói quen", command=self.app.tinh_nang.phan_tich_thoiquen)
        feature_menu.add_command(label="🔔 Quản lý nhắc nhở", command=self.app.tinh_nang.xem_nhacnho)
        feature_menu.add_command(label="➕ Thêm nhắc nhở", command=self.app.thong_bao.them_nhacnho)
        
        # Menu Bảo mật
        security_menu = Menu(menubar, tearoff=0)
        menubar.add_cascade(label="🔒 Bảo mật", menu=security_menu)
        security_menu.add_command(label="🔐 Mã hóa dữ liệu", command=self.app.bao_mat.ma_hoa_dulieu)
        security_menu.add_command(label="🔓 Giải mã dữ liệu", command=self.app.bao_mat.giai_ma_dulieu)
        security_menu.add_separator()
        security_menu.add_command(label="🔍 Kiểm tra bảo mật", command=self.app.bao_mat.kiem_tra_baomat)
        security_menu.add_command(label="📦 Sao lưu bảo mật", command=self.app.bao_mat.sao_luu_baomat)
        security_menu.add_command(label="↩️ Khôi phục bảo mật", command=self.app.bao_mat.khoi_phuc_baomat)
        security_menu.add_separator()
        security_menu.add_command(label="🔑 Đổi mật khẩu", command=self.app.bao_mat.doi_matkhau)
        security_menu.add_command(label="🗑️ Xóa dữ liệu mã hóa", command=self.app.bao_mat.xoa_dulieu_baomat)
        security_menu.add_command(label="⚠️ Kiểm tra quyền truy cập", command=self.app.bao_mat.kiem_tra_quyen)
        security_menu.add_command(label="✅ Kiểm tra tính nguyên vẹn", command=self.app.bao_mat.kiem_tra_tinhnguyenven)
        security_menu.add_separator()
        security_menu.add_command(label="📦 Nén dữ liệu", command=self.app.xu_ly_du_lieu.compress_data)
        security_menu.add_command(label="🗑️ Xóa dữ liệu cũ", command=self.app.xu_ly_du_lieu.delete_old_data)
        
        # Menu Công cụ
        tools_menu = Menu(menubar, tearoff=0)
        menubar.add_cascade(label="🔧 Công cụ", menu=tools_menu)
        tools_menu.add_command(label="🧮 Tính toán đơn giản", command=self.app.tinh_toan.tinh_toan_don_gian)
        tools_menu.add_command(label="💲 Chuyển đổi tiền tệ", command=self.app.tinh_toan.chuyen_doi_tien_te)
        tools_menu.add_command(label="💡 Đề xuất tối ưu", command=self.app.tinh_toan.de_xuat_toiuu)
        
        # Menu Trợ giúp
        help_menu = Menu(menubar, tearoff=0)
        menubar.add_cascade(label="❓ Trợ giúp", menu=help_menu)
        help_menu.add_command(label="📖 Hướng dẫn", command=self.app.xem_huongdan)
        help_menu.add_command(label="ℹ️ Giới thiệu", command=self.app.xem_gioithieu)
        help_menu.add_command(label="🔄 Kiểm tra cập nhật", command=self.app.kiem_tra_capnhat)
        help_menu.add_command(label="🐛 Báo lỗi", command=self.app.bao_loi)

    def tao_thanh_congcu(self):
        toolbar = ctk.CTkFrame(self.root, height=40)
        toolbar.pack(fill=tk.X, padx=5, pady=2)
        
        # Nút thêm giao dịch nhanh
        ctk.CTkButton(toolbar, text="➕ Giao dịch mới", 
                     command=lambda: self.tao_cua_so_them_giao_dich()).pack(side=tk.LEFT, padx=5)
        
        # Nút chuyển đổi theme
        ctk.CTkButton(toolbar, text="🌓 Đổi theme", 
                     command=self.app.doi_theme).pack(side=tk.LEFT, padx=5)
        
        # Nút xuất báo cáo
        ctk.CTkButton(toolbar, text="📊 Xuất báo cáo", 
                     command=self.app.bao_cao.xem_baocao).pack(side=tk.LEFT, padx=5)
        
        # Nút nhập/sửa ngân sách
        ctk.CTkButton(toolbar, text="💸 Ngân sách", 
                     command=self.app.nhap_sua_ngansach).pack(side=tk.LEFT, padx=5)
        
        # Nút chatbot AI (đặt bên cạnh nút cài đặt)
        ctk.CTkButton(toolbar, text="🤖 Trò chuyện AI", 
                     command=self.app.mo_chatbot).pack(side=tk.RIGHT, padx=5)

        # Nút cài đặt
        ctk.CTkButton(toolbar, text="⚙️ Cài đặt", 
                     command=self.app.mo_caidat).pack(side=tk.RIGHT, padx=5)

    def tao_cua_so_them_giao_dich(self, transaction_type=None):
        """Tạo cửa sổ thêm giao dịch mới"""
        window = ctk.CTkToplevel(self.root)
        window.title("Thêm Giao Dịch")
        window.geometry("600x700")
        window.transient(self.root)
        window.grab_set()
        window.focus_force()

        # Configure grid for the window to allow input_frame to expand
        window.grid_columnconfigure(0, weight=1)
        window.grid_rowconfigure(0, weight=1) 

        # Frame chứa các trường nhập liệu
        input_frame = ctk.CTkFrame(window)
        input_frame.grid(row=0, column=0, pady=10, padx=10, sticky="nsew")

        # Configure grid for input_frame content
        input_frame.grid_columnconfigure(1, weight=1) # Make the input column expandable

        row_idx = 0

        # Ngày (mặc định là ngày hiện tại)
        ctk.CTkLabel(input_frame, text="Ngày:").grid(row=row_idx, column=0, pady=5, padx=10, sticky="w")
        date_entry = ctk.CTkEntry(input_frame)
        date_entry.insert(0, datetime.now().strftime("%d/%m/%Y"))
        date_entry.grid(row=row_idx, column=1, pady=5, padx=10, sticky="ew")
        row_idx += 1
        
        # Loại (Thu/Chi)
        ctk.CTkLabel(input_frame, text="Loại:").grid(row=row_idx, column=0, pady=5, padx=10, sticky="w")

        # Biến thực tế
        type_var = ctk.StringVar(value=transaction_type if transaction_type else "expense")

        # Danh sách hiển thị và ánh xạ
        value_to_display = {
            "income": "income (thu)",
            "expense": "expense (chi)"
        }
        display_to_value = {v: k for k, v in value_to_display.items()}
        display_values = list(display_to_value.keys())

        # Tìm giá trị hiển thị ban đầu
        initial_display_value = value_to_display[type_var.get()]

        # Biến hiển thị
        type_display_var = ctk.StringVar(value=initial_display_value)

        # Hàm cập nhật biến thực tế khi chọn
        def on_type_selected(choice):
            type_var.set(display_to_value[choice])

        # Tạo OptionMenu
        type_optionmenu = ctk.CTkOptionMenu(
            input_frame,
            variable=type_display_var,
            values=display_values,
            command=on_type_selected
        )
        type_optionmenu.grid(row=row_idx, column=1, pady=5, padx=10, sticky="ew")

        row_idx += 1

        
        # Số tiền
        ctk.CTkLabel(input_frame, text="Số tiền:").grid(row=row_idx, column=0, pady=5, padx=10, sticky="w")
        amount_entry = ctk.CTkEntry(input_frame)
        amount_entry.grid(row=row_idx, column=1, pady=5, padx=10, sticky="ew")
        row_idx += 1
        
        # Danh mục
        ctk.CTkLabel(input_frame, text="Danh mục:").grid(row=row_idx, column=0, pady=5, padx=10, sticky="w")
        category_combobox = ctk.CTkComboBox(input_frame, values=self.app.categories[type_var.get()])
        category_combobox.grid(row=row_idx, column=1, pady=5, padx=10, sticky="ew")
        row_idx += 1
        
        # Cập nhật danh mục khi loại thay đổi
        def update_categories(*args):
            category_combobox.configure(values=self.app.categories[type_var.get()])
            category_combobox.set("") # Clear selected category
            
        type_var.trace_add("write", update_categories)

        # Ghi chú
        ctk.CTkLabel(input_frame, text="Ghi chú:").grid(row=row_idx, column=0, pady=5, padx=10, sticky="w")
        note_entry = ctk.CTkEntry(input_frame)
        note_entry.grid(row=row_idx, column=1, pady=5, padx=10, sticky="ew")
        row_idx += 1

        def add_transaction():
            try:
                date_str = date_entry.get()
                # Validate date format
                datetime.strptime(date_str, "%d/%m/%Y") 

                transaction = {
                    'date': date_str,
                    'type': type_var.get(),
                    'amount': float(amount_entry.get()),
                    'category': category_combobox.get(),
                    'note': note_entry.get()
                }
                self.app.transactions.append(transaction)
                self.app.xu_ly_du_lieu.save_database()
                self.app.update_financial_summary()
                self.app.update_category_stats()
                self.app.xu_ly_du_lieu.load_transaction_data() # Cập nhật bảng hiển thị
                window.destroy()
            except ValueError as ve:
                 messagebox.showerror("Lỗi", f"Định dạng ngày hoặc số tiền không hợp lệ: {str(ve)}")
            except Exception as e:
                messagebox.showerror("Lỗi", f"Không thể thêm giao dịch: {str(e)}")

        # Nút Thêm
        add_button = ctk.CTkButton(window, text="Thêm", command=add_transaction)
        add_button.grid(row=1, column=0, pady=10) # Place it in the window's grid, below input_frame

    def tao_layout_chinh(self):
        # Tạo layout 3 cột
        left_frame = ctk.CTkFrame(self.main_frame, width=400)
        left_frame.pack(side=tk.LEFT, fill=tk.Y, padx=5, pady=5)
        
        center_frame = ctk.CTkFrame(self.main_frame)
        center_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        right_frame = ctk.CTkFrame(self.main_frame, width=400)
        right_frame.pack(side=tk.LEFT, fill=tk.Y, padx=5, pady=5)
        
        # Cột trái - Thông tin tổng quan
        self.tao_thongtin_tongquan(left_frame)
        
        # Cột giữa - Danh sách giao dịch và biểu đồ
        # Tạo frame cho danh sách giao dịch
        transaction_list_frame = ctk.CTkFrame(center_frame)
        transaction_list_frame.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        self.tao_danhsach_giaodich(transaction_list_frame)

        # Tạo frame riêng cho các biểu đồ trong cột giữa
        chart_display_frame = ctk.CTkFrame(center_frame)
        chart_display_frame.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        # Tạo frame cho biểu đồ tròn bên trái trong chart_display_frame
        self.pie_chart_frame = ctk.CTkFrame(left_frame)
        self.pie_chart_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=5)
        
        # Tạo frame cho biểu đồ xu hướng bên phải trong chart_display_frame
        self.trend_chart_frame = ctk.CTkFrame(chart_display_frame)
        self.trend_chart_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=5)
        
        # Thêm frame chứa nút cho biểu đồ
        chart_buttons_frame = ctk.CTkFrame(self.trend_chart_frame)
        chart_buttons_frame.pack(fill=tk.X, pady=5)

        # Nút cập nhật biểu đồ
        ctk.CTkButton(chart_buttons_frame, text="🔄 Cập nhật biểu đồ",
                     command=self.app.update_charts).pack(side=tk.LEFT, padx=5)

        # Cột phải - Nhắc nhở và thống kê
        self.tao_nhacnho_thongke(right_frame)

    def tao_thongtin_tongquan(self, parent):
        # Tiêu đề
        ctk.CTkLabel(parent, text="     Tổng quan tài chính     ", 
                    font=("Arial", 27, "bold")).pack(pady=10)
        
        # Thông tin số dư
        balance_frame = ctk.CTkFrame(parent)
        balance_frame.pack(fill=tk.X, padx=5, pady=5)
        
        ctk.CTkLabel(balance_frame, text="Số dư hiện tại:").pack()
        self.balance_label = ctk.CTkLabel(balance_frame, text="0 VNĐ", 
                                        font=("Arial", 20, "bold"))
        self.balance_label.pack()
        
        # Thông tin thu chi tháng
        month_frame = ctk.CTkFrame(parent)
        month_frame.pack(fill=tk.X, padx=5, pady=5)
        
        ctk.CTkLabel(month_frame, text="Tháng này:").pack()
        self.income_month_label = ctk.CTkLabel(month_frame, text="Thu: 0 VNĐ")
        self.income_month_label.pack()
        self.expense_month_label = ctk.CTkLabel(month_frame, text="Chi: 0 VNĐ")
        self.expense_month_label.pack()
        
        # Thông tin ngân sách
        budget_frame = ctk.CTkFrame(parent)
        budget_frame.pack(fill=tk.X, padx=5, pady=5)
        
        ctk.CTkLabel(budget_frame, text="Ngân sách tháng:").pack()
        self.budget_label = ctk.CTkLabel(budget_frame, text="0 VNĐ", font=("Arial", 16, "bold"))
        self.budget_label.pack()
        
        self.budget_current_amount_label = ctk.CTkLabel(budget_frame, text="Đã chi: 0 VNĐ", font=("Arial", 14))
        self.budget_current_amount_label.pack()

        self.budget_progress = ctk.CTkProgressBar(budget_frame, fg_color="gray", progress_color="#28a745")
        self.budget_progress.pack(fill=tk.X, padx=5, pady=5)
        self.budget_progress.set(0)
        
        # Thêm nút cập nhật
        ctk.CTkButton(month_frame, text="🔄 Cập nhật", 
                     command=self.app.update_financial_summary).pack(pady=5)
        
        # Removed chart frame from here - charts will be in center_frame

    def tao_danhsach_giaodich(self, parent):
        # Thanh tìm kiếm và lọc
        filter_frame = ctk.CTkFrame(parent)
        filter_frame.pack(fill=tk.X, padx=5, pady=5)
        
        ctk.CTkLabel(filter_frame, text=" ").pack(side=tk.LEFT, padx=5)
        self.search_entry = ctk.CTkEntry(filter_frame, width=100)
        self.search_entry.pack(side=tk.LEFT, fill=tk.X, padx=5)
        
        ctk.CTkLabel(filter_frame, text=" ").pack(side=tk.LEFT, padx=5)
        self.type_var = ctk.StringVar(value="Loại")
        type_combo = ctk.CTkComboBox(filter_frame, values=["Tất cả", "Thu", "Chi"], variable=self.type_var)
        type_combo.pack(side=tk.LEFT, padx=5)
        
        ctk.CTkLabel(filter_frame, text=" ").pack(side=tk.LEFT, padx=5)
        self.category_var = ctk.StringVar(value="Danh mục")
        category_combo = ctk.CTkComboBox(filter_frame, values=["Tất cả"] + self.app.categories['income'] + self.app.categories['expense'], variable=self.category_var)
        category_combo.pack(side=tk.LEFT, padx=5)
        
        # Khoảng ngày - Thay thế bằng nút lịch
        ctk.CTkLabel(filter_frame, text="Ngày:").pack(side=tk.LEFT, padx=5)
        self.date_range_label = ctk.CTkLabel(filter_frame, text="Tất cả các ngày")
        self.date_range_label.pack(side=tk.LEFT, padx=5)
        
        self.calendar_button = ctk.CTkButton(filter_frame, text="🗓️", width=10, 
                                           command=self.open_calendar_selector)
        self.calendar_button.pack(side=tk.LEFT, padx=5)
        
        # Tạo lại các entry ngày nhưng ẩn đi để lưu trữ giá trị cho hàm tìm kiếm
        self.start_date_entry = ctk.CTkEntry(filter_frame)
        self.start_date_entry.pack_forget()
        self.end_date_entry = ctk.CTkEntry(filter_frame)
        self.end_date_entry.pack_forget()
        
        # Nút tìm kiếm
        ctk.CTkButton(filter_frame, text="Tìm kiếm", command=self.tim_kiem_nang_cao).pack(side=tk.LEFT, padx=5)
        
        # Frame cho bảng giao dịch
        table_frame = ctk.CTkFrame(parent)
        table_frame.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        # Tạo bảng giao dịch
        columns = ("Ngày", "Loại", "Danh mục", "Số tiền", "Ghi chú")
        self.tree = ttk.Treeview(table_frame, columns=columns, show="headings")
        
        # Định dạng cột
        for col in columns:
            self.tree.heading(col, text=col)
            self.tree.column(col, width=100)
        
        # Thêm thanh cuộn
        scrollbar = ttk.Scrollbar(table_frame, orient=tk.VERTICAL, command=self.tree.yview)
        self.tree.configure(yscrollcommand=scrollbar.set)
        
        # Sắp xếp layout
        self.tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        # Tạo menu chuột phải
        self.tao_menu_chuotphai()
        self.tree.bind("<Button-3>", self.show_context_menu)
        
        def update_transaction_list(*args):
            search_text = self.search_entry.get().lower()
            type_filter = self.type_var.get()
            category_filter = self.category_var.get()
            
            filtered_transactions = []
            for transaction in self.app.transactions:
                if type_filter != "Tất cả":
                    mapped_type = "Thu" if transaction['type'] == 'income' else "Chi"
                    if mapped_type != type_filter:
                        continue
                if category_filter != "Tất cả" and transaction['category'] != category_filter:
                    continue
                if search_text and search_text not in transaction['note'].lower():
                    continue
                filtered_transactions.append(transaction)
            
            self.update_transaction_table(filtered_transactions)
        
        # Gắn sự kiện cập nhật
        self.search_entry.bind("<KeyRelease>", update_transaction_list)
        self.type_var.trace_add("write", update_transaction_list)
        self.category_var.trace_add("write", update_transaction_list)
        
        # Cập nhật lần đầu
        update_transaction_list()

    def tao_bang_giaodich(self, parent):
        # Tạo frame cho bảng
        table_frame = ctk.CTkFrame(parent)
        table_frame.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        # Tạo Treeview
        columns = ("Ngày", "Loại", "Danh mục", "Số tiền", "Ghi chú")
        self.tree = ttk.Treeview(table_frame, columns=columns, show="headings")
        
        # Định dạng cột
        for col in columns:
            self.tree.heading(col, text=col)
            self.tree.column(col, width=100)
        
        # Thêm thanh cuộn
        scrollbar = ttk.Scrollbar(table_frame, orient=tk.VERTICAL, command=self.tree.yview)
        self.tree.configure(yscrollcommand=scrollbar.set)
        
        # Đặt vị trí
        self.tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        # Tạo menu chuột phải
        self.tao_menu_chuotphai()
        
        # Load dữ liệu
        # Loading data will be handled after UI and charts are ready

    def tao_menu_chuotphai(self):
        self.context_menu = Menu(self.tree, tearoff=0)
        self.context_menu.add_command(label="✏️ Sửa", command=self.app.xu_ly_du_lieu.sua_giaodich)
        self.context_menu.add_command(label="🗑️ Xóa", command=self.app.xu_ly_du_lieu.xoa_giaodich)
        self.context_menu.add_command(label="📋 Sao chép", command=self.app.xu_ly_du_lieu.sao_chep_giaodich)
        
        self.tree.bind("<Button-3>", self.show_context_menu)

    def show_context_menu(self, event):
        try:
            self.tree.selection()
            self.context_menu.tk_popup(event.x_root, event.y_root)
        finally:
            self.context_menu.grab_release()

    def update_transaction_table(self, transactions):
        # Xóa tất cả các mục hiện có
        for item in self.tree.get_children():
            self.tree.delete(item)
        
        # Chèn các giao dịch đã lọc
        for transaction in transactions:
            self.tree.insert("", tk.END, values=(
                transaction.get('date', ''),
                "Thu" if transaction.get('type') == 'income' else "Chi",
                transaction.get('category', ''),
                f"{transaction.get('amount', 0):,.0f}",
                transaction.get('note', '')
            ))

    def tao_nhacnho_thongke(self, parent):
        # Tiêu đề
        ctk.CTkLabel(parent, text="  Nhắc nhở & Thống kê  ", 
                    font=("Arial", 27, "bold")).pack(pady=10)
        
        # Frame nhắc nhở
        reminder_frame = ctk.CTkFrame(parent)
        reminder_frame.pack(fill=tk.X, padx=5, pady=5)
        
        ctk.CTkLabel(reminder_frame, text="Nhắc nhở:", font=("Arial", 16, "bold")).pack()
        self.reminder_list = ctk.CTkTextbox(reminder_frame, height=150, font=("Arial", 12))
        self.reminder_list.pack(fill=tk.X, padx=5, pady=5)
        
        # Frame thống kê
        stats_frame = ctk.CTkFrame(parent)
        stats_frame.pack(fill=tk.X, padx=5, pady=5)
        
        ctk.CTkLabel(stats_frame, text="Thống kê:", font=("Arial", 16, "bold")).pack()
        self.stats_list = ctk.CTkTextbox(stats_frame, height=350, font=("Arial", 12))
        self.stats_list.pack(fill=tk.X, padx=5, pady=5)

        # Nút cập nhật cho phần Nhắc nhở & Thống kê
        ctk.CTkButton(parent, text="🔄 Cập nhật", 
                     command=lambda: [self.update_reminders(), self.update_stats()]).pack(pady=10)

        # Cập nhật dữ liệu ban đầu cho thống kê và nhắc nhở
        self.update_reminders()
        self.update_stats()

    def update_reminders(self):
        try:
            self.reminder_list.delete("1.0", tk.END)
            
            # Add existing reminders
            for reminder in self.app.reminders:
                # Display all reminders regardless of notified status
                self.reminder_list.insert(tk.END, f"• {reminder.get('title', '')} - {reminder.get('content', '')} ({reminder.get('datetime', '')})\n")

            current_date = datetime.now()

            # Check for overdue goals and goals approaching deadline
            for goal in self.app.goals:
                try:
                    deadline_str = goal.get('deadline', '')
                    if not deadline_str:
                        continue

                    deadline = datetime.strptime(deadline_str, "%d/%m/%Y")
                    title = goal.get('title', '')
                    is_completed = goal.get('completed', False)

                    if not is_completed:
                        if deadline < current_date:
                            self.reminder_list.insert(tk.END, f"• Mục tiêu quá hạn: {title} (Hạn: {deadline_str})\n")
                        elif (deadline - current_date).days <= 7:
                            self.reminder_list.insert(tk.END, f"• Mục tiêu sắp đến hạn: {title} (Còn {(deadline - current_date).days} ngày)\n")
                except Exception as e:
                    print(f"Lỗi khi kiểm tra mục tiêu cho nhắc nhở: {title} - {e}")
                    continue

            # Check for budget exceeded
            budget_limit = self.app.settings.get('budget_limit', 0)
            if budget_limit > 0:
                total_expense_this_month = sum(t['amount'] for t in self.app.transactions
                                               if t['type'] == 'expense' and 
                                               datetime.strptime(t['date'], "%d/%m/%Y").strftime("%Y-%m") == current_date.strftime("%Y-%m"))
                
                if total_expense_this_month > budget_limit:
                    self.reminder_list.insert(tk.END, f"• Ngân sách tháng đã vượt quá: {total_expense_this_month:,.0f}/{budget_limit:,.0f} VNĐ\n")

            # If no reminders (after adding actual reminders and goals/budget alerts), show a default message
            if self.reminder_list.get("1.0", tk.END).strip() == "":
                self.reminder_list.insert(tk.END, "Cập nhật để dữ liệu luôn chính xác nhất ✅\nXem hướng dẫn trong phần trợ giúp!\nCảm ơn sử dụng chương trình (●'◡'●)\nChúc bạn một ngày tốt lành!\n\n\nNHÓM 8\nTác giả: Lê Trọng Chiến.\nHỗ trợ: Nguyễn Hữu Dũng.\n")
        except Exception as e:
            print(f"Lỗi khi cập nhật nhắc nhở: {e}")
            self.reminder_list.delete("1.0", tk.END)
            self.reminder_list.insert(tk.END, f"Lỗi khi cập nhật nhắc nhở: {e}\n")

    def update_stats(self):
        # Cập nhật thống kê
        self.stats_list.delete("1.0", tk.END)
        
        # Tính toán thống kê tổng quan
        total_income = sum(t['amount'] for t in self.app.transactions if t['type'] == 'income')
        total_expense = sum(t['amount'] for t in self.app.transactions if t['type'] == 'expense')
        balance = total_income - total_expense
        total_transactions = len(self.app.transactions)
        
        # Thống kê theo loại giao dịch
        income_count = len([t for t in self.app.transactions if t['type'] == 'income'])
        expense_count = len([t for t in self.app.transactions if t['type'] == 'expense'])
        
        # Thống kê theo danh mục
        categories = {}
        for t in self.app.transactions:
            cat = t.get('category', 'Không phân loại')
            if cat not in categories:
                categories[cat] = {'income': 0, 'expense': 0, 'count': 0}
            categories[cat][t['type']] += t['amount']
            categories[cat]['count'] += 1
        
        # Hiển thị thống kê tổng quan
        self.stats_list.insert(tk.END, "=== THỐNG KÊ TỔNG QUAN ===\n\n")
        self.stats_list.insert(tk.END, f"Tổng thu: {total_income:,.0f} VNĐ ({income_count} giao dịch)\n")
        self.stats_list.insert(tk.END, f"Tổng chi: {total_expense:,.0f} VNĐ ({expense_count} giao dịch)\n")
        self.stats_list.insert(tk.END, f"Số dư: {balance:,.0f} VNĐ\n")
        self.stats_list.insert(tk.END, f"Tổng số giao dịch: {total_transactions}\n\n")
        
        # Hiển thị thống kê theo danh mục
        self.stats_list.insert(tk.END, "=== THỐNG KÊ THEO DANH MỤC ===\n\n")
        for cat, stats in categories.items():
            self.stats_list.insert(tk.END, f"{cat}:\n")
            self.stats_list.insert(tk.END, f"  - Số giao dịch: {stats['count']}\n")
            if stats['income'] > 0:
                self.stats_list.insert(tk.END, f"  - Thu: {stats['income']:,.0f} VNĐ\n")
            if stats['expense'] > 0:
                self.stats_list.insert(tk.END, f"  - Chi: {stats['expense']:,.0f} VNĐ\n")
            self.stats_list.insert(tk.END, "\n")

    def update_summary(self, total_income, total_expense, balance):
        # Cập nhật thông tin tổng quan
        self.balance_label.configure(text=f"{balance:,.0f} VNĐ")
        self.income_month_label.configure(text=f"Thu: {total_income:,.0f} VNĐ")
        self.expense_month_label.configure(text=f"Chi: {total_expense:,.0f} VNĐ")

    def update_category_stats(self, category_stats):
        # Cập nhật thống kê theo danh mục
        self.stats_list.delete("1.0", tk.END)
        for category, stats in category_stats.iterrows():
            self.stats_list.insert(tk.END, 
                f"{category}: {stats['sum']:,.0f} VNĐ ({stats['count']} giao dịch)\n")

    def update_colors(self, colors):
        # Cập nhật màu sắc cho các thành phần UI
        self.root.configure(bg=colors['bg'])
        self.main_frame.configure(fg_color=colors['bg'])
        
        # Cập nhật màu cho các label
        for widget in self.root.winfo_children():
            if isinstance(widget, ctk.CTkLabel):
                widget.configure(text_color=colors['fg'])
        
        # Cập nhật màu cho các button
        for widget in self.root.winfo_children():
            if isinstance(widget, ctk.CTkButton):
                widget.configure(fg_color=colors['accent'])

    def update_charts(self):
        # Code cập nhật biểu đồ
        pass

    def auto_backup_service(self):
        # Code dịch vụ sao lưu tự động
        pass

    def notification_service(self):
        # Code dịch vụ thông báo
        pass

    def open_calendar_selector(self):
        # Tạo cửa sổ chọn ngày
        calendar_window = ctk.CTkToplevel(self.app.root)
        calendar_window.title("Chọn khoảng ngày")
        calendar_window.geometry("350x400")
        calendar_window.transient(self.app.root)
        calendar_window.grab_set()
        calendar_window.focus_force()

        cal = Calendar(calendar_window, selectmode='day', date_pattern='yyyy-mm-dd')
        cal.pack(pady=20, fill=tk.BOTH, expand=True)

        selected_start_date = None
        selected_end_date = None

        def on_date_select():
            nonlocal selected_start_date, selected_end_date
            selected_date = cal.selection_get()
            if not selected_start_date:
                selected_start_date = selected_date
                cal.selection_set(selected_date) # Select the start date visually
                messagebox.showinfo("Chọn ngày", f"Đã chọn ngày bắt đầu: {selected_start_date}. Vui lòng chọn ngày kết thúc.")
            elif not selected_end_date and selected_date >= selected_start_date:
                selected_end_date = selected_date
                messagebox.showinfo("Chọn ngày", f"Khoảng ngày đã chọn: {selected_start_date} đến {selected_end_date}")
                self.date_range_label.configure(text=f"{selected_start_date} đến {selected_end_date}")
                # Cập nhật các entry ẩn cho hàm tìm kiếm
                self.start_date_entry.delete(0, tk.END)
                self.start_date_entry.insert(0, selected_start_date.strftime("%Y-%m-%d"))
                self.end_date_entry.delete(0, tk.END)
                self.end_date_entry.insert(0, selected_end_date.strftime("%Y-%m-%d"))
                calendar_window.destroy()
            elif selected_date < selected_start_date:
                messagebox.showwarning("Cảnh báo", "Ngày kết thúc không thể nhỏ hơn ngày bắt đầu. Vui lòng chọn lại ngày kết thúc.")
            else:
                # Reset selection if picking a third date
                selected_start_date = selected_date
                selected_end_date = None
                cal.selection_set(selected_date)
                messagebox.showinfo("Chọn ngày", f"Đã chọn ngày bắt đầu mới: {selected_start_date}. Vui lòng chọn ngày kết thúc.")

        def on_cancel():
            # Khi hủy, đặt lại về "Tất cả các ngày" và xóa giá trị trong các entry ẩn
            self.date_range_label.configure(text="Tất cả các ngày")
            self.start_date_entry.delete(0, tk.END)
            self.end_date_entry.delete(0, tk.END)
            calendar_window.destroy()

        cal.bind("<<CalendarSelected>>", lambda e: on_date_select())
        # Note: tkcalendar does not have a direct 'select range' mode. We implement it manually.
        # The user clicks once for start_date, and a second time for end_date.

        # Nút xác nhận và hủy
        button_frame = ctk.CTkFrame(calendar_window)
        button_frame.pack(pady=10)

        ctk.CTkButton(button_frame, text="OK", command=on_date_select).pack(side=tk.LEFT, padx=5)
        ctk.CTkButton(button_frame, text="Hủy", command=on_cancel).pack(side=tk.LEFT, padx=5)

    def update_budget_display(self, budget_limit, total_expense):
        self.budget_label.configure(text=f"Ngân sách tháng: {budget_limit:,.0f} VNĐ")
        self.budget_current_amount_label.configure(text=f"Đã chi: {total_expense:,.0f} VNĐ")

        if budget_limit > 0:
            progress = total_expense / budget_limit
            self.budget_progress.set(min(progress, 1)) # Giới hạn tiến độ ở 100%
            if total_expense > budget_limit:
                self.budget_progress.configure(progress_color="#dc3545") # Màu đỏ khi vượt ngân sách
            else:
                self.budget_progress.configure(progress_color="#28a745") # Màu xanh khi trong ngân sách
        else:
            self.budget_progress.set(0)
            self.budget_progress.configure(progress_color="#28a745") # Mặc định màu xanh 

    def tao_thanh_trangthai(self):
        # Tạo thanh trạng thái
        self.status_bar = ctk.CTkFrame(self.root, height=20)
        self.status_bar.pack(fill=tk.X, side=tk.BOTTOM)
        
        # Thời gian
        self.time_label = ctk.CTkLabel(self.status_bar, text="")
        self.time_label.pack(side=tk.RIGHT, padx=5)
        
        # Trạng thái
        device_name = platform.node()
        self.status_label = ctk.CTkLabel(self.status_bar, text=f"Thiết bị: {device_name} ✅")
        self.status_label.pack(side=tk.LEFT, padx=5)
        
        # Cập nhật thời gian
        self.update_time()

    def update_time(self):
        # Cập nhật thời gian
        current_time = datetime.now().strftime("%H:%M:%S")
        self.time_label.configure(text=current_time)
        self.root.after(1000, self.update_time) 

    def _select_backup_file_and_restore(self):
        backup_file = filedialog.askopenfilename(
            title="Chọn tệp sao lưu để khôi phục",
            filetypes=[("JSON files", "*.json"), ("ZIP files", "*.zip"), ("All files", "*.*")]
        )
        if backup_file:
            self.app.xu_ly_du_lieu.restore_database(backup_file) 

    def tim_kiem_nang_cao(self):
        """Tìm kiếm giao dịch với nhiều điều kiện"""
        try:
            # Lấy các điều kiện tìm kiếm
            keyword = self.search_entry.get().lower()
            type_filter = self.type_var.get()
            category_filter = self.category_var.get()
            start_date_str = self.start_date_entry.get()
            end_date_str = self.end_date_entry.get()
            
            # Chuyển đổi ngày
            start_date = None
            if start_date_str:
                try:
                    start_date = datetime.strptime(start_date_str, "%Y-%m-%d")
                except ValueError:
                    messagebox.showwarning("Lỗi", "Định dạng 'Từ ngày' không hợp lệ. Vui lòng sử dụng YYYY-MM-DD (VD: 2024-01-31).")
                    return
            
            end_date = None
            if end_date_str:
                try:
                    end_date = datetime.strptime(end_date_str, "%Y-%m-%d")
                except ValueError:
                    messagebox.showwarning("Lỗi", "Định dạng 'Đến ngày' không hợp lệ. Vui lòng sử dụng YYYY-MM-DD (VD: 2024-01-31).")
                    return
            
            # Thực hiện tìm kiếm
            filtered_transactions = self.app.xu_ly_du_lieu.tim_kiem_nang_cao(
                keyword=keyword,
                start_date=start_date,
                end_date=end_date,
                category=category_filter if category_filter != "Tất cả" else None,
                type_filter=type_filter if type_filter != "Tất cả" else None
            )
            
            # Cập nhật bảng giao dịch
            self.update_transaction_table(filtered_transactions)
            
        except Exception as e:
            messagebox.showerror("Lỗi", f"Không thể thực hiện tìm kiếm: {str(e)}") 