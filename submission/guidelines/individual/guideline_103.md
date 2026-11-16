# Guideline gán nhãn — v0.1 (cá nhân) — 103

- Phiên bản: v0.1
- Người viết: 103
- Loại nhãn: bounding box (hộp chữ nhật) trên ảnh đường phố
- Công cụ: CVAT, xuất COCO 1.0

---

## 1. Mục tiêu

Nhãn dùng để huấn luyện mô hình phát hiện người và phương tiện trên ảnh đường phố (ví dụ cho camera giao thông hoặc xe tự lái).
## 2. Lớp và thuộc tính

### Lớp (mỗi vật thuộc đúng một lớp)

| Lớp | Định nghĩa | Ví dụ | Phản ví dụ / dễ nhầm |
|---|---|---|---|
| `car` | Ô tô con, taxi, SUV, xe điện kín 4 bánh. | img_006, 012, 023, 040 | Bán tải thùng hở là `truck`. |
| `truck` | Xe tải, đầu kéo, xe có thùng hàng riêng, bao gồm bán tải. | img_001, 002, 007, 012, 036, 037 | Xe thùng kín cỡ nhỏ chở người là `van`. |
| `van` | Xe thùng kín cỡ nhỏ, minivan. | img_005, 016 | Xe khách nhiều hàng ghế là `bus`. |
| `bus` | Các loại xe buýt, minibus chở khách. | img_009, 031, 037, 040 | Minivan gia đình là `van`. |
| `motorcycle` | Xe máy, scooter, mô tô, quad, xe điện cưỡi; xe có sidecar tính một box. | img_006, 008, 022 | Xe ba bánh có mui là `three_wheeler`. |
| `bicycle` | Xe đạp hai bánh, kể cả xe đạp chở hàng. | img_003, 006, 010, 029 | Xích lô (3 bánh) là `three_wheeler`. |
| `three_wheeler` | Xe ba bánh: tuk-tuk, xe lam, ba gác máy, xích lô. | img_004, 016, 023, 035, 040 | Xe máy có sidecar là `motorcycle`. |
| `person` | Người ở **ngoài** thân xe: đi bộ, đứng, ngồi, người cưỡi xe máy/xe đạp, người đạp xích lô. | img_005, 014, 026, 034 | Tượng, ma-nơ-canh, người trên biển quảng cáo không phải `person`. |
| `other_vehicle` | Xe thật không thuộc các lớp trên: xe trâu bò kéo, xe đẩy, xe diễu hành tự chế. | img_019 | Xe mô hình, đồ chơi, xe điêu khắc không gán (R-11). |
| `ignore_region` | Vùng không cần gán từng vật: đám đông hoặc xe dày đặc, vật cao < 20 px, vật chỉ lộ vài điểm không xác định được lớp. | img_008, 021, 030, 032 | Vật tiền cảnh rõ trong vùng đông vẫn gán box riêng. |

Vật thật **không thuộc lớp nào** và không phải phương tiện (con vật, cột, biển báo): không gán.

### Thuộc tính

| Thuộc tính | Giá trị | Ý nghĩa và ngưỡng |
|---|---|---|
| `occluded_level` | `0`, `1`, `2`, `3` | Tỉ lệ diện tích vật bị che: `0` là ≤ 5%; `1` là > 5% và < 50%; `2` là 50% đến < 80%; `3` là ≥ 80% nhưng vẫn xác định được lớp. Không xác định được lớp thì không vẽ box, gom vào `ignore_region`. |
| `truncated` | `no`, `yes` | `yes` khi ước lượng ≥ 5% diện tích vật nằm ngoài khung hình; ngược lại `no`. |
| `can_review` | tick / không | Tick khi không chắc lớp hoặc không chắc vật có thuộc phạm vi bài, để người khác xem lại. |

## 3. Quy tắc vẽ box

