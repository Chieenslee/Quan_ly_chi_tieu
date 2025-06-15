import customtkinter as ctk
from tkinter import messagebox
import threading
import time
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.application import MIMEApplication
import webbrowser
import requests
import json
import os
from datetime import datetime, timedelta
import sys

class ThongBao:
    def __init__(self, app):
        self.app = app
        self.notifications = []
        self.notification_thread = None
        self.is_running = True

    def them_nhacnho(self):
        # Tạo cửa sổ thêm nhắc nhở
        window = ctk.CTkToplevel(self.app.root)
        window.title("Thêm nhắc nhở")
        window.geometry("500x400")  # Tăng kích thước cửa sổ
        window.transient(self.app.root)
        window.grab_set()
        window.focus_force()
        
        # Tạo frame chính để căn giữa nội dung
        main_frame = ctk.CTkFrame(window)
        main_frame.pack(expand=True, fill="both", padx=20, pady=20)
        
        # Tạo các trường nhập liệu với kích thước lớn hơn
        ctk.CTkLabel(main_frame, text="Tiêu đề:", font=("Arial", 14, "bold")).pack(pady=5)
        title_entry = ctk.CTkEntry(main_frame, width=400, height=35)
        title_entry.pack(pady=5)
        
        ctk.CTkLabel(main_frame, text="Nội dung:", font=("Arial", 14, "bold")).pack(pady=5)
        content_entry = ctk.CTkEntry(main_frame, width=400, height=35)
        content_entry.pack(pady=5)
        
        # Frame cho ngày và giờ
        datetime_frame = ctk.CTkFrame(main_frame)
        datetime_frame.pack(fill="x", pady=10)
        
        # Ngày
        date_frame = ctk.CTkFrame(datetime_frame)
        date_frame.pack(side="left", expand=True, padx=5)
        ctk.CTkLabel(date_frame, text="Ngày:", font=("Arial", 14, "bold")).pack(pady=5)
        date_entry = ctk.CTkEntry(date_frame, width=180, height=35)
        date_entry.insert(0, datetime.now().strftime("%Y-%m-%d"))
        date_entry.pack(pady=5)
        
        # Giờ
        time_frame = ctk.CTkFrame(datetime_frame)
        time_frame.pack(side="right", expand=True, padx=5)
        ctk.CTkLabel(time_frame, text="Giờ:", font=("Arial", 14, "bold")).pack(pady=5)
        time_entry = ctk.CTkEntry(time_frame, width=180, height=35)
        time_entry.insert(0, datetime.now().strftime("%H:%M"))
        time_entry.pack(pady=5)
        
        # Tạo nút lưu với kích thước lớn hơn
        def save_reminder():
            try:
                title = title_entry.get()
                content = content_entry.get()
                date = date_entry.get()
                time = time_entry.get()
                
                # Kiểm tra dữ liệu
                if not title or not content or not date or not time:
                    messagebox.showerror("Lỗi", "Vui lòng điền đầy đủ thông tin")
                    return
                
                # Tạo nhắc nhở mới
                reminder = {
                    "id": len(self.app.reminders) + 1,  # Thêm ID
                    "title": title,
                    "content": content,
                    "date": date,
                    "time": time,
                    "datetime": f"{date} {time}",
                    "notified": False
                }
                
                # Thêm vào danh sách
                self.app.reminders.append(reminder)
                self.app.xu_ly_du_lieu.save_database()
                
                messagebox.showinfo("Thành công", "Đã thêm nhắc nhở mới")
                window.destroy()
                
            except Exception as e:
                messagebox.showerror("Lỗi", f"Không thể thêm nhắc nhở: {str(e)}")
        
        ctk.CTkButton(main_frame, text="Lưu", command=save_reminder, 
                     width=200, height=40, font=("Arial", 14, "bold")).pack(pady=20)

    def start_notification_service(self):
        # Khởi động dịch vụ thông báo
        self.notification_thread = threading.Thread(target=self.notification_service)
        self.notification_thread.daemon = True
        self.notification_thread.start()

    def stop_notification_service(self):
        # Dừng dịch vụ thông báo
        self.is_running = False
        if self.notification_thread:
            self.notification_thread.join()

    def notification_service(self):
        # Dịch vụ thông báo
        while self.is_running:
            try:
                current_time = datetime.now()
                
                # Kiểm tra nhắc nhở
                for reminder in self.app.reminders:
                    if not reminder.get("notified", False):
                        try:
                            reminder_datetime = datetime.strptime(reminder["datetime"], "%Y-%m-%d %H:%M")
                            if current_time >= reminder_datetime:
                                # Hiển thị thông báo
                                messagebox.showinfo(reminder["title"], reminder["content"])
                                reminder["notified"] = True
                                self.app.xu_ly_du_lieu.save_database()
                        except Exception as e:
                            print(f"Lỗi khi kiểm tra reminder: {reminder.get('title', '')} - {e}")
                            continue
                
                # Kiểm tra mục tiêu
                for goal in self.app.goals:
                    if not goal.get("completed", False):
                        try:
                            deadline = datetime.strptime(goal["deadline"], "%Y-%m-%d")
                            days_left = (deadline - current_time).days
                            
                            if days_left <= 7 and days_left > 0:
                                # Hiển thị thông báo
                                messagebox.showinfo("Nhắc nhở mục tiêu", 
                                    f"Mục tiêu '{goal['name']}' còn {days_left} ngày nữa!")
                        except Exception as e:
                            print(f"Lỗi khi kiểm tra goal: {goal.get('name', '')} - {e}")
                            continue
                
                # Kiểm tra ngân sách
                monthly_expense = self.app.get_monthly_expense()
                monthly_budget = self.app.get_monthly_budget()
                
                if monthly_budget > 0:
                    expense_ratio = monthly_expense / monthly_budget
                    if expense_ratio >= 0.8 and expense_ratio < 1:
                        messagebox.showwarning("Cảnh báo ngân sách",
                            "Chi tiêu đã vượt quá 80% ngân sách tháng!")
                    elif expense_ratio >= 1:
                        messagebox.showerror("Cảnh báo ngân sách",
                            "Chi tiêu đã vượt quá ngân sách tháng!")
                
                # Đợi 1 phút
                time.sleep(60)
                
            except Exception as e:
                print(f"Lỗi trong dịch vụ thông báo: {str(e)}")
                time.sleep(60)

    def kiem_tra_capnhat(self):
        # repo_owner = "Chieenslee"
        # repo_name = "Quan_ly_chi_tieu"
        # release_api_url = f"https://api.github.com/repos/{repo_owner}/{repo_name}/releases/latest"
        
        # current_version_str = "1.0.0" # Phiên bản hiện tại của ứng dụng
        # current_version_tuple = self._parse_version(current_version_str)

        # try:
        #     response = requests.get(release_api_url, timeout=10) # Thêm timeout
        #     response.raise_for_status() # Báo lỗi cho các phản hồi HTTP xấu (4xx hoặc 5xx)
            
        #     latest_release = response.json()
            
        #     if not latest_release: # Nếu phản hồi trống, có thể không có bản phát hành nào
        #         messagebox.showinfo("Cập nhật", "Không tìm thấy phiên bản mới. Kho lưu trữ có thể trống hoặc không có bản phát hành nào.")
        #         return

        #     latest_version_str = latest_release.get("tag_name")
        #     if not latest_version_str:
        #         messagebox.showinfo("Cập nhật", "Không tìm thấy thông tin phiên bản mới nhất từ kho lưu trữ.")
        #         return

        #     latest_version_tuple = self._parse_version(latest_version_str)
        #     download_url = latest_release.get("html_url")

        #     if latest_version_tuple > current_version_tuple:
        #         if messagebox.askyesno("Cập nhật", 
        #             f"Đã có phiên bản mới {latest_version_str}. Bạn có muốn cập nhật không?"):
        #             if download_url:
        #                 webbrowser.open(download_url)
        #             else:
        #                 messagebox.showerror("Lỗi", "Không tìm thấy liên kết tải xuống cho phiên bản mới.")
        #     else:
        #         messagebox.showinfo("Cập nhật", f"Bạn đang sử dụng phiên bản mới nhất ({current_version_str}).")
                
        # except requests.exceptions.RequestException as req_e:
        #     messagebox.showerror("Lỗi", f"Không thể kết nối đến máy chủ GitHub để kiểm tra cập nhật: {req_e}")
        # except json.JSONDecodeError:
        #     messagebox.showerror("Lỗi", "Không thể đọc thông tin cập nhật từ phản hồi máy chủ.")
        # except Exception as e:
        #     messagebox.showerror("Lỗi", f"Đã xảy ra lỗi khi kiểm tra cập nhật: {str(e)}")

        messagebox.showinfo("Phiên bản hiện tại 1.0.0", "Phiên bản mới nhất!")

    def _parse_version(self, version_str):
        # Helper để phân tích chuỗi phiên bản (ví dụ: "v1.2.3" hoặc "1.2.3") thành tuple có thể so sánh (1, 2, 3)
        if version_str.startswith('v'):
            version_str = version_str[1:]
        try:
            return tuple(map(int, version_str.split('.')))
        except ValueError:
            return (0,) # Trả về phiên bản rất cũ nếu phân tích thất bại

    def bao_loi(self):
        # Tạo cửa sổ báo lỗi
        window = ctk.CTkToplevel(self.app.root)
        window.title("Báo lỗi")
        window.geometry("600x550") # Increased window size
        window.transient(self.app.root)
        window.grab_set()
        window.focus_force()

        # Configure grid layout
        window.grid_columnconfigure(0, weight=1)
        window.grid_rowconfigure(5, weight=1) # Make description_text expandable

        # Tạo các trường nhập liệu
        ctk.CTkLabel(window, text="Tiêu đề:").grid(row=0, column=0, pady=5, sticky="w", padx=10)
        title_entry = ctk.CTkEntry(window)
        title_entry.grid(row=1, column=0, pady=5, padx=10, sticky="ew")

        ctk.CTkLabel(window, text="Email của bạn:").grid(row=2, column=0, pady=5, sticky="w", padx=10)
        sender_email_entry = ctk.CTkEntry(window)
        sender_email_entry.grid(row=3, column=0, pady=5, padx=10, sticky="ew")

        ctk.CTkLabel(window, text="Mật khẩu email:").grid(row=4, column=0, pady=5, sticky="w", padx=10)
        sender_password_entry = ctk.CTkEntry(window, show="*") # Use show="*" for password masking
        sender_password_entry.grid(row=5, column=0, pady=5, padx=10, sticky="ew")

        ctk.CTkLabel(window, text="Mô tả lỗi:").grid(row=6, column=0, pady=5, sticky="w", padx=10)
        description_text = ctk.CTkTextbox(window, height=150) # Increased height
        description_text.grid(row=7, column=0, pady=5, padx=10, sticky="nsew")

        ctk.CTkLabel(window, text="Các bước tái hiện lỗi:").grid(row=8, column=0, pady=5, sticky="w", padx=10)
        steps_text = ctk.CTkTextbox(window, height=150) # Increased height
        steps_text.grid(row=9, column=0, pady=5, padx=10, sticky="nsew")

        # Tạo nút gửi
        def send_error_report():
            try:
                title = title_entry.get()
                sender_email = sender_email_entry.get()
                sender_password = sender_password_entry.get()
                description = description_text.get("1.0", "end-1c")
                steps = steps_text.get("1.0", "end-1c")

                # Kiểm tra dữ liệu
                if not title or not description or not sender_email or not sender_password:
                    messagebox.showerror("Lỗi", "Vui lòng điền đầy đủ thông tin, bao gồm Email và Mật khẩu của bạn.")
                    return

                # Gửi báo lỗi
                self.gui_baoloi(window, title, description, steps, sender_email, sender_password)

            except Exception as e:
                messagebox.showerror("Lỗi", f"Không thể gửi báo lỗi: {str(e)}")

        ctk.CTkButton(window, text="Gửi báo lỗi", command=send_error_report).grid(row=10, column=0, pady=20)

    def gui_baoloi(self, window, title, description, steps, sender_email, sender_password):
        try:
            # Tạo nội dung email
            msg = MIMEMultipart()
            msg['Subject'] = f"Báo lỗi: {title}"
            msg['From'] = sender_email
            msg['To'] = "lc0949523331@gmail.com"
            
            # Thêm nội dung
            body = f"""
            Tiêu đề: {title}
            
            Mô tả lỗi:
            {description}
            
            Các bước tái hiện lỗi:
            {steps}
            
            Thông tin hệ thống:
            - Phiên bản: 1.0.0
            - Hệ điều hành: {os.name}
            - Python: {sys.version}
            """
            
            msg.attach(MIMEText(body, 'plain'))
            
            # Gửi email
            with smtplib.SMTP('smtp.gmail.com', 587) as server:
                server.starttls()
                server.login(sender_email, sender_password)
            
            messagebox.showinfo("Thành công", "Đã gửi báo lỗi thành công")
            window.destroy()
            
        except Exception as e:
            messagebox.showerror("Lỗi", f"Không thể gửi báo lỗi: {str(e)}") 