# Bài thực hành Tuần 2 — Nhìn thấy entropy của văn bản

## 1. Cách chạy

```bash
cd text_entropy_app
pip install -r requirements.txt
python app.py
```

Mở trình duyệt tại **http://127.0.0.1:5000**.

## 2. Kiến trúc

- `app.py` (Flask):
  - `count_letters(text)` — đếm tần suất 26 chữ cái bằng vòng lặp thủ công (không
    dùng `collections.Counter`), không phân biệt hoa/thường, bỏ qua ký tự khác.
  - `entropy_bits(counts)` — tính `H = -Σ pᵢ·log2(pᵢ)` thủ công bằng `math.log2`.
  - `caesar_encrypt(text, k)` — mã Caesar thủ công: `c = (chữ + k) mod 26`.
  - Route `POST /analyze` nhận `{text, k}`, trả về tần suất + entropy của cả bản rõ
    và bản mã.
- `templates/index.html` — giao diện: ô nhập văn bản, thanh trượt `k`, hai biểu đồ
  cột (Chart.js) vẽ tần suất 26 chữ cái của bản rõ và bản mã, kèm đường ngang 1/26.

## 3. Tự kiểm tra (đã test thủ công, đều khớp bảng trong đề)

| Đầu vào | Kết quả đo được |
|---|---|
| `"aaaaaaaa"` | H = 0.0, biểu đồ chỉ có 1 cột |
| Đủ 26 chữ, mỗi chữ 1 lần | H = 4.7004 ≈ max, biểu đồ phẳng |
| Đoạn tiếng Anh dài (508 ký tự) | H ≈ 4.24, cột "e", "t" cao nhất |
| Đoạn trên mã Caesar k=7 | H vẫn 4.24 (không đổi); đã kiểm chứng bằng code:
  `cipher_counts[(i+k) % 26] == plain_counts[i]` cho mọi i → histogram dịch đúng k ô |

## 4. Trả lời 2 câu hỏi (nháp — hãy tự chỉnh theo lời văn của bạn và chèn ảnh chụp biểu đồ thật)

**Câu 1 — Vì sao H của văn bản tiếng Anh thấp hơn 4,70? Điều đó có ích gì cho người
muốn đoán nội dung?**

Vì các chữ cái trong tiếng Anh không xuất hiện đều nhau: e, t, a, o, i, n xuất hiện
rất thường xuyên trong khi q, x, z, j cực hiếm, nên phân phối tần suất lệch hẳn khỏi
phân phối đều (mỗi chữ 1/26) — mà entropy càng thấp khi phân phối càng lệch, càng cao
khi càng đều (đạt max log2(26) khi đều tuyệt đối). Sự không đều này nghĩa là văn bản
tiếng Anh *có thể đoán được* ở một mức độ nhất định: kẻ tấn công có thể dùng phân tích
tần suất (frequency analysis) để đoán ký tự còn thiếu, nén dữ liệu hiệu quả hơn, hoặc
phá các mã thay thế đơn giản như Caesar/substitution cipher mà không cần vét cạn toàn
bộ không gian khóa.

**Câu 2 — Caesar không làm đổi H, nhưng biểu đồ bản mã khác bản rõ ở điểm nào? Từ đó
đoán khóa k như thế nào?**

Caesar cipher là một phép hoán vị (song ánh) trên tập 26 chữ cái — nó chỉ *đổi vị trí
(nhãn cột)* trong biểu đồ bằng cách dịch toàn bộ sang phải k vị trí (có vòng lại từ
z về a), chứ không làm thay đổi *tập các giá trị tần suất*; vì entropy chỉ phụ thuộc
vào tập xác suất {pᵢ}, không phụ thuộc thứ tự/nhãn của chúng, nên H giữ nguyên. Về mặt
hình ảnh, hình dạng (shape) của histogram bản mã giống hệt bản rõ nhưng toàn bộ bị
trượt ngang đúng k cột. Do đó để đoán khóa k, ta chỉ cần so khớp vị trí cột cao nhất
của bản mã (thường tương ứng với chữ phổ biến nhất trong tiếng Anh là "e") với vị trí
"e" đã biết trong bản rõ tham chiếu — độ lệch giữa hai vị trí đó chính là k. Đây chính
là cách tấn công tần suất (frequency attack) phá Caesar cipher mà không cần thử cả 26
khóa.

> Nhớ chụp ảnh màn hình biểu đồ thật (với văn bản bạn tự chọn) để đính kèm theo yêu
> cầu của đề — các con số/hình trên chỉ là kết quả test của mình để kiểm tra code
> chạy đúng.
