# Guideline gán nhãn — v0.1 — Thành viên 102

> Bản guideline cá nhân của thành viên **102** (Phạm Đức Mạnh) xây dựng độc lập trong Pha 1 dựa trên việc khảo sát toàn bộ 40 ảnh đường phố (`img_001.jpg` đến `img_040.jpg`), khắc phục các điểm mơ hồ của `guideline_v0_starter.md`.

- Phiên bản: `v0.1_individual_102`
- Ngày: 2026-11-16
- Người viết: `102`
- Định dạng nhãn: Bounding Box 2D (hình chữ nhật ôm sát đối tượng) trên CVAT, xuất định dạng COCO 1.0

---

## 1. Mục tiêu

Tập dữ liệu bounding box 2D này được xây dựng nhằm mục đích huấn luyện và đánh giá các mô hình học sâu phát hiện vật thể (2D Object Detection) phục vụ bài toán **Hệ thống lái xe tự động (ADAS/Autonomous Driving)** và **Camera giám sát giao thông thông minh**:
- **Tầm quan trọng:** Phát hiện chính xác vị trí, phân lớp và mức độ che khuất của các phương tiện di chuyển và người tham gia giao thông trong điều kiện đô thị ban ngày.
- **Rủi ro nguy hiểm nếu sai nhãn:**
  - *Bỏ sót (False Negative):* Bỏ sót người đi bộ hoặc xe máy đang lưu thông có thể dẫn đến nguy cơ đâm va, tai nạn thảm khốc.
  - *Gán nhầm / Dương tính giả (False Positive):* Gán nhãn các đối tượng tĩnh như tượng nghệ thuật, ma-nơ-canh, tranh quảng cáo hoặc hình phản chiếu qua gương làm xe tự hành phanh gấp bất ngờ (phantom braking), gây nguy hiểm cho các phương tiện phía sau.
  - *Box sai kích thước:* Vẽ box quá rộng (ôm cả hàng hóa cồng kềnh hoặc bóng đổ) khiến hệ thống ước lượng sai khoảng cách an toàn.

---

## 2. Lớp và thuộc tính

### 2.1. Phân loại đối tượng (Classes)
Mỗi đối tượng hợp lệ trong ảnh chỉ được gán đúng một lớp duy nhất:

| Lớp | Định nghĩa cốt lõi | Ví dụ thực tế | Phản ví dụ / Dễ nhầm lẫn |
|---|---|---|---|
| `car` | Ô tô con từ 4–7 chỗ chở người, xe bán tải gầm thấp không gắn thùng cao. | Sedan, hatchback, SUV, CUV, xe taxi (`img_001.jpg`, `img_002.jpg`). | Xe tải nhỏ, xe van thùng kín, xe chở hàng, ô tô đồ chơi (`img_038.jpg`). |
| `truck` | Xe tải chở hàng có thùng hở/thùng kín, xe bồn, xe đầu kéo kéo rơ-moóc hoặc xe chuyên dụng. | Xe tải chở ô tô (`img_002.jpg`), xe tải nhỏ chở hàng (`img_001.jpg`). | Xe bán tải nhỏ không thùng hàng, xe buýt lớn. |
| `van` | Xe ô tô chở người hoặc hàng cỡ trung có thân thùng liền khối dạng kín. | Minivan, xe van giao hàng, xe cứu thương. | Xe buýt lớn chở khách (`img_009.jpg`), xe tải có thùng rời. |
| `bus` | Xe khách lớn hoặc xe buýt công cộng từ 16 chỗ ngồi trở lên. *(Đề xuất bổ sung thay cho v0)* | Xe buýt công cộng, xe khách liên tỉnh (`img_009.jpg`, `img_031.jpg`, `img_040.jpg`). | Xe van nhỏ 7 chỗ, xe tải chở người. |
| `tuk_tuk` | Phương tiện giao thông cơ giới 3 bánh có động cơ chở khách hoặc chở hàng. *(Đề xuất bổ sung)* | Xe tuk-tuk Thái Lan, xe ba gác máy chở hàng (`img_004.jpg`, `img_016.jpg`, `img_035.jpg`). | Xe xích lô đạp chân (`img_029.jpg`), xe máy 2 bánh. |
| `motorcycle` | Xe mô tô 2 bánh, xe gắn máy, xe tay ga chạy bằng động cơ xăng hoặc điện. | Xe máy số, xe tay ga, mô tô phân khối lớn (`img_003.jpg`, `img_008.jpg`). | Xe đạp không động cơ (`img_006.jpg`), xe xích lô, xe máy điện 3 bánh. |
| `person` | Người thật đang tham gia giao thông (đi bộ, đứng, hoặc đang ngồi/điều khiển trên phương tiện hở). | Người đi bộ trên vỉa hè (`img_001.jpg`), người điều khiển xe máy/tuk-tuk. | Tượng người bằng đồng/đá (`img_011.jpg`, `img_017.jpg`), ma-nơ-canh (`img_033.jpg`), người in trên biển quảng cáo (`img_018.jpg`). |
| `ignore_region` | Vùng đánh dấu không cần tách box đối tượng do mật độ quá dày đặc hoặc quá xa. | Đám đông dày đặc chen chúc ở hậu cảnh, cụm xe đậu quá xa có chiều cao `< 20 px`. | Xe hoặc người riêng lẻ nhìn rõ bộ phận. |