- **R-01.** Gán box cho mọi người và phương tiện thật trong ảnh, mỗi vật một box riêng; các box được phép chồng lấn.
- **R-02.** Box ôm sát phần nhìn thấy của vật, không thừa nền, không cắt mất phần thấy được; vật bị che chỉ bao phần thấy được.
- **R-03.** Chọn lớp theo bảng mục 2 và đặt thuộc tính theo đúng ngưỡng.
- **R-04.** Xe chở hàng: hàng dính liền với xe thì một box bao cả xe và hàng, vì xe tự lái phải tránh cả phần hàng. Lớp là lớp của xe: bán tải chở hàng là `truck` (img_001, 012); xe máy chở ống dài là `motorcycle` (img_029); tuk-tuk chất hàng cao là `three_wheeler` (img_035); xe đạp chở rau là `bicycle` (img_010).
- **R-05.** Xe chở xe (img_002): một box `truck` bao cả xe được chở, không gán từng xe trên đó.
- **R-06.** Người trên xe: mỗi xe một box xe, mỗi người nhìn thấy rõ ở ngoài thân xe một box `person` (img_005, 026). Người ngồi trong khoang kín hoặc dưới mui (ô tô, tuk-tuk có mui) không gán.
- **R-07.** Xe ba bánh: một box bao cả thân và mui. Xe trâu bò kéo: `other_vehicle`, một box bao cả xe và con vật kéo.
- **R-08.** Dày đặc: xe hoặc người lộ đủ để xác định lớp thì vẽ box riêng, `occluded_level` theo tỉ lệ bị che; phần không xác định được thì gom vào một `ignore_region` (img_008, 019, 021, 030, 032).
- **R-09.** Vật cao < 20 px không gán từng vật, gom vào `ignore_region` (img_013, 025, 039).
- **R-10.** Vật bị cắt ở mép ảnh: box dừng ở mép ảnh, `truncated` theo ngưỡng mục 2 (img_005, 008, 012, 015, 016, 032, 034, 040).
- **R-11.** Không gán vật không thật: tượng, xe điêu khắc (img_011, 017), ma-nơ-canh (img_033), hình trên biển quảng cáo (img_018), tranh tường (img_026), bia mộ hình xe (img_027), xe mô hình và đồ chơi (img_038), phản chiếu trong gương hay kính (img_020), xe của chính mình (ego, img_020).
- **R-12.** Thiếu sáng hoặc nhoè chuyển động: xác định được lớp thì gán (img_007, 013, 031); không thì `ignore_region` (img_014, 015).

## 4. Ca khó

Các ca đã có quy tắc rõ ở mục 3 không nhắc lại.

| Ảnh | Tình huống | Rule ID | Quyết định | Lý do |
|---|---|---|---|---|
| img_002 | Đầu kéo chở 7 ô tô | R-04, R-05 | Một box `truck` bao cả xe được chở | Các ô tô được chở là hàng dính liền xe (R-04); xe tự lái cần tránh cả khối xe và hàng |
| img_028 | Bán tải thật chở tượng ngựa | R-04, R-11 | Một box `truck` bao cả tượng; không gán con ngựa | Tượng là hàng dính liền xe, không phải vật thật cần phát hiện riêng |
| img_019 | Xe diễu hành tự chế, tài xế ngồi trên xe mui trần, đám đông phía sau | R-06, R-08 | Xe `other_vehicle`; tài xế `person`; tick `can_review`; đám đông sau rào `ignore_region` | Xe thật nhưng không thuộc lớp nào; xe mui trần nên tài xế lộ ra ngoài thân xe, gán `person` theo R-06 |
| img_024 | Xe vàng đặt trên nóc xe đen, trong bảo tàng | R-11 | Xe đen `car`; xe vàng không gán, tick `can_review` trên xe đen | Không xác định được xe vàng là xe thật hay mô hình nên không gán theo R-11; `can_review` để người review kiểm tra |
| img_022 | Xe sidecar, ảnh đen trắng, nhỏ | R-03 | `motorcycle`, một box gồm cả sidecar | Sidecar gắn liền và di chuyển cùng xe máy nên tính chung một box |
| img_026 | Hai người đi xe máy thật trước tranh tường vẽ tàu thuyền | R-06, R-11 | Gán `motorcycle` và `person`; không gán gì trong tranh | Chỉ vật thật mới gán |

Ca còn mơ hồ: tick `can_review` trên box hoặc ghi vấn đề cấp ảnh. Dùng Rule ID trong nhật ký QC.

## 5. QC và phiên bản

- Mọi thay đổi làm đổi nhãn đều tăng phiên bản guideline.
- Ca mơ hồ: tick `can_review`, không tự đoán; nhóm chốt ở buổi calibration.
- Lỗi khi QC gồm 5 loại: bỏ sót, thừa, sai lớp, sai vị trí hoặc kích thước, sai thuộc tính.
- Ngưỡng đạt (giữ nguyên `rules` trong `taxonomy.json`): IoU ≥ 0,85 (vật ≥ 50 px), ≥ 0,7 (vật 20–50 px); IAA: IoU trung bình ≥ 0,85, đồng thuận lớp ≥ 95%; Release khi ≤ 2% số ảnh có lỗi.

| Phiên bản | Thay đổi | Lý do (ca nào) |
|---|---|---|
| v0 | Bản khởi đầu của giảng viên | — |
| v0.1 | Thêm `bus`, `bicycle`, `three_wheeler`, `other_vehicle`; ngưỡng `occluded_level`/`truncated`; quy tắc R-04 đến R-12 | Tuk-tuk, xích lô (img_004, 023); xe chở hàng (img_002, 029, 035); vật không thật (img_017, 027, 033, 038); đám đông (img_021, 030) |
