# 042020_HCM_TuanNguyen_SE

**Framework:** Odoo v.12

**Mô tả:**
```
- Cinema: quản lý các rạp phim với các thông tin tên, địa chỉ, người quản lý ....
- Room: Quản lý các phòng chiếu trong 1 rạp phim
- Seat: Quản lý các ghế ngồi theo hàng và cột trong rạp phim (Để thống kê khi cần thiết)
- Movie: Quản lý các bộ phim với các thông tin:
    - Từ ngày ... đến ngày
    - Trailer
    - Nội dung tóm gọn
    - Diễn viên
    - ...
- Showing: quản lý các suất chiếu với các thông tin:
    - Từ giờ ... đến giờ
    - Room
    - Movie
    - ...
- Ticket: Quản lý vé xem phim với các thông tin:
    - Người bán
    - Suất chiếu
    - Ghế
    - Trạng thái (Đã thanh toán, đặt trước, hủy ...)
    - ...
- Transaction Payment: Quản lý các luồng thanh toán với các thông tin
    - Đối tác thanh toán
    - Ngày giờ
    - Thanh toán qua App, POS, ...
    - Trạng thái (Chờ thanh toán, đã thanh toán, thanh toán lỗi, đã hủy ....)
```

**Phân quyền:**
```
- Đội ngũ vận hành nội dung: chỉ được action trên Movie
- Đội quản lý bán vé ở rạp:
    - Manager: Sắp xếp các Room và Showing dựa trên Cinema mà họ quản lý. Kèm theo action Hủy Vé
    - Staff: Action với Ticket thông qua POS
- Đối tác cung cấp nội dung:
    - TH1: Đối tác không được phép login vào hệ thống thì sẽ làm việc offline với đội ngũ vận hành nội dung thông qua
    mail, chat, ...
    - TH2: Đối tác được phép login vào hệ thống thì sẽ được phép action edit, create trên Movie nhưng sẽ phải thông qua
    sự approve của đội ngũ vận hành nội dung
- Đối tác ví điện tử tích hợp thanh toán:
    - TH1: Đối tác không được phép login vào hệ thống thì sẽ làm việc offline với đội ngũ vận hành nội dung thông qua
    mail, chat, ...
    - TH2: Đối tác được phép login vào hệ thống thì sẽ được phép action create trên Payment nhưng sẽ phải thông qua
    sự approve của đội ngũ Admin. Create sẽ tạo ra version mới cho việc thanh toán, không cho phép edit version đã run
    để đảm bảo việc vận hành không bị gián đoạn
```

**Restful API**:
```
- getShowing: Trả về thông tin rạp - phim - suất chiếu tương ứng.
    - Input: token
    - Output: Danh sách rạp - phim - suất chiếu
- getSeat: Trả về danh sách ghế ngồi sau khi chọn suất chiếu
    - Input: token - suất chiếu
    - Output: Danh sách ghế của suất chiếu đó
- postTicket: Gửi thông tin ghế ngồi và suất chiếu để lưu trữ vé.
    - Input: token - ghế - suất chiếu
    - Output: fail - success
- payment_*: API tạo thanh toán cho các đối tác
    - Input: Data Ticket dạng json
    - Output: Redirect về các trang thanh toán
- payment_return_*: API trả kết quả thanh toán
    - Input: Data ticket đã thực hiện trên app đối tác
    - Output: Trả về thông tin vé cho khách
- payment_refund_*: Tùy đối tác mà có thêm API refund theo business
```
**API giao dịch mua vé:**
```
- Tham khảo từ: https://sandbox.vnpayment.vn/apis/docs/huong-dan-tich-hop/
- Code nằm trong phần controller/main.py
- Config nằm ở controller/__init__.py
- Odoo cung cấp sẵn việc authen cho HTTP route
```

**Report thống kê:**
>Với loại report thống kê các tác vụ bị chậm: Google Analytic là option tốt để thực hiện với các sản phẩm
    mà team dev không có cơ hội gặp end-user. Nhưng GA sẽ không work tốt với Odoo, vì đây là dạng single page application.
    Vì thế chúng ta có thể sử dụng GA Tag để detect các vấn đề. Hoặc triển khai front-end Qweb để sử dụng GA

>Với loại report thống báo lỗi daily, Graylog https://www.graylog.org/products/open-source là 1 option nên cân nhắc.

**Docker:**
>Hiện tại Docker dành cho các version của Odoo cực kỳ phổ biến trên mạng. Chúng ta có thể get trực tiếp docker image
    với lệnh: docker pull odoo.
    
>Tham khảo thêm: https://hub.docker.com/_/odoo

**CI/CD:**
>Jenkins là 1 app CI sử dụng khá tốt với việc phân quyền và automation build.

CD đề xuất:
- Bao gồm 4 môi trường chính: Local - UAT - Staging - Production
- Kết hợp giữa mô hình scrum và việc quản lý code của Git, CD có thể được thực hiện như sau
>Scrum: Chốt các task có thể release trong mỗi spring. Nếu sprint đó có task hot fix, hãy đảm bảo task đó sẽ được release trước goal của sprint.
```
- Git: Bộ source của production sẽ là source Master.
- Khi dev thực hiện code 1 task, thì mỗi task sẽ ứng với 1 branch có tên qui ước DEV/....
- Khi QC thực hiện test goal của spring thì sẽ tạo 1 branch có tên qui ước UAT/... và merge các task
sẽ release vào branch đó.
- Khi hoàn tất việc testing, PM/Team Lead sẽ tạo 1 branch tên Staging/Date để release lên staging,
kiểm tra lại lần cuối về tính tương thích giữa bản build mới và production.
Nhánh UAT đã được confirm sẽ được merge vào nhánh Staging này
Staging được kiến nghị sử dụng bản backup mới nhất của production. (mã hóa hoặc không tùy theo team)
- Final, sẽ merge nhánh staging vào master và release production. Đồng thời, nhánh staging cũng sẽ là 
nhánh backup nếu release production gặp lỗi. Nếu gặp trường hợp lỗi, chúng ta sẽ tạm release nhánh 
Staging trước đó để business vẫn work.
```