> **Xử lý đối tượng ngoài danh mục:**
> - Xe đạp không động cơ, xe xích lô đạp chân (`img_006.jpg`, `img_029.jpg`, `img_039.jpg`): Không gán nhãn phương tiện, chỉ gán nhãn `person` cho người đạp xe nếu nhìn thấy rõ.
> - Đồ vật, động vật, nhà cửa, cây cối, cột đèn: Tuyệt đối không gán nhãn.

---

### 2.2. Thuộc tính (Attributes) với ngưỡng định lượng

Toàn bộ 3 thuộc tính áp dụng cho từng bounding box phải được xác định dựa trên ranh giới định lượng cụ thể:

| Thuộc tính | Kiểu dữ liệu | Giá trị | Ngưỡng đo lường và Ý nghĩa cụ thể |
|---|---|---|---|
| `occluded_level` | Select | `0` | **Không bị che khuất:** 100% diện tích nhìn thấy rõ, không bị vật khác cản trở tầm nhìn. |
| | | `1` | **Che khuất nhẹ:** Bị vật khác (xe khác, người, cây cối, rào chắn) che từ **1% đến 30%** diện tích bề mặt. |
| | | `2` | **Che khuất vừa:** Bị che khuất từ **31% đến 70%** diện tích bề mặt. |
| | | `3` | **Che khuất nặng:** Bị che khuất **> 70%** diện tích bề mặt nhưng các đặc điểm nhận dạng cốt lõi vẫn đủ để người gán nhận diện chắc chắn. (Nếu che > 90% không còn nhận dạng được thì không gán). |
| `truncated` | Select | `no` | **Nguyên vẹn:** Toàn bộ đối tượng nằm hoàn toàn bên trong khung ảnh. |
| | | `yes` | **Bị cắt mép:** Đối tượng bị cắt ngang bởi ít nhất một trong 4 mép viền của bức ảnh (trên, dưới, trái, phải). |
| `can_review` | Checkbox | `false` / `true` | Đánh dấu `true` khi người gán lưỡng lự về lớp, ranh giới hoặc trường hợp biên chưa được quy tắc nêu rõ, cần đưa ra thảo luận nhóm tại Pha 2. |

---

## 3. Quy tắc vẽ Bounding Box

- **R-01 — Đối tượng thực tế (Real-world only):** Chỉ gán nhãn cho người và phương tiện cơ giới thật đang tham gia hoặc lưu thông trên đường. Tuyệt đối **không gán**:
  - Tượng người, tượng phương tiện bằng đồng, đá, xi măng (`img_011.jpg`, `img_017.jpg`, `img_027.jpg`).
  - Ma-nơ-canh, búp bê, đồ chơi trong tủ kính hoặc trên vỉa hè (`img_033.jpg`, `img_038.jpg`).
  - Hình vẽ, tranh ảnh người/xe in trên biển quảng cáo, áp phích (`img_018.jpg`).
  - Ảnh phản chiếu của người/xe qua gương chiếu hậu hoặc kính cửa sổ sổ (`img_020.jpg`).
- **R-02 — Xe chở phương tiện khác (Car carrier truck - `img_002.jpg`):**
  - Gán 1 box `truck` bao trọn thân xe tải chở hàng (bao gồm cabin và toàn bộ giàn sàn xe chở).
  - Gán từng box `car` độc lập cho từng ô tô con nằm trên sàn xe nếu nhìn thấy rõ thân xe (đánh dấu `occluded_level=1` hoặc `2` tùy mức che khuất bởi giàn kim loại).
- **R-03 — Người điều khiển xe máy (Rider on motorcycle):**
  - Luôn tách biệt thành **2 box độc lập**:
    - 1 box `person`: Ôm trọn người lái/người ngồi sau (từ đỉnh mũ bảo hiểm đến hết phần chân người nhìn thấy).
    - 1 box `motorcycle`: Ôm trọn khung xe máy (từ đầu xe, bánh trước đến đuôi xe, bánh sau).
- **R-04 — Ôm sát phần nhìn thấy (Visible extent only):**
  - Bounding box phải ôm khít các pixel nhìn thấy thực tế của vật thể.
  - Không vẽ dự đoán phần thân xe hoặc chân người bị che khuất phía sau chướng ngại vật.
- **R-05 — Ngưỡng kích thước tối thiểu (Min size threshold):**
  - Bỏ qua các đối tượng có chiều cao hoặc chiều rộng `< 20 px`.
  - Nếu ở hậu cảnh có cụm phương tiện hoặc cụm người quá nhỏ nằm sát nhau, bao toàn bộ cụm đó bằng 1 box `ignore_region`.
