# Mâm Cơm Hôm Nay — hướng dẫn dùng

## Trong thư mục này có gì

| Tệp | Dùng để |
|---|---|
| `docs/` | Bản đưa lên mạng: mở bằng đường link trên mọi điện thoại, cài ra màn hình chính, dùng được khi mất mạng |
| `mam_com_hom_nay.html` | Cùng nội dung, một file duy nhất, mở bằng Chrome không cần mạng |
| `cap_nhat_gia.py` | Đọc giá chợ mới trên gia247.com rồi ghi vào cả hai bản trên |
| `kiem_du_lieu.py` | Kiểm dữ liệu món ăn sau khi sửa tay |
| `.github/workflows/cap_nhat_gia.yml` | Cho GitHub tự chạy cập nhật giá lúc 6 giờ sáng mỗi ngày |

## Vì sao gửi qua Zalo chỉ thấy giao diện

Zalo mở file HTML bằng trình xem riêng. Trình xem đó tắt JavaScript, nên chỉ hiện chữ và nút mà không bấm được.
Ứng dụng giờ hiện một dòng đỏ báo việc này khi bị chặn.

Có hai cách, cách 1 tiện hơn nhiều.

## Cách 1 — Đưa lên mạng bằng GitHub Pages (miễn phí, giá tự cập nhật)

Làm một lần trên máy tính, khoảng 10 phút.

1. Tạo tài khoản ở github.com nếu chưa có.
2. Bấm dấu **+** góc trên, chọn **New repository**. Đặt tên, ví dụ `mam-com`. Chọn **Public**. Bấm **Create repository**.
3. Bấm **uploading an existing file**. Kéo thả vào: thư mục `docs`, `mam_com_hom_nay.html`, `cap_nhat_gia.py`, `kiem_du_lieu.py`. Bấm **Commit changes**.
4. Trình duyệt thường bỏ qua thư mục ẩn `.github`, nên tạo tệp tự cập nhật bằng tay: bấm **Add file → Create new file**, gõ tên `.github/workflows/cap_nhat_gia.yml`, dán nội dung tệp cùng tên trong thư mục này, bấm **Commit**.
5. Vào **Settings → Pages**. Mục **Branch** chọn `main` và thư mục `/docs`. Bấm **Save**.
6. Đợi 1–2 phút, trang hiện đường link dạng `https://<tên-tài-khoản>.github.io/mam-com/`.
7. Vào **Settings → Actions → General**, mục **Workflow permissions** chọn **Read and write permissions**, bấm **Save**. Không bật thì GitHub đọc được giá mà không ghi vào ứng dụng được.

Gửi đường link đó qua Zalo. Trên điện thoại:

- **Android:** mở link bằng Chrome, bấm menu ba chấm, chọn **Thêm vào màn hình chính** hoặc **Cài đặt ứng dụng**.
- **iPhone:** mở link bằng Safari, bấm nút chia sẻ, chọn **Thêm vào MH chính**.

Sau lần mở đầu tiên, ứng dụng chạy được cả khi mất mạng. Khi có mạng nó tự lấy bản có giá mới nhất.

## Cách 2 — Dùng file, không cần mạng

- **Android:** tải file `mam_com_hom_nay.html` về máy. Mở ứng dụng **Tệp** hoặc **Quản lý tệp**, bấm giữ file, chọn **Mở bằng → Chrome**.
- **iPhone:** iPhone không cho mở file HTML có chương trình bên trong. Dùng cách 1.

Muốn giá mới thì chạy `python cap_nhat_gia.py` trên máy tính rồi gửi lại file.

## Cập nhật giá bằng tay trên máy tính

```bash
python cap_nhat_gia.py --thu
```

Lệnh trên chỉ in bảng giá cũ và mới để xem trước. Bỏ `--thu` để ghi thật.

Giá lấy từ gia247.com vì đây là trang duy nhất đã thử mà trả giá dạng đọc được. Kingfoodmart, AEON, GO, WinMart, Bách Hóa Xanh chỉ hiện giá sau khi chọn cửa hàng trên trình duyệt, chương trình không đọc được.

Bảng rau củ và hải sản trên trang là giá chợ đầu mối, nên chương trình nhân thêm hệ số bán lẻ: rau củ 1,4 lần, hải sản 1,15 lần. Sửa hai con số này ở đầu `cap_nhat_gia.py` nếu thấy chưa sát. Giá nào lệch quá 2,5 lần so với giá cũ sẽ bị bỏ qua và in ra để kiểm.

Nguyên liệu không có trên trang, như gia vị, đậu phụ, trứng, giữ nguyên giá cũ. Anh sửa được từng giá trong tab **Giá chợ** trên điện thoại, máy tự nhớ.

## Sau khi sửa món ăn bằng tay

```bash
python kiem_du_lieu.py
```

Phải ra `KET QUA: KHONG CO LOI`. Sửa `docs/index.html` xong thì chép đè sang `mam_com_hom_nay.html` để hai bản giống nhau.
