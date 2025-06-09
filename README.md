![GitHub Stars](https://img.shields.io/github/stars/Chieenslee/Quan_ly_chi_tieu?style=social)

# Ứng dụng Quản lý Chi tiêu Cá nhân - Nâng tầm tài chính của bạn

## 🚀 Giới thiệu

Ứng dụng Quản lý Chi tiêu Cá nhân là giải pháp toàn diện giúp bạn nắm quyền kiểm soát tài chính cá nhân một cách dễ dàng và hiệu quả. Với giao diện người dùng hiện đại, trực quan và các tính năng mạnh mẽ, ứng dụng cung cấp cho bạn cái nhìn sâu sắc về thói quen chi tiêu, thu nhập, và giúp bạn thiết lập, đạt được các mục tiêu tài chính một cách thông minh. Hãy để ứng dụng của chúng tôi đồng hành cùng bạn trên hành trình quản lý tiền bạc, hướng tới một tương lai tài chính vững chắc và thịnh vượng hơn.

## ✨ Tính năng nổi bật

-   **Quản lý Thu & Chi thông minh**: Ghi lại mọi giao dịch một cách nhanh chóng và chính xác.
-   **Báo cáo tài chính chuyên sâu**: Tạo các báo cáo chi tiết về dòng tiền, giúp bạn hiểu rõ hơn về tình hình tài chính.
-   **Biểu đồ trực quan & Thống kê**: Biến dữ liệu số thành những biểu đồ sinh động, dễ hiểu, giúp bạn theo dõi xu hướng chi tiêu và thu nhập.
-   **Nhắc nhở & Mục tiêu tài chính**: Đặt nhắc nhở cho các hóa đơn sắp tới và thiết lập mục tiêu tiết kiệm, chi tiêu để luôn đi đúng hướng.
-   **Sao lưu & Khôi phục dữ liệu**: Bảo vệ dữ liệu của bạn an toàn với tính năng sao lưu và khôi phục dễ dàng.
-   **Bảo mật dữ liệu**: Đảm bảo thông tin tài chính của bạn luôn được bảo mật.
-   **Tùy chỉnh linh hoạt**: Cá nhân hóa ứng dụng với nhiều theme và tùy chọn ngôn ngữ.

## ⬇️ Tải về ứng dụng

Để sử dụng ứng dụng ngay lập tức, bạn có thể tải về phiên bản cài đặt (.exe) mới nhất tại đây:

**[TẢI XUỐNG NGAY](ĐIỀN_LIÊN_KẾT_TẢI_VỀ_FILE_EXE_CỦA_BẠN_VÀO_ĐÂY)**

## 🛠️ Yêu cầu hệ thống (Nếu bạn muốn chạy từ mã nguồn)

-   Python 3.8 trở lên
-   Các thư viện Python cần thiết (xem `requirements.txt`)

## ⚙️ Cài đặt (Chỉ dành cho nhà phát triển/chạy từ mã nguồn)

1.  Clone repository:
    ```bash
    git clone https://github.com/yourusername/quanlychitieu.git
    cd quanlychitieu
    ```

2.  Cài đặt dependencies:
    ```bash
    pip install -r requirements.txt
    ```

3.  Chạy ứng dụng:
    ```bash
    python run.py
    ```

## 📂 Cấu trúc thư mục

-   `run.py`: File khởi chạy chính của ứng dụng.
-   `quanlychitieu.py`: Class chính chứa logic nghiệp vụ và quản lý các module.
-   `giao_dien.py`: Quản lý giao diện người dùng.
-   `bao_mat.py`: Xử lý bảo mật và mã hóa.
-   `bieu_do.py`: Tạo và cập nhật biểu đồ.
-   `bao_cao.py`: Tạo báo cáo tài chính.
-   `tinh_nang.py`: Các tính năng bổ sung như nhắc nhở, mục tiêu, kế hoạch.
-   `tinh_toan.py`: Xử lý các phép tính tài chính (lãi suất, thuế).
-   `thong_bao.py`: Quản lý thông báo và nhắc nhở hệ thống.
-   `xuly_du_lieu.py`: Xử lý đọc, ghi và quản lý dữ liệu giao dịch.
-   `cai_dat.py`: Quản lý cài đặt ứng dụng.
-   `chatbot.py`: Module chatbot hỗ trợ người dùng (nếu có).

## 🗄️ Thư mục dữ liệu

-   `data/`: Lưu trữ dữ liệu giao dịch.
-   `backup/`: Lưu trữ bản sao lưu.
-   `reports/`: Lưu trữ báo cáo.
-   `temp/`: Lưu trữ file tạm thời.
-   `keys/`: Lưu trữ khóa mã hóa (nếu sử dụng).

## 📸 Ảnh chụp màn hình

Để thêm ảnh chụp màn hình ứng dụng của bạn, hãy tạo một thư mục `images/` trong thư mục gốc của dự án và đặt các file ảnh vào đó. Sau đó, bạn có thể tham chiếu chúng tại đây:

Ví dụ:

![Màn hình chính](images/main_screen.png)
![Báo cáo chi tiêu](images/expense_report.png)

## 📖 Hướng dẫn sử dụng

1.  **Thêm giao dịch**:
    -   Nhấn nút "Thêm thu" hoặc "Thêm chi".
    -   Điền thông tin giao dịch cần thiết.
    -   Nhấn "Lưu" để hoàn tất.

2.  **Xem báo cáo**:
    -   Chọn "Báo cáo" từ menu chính.
    -   Chọn loại báo cáo bạn muốn xem (ví dụ: Thu theo tháng, Chi theo danh mục).
    -   Chọn khoảng thời gian mong muốn.
    -   Nhấn "Tạo báo cáo" để xem kết quả.

3.  **Cài đặt ứng dụng**:
    -   Chọn "Cài đặt" từ menu.
    -   Thay đổi theme giao diện, đơn vị tiền tệ, hoặc ngôn ngữ.
    -   Quản lý các danh mục thu/chi của bạn.
    -   Nhấn "Lưu" để áp dụng các thay đổi.

## 🤝 Đóng góp

Mọi đóng góp nhằm cải thiện ứng dụng đều được chào đón! Vui lòng tạo issue hoặc pull request trên GitHub của chúng tôi.

## 📄 Giấy phép

MIT License 