- **R-06 — Ranh giới hàng hóa cồng kềnh (`img_035.jpg`):**
  - Với xe tuk-tuk hoặc xe tải chở hàng hóa chất cao vượt khổ thùng: Bounding box chỉ ôm trọn khung thân vỏ của phương tiện, không kéo bao cả các khối bao tải/hàng hóa cồng kềnh nhô lên cao phía trên.

---

## 4. Bảng ca khó khảo sát qua 40 ảnh

Dưới đây là 8 tình huống biên tiêu biểu phát hiện được trong 40 ảnh gốc mà `guideline_v0_starter.md` chưa xử lý:

| Ảnh | Tình huống phát hiện | Đề xuất Rule ID | Quyết định ban đầu của cá nhân 102 | Lý do đề xuất |
|---|---|---|---|---|
| `img_002.jpg` | Xe tải dài chở 8 ô tô con trên hai tầng sàn giàn thép | `R-02` | Gán 1 box `truck` cho xe kéo + gán đủ 8 box `car` riêng cho 8 ô tô con trên sàn. | Xe con là đối tượng độc lập có nguy cơ rơi hoặc tách rời; mô hình tự hành cần nhận biết cả tải trọng xe con. |
| `img_004.jpg`, `img_035.jpg` | Xe 3 bánh tuk-tuk chở khách và chở bao tải hàng hóa cồng kềnh | `R-05`, `R-06` | Bổ sung lớp `tuk_tuk`; box chỉ ôm thân xe, không bao khối bao tải nhô cao. | v0 không có lớp xe 3 bánh; ôm hàng hóa sẽ làm sai lệch kích thước hình học của xe. |
| `img_009.jpg`, `img_031.jpg` | Xe buýt chở khách công cộng cỡ lớn | `R-05` | Bổ sung lớp `bus` vào danh mục classes. | Xe buýt có kích thước và hành vi dừng đón trả khách khác hẳn xe tải `truck` hay xe con `car`. |
| `img_017.jpg` | Tượng đồng tướng quân cưỡi ngựa đặt trên bệ đá công viên | `R-01` | **Không gán box** (0 annotation trên ảnh). | Đây là tượng nghệ thuật tĩnh, không tham gia giao thông; gán `person` sẽ gây dương tính giả cho ADAS. |
| `img_018.jpg` | Hình chân dung người in trên tấm pano áp phích quảng cáo | `R-01` | **Không gán box**. | Hình in 2D trên biển hiệu tĩnh, không phải người thật lưu thông. |
| `img_020.jpg` | Phương tiện phản chiếu qua mặt gương chiếu hậu | `R-01` | **Không gán box**. | Ảnh ảo phản chiếu qua gương, gán nhãn sẽ khiến mô hình phán đoán sai tọa độ thực tế phía trước. |
| `img_027.jpg` | Mô hình xe bán tải bằng đá/kim loại đặt trang trí | `R-01` | **Không gán box**. | Tượng trang trí bất động ngoài vỉa hè. |
| `img_037.jpg` | Xe bán tải lắp thêm nắp thùng cao ngang nóc cabin | `R-05` | Tạm thời gán `van`, đánh dấu cờ `can_review=true`. | Ranh giới giữa `van` và `truck` thùng kín bị nhập nhằng, cần đưa ra họp nhóm Pha 2 để chốt chung. |

---

## 5. Kiểm soát chất lượng (QC) và Lịch sử phiên bản

- **Ngưỡng kiểm soát chất lượng cam kết:**
  - Độ bao phủ gán nhãn: Đảm bảo 100% số ảnh được phân công tại Pha 3.
  - Sai số tọa độ: Bounding box ôm sát mép ngoài nhìn thấy trong phạm vi `<= 2 px`.
  - Phân định thuộc tính: Tuân thủ đúng ngưỡng % che khuất tại Mục 2.2.
- **Quy trình xử lý ca mơ hồ:** Khi gặp tình huống chưa có trong guideline, người gán tick chọn `can_review=true` và lưu lại mã ảnh để mang ra phiên họp Calibration của nhóm.

### Lịch sử thay đổi:
| Phiên bản | Ngày | Nội dung thay đổi | Cơ sở / Tình huống ảnh |
|---|---|---|---|
| `v0` | 2026-11-16 | Bản starter khởi đầu từ giảng viên. | Chỉ có 5 lớp cơ bản, thiếu định nghĩa xe đặc thù và ngưỡng đo thuộc tính. |
| `v0.1_individual_102` | 2026-11-16 | Khảo sát 40 ảnh; đề xuất bổ sung lớp `bus`, `tuk_tuk`; định lượng 4 mức `occluded_level`; chốt quy tắc R-01 đến R-06 và bảng 8 ca khó. | Các ảnh `img_002`, `img_004`, `img_009`, `img_017`, `img_020`, `img_035`... |
