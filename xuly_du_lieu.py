import json
import pandas as pd
from datetime import datetime
import os
import shutil
import zipfile
import customtkinter as ctk
from tkinter import messagebox, filedialog
import numpy as np
import random
from datetime import timedelta

class XuLyDuLieu:
    def __init__(self, app):
        self.app = app
        self.db_file = "database.json"
        self.backup_dir = "backups"
        self.load_database()
        
    def load_database(self):
        """Load dữ liệu từ file database.json"""
        try:
            # Khởi tạo các biến mặc định
            default_categories = {
                'income': ['Lương', 'Thưởng', 'Đầu tư', 'Khác'],
                'expense': ['Ăn uống', 'Di chuyển', 'Mua sắm', 'Giải trí', 'Khác']
            }
            default_settings = {
                'currency': 'VND',
                'language': 'vi',
                'theme': 'light',
                'auto_backup': True,
                'backup_interval': 24,
                'last_backup': None,
                'notify_expense': True,
                'notify_budget': True,
                'budget_limit': 10000000
            }
            self.app.transactions = []
            self.app.categories = default_categories
            self.app.settings = default_settings
            self.app.goals = []
            self.app.reminders = []

            database_exists = os.path.exists(self.db_file)

            if database_exists:
                with open(self.db_file, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    
                    # Tải transactions
                    transactions_data = data.get('transactions', [])
                    if isinstance(transactions_data, list):
                        self.app.transactions = transactions_data
                    elif isinstance(transactions_data, dict):
                        for income in transactions_data.get('income', []):
                            try:
                                date_obj = datetime.strptime(income['date'], "%Y-%m-%d")
                                formatted_date = date_obj.strftime("%d/%m/%Y")
                                self.app.transactions.append({
                                    'date': formatted_date,
                                    'type': 'income',
                                    'amount': float(income['amount']),
                                    'category': income.get('category', 'Không xác định'),
                                    'note': income.get('description', '')
                                })
                            except Exception as e:
                                print(f"Lỗi khi xử lý thu nhập: {str(e)}")
                                continue
                        for expense in transactions_data.get('expenses', []):
                            try:
                                date_obj = datetime.strptime(expense['date'], "%Y-%m-%d")
                                formatted_date = date_obj.strftime("%d/%m/%Y")
                                self.app.transactions.append({
                                    'date': formatted_date,
                                    'type': 'expense',
                                    'amount': float(expense['amount']),
                                    'category': expense.get('category', 'Không xác định'),
                                    'note': expense.get('description', '')
                                })
                            except Exception as e:
                                print(f"Lỗi khi xử lý chi tiêu: {str(e)}")
                                continue
                    
                    # Tải categories
                    loaded_categories = data.get('categories', {})
                    if isinstance(loaded_categories, dict):
                        self.app.categories = {
                            'income': loaded_categories.get('income', default_categories['income']),
                            'expense': loaded_categories.get('expense', default_categories['expense'])
                        }
                    else:
                        self.app.categories = default_categories
                    
                    # Tải settings
                    loaded_settings = data.get('settings', {})
                    self.app.settings = {**default_settings, **loaded_settings}
                    
                    # Tải goals
                    for goal in data.get('goals', []):
                        try:
                            if 'deadline' not in goal or not goal['deadline']:
                                goal['deadline'] = datetime.now().strftime("%d/%m/%Y")
                                print(f"DEBUG: Thêm khóa 'deadline' mặc định cho mục tiêu: {goal.get('name', 'Không tên')}")
                            datetime.strptime(goal['deadline'], "%d/%m/%Y")
                            if 'completed' not in goal:
                                goal['completed'] = False
                            if 'amount' not in goal:
                                goal['amount'] = 0.0
                            self.app.goals.append(goal)
                        except Exception as e:
                            print(f"Lỗi khi xử lý mục tiêu: {goal.get('name', 'Không tên')} - {str(e)}")
                            continue
                    
                    # Tải reminders
                    for reminder in data.get('reminders', []):
                        try:
                            if 'title' not in reminder or not reminder['title']:
                                reminder['title'] = "Nhắc nhở không tiêu đề"
                            if 'content' not in reminder or not reminder['content']:
                                reminder['content'] = "Nội dung trống"

                            if 'datetime' not in reminder or not reminder['datetime']:
                                if 'date' in reminder and 'time' in reminder:
                                    reminder['datetime'] = f"{reminder['date']} {reminder['time']}"
                                else:
                                    reminder['datetime'] = datetime.now().strftime("%Y-%m-%d %H:%M")
                                print(f"DEBUG: Thêm khóa 'datetime' mặc định cho nhắc nhở: {reminder.get('title', 'Không tên')}")
                            if 'notified' not in reminder:
                                reminder['notified'] = False
                            if 'id' not in reminder:
                                reminder['id'] = len(self.app.reminders) + 1
                            self.app.reminders.append(reminder)
                        except Exception as e:
                            print(f"Lỗi khi xử lý nhắc nhở: {reminder.get('title', 'Không tên')} - {str(e)}")
                            continue
            
            # Nếu không có nhắc nhở nào sau khi tải hoặc mặc định, thêm một cái
            if not self.app.reminders:
                self.app.reminders.append({
                    "id": 1,
                    "title": "Chào mừng bạn đến với ứng dụng!",
                    "content": "Hãy thêm nhắc nhở đầu tiên của bạn.",
                    "date": datetime.now().strftime("%Y-%m-%d"),
                    "time": datetime.now().strftime("%H:%M"),
                    "datetime": datetime.now().strftime("%Y-%m-%d %H:%M"),
                    "notified": False
                })
                print("DEBUG: Đã thêm nhắc nhở mặc định vì không có nhắc nhở nào được tải.")
            
            # Luôn lưu database nếu nó mới được tạo hoặc dữ liệu đã được sửa đổi (ví dụ: thêm nhắc nhở mặc định)
            if not database_exists or not self.app.reminders or not self.app.transactions:
                self.save_database() # Lưu lại dữ liệu mặc định/đã thêm

        except Exception as e:
            print(f"Lỗi khi tải database: {str(e)}")
            # Trong trường hợp có lỗi nghiêm trọng, đảm bảo các danh sách vẫn được khởi tạo rỗng
            self.app.transactions = []
            self.app.categories = default_categories # Sử dụng lại default_categories đã định nghĩa
            self.app.settings = default_settings # Sử dụng lại default_settings đã định nghĩa
            self.app.goals = []
            self.app.reminders = []

    def save_database(self):
        try:
            # Đảm bảo thư mục của database tồn tại
            db_dir = os.path.dirname(self.db_file)
            if db_dir and not os.path.exists(db_dir):
                os.makedirs(db_dir)

            # Chuyển đổi transactions từ list sang dict
            transactions_dict = {
                'income': [],
                'expenses': []  # Giữ nguyên key 'expenses' để tương thích với file cũ
            }
            for transaction in self.app.transactions:
                try:
                    # Chuyển đổi định dạng ngày từ DD/MM/YYYY sang YYYY-MM-DD
                    date_obj = datetime.strptime(transaction['date'], "%d/%m/%Y")
                    formatted_date = date_obj.strftime("%Y-%m-%d")
                    
                    if transaction['type'] == 'income':
                        transactions_dict['income'].append({
                            'date': formatted_date,
                            'amount': float(transaction['amount']),
                            'category': transaction['category'],
                            'description': transaction['note']
                        })
                    elif transaction['type'] == 'expense':
                        transactions_dict['expenses'].append({
                            'date': formatted_date,
                            'amount': float(transaction['amount']),
                            'category': transaction['category'],
                            'description': transaction['note']
                        })
                except Exception as e:
                    print(f"Lỗi khi xử lý giao dịch: {str(e)}")
                    continue

            data = {
                'transactions': transactions_dict,
                'categories': {
                    'income': self.app.categories['income'],
                    'expense': self.app.categories['expense']  # Giữ key 'expense' trong categories
                },
                'settings': self.app.settings,
                'goals': self.app.goals,
                'reminders': self.app.reminders
            }
            with open(self.db_file, 'w', encoding='utf-8') as f:
                json.dump(data, f, ensure_ascii=False, indent=4)
            
            # Cập nhật nhắc nhở trên giao diện chính sau khi lưu database, nếu giao diện đã được khởi tạo
            if self.app.giao_dien:
                self.app.giao_dien.update_reminders()
        except Exception as e:
            print(f"Lỗi khi lưu database: {str(e)}")

    def backup_database(self):
        try:
            if not os.path.exists(self.backup_dir):
                os.makedirs(self.backup_dir)
            
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            backup_file = os.path.join(self.backup_dir, f"backup_{timestamp}.zip")
            
            with zipfile.ZipFile(backup_file, 'w') as zipf:
                zipf.write(self.db_file, os.path.basename(self.db_file))
            
            self.app.settings['last_backup'] = timestamp
            self.save_database()
            return True
        except Exception as e:
            print(f"Lỗi khi sao lưu database: {str(e)}")
            return False

    def restore_database(self, backup_file):
        try:
            with zipfile.ZipFile(backup_file, 'r') as zipf:
                zipf.extractall()
            self.load_database()
            return True
        except Exception as e:
            print(f"Lỗi khi khôi phục database: {str(e)}")
            return False

    def get_transactions_dataframe(self, date_from=None, date_to=None, type_filter=None, category_filter=None, keyword=None):
        filtered_transactions = []
        for t in self.app.transactions:
            match = True

            # Apply date filters
            if date_from and date_to:
                start_date = datetime.strptime(date_from, "%Y-%m-%d").date()
                end_date = datetime.strptime(date_to, "%Y-%m-%d").date()
                transaction_date = datetime.strptime(t['date'], "%d/%m/%Y").date()
                if not (start_date <= transaction_date <= end_date):
                    match = False

            # Apply type filter
            if type_filter and type_filter != "Tất cả":
                # Loại giao dịch trong self.app.transactions là 'income' hoặc 'expense'
                # Cần so sánh với giá trị đã được chuyển đổi từ type_filter (Thu -> income, Chi -> expense)
                mapped_type_filter = type_filter
                if type_filter == "Thu":
                    mapped_type_filter = "income"
                elif type_filter == "Chi":
                    mapped_type_filter = "expense"
                
                if t['type'] != mapped_type_filter:
                    match = False

            # Apply category filter
            if category_filter and category_filter != "Tất cả":
                if t['category'] != category_filter:
                    match = False

            # Apply keyword filter (search in description/note)
            if keyword:
                if keyword.lower() not in t.get('note', '').lower():
                    match = False

            if match:
                filtered_transactions.append(t)
        
        # Chuyển đổi list of dicts thành DataFrame
        if not filtered_transactions:
            return pd.DataFrame()  # Trả về DataFrame rỗng nếu không có giao dịch
        
        df = pd.DataFrame(filtered_transactions)
        
        # Chuyển đổi cột 'amount' sang dạng số
        df['amount'] = pd.to_numeric(df['amount'])
        
        # Sắp xếp theo ngày
        df['date'] = pd.to_datetime(df['date'], format='%d/%m/%Y')
        df = df.sort_values(by='date').reset_index(drop=True)
        
        return df

    def compress_data(self):
        try:
            # Tạo bản sao lưu trước khi nén
            self.backup_database()
            
            # Nén dữ liệu
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            compressed_file = f"compressed_data_{timestamp}.zip"
            
            with zipfile.ZipFile(compressed_file, 'w', compression=zipfile.ZIP_DEFLATED) as zipf:
                zipf.write(self.db_file, os.path.basename(self.db_file))
            
            return compressed_file
        except Exception as e:
            print(f"Lỗi khi nén dữ liệu: {str(e)}")
            return None

    def delete_old_data(self, days=365):
        try:
            current_date = datetime.now()
            self.app.transactions = [
                t for t in self.app.transactions
                if (current_date - datetime.strptime(t['date'], "%d/%m/%Y")).days <= days
            ]
            self.save_database()
            return True
        except Exception as e:
            print(f"Lỗi khi xóa dữ liệu cũ: {str(e)}")
            return False

    def load_transaction_data(self):
        # Kiểm tra giao_dien đã được khởi tạo chưa
        if self.app.giao_dien is None:
            return
        # Xóa dữ liệu cũ
        for item in self.app.giao_dien.tree.get_children():
            self.app.giao_dien.tree.delete(item)
        
        # Thêm dữ liệu mới
        for transaction in self.app.transactions:
            self.app.giao_dien.tree.insert('', 'end', values=(
                transaction['date'],
                transaction['type'],
                transaction['category'],
                f"{transaction['amount']:,.0f} VNĐ",
                transaction['note']
            ))

    def tim_kiem(self):
        # Lấy từ khóa tìm kiếm
        keyword = self.app.giao_dien.search_entry.get().lower()
        
        # Xóa dữ liệu cũ
        for item in self.app.giao_dien.tree.get_children():
            self.app.giao_dien.tree.delete(item)
        
        # Tìm kiếm và hiển thị kết quả
        for transaction in self.app.transactions:
            if (keyword in transaction['date'].lower() or
                keyword in transaction['type'].lower() or
                keyword in transaction['category'].lower() or
                keyword in str(transaction['amount']).lower() or
                keyword in transaction['note'].lower()):
                self.app.giao_dien.tree.insert('', 'end', values=(
                    transaction['date'],
                    transaction['type'],
                    transaction['category'],
                    f"{transaction['amount']:,.0f} VNĐ",
                    transaction['note']
                ))

    def sua_giaodich(self):
        # Lấy giao dịch được chọn
        selected = self.app.giao_dien.tree.selection()
        if not selected:
            messagebox.showwarning("Cảnh báo", "Vui lòng chọn giao dịch cần sửa")
            return
        
        # Lấy thông tin giao dịch
        item = self.app.giao_dien.tree.item(selected[0])
        values = item['values']
        
        # Tìm giao dịch trong danh sách
        for i, transaction in enumerate(self.app.transactions):
            if (transaction['date'] == values[0] and
                transaction['type'] == values[1] and
                transaction['category'] == values[2] and
                f"{transaction['amount']:,.0f} VNĐ" == values[3] and
                transaction['note'] == values[4]):
                
                # Tạo cửa sổ sửa
                window = ctk.CTkToplevel(self.app.root)
                window.title("Sửa giao dịch")
                window.geometry("400x300")
                
                # Tạo các trường nhập liệu
                ctk.CTkLabel(window, text="Số tiền:").pack(pady=5)
                amount = ctk.CTkEntry(window)
                amount.insert(0, str(transaction['amount']))
                amount.pack(pady=5)
                
                ctk.CTkLabel(window, text="Danh mục:").pack(pady=5)
                category = ctk.CTkComboBox(window, 
                    values=self.app.categories[transaction['type']])
                category.set(transaction['category'])
                category.pack(pady=5)
                
                ctk.CTkLabel(window, text="Ghi chú:").pack(pady=5)
                note = ctk.CTkEntry(window)
                note.insert(0, transaction['note'])
                note.pack(pady=5)
                
                def save_changes():
                    try:
                        # Cập nhật thông tin
                        self.app.transactions[i]['amount'] = float(amount.get())
                        self.app.transactions[i]['category'] = category.get()
                        self.app.transactions[i]['note'] = note.get()
                        
                        # Lưu dữ liệu
                        self.save_database()
                        self.load_transaction_data()
                        self.app.update_financial_summary()
                        window.destroy()
                    except Exception as e:
                        messagebox.showerror("Lỗi", f"Không thể sửa giao dịch: {str(e)}")
                
                ctk.CTkButton(window, text="Lưu", command=save_changes).pack(pady=20)
                break

    def xoa_giaodich(self):
        # Lấy giao dịch được chọn
        selected = self.app.giao_dien.tree.selection()
        if not selected:
            messagebox.showwarning("Cảnh báo", "Vui lòng chọn giao dịch cần xóa")
            return
        
        # Xác nhận xóa
        if messagebox.askyesno("Xác nhận", "Bạn có chắc muốn xóa giao dịch này?"):
            # Lấy thông tin giao dịch
            item = self.app.giao_dien.tree.item(selected[0])
            values = item['values']
            
            # Tìm và xóa giao dịch
            for i, transaction in enumerate(self.app.transactions):
                if (transaction['date'] == values[0] and
                    transaction['type'] == values[1] and
                    transaction['category'] == values[2] and
                    f"{transaction['amount']:,.0f} VNĐ" == values[3] and
                    transaction['note'] == values[4]):
                    del self.app.transactions[i]
                    break
            
            # Lưu dữ liệu
            self.save_database()
            self.load_transaction_data()
            self.app.update_financial_summary()

    def sao_chep_giaodich(self):
        # Lấy giao dịch được chọn
        selected = self.app.giao_dien.tree.selection()
        if not selected:
            messagebox.showwarning("Cảnh báo", "Vui lòng chọn giao dịch cần sao chép")
            return
        
        # Lấy thông tin giao dịch
        item = self.app.giao_dien.tree.item(selected[0])
        values = item['values']
        
        # Tìm giao dịch trong danh sách
        for transaction in self.app.transactions:
            if (transaction['date'] == values[0] and
                transaction['type'] == values[1] and
                transaction['category'] == values[2] and
                f"{transaction['amount']:,.0f} VNĐ" == values[3] and
                transaction['note'] == values[4]):
                
                # Tạo bản sao
                new_transaction = transaction.copy()
                new_transaction['date'] = datetime.now().strftime("%d/%m/%Y")
                
                # Thêm vào danh sách
                self.app.transactions.append(new_transaction)
                
                # Lưu dữ liệu
                self.save_database()
                self.load_transaction_data()
                self.app.update_financial_summary()
                break

    def nhap_dulieu(self):
        """Nhập dữ liệu từ file"""
        try:
            # Mở hộp thoại chọn file
            file_path = filedialog.askopenfilename(
                title="Chọn file dữ liệu",
                filetypes=[
                    ("CSV files", "*.csv"),
                    ("Excel files", "*.xlsx"),
                    ("JSON files", "*.json"),
                    ("All files", "*.*")
                ]
            )
            
            if not file_path:
                return False
                
            # Nhập dữ liệu từ file
            if self.import_data(file_path):
                messagebox.showinfo("Thành công", "Đã nhập dữ liệu thành công!")
                return True
            else:
                messagebox.showerror("Lỗi", "Không thể nhập dữ liệu từ file!")
                return False
                
        except Exception as e:
            messagebox.showerror("Lỗi", f"Lỗi khi nhập dữ liệu: {str(e)}")
            return False

    def xuat_dulieu(self):
        """Xuất dữ liệu ra file"""
        try:
            # Mở hộp thoại chọn định dạng và vị trí lưu file
            file_path = filedialog.asksaveasfilename(
                title="Lưu dữ liệu",
                defaultextension=".csv",
                filetypes=[
                    ("CSV files", "*.csv"),
                    ("Excel files", "*.xlsx"),
                    ("JSON files", "*.json")
                ]
            )
            
            if not file_path:
                return False
                
            # Xác định định dạng file từ phần mở rộng
            format = file_path.split('.')[-1].lower()
            
            # Xuất dữ liệu ra file
            filename = self.export_data(format)
            if filename:
                # Di chuyển file đã xuất đến vị trí người dùng chọn
                shutil.move(filename, file_path)
                messagebox.showinfo("Thành công", "Đã xuất dữ liệu thành công!")
                return True
            else:
                messagebox.showerror("Lỗi", "Không thể xuất dữ liệu!")
                return False
                
        except Exception as e:
            messagebox.showerror("Lỗi", f"Lỗi khi xuất dữ liệu: {str(e)}")
            return False

    def get_all_categories(self):
        categories = set()
        for transaction in self.app.transactions:
            if 'category' in transaction and transaction['category']:
                categories.add(transaction['category'])
        return sorted(list(categories))

    def tim_kiem_nang_cao(self, keyword="", start_date=None, end_date=None, min_amount=None, max_amount=None, category=None, type_filter=None):
        """Tìm kiếm giao dịch với nhiều điều kiện"""
        try:
            # Đọc dữ liệu
            giao_dich = self.doc_du_lieu()
            
            # Lọc theo từ khóa
            if keyword:
                giao_dich = [g for g in giao_dich if keyword.lower() in g['mo_ta'].lower()]
            
            # Lọc theo khoảng thời gian
            if start_date:
                giao_dich = [g for g in giao_dich if g['ngay'] >= start_date]
            if end_date:
                giao_dich = [g for g in giao_dich if g['ngay'] <= end_date]
            
            # Lọc theo khoảng tiền
            if min_amount is not None:
                giao_dich = [g for g in giao_dich if g['so_tien'] >= min_amount]
            if max_amount is not None:
                giao_dich = [g for g in giao_dich if g['so_tien'] <= max_amount]
            
            # Lọc theo danh mục
            if category:
                giao_dich = [g for g in giao_dich if g['danh_muc'] == category]
            
            # Lọc theo loại giao dịch
            if type_filter:
                giao_dich = [g for g in giao_dich if g['loai'] == type_filter]
            
            return giao_dich
        except Exception as e:
            print(f"Lỗi khi tìm kiếm nâng cao: {str(e)}")
            return []

    def _initialize_default_data(self):
        self.app.transactions = []
        self.app.categories = {
            'income': ['Lương', 'Thưởng', 'Đầu tư', 'Khác'],
            'expense': ['Ăn uống', 'Di chuyển', 'Mua sắm', 'Giải trí', 'Khác']
        }
        self.app.settings = {
            'currency': 'VND',
            'language': 'vi',
            'theme': 'light',
            'auto_backup': True,
            'backup_interval': 24,
            'last_backup': None,
            'notify_expense': True,
            'notify_budget': True,
            'budget_limit': 10000000
        }
        self.app.goals = []
        self.app.reminders = []

    def generate_dummy_transactions(self, num_transactions=100):
        start_date = datetime.now() - timedelta(days=365) # Giao dịch trong vòng 1 năm qua
        
        income_categories = self.app.categories['income']
        expense_categories = self.app.categories['expense']

        new_transactions = []

        for _ in range(num_transactions):
            is_income = random.choice([True, False])
            
            date = start_date + timedelta(days=random.randint(0, 365))
            amount = random.randint(10000, 5000000) # Số tiền ngẫu nhiên

            if is_income:
                transaction_type = 'income'
                category = random.choice(income_categories)
                description = f"Thu nhập ngẫu nhiên {random.randint(1, 100)}"
            else:
                transaction_type = 'expense'
                category = random.choice(expense_categories)
                description = f"Chi tiêu ngẫu nhiên {random.randint(1, 100)}"
            
            new_transactions.append({
                'date': date.strftime("%d/%m/%Y"),
                'type': transaction_type,
                'amount': float(amount),
                'category': category,
                'note': description
            })
        
        # Add new transactions to existing ones to avoid overwriting
        # self.app.transactions.extend(new_transactions) 
        # For this test, let's just use the new transactions to have a clean set of 100.
        # If you run this multiple times, it will keep adding. 
        # For a clean test, you might want to clear existing transactions before generating.
        self.app.transactions = new_transactions

        self.save_database()
        messagebox.showinfo("Thông báo", f"Đã tạo {num_transactions} giao dịch mẫu thành công và lưu vào database.json!")

    def doc_du_lieu(self):
        """Đọc dữ liệu giao dịch từ database"""
        try:
            with open(self.db_file, 'r', encoding='utf-8') as f:
                data = json.load(f)
                transactions_data = data.get('transactions', {})
                
                # Đảm bảo transactions_data là một từ điển với các khóa 'income' và 'expenses'
                if not isinstance(transactions_data, dict):
                    transactions_data = {}
                
                income_transactions = transactions_data.get('income', [])
                expense_transactions = transactions_data.get('expenses', [])

                # Kết hợp thành một danh sách phẳng và thêm trường 'type'
                all_transactions = []
                for t in income_transactions:
                    t['type'] = 'income'  # Thêm lại trường type cho nhất quán
                    all_transactions.append(t)
                for t in expense_transactions:
                    t['type'] = 'expense'  # Thêm lại trường type cho nhất quán
                    all_transactions.append(t)
                return all_transactions
        except Exception as e:
            print(f"Lỗi khi đọc dữ liệu: {str(e)}")
            return []  # Trả về một danh sách rỗng nếu có bất kỳ lỗi nào xảy ra 