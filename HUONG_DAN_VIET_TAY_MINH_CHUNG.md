# HƯỚNG DẪN VIẾT TAY MINH CHỨNG LAB 7 (DÀNH CHO SINH VIÊN)
**Môn học:** Kiểm thử Phần mềm  
**Bài thực hành:** Bài 7 - Kiểm thử Mocking ứng dụng di động và Tích hợp liên tục (CI/CD)  
**Sinh viên thực hiện:** Phan Khánh Vương  
**Mã số sinh viên (MSSV):** 2312802  
**Ngày thực hành:** 16/10/2026  

> ⚠️ **QUY ĐỊNH BẮT BUỘC CỦA GIẢNG VIÊN:**  
> - Sinh viên phải chuẩn bị **4 trang giấy A4 trắng**.
> - Ở góc trên cùng mỗi trang, bắt buộc ghi rõ:
>   + **Họ và tên:** Phan Khánh Vương
>   + **MSSV:** 2312802
>   + **Ngày thực hành:** 16/10/2026
>   + **Chữ ký tươi bằng bút mực xanh** (hoặc đặt thẻ sinh viên bên cạnh khi chụp).
> - Sau khi viết xong, dùng điện thoại chụp ảnh rõ nét hoặc scan 4 trang, ghép thành 01 file PDF duy nhất đặt tên là: `MinhChung_VietTay_2312802.pdf` và lưu tại thư mục gốc của bài lab.

---

## TRANG 1: SƠ ĐỒ LUỒNG KIẾN TRÚC CI PIPELINE (Vẽ tay hoàn toàn)

### Thông tin đầu trang:
- **Họ và tên:** Phan Khánh Vương
- **MSSV:** 2312802
- **Ngày thực hành:** 16/10/2026
- **Chữ ký tươi:** *(Ký tên bằng bút mực xanh)*

### Nội dung vẽ tay:
*(Vẽ các khối chữ nhật nối tiếp nhau bằng mũi tên từ trái qua phải hoặc từ trên xuống dưới theo thứ tự sau):*

```
+-------------------------------------------------------------+
|               1. SỰ KIỆN KÍCH HOẠT (TRIGGER)                |
|           git push / pull_request -> branch: main           |
+-------------------------------------------------------------+
                              |
                              v
+-------------------------------------------------------------+
|                 2. CHECKOUT SOURCE CODE                     |
|                   actions/checkout@v4                       |
|           Kéo mã nguồn từ GitHub về Runner Ubuntu           |
+-------------------------------------------------------------+
                              |
                              v
+-------------------------------------------------------------+
|              3. SETUP PYTHON ENVIRONMENT                    |
|                 actions/setup-python@v5                     |
|           Khởi tạo môi trường Python 3.11 sạch              |
+-------------------------------------------------------------+
                              |
                              v
+-------------------------------------------------------------+
|                4. INSTALL DEPENDENCIES                      |
|         pip install -r requirements.txt (Ghim bản)          |
|              requests, coverage, flake8                     |
+-------------------------------------------------------------+
                              |
                              v
+-------------------------------------------------------------+
|             5. STATIC CODE ANALYSIS (LINTER)                |
|             flake8 . (Kiểm tra cú pháp tĩnh)                |
|   -> Nếu Lỗi cú pháp: Exit Code != 0 -> FAIL (Báo Đỏ)       |
+-------------------------------------------------------------+
                              | (Pass: Exit Code = 0)
                              v
+-------------------------------------------------------------+
|           6. EXECUTE TESTS & QUALITY GATE                   |
|   - Chạy 13 Unit Test + Mocking GPS (unittest.mock)         |
|   - Đo lường Coverage: coverage report --fail-under=80      |
|   -> Nếu Coverage < 80%: Exit Code != 0 -> FAIL (Báo Đỏ)    |
|   -> Nếu Coverage >= 80%: Exit Code = 0 -> PASS (Xanh)      |
+-------------------------------------------------------------+
                              |
                              v
+-------------------------------------------------------------+
|           7. UPLOAD COVERAGE REPORT ARTIFACT                |
|                actions/upload-artifact@v4                   |
|           Lưu trữ thư mục coverage_html (7 ngày)            |
+-------------------------------------------------------------+
```

