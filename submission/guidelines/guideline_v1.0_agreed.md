# Guideline gán nhãn — v1.0 — Thống nhất nhóm NhomC303

> Bản guideline thống nhất của nhóm **NhomC303** (thành viên `101`, `102`, `103`, `104`) đạt được sau phiên họp Pha 2, tích hợp và chuẩn hóa từ 4 bản guideline cá nhân để khóa quy tắc cho lượt gán độc lập K=2 tại Pha 3.

- Phiên bản: `v1.0`
- Ngày thống nhất: 2026-11-16
- Nhóm thực hiện: `NhomC303` (`101` Xuân Toàn, `102` Phạm Đức Mạnh, `103` Nguyễn Thị Thúy An, `104` Trương Tuấn Vũ)
- Công cụ gán nhãn: CVAT v2.74.1, xuất dữ liệu COCO 1.0

---

## 1. Mục tiêu mô hình 2D

Tập dữ liệu bounding box 2D đường phố phục vụ huấn luyện mô hình thị giác máy tính cho xe tự lái (ADAS) và camera an toàn giao thông:
- Nhận diện chính xác vị trí và lớp của phương tiện cơ giới và con người trong điều kiện giao thông ban ngày.
- **Rủi ro bỏ sót:** Bỏ sót người đi bộ hoặc xe máy dẫn đến nguy cơ va chạm giao thông nghiêm trọng.
- **Rủi ro dương tính giả:** Gán nhầm tượng trang trí, hình in quảng cáo hoặc bóng phản chiếu qua gương khiến xe tự hành phanh gấp nguy hiểm.

---

## 2. Danh mục Lớp và Thuộc tính

### 2.1. Lớp đối tượng (Classes)
| Lớp | Định nghĩa thống nhất | Ví dụ thực tế | Phản ví dụ / Lưu ý |
|---|---|---|---|
| `car` | Ô tô con 4–7 chỗ, sedan, hatchback, SUV, CUV, xe bán tải gầm thấp không nắp thùng cao. | Taxi, xe gia đình (`img_001.jpg`, `img_002.jpg`). | Xe tải nhỏ, xe van thùng kín, xe mô hình đồ chơi (`img_038.jpg`). |
| `truck` | Xe tải chở hàng có sàn/thùng hàng riêng biệt, xe đầu kéo, xe chuyên dụng. | Xe tải chở ô tô (`img_002.jpg`), xe tải chở hàng (`img_036.jpg`). | Bán tải nhỏ, xe buýt lớn. |
| `van` | Xe ô tô khoang hàng/khoang khách liền khối dạng thùng kín. | Minivan, xe giao hàng bưu chính (`img_005.jpg`). | Xe tải có cabin tách biệt, xe buýt công cộng. |
| `motorcycle` | Xe mô tô 2 bánh, xe gắn máy, xe tay ga có động cơ (kèm sidecar nếu có). | Xe máy số, xe tay ga (`img_003.jpg`, `img_026.jpg`). | Xe đạp không động cơ, xe 3 bánh xích lô (`img_029.jpg`). |
| `person` | Người thật tham gia giao thông (người đi bộ, người điều khiển hoặc hành khách trên xe hở). | Người đi bộ (`img_001.jpg`), người ngồi trên xe máy (`img_026.jpg`). | Tượng đồng/đá (`img_011.jpg`, `img_017.jpg`), ma-nơ-canh (`img_033.jpg`), người in áp phích (`img_018.jpg`). |
| `ignore_region` | Vùng đánh dấu không tách box cá thể do quá đông đúc hoặc quá xa (< 20 px). | Dòng xe quá xa ở hậu cảnh (`img_021.jpg`), đám đông dày đặc. | Người hoặc xe ở cự ly gần nhìn rõ chi tiết. |

> **Đối tượng ngoài phạm vi:**
> - Xe 3 bánh tuk-tuk (`img_004.jpg`, `img_035.jpg`), xe đạp, xe buýt: Tạm thời không gán box phương tiện nếu chưa mở rộng lớp trong taxonomy v1.0, nhưng **vẫn gán box `person`** cho người thật ngồi trên xe nếu nhìn thấy rõ.
> - Đồ vật, động vật, cây cối, mặt đường, cột đèn: Tuyệt đối không gán.

---

### 2.2. Thuộc tính định lượng (Attributes)

| Thuộc tính | Giá trị | Ngưỡng định lượng |
|---|---|---|
| `occluded_level` | `0` | Không bị che khuất (100% diện tích nhìn thấy). |
| | `1` | Bị che khuất nhẹ: từ **1% đến 30%** diện tích. |
| | `2` | Bị che khuất vừa: từ **31% đến 70%** diện tích. |
| | `3` | Bị che khuất nặng: trên **70%** nhưng còn nhận diện được (nếu che > 90% mất nhận dạng thì không gán). |
| `truncated` | `no` | Đối tượng nằm trọn vẹn trong khung hình. |
| | `yes` | Đối tượng bị cắt ngang bởi ít nhất một mép ảnh. |
| `can_review` | `true`/`false` | Bật khi phân vân ranh giới, lớp hoặc ca khó cần nhóm xem xét lại trong Pha 5. |

---

## 3. Quy tắc vẽ Bounding Box (Rule IDs)

- **`R-01` — Đối tượng thực tế (Real-world):** Chỉ gán người thật và phương tiện thật. Bỏ qua tượng đồng/đá (`img_017.jpg`), ma-nơ-canh (`img_033.jpg`), tranh in quảng cáo (`img_018.jpg`) và ảnh phản chiếu qua gương (`img_020.jpg`).
- **`R-02` — Xe chở ô tô (`img_002.jpg`):** Vẽ 1 box `truck` bao toàn bộ thân xe tải chở. Gán riêng từng box `car` cho các ô tô con nằm trên sàn xe nếu nhìn thấy rõ thân xe.
- **`R-03` — Tách người và xe máy:** Luôn vẽ 2 box độc lập: 1 box `person` (người ngồi trên xe) và 1 box `motorcycle` (khung xe máy).
- **`R-04` — Ngưỡng kích thước tối thiểu:** Bỏ qua vật có chiều cao hoặc chiều rộng `< 20 px`. Cụm vật nhỏ tập trung gom vào `ignore_region`.
- **`R-05` — Ôm sát phần nhìn thấy (Visible Extent):** Bounding box ôm khít các pixel nhìn thấy thực tế, không vẽ ước đoán phần thân bị vật khác che khuất.
- **`R-06` — Hàng hóa cồng kềnh:** Box phương tiện chỉ ôm khung vỏ kết cấu xe, không bao khối hàng hóa/bao tải chất cao vượt khổ nóc xe.

---

## 4. Bảng ca khó tiêu biểu

| Ảnh | Tình huống | Mã Rule | Quyết định thống nhất của nhóm |
|---|---|---|---|
| `img_002.jpg` | Xe tải chở 8 ô tô con hai tầng | `R-02` | Gán 1 `truck` cho xe chở + 8 box `car` riêng cho 8 xe con trên giàn. |
| `img_017.jpg` | Tượng đồng tướng quân cưỡi ngựa | `R-01` | **Không gán** (0 annotation trên ảnh). |
| `img_018.jpg` | Chân dung in trên biển pano quảng cáo | `R-01` | **Không gán**. |
| `img_020.jpg` | Xe ô tô phản chiếu qua gương chiếu hậu | `R-01` | **Không gán**. |
| `img_027.jpg` | Tượng mô hình xe bán tải trang trí | `R-01` | **Không gán**. |
| `img_035.jpg` | Xe chở bao tải hàng hóa chất cao | `R-06` | Box chỉ ôm sát thân xe, không bao khối bao tải nhô cao. |

---

## 5. Lịch sử phiên bản
| Phiên bản | Ngày | Nội dung |
|---|---|---|
| `v0` | 2026-11-16 | Khởi đầu sơ sài từ giảng viên. |
| `v1.0` | 2026-11-16 | Thống nhất từ 4 bản cá nhân: chuẩn hóa 6 lớp, định lượng 4 mức che khuất, chốt các mã quy tắc R-01 đến R-06 và bảng ca khó. Khóa đặc tả cho lượt gán Pha 3. |
