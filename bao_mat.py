from cryptography.fernet import Fernet
import base64
import hashlib
import json
import zipfile
import os
import customtkinter as ctk
from tkinter import messagebox, filedialog
import io
from datetime import datetime

class BaoMat:
    def __init__(self, app):
        self.app = app
        self.key = self.load_or_generate_key()

    def load_or_generate_key(self):
        try:
            # Tạo thư mục keys nếu chưa tồn tại
            if not os.path.exists("keys"):
                os.makedirs("keys")
            
            # Tải khóa từ file
            key_file = "keys/encryption.key"
            if os.path.exists(key_file):
                with open(key_file, "rb") as f:
                    return f.read()
            
            # Tạo khóa mới
            key = Fernet.generate_key()
            with open(key_file, "wb") as f:
                f.write(key)
            return key
        except Exception as e:
            messagebox.showerror("Lỗi", f"Không thể tải/tạo khóa: {str(e)}")
            return None

    def ma_hoa_dulieu(self):
        # Tạo cửa sổ mã hóa
        window = ctk.CTkToplevel(self.app.root)
        window.title("Mã hóa dữ liệu")
        window.geometry("400x300")
        
        # Tạo các trường nhập liệu
        ctk.CTkLabel(window, text="Nhập mật khẩu:").pack(pady=5)
        password = ctk.CTkEntry(window, show="*")
        password.pack(pady=5)
        
        ctk.CTkLabel(window, text="Xác nhận mật khẩu:").pack(pady=5)
        confirm = ctk.CTkEntry(window, show="*")
        confirm.pack(pady=5)
        
        def encrypt():
            try:
                # Kiểm tra mật khẩu
                if password.get() != confirm.get():
                    messagebox.showerror("Lỗi", "Mật khẩu không khớp")
                    return
                
                # Tạo khóa từ mật khẩu
                key = self.generate_key_from_password(password.get())
                f = Fernet(key)
                
                # Mã hóa dữ liệu
                data = {
                    'transactions': self.app.transactions,
                    'categories': self.app.categories,
                    'settings': self.app.settings,
                    'goals': self.app.goals,
                    'reminders': self.app.reminders
                }
                
                encrypted_data = f.encrypt(json.dumps(data).encode())
                
                # Lưu dữ liệu đã mã hóa
                with open("encrypted_data.bin", "wb") as file:
                    file.write(encrypted_data)
                
                messagebox.showinfo("Thành công", "Đã mã hóa dữ liệu")
                window.destroy()
            except Exception as e:
                messagebox.showerror("Lỗi", f"Không thể mã hóa dữ liệu: {str(e)}")
        
        ctk.CTkButton(window, text="Mã hóa", command=encrypt).pack(pady=20)

    def giai_ma_dulieu(self):
        # Tạo cửa sổ giải mã
        window = ctk.CTkToplevel(self.app.root)
        window.title("Giải mã dữ liệu")
        window.geometry("400x200")
        
        # Tạo trường nhập liệu
        ctk.CTkLabel(window, text="Nhập mật khẩu:").pack(pady=5)
        password = ctk.CTkEntry(window, show="*")
        password.pack(pady=5)
        
        def decrypt():
            try:
                # Tạo khóa từ mật khẩu
                key = self.generate_key_from_password(password.get())
                f = Fernet(key)
                
                # Đọc dữ liệu đã mã hóa
                with open("encrypted_data.bin", "rb") as file:
                    encrypted_data = file.read()
                
                # Giải mã dữ liệu
                decrypted_data = json.loads(f.decrypt(encrypted_data))
                
                # Cập nhật dữ liệu
                self.app.transactions = decrypted_data['transactions']
                self.app.categories = decrypted_data['categories']
                self.app.settings = decrypted_data['settings']
                self.app.goals = decrypted_data['goals']
                self.app.reminders = decrypted_data['reminders']
                
                # Lưu dữ liệu
                self.app.xu_ly_du_lieu.save_database()
                
                messagebox.showinfo("Thành công", "Đã giải mã dữ liệu")
                window.destroy()
            except Exception as e:
                messagebox.showerror("Lỗi", f"Không thể giải mã dữ liệu: {str(e)}")
        
        ctk.CTkButton(window, text="Giải mã", command=decrypt).pack(pady=20)

    def generate_key_from_password(self, password):
        # Tạo khóa 32 byte từ mật khẩu
        key = hashlib.sha256(password.encode()).digest()
        return base64.urlsafe_b64encode(key)

    def kiem_tra_baomat(self):
        # Kiểm tra các vấn đề bảo mật
        issues = []
        
        # Kiểm tra file khóa
        if not os.path.exists("keys/encryption.key"):
            issues.append("Không tìm thấy file khóa mã hóa")
        
        # Kiểm tra quyền truy cập
        try:
            with open("database.json", "r") as f:
                pass
        except:
            issues.append("Không có quyền truy cập database")
        
        # Kiểm tra dữ liệu đã mã hóa
        if not os.path.exists("encrypted_data.bin"):
            issues.append("Dữ liệu chưa được mã hóa")
        
        # Hiển thị kết quả
        if issues:
            messagebox.showwarning("Cảnh báo bảo mật", "\n".join(issues))
        else:
            messagebox.showinfo("Thông báo", "Không phát hiện vấn đề bảo mật")

    def sao_luu_baomat(self):
        try:
            # Tạo thư mục backups nếu chưa tồn tại
            if not os.path.exists("backups"):
                os.makedirs("backups")
            
            # Tạo file zip
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            zip_filename = f"backups/backup_{timestamp}.zip"
            
            with zipfile.ZipFile(zip_filename, 'w') as zipf:
                # Thêm các file quan trọng
                if os.path.exists("database.json"):
                    zipf.write("database.json")
                if os.path.exists("encrypted_data.bin"):
                    zipf.write("encrypted_data.bin")
                if os.path.exists("keys/encryption.key"):
                    zipf.write("keys/encryption.key")
            
            # Mã hóa file backup
            with open(zip_filename, 'rb') as f:
                data = f.read()
            
            encrypted_data = Fernet(self.key).encrypt(data)
            
            with open(zip_filename, 'wb') as f:
                f.write(encrypted_data)
            
            messagebox.showinfo("Thành công", "Đã tạo bản sao lưu bảo mật")
        except Exception as e:
            messagebox.showerror("Lỗi", f"Không thể tạo bản sao lưu: {str(e)}")

    def khoi_phuc_baomat(self):
        try:
            # Chọn file backup
            backup_file = filedialog.askopenfilename(
                title="Chọn file backup",
                filetypes=[("Zip files", "*.zip")],
                initialdir="backups"
            )
            
            if not backup_file:
                return
            
            # Giải mã file backup
            with open(backup_file, 'rb') as f:
                encrypted_data = f.read()
            
            decrypted_data = Fernet(self.key).decrypt(encrypted_data)
            
            # Giải nén dữ liệu
            with zipfile.ZipFile(io.BytesIO(decrypted_data)) as zipf:
                # Khôi phục database
                if "database.json" in zipf.namelist():
                    with zipf.open("database.json") as source, open("database.json", 'wb') as target:
                        target.write(source.read())
                
                # Khôi phục dữ liệu mã hóa
                if "encrypted_data.bin" in zipf.namelist():
                    with zipf.open("encrypted_data.bin") as source, open("encrypted_data.bin", 'wb') as target:
                        target.write(source.read())
                
                # Khôi phục khóa
                if "keys/encryption.key" in zipf.namelist():
                    os.makedirs("keys", exist_ok=True)
                    with zipf.open("keys/encryption.key") as source, open("keys/encryption.key", 'wb') as target:
                        target.write(source.read())
            
            # Tải lại dữ liệu
            self.app.xu_ly_du_lieu.load_database()
            
            messagebox.showinfo("Thành công", "Đã khôi phục dữ liệu")
        except Exception as e:
            messagebox.showerror("Lỗi", f"Không thể khôi phục dữ liệu: {str(e)}")

    def doi_matkhau(self):
        # Tạo cửa sổ đổi mật khẩu
        window = ctk.CTkToplevel(self.app.root)
        window.title("Đổi mật khẩu")
        window.geometry("400x300")
        
        # Tạo các trường nhập liệu
        ctk.CTkLabel(window, text="Mật khẩu hiện tại:").pack(pady=5)
        current = ctk.CTkEntry(window, show="*")
        current.pack(pady=5)
        
        ctk.CTkLabel(window, text="Mật khẩu mới:").pack(pady=5)
        new = ctk.CTkEntry(window, show="*")
        new.pack(pady=5)
        
        ctk.CTkLabel(window, text="Xác nhận mật khẩu mới:").pack(pady=5)
        confirm = ctk.CTkEntry(window, show="*")
        confirm.pack(pady=5)
        
        def change():
            try:
                # Kiểm tra mật khẩu hiện tại
                current_key = self.generate_key_from_password(current.get())
                if current_key != self.key:
                    messagebox.showerror("Lỗi", "Mật khẩu hiện tại không đúng")
                    return
                
                # Kiểm tra mật khẩu mới
                if new.get() != confirm.get():
                    messagebox.showerror("Lỗi", "Mật khẩu mới không khớp")
                    return
                
                # Tạo khóa mới
                new_key = self.generate_key_from_password(new.get())
                
                # Mã hóa lại dữ liệu với khóa mới
                if os.path.exists("encrypted_data.bin"):
                    with open("encrypted_data.bin", "rb") as f:
                        encrypted_data = f.read()
                    
                    # Giải mã với khóa cũ
                    f = Fernet(current_key)
                    decrypted_data = f.decrypt(encrypted_data)
                    
                    # Mã hóa với khóa mới
                    f = Fernet(new_key)
                    new_encrypted_data = f.encrypt(decrypted_data)
                    
                    # Lưu dữ liệu đã mã hóa
                    with open("encrypted_data.bin", "wb") as f:
                        f.write(new_encrypted_data)
                
                # Lưu khóa mới
                with open("keys/encryption.key", "wb") as f:
                    f.write(new_key)
                
                self.key = new_key
                
                messagebox.showinfo("Thành công", "Đã đổi mật khẩu")
                window.destroy()
            except Exception as e:
                messagebox.showerror("Lỗi", f"Không thể đổi mật khẩu: {str(e)}")
        
        ctk.CTkButton(window, text="Đổi mật khẩu", command=change).pack(pady=20)

    def xoa_dulieu_baomat(self):
        # Xác nhận xóa
        if not messagebox.askyesno("Xác nhận", "Bạn có chắc muốn xóa dữ liệu đã mã hóa?"):
            return
        
        try:
            # Xóa các file bảo mật
            if os.path.exists("encrypted_data.bin"):
                os.remove("encrypted_data.bin")
            
            if os.path.exists("keys/encryption.key"):
                os.remove("keys/encryption.key")
            
            messagebox.showinfo("Thành công", "Đã xóa dữ liệu đã mã hóa")
        except Exception as e:
            messagebox.showerror("Lỗi", f"Không thể xóa dữ liệu: {str(e)}")

    def kiem_tra_quyen(self):
        # Kiểm tra quyền truy cập
        issues = []
        
        # Kiểm tra quyền đọc/ghi
        try:
            with open("database.json", "r") as f:
                pass
            with open("database.json", "a") as f:
                pass
        except:
            issues.append("Không có quyền đọc/ghi database")
        
        # Kiểm tra quyền thư mục
        try:
            os.makedirs("backups", exist_ok=True)
            os.makedirs("keys", exist_ok=True)
        except:
            issues.append("Không có quyền tạo thư mục")
        
        # Hiển thị kết quả
        if issues:
            messagebox.showwarning("Cảnh báo quyền truy cập", "\n".join(issues))
        else:
            messagebox.showinfo("Thông báo", "Không phát hiện vấn đề quyền truy cập")

    def kiem_tra_tinhnguyenven(self):
        # Kiểm tra tính nguyên vẹn dữ liệu
        issues = []
        
        # Kiểm tra database
        try:
            with open("database.json", "r") as f:
                data = json.load(f)
                
                # Kiểm tra cấu trúc
                required_keys = ['transactions', 'categories', 'settings', 'goals', 'reminders']
                for key in required_keys:
                    if key not in data:
                        issues.append(f"Thiếu trường {key} trong database")
        except:
            issues.append("Không thể đọc database")
        
        # Kiểm tra dữ liệu mã hóa
        try:
            if os.path.exists("encrypted_data.bin"):
                with open("encrypted_data.bin", "rb") as f:
                    encrypted_data = f.read()
                
                # Thử giải mã
                Fernet(self.key).decrypt(encrypted_data)
        except:
            issues.append("Dữ liệu mã hóa bị hỏng")
        
        # Hiển thị kết quả
        if issues:
            messagebox.showwarning("Cảnh báo tính nguyên vẹn", "\n".join(issues))
        else:
            messagebox.showinfo("Thông báo", "Không phát hiện vấn đề tính nguyên vẹn") 