### Chú thích nguyên lý cốt lõi viết thêm bên dưới sơ đồ:
- **Fail-Fast (Thất bại sớm):** Bước Linter (flake8) đứng trước Unit Test để phát hiện lỗi cú pháp tức thì mà không cần chạy kiểm thử, tiết kiệm thời gian runner.
- **Quality Gate:** Cổng chặn chất lượng khóa tiến trình build nếu tỷ lệ bao phủ mã nguồn không đạt ngưỡng tối thiểu 80%.

---

## TRANG 2: BẢNG MA TRẬN THIẾT KẾ KỊCH BẢN TEST CASE MOCKING (Kẻ bảng và viết tay)

### Thông tin đầu trang:
- **Họ và tên:** Phan Khánh Vương
- **MSSV:** 2312802
- **Ngày thực hành:** 16/10/2026
- **Chữ ký tươi:** *(Ký tên bằng bút mực xanh)*

### Nội dung bảng kẻ tay (gồm 4 cột):

| STT | Tên Test Case | Hàm được gọi | Đối tượng & Giá trị Mocking | Kết quả kỳ vọng (Assert) |
|:---:|---|---|---|---|
| **1** | `test_apply_promo_online_valid` | `apply_promo_code` | Không mock<br>- Thiết bị: `online`<br>- OS Version: `15`<br>- Mã: `"GIAM10"` | Áp mã giảm 10% thành công.<br>`assertEqual(result, 90000.0)` |
| **2** | `test_apply_promo_offline_raises_connection_error` | `apply_promo_code` | Không mock<br>- Thiết bị: `offline`<br>- OS Version: `15`<br>- Mã: `"GIAM10"` | Ném ngoại lệ kết nối mạng.<br>`assertRaises(ConnectionError)` |
| **3** | `test_apply_promo_special_code_os15` | `apply_promo_code` | Không mock<br>- Thiết bị: `online`<br>- OS Version: `15`<br>- Mã: `"NEW_OS_ONLY"` | Áp mã giảm 20% thành công trên OS 15.<br>`assertEqual(result, 80000.0)` |
| **4** | `test_apply_promo_special_code_os14_raises_value_error` | `apply_promo_code` | Không mock<br>- Thiết bị: `online`<br>- OS Version: `14`<br>- Mã: `"NEW_OS_ONLY"` | Ném ngoại lệ do phiên bản OS không đủ điều kiện (cần OS 15+).<br>`assertRaises(ValueError)` |
| **5** | `test_get_nearby_restaurants_in_range` | `get_nearby_restaurants` | `@patch('yummy_app.gps_service.get_current_location')`<br>Giá trị mock: `return_value = (10.0, 105.0)` | Trả về danh sách nhà hàng tương ứng tọa độ:<br>`["Nha hang Pho Ly Quoc Su", "Bun cha Huong Lien"]` |
| **6** | `test_get_nearby_restaurants_out_of_range` | `get_nearby_restaurants` | `@patch('yummy_app.gps_service.get_current_location')`<br>Giá trị mock: `return_value = (20.0, 110.0)` | Tọa độ không có đối tác, trả về danh sách rỗng:<br>`assertEqual(restaurants, [])` |
| **7** | `test_get_nearby_restaurants_signal_lost` | `get_nearby_restaurants` | `@patch('yummy_app.gps_service.get_current_location')`<br>Giá trị mock: `side_effect = GPSSignalLostError()` | Bắt ngoại lệ mất GPS và trả về chuỗi thông báo:<br>`"Khong the xac dinh vi tri."` |

---

## TRANG 3: LỜI GIẢI CÂU HỎI PHÂN TÍCH CẤP ĐỘ 2 (Viết tay)

### Thông tin đầu trang:
- **Họ và tên:** Phan Khánh Vương
- **MSSV:** 2312802
- **Ngày thực hành:** 16/10/2026
- **Chữ ký tươi:** *(Ký tên bằng bút mực xanh)*

### Nội dung trả lời chi tiết:

#### Câu 2.1: Tại sao bước chạy Linter (flake8) phải đặt trước bước chạy test trong đường ống CI?
**Trả lời:**
1. **Áp dụng nguyên lý Thất bại sớm (Fail-Fast):**
   - Linter (`flake8`) thực hiện kiểm tra tĩnh (Static Code Analysis) để phát hiện ngay các lỗi cú pháp nghiêm trọng (`SyntaxError`, thụt lề sai, gọi biến chưa định nghĩa, import thừa...) mà không cần nạp bộ thông dịch để chạy mã.
   - Thời gian quét của linter diễn ra cực kỳ nhanh chóng (chỉ từ 1 - 2 giây), nhẹ hơn rất nhiều so với thời gian khởi tạo và thực thi toàn bộ test suite.
2. **Tiết kiệm tài nguyên và chi phí máy chủ CI:**
   - Nếu mã nguồn có lỗi cú pháp cơ bản thì chắc chắn các test case sẽ bị crash hoặc fail.
   - Việc đặt Linter lên đầu giúp chặn đứng và kết thúc (break) pipeline ngay lập tức khi phát hiện mã lỗi, tránh lãng phí hạn ngạch thời gian chạy (GitHub Actions runner minutes) và điện năng tính toán của hệ thống.
3. **Đảm bảo chuẩn mực chất lượng mã nguồn:**
   - Buộc lập trình viên phải duy trì mã nguồn sạch, tuân thủ quy chuẩn PEP 8 trước khi tiến hành xác minh nghiệp vụ.

---

#### Câu 2.2: Tham số `--fail-under=80` của lệnh coverage report hoạt động theo nguyên lý nào trong hệ điều hành Linux để báo hiệu cho GitHub Actions dừng tiến trình build?
**Trả lời:**
1. **Cơ chế mã thoát (Exit Code / Return Code) trong Linux:**
   - Trong hệ điều hành Linux/POSIX, mọi tiến trình (process) khi kết thúc đều trả về một giá trị số nguyên nguyên thủy cho hệ điều hành gọi là Exit Code:
     + Mã `0`: Biểu thị tiến trình kết thúc thành công (Success).
     + Mã khác `0` (Non-zero, từ `1` đến `255`): Biểu thị tiến trình gặp lỗi hoặc điều kiện thất bại (Failure).
2. **Cơ chế kiểm soát của tham số `--fail-under=80`:**
   - Khi chạy lệnh `coverage report --fail-under=80`, công cụ `coverage` sẽ tính tổng tỷ lệ bao phủ mã nguồn:
     + Nếu `Coverage >= 80%`: Tiến trình kết thúc bình thường và trả về Exit Code `0`.
     + Nếu `Coverage < 80%`: Công cụ nhận diện không thỏa ngưỡng, in thông báo `Coverage failure: total is less than fail-under=80` và chủ động gọi `sys.exit(2)` (Exit Code = 2).
3. **Phản ứng của GitHub Actions runner:**
   - Mỗi step `run` trên runner Linux chạy trong shell mặc định với cơ chế tương đương cờ `set -e` (kiểm tra trạng thái `$?` sau mỗi lệnh).
   - Khi lệnh trả về Exit Code khác `0`, runner xem đây là lỗi nghiêm trọng, lập tức đánh dấu step và job đó là `FAILED` (Báo Đỏ) và ngừng toàn bộ các step kế tiếp (ngoại trừ step có `if: always()`).

---

#### Câu 2.3: Tham số `-m` trong lệnh `coverage report -m` hiển thị thêm thông tin gì và giúp ích gì cho kỹ sư kiểm thử khi tối ưu độ bao phủ mã nguồn?
**Trả lời:**
1. **Thông tin hiển thị:**
   - Tham số `-m` (viết tắt của `--show-missing`) yêu cầu bộ đo độ bao phủ bổ sung thêm một cột có tên là **`Missing`** trong bảng báo cáo terminal.
   - Cột `Missing` liệt kê cụ thể các số dòng (Line Numbers) hoặc dải dòng mã nguồn chưa từng được luồng kiểm thử chạm tới (chưa được thực thi) trong suốt quá trình chạy test (ví dụ: `34-43, 47-52`).
2. **Lợi ích đối với Kỹ sư kiểm thử (SET):**
   - **Xóa bỏ điểm mù kiểm thử (Zero Guesswork):** Kỹ sư không cần phải phỏng đoán xem nhánh rẽ nào (`if`, `elif`, `else`, `try-except`) còn sót.
   - **Thiết kế test case có mục tiêu chính xác:** Dễ dàng đối chiếu dòng code bị thiếu để bổ sung ngay test case cho trường hợp đó (ví dụ phát hiện dòng `34-43` là nhánh xử lý mã khuyến mãi khi `network_status == "offline"` và lỗi phiên bản OS).
   - **Tối ưu hóa thời gian và năng suất:** Giúp nhanh chóng đưa độ bao phủ từ mức thấp (35%) vượt ngưỡng Quality Gate (>= 80%) mà không phải viết các test thừa thãi.

---

## TRANG 4: LỜI GIẢI CÂU HỎI PHÂN TÍCH CẤP ĐỘ 3 (Viết tay)

### Thông tin đầu trang:
- **Họ và tên:** Phan Khánh Vương
- **MSSV:** 2312802
- **Ngày thực hành:** 16/10/2026
- **Chữ ký tươi:** *(Ký tên bằng bút mực xanh)*

### Nội dung trả lời chi tiết:

#### Câu 3.1: Phân biệt giữa khái niệm Flaky Test và lỗi do sai lệch môi trường phụ thuộc.
**Trả lời:**

1. **Flaky Test (Kiểm thử không ổn định / Chập chờn):**
   - **Định nghĩa:** Là bài test có kết quả không nhất quán (lúc Pass, lúc Fail) dù mã nguồn không thay đổi và chạy trên cùng một môi trường máy chủ.
   - **Nguyên nhân:** Do các yếu tố bất định (non-deterministic) nội tại:
     + Tranh chấp tài nguyên (Race Conditions) trong xử lý đa luồng.
     + Phụ thuộc vào độ trễ mạng ngoại vi hoặc máy chủ bên thứ ba khi không mock (timeout, mạng chập chờn).
     + Phụ thuộc vào thứ tự ngẫu nhiên của các test case khi chạy song song.
     + Phụ thuộc vào thời gian hệ thống thực tế (Timezone, Date).
   - **Đặc điểm:** Thất bại mang tính ngẫu nhiên, khó tái hiện lại theo ý muốn.

2. **Lỗi do sai lệch môi trường phụ thuộc (Environment Drift / Dependency Drift):**
   - **Định nghĩa:** Là tình trạng test luôn chạy Pass ổn định 100% trên môi trường này (ví dụ máy cá nhân lập trình viên) nhưng luôn bị Fail xác định 100% trên môi trường khác (ví dụ máy chủ CI runner hoặc máy staging).
   - **Nguyên nhân:** Do sự không đồng nhất về cấu hình môi trường:
     + Khác biệt hệ điều hành (Windows dùng dấu phân cách thư mục `\`, Linux dùng `/`).
     + Sai lệch phiên bản Python (ví dụ cú pháp chỉ có trên Python 3.11+ chạy trên Python 3.9).
     + Sai lệch phiên bản thư viện (do không ghim phiên bản trong `requirements.txt`).
   - **Đặc điểm:** Thất bại mang tính xác định (deterministic) trên môi trường có cấu hình lệch.

3. **Bảng so sánh cốt lõi:**
   - *Flaky Test:* Bất định (Non-deterministic) ngay trên cùng 1 máy -> Khắc phục bằng Mocking, cô lập dữ liệu.
   - *Sai lệch môi trường:* Xác định (Deterministic) giữa các máy khác nhau -> Khắc phục bằng Ghim phiên bản và đồng bộ hóa môi trường (Docker / CI runner chuẩn).

---

#### Câu 3.2: Tại sao trên máy chủ CI bắt buộc phải tuân thủ nguyên tắc ghim phiên bản (Version Pinning) trong requirements.txt?
**Trả lời:**
1. **Đảm bảo tính tái lập (Reproducibility) và ổn định của CI Pipeline:**
   - Mỗi lần CI chạy là một máy chủ ảo sạch (ephemeral container). Nếu không ghim phiên bản (ví dụ chỉ ghi `requests` hoặc `requests>=2.0.0`), lệnh `pip install` sẽ tự động tải phiên bản mới nhất trên PyPI tại thời điểm đó.
   - Ghim phiên bản chuẩn xác (`package==x.y.z`) đảm bảo môi trường CI luôn đồng nhất 100% với môi trường máy lập trình viên ở mọi thời điểm chạy.
2. **Ngăn chặn lỗi phá vỡ tương thích ngược (Breaking Changes):**
   - Các gói thư viện mã nguồn mở cập nhật liên tục. Bản cập nhật mới có thể thay đổi cách gọi hàm (API contract), bỏ các hàm cũ (deprecated) hoặc sinh ra bug mới.
   - Không ghim phiên bản sẽ dẫn đến hiện tượng pipeline bị "sập" bất thình lình vào một ngày đẹp trời dù nhóm phát triển không hề thay đổi một dòng code nào trong dự án.
3. **Bảo mật chuỗi cung ứng phần mềm (Supply Chain Security):**
   - Ngăn chặn việc máy chủ CI vô tình tự động tải về các bản phát hành độc hại vừa bị tin tặc tấn công đầu độc trên kho PyPI trước khi được đội ngũ kỹ sư thẩm định.

---

#### Câu 3.3: Trình bày quy trình 6 bước chuẩn để nâng cấp một thư viện lên phiên bản mới an toàn qua Pull Request mà không làm gián đoạn nhánh main.
**Trả lời:**
Quy trình 6 bước chuẩn kỹ nghệ phần mềm:
- **Bước 1: Tạo nhánh làm việc độc lập (Isolation Branch):**
  Từ nhánh `main` mới nhất, tạo một nhánh mới riêng biệt (ví dụ: `git checkout -b chore/upgrade-requests-to-2.32`). Tuyệt đối không nâng cấp trực tiếp trên nhánh `main`.
- **Bước 2: Cập nhật tệp cấu hình phụ thuộc (`requirements.txt`):**
  Chỉnh sửa số phiên bản của thư viện cần nâng cấp trong `requirements.txt` sang phiên bản mục tiêu mới. Đọc kỹ tài liệu Release Notes và Changelog của thư viện để nắm các thay đổi lớn.
- **Bước 3: Kiểm thử và tinh chỉnh mã nguồn cục bộ (Local Verification):**
  Cài đặt phiên bản mới trên máy phát triển cá nhân (`pip install -r requirements.txt`). Chạy toàn bộ bộ test và linter. Nếu phát sinh lỗi do thư viện mới thay đổi cấu trúc, tiến hành refactor code nghiệp vụ và cập nhật test case tương ứng cho đến khi 100% test Pass.
- **Bước 4: Commit và đẩy nhánh lên GitHub (Push Branch):**
  Commit các thay đổi kèm thông điệp rõ ràng theo chuẩn Conventional Commits (ví dụ: `chore: upgrade requests from 2.31.0 to 2.32.3`). Đẩy nhánh lên remote repository: `git push origin chore/upgrade-requests-to-2.32`.
- **Bước 5: Tạo Pull Request (PR) và xác minh qua CI Pipeline:**
  Tạo Pull Request hợp nhất nhánh vừa nâng cấp vào `main`. Hệ thống CI Pipeline tự động khởi chạy trên môi trường Ubuntu sạch để kiểm tra Linter, Unit Test và Cổng chất lượng Quality Gate. Đảm bảo toàn bộ checks đạt màu Xanh (Pass).
- **Bước 6: Duyệt mã nguồn (Code Review) và Hợp nhất (Merge):**
  Gửi PR cho Tech Lead / Đồng nghiệp đánh giá rủi ro. Sau khi được chấp thuận (Approve) và CI hoàn toàn Pass, tiến hành hợp nhất PR vào nhánh `main` (Squash & Merge) và xóa nhánh tính năng tạm để giữ lịch sử Git gọn gàng.
