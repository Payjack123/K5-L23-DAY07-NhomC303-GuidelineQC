# Guideline gán nhãn 2D — v0.1 — Thành viên 102

> **Bản dự thảo cá nhân của thành viên 102** xây dựng độc lập trong Pha 1 dựa trên việc khảo sát toàn bộ 40 ảnh thực tế (`data/images/img_001.jpg` đến `img_040.jpg`), khắc phục triệt để các điểm mơ hồ, thiếu định lượng của `guideline_v0_starter.md` để chuẩn bị cho buổi họp thống nhất nhóm tại Pha 2.

- **Phiên bản:** `v0.1_individual_102`
- **Mã thành viên:** `102`
- **Ngày lập:** 2026-11-16
- **Phạm vi dữ liệu:** 40 ảnh giao thông đường phố (`img_001.jpg` – `img_040.jpg`)
- **Công cụ & Định dạng:** CVAT Rectangle, xuất chuẩn COCO 1.0 (Bounding Box 2D `[x, y, width, height]`)

---

## 1. Mục tiêu và Giới hạn sử dụng

Nhãn bounding box 2D được xây dựng nhằm mục đích huấn luyện và đánh giá các mô hình học sâu phát hiện vật thể (2D Object Detection) phục vụ bài toán **Hệ thống lái xe tự động (ADAS / Autonomous Driving)** và **Camera giám sát giao thông thông minh**:
- **Yêu cầu cốt lõi:** Định vị chính xác ranh giới nhìn thấy, phân loại đúng đối tượng thực tế và định lượng mức độ che khuất của người cùng các phương tiện đang tham gia giao thông.
- **Phân tích rủi ro an toàn nếu sai lệch nhãn:**
  - *Bỏ sót đối tượng (False Negative):* Bỏ sót người đi bộ, người điều khiển xe máy hoặc xe đạp đang lưu thông dẫn đến việc hệ thống tự hành không kích hoạt phanh khẩn cấp, gây ra tai nạn giao thông nghiêm trọng.
  - *Dương tính giả (False Positive):* Gán nhãn cho các vật không có khả năng di chuyển hoặc không phải vật thể thật (tượng nghệ thuật, ma-nơ-canh, tranh ảnh pano quảng cáo, hình phản chiếu qua gương kính) khiến hệ thống nhận nhầm là chướng ngại vật thực tế, dẫn đến hiện tượng phanh gấp bất ngờ (*phantom braking*), gây tai nạn dồn toa cho xe phía sau.
  - *Sai lệch ranh giới hình học (Bounding Box ôm sai):* Vẽ box quá rộng (ôm cả hàng hóa cồng kềnh chất vượt nóc, ôm bóng đổ) làm sai lệch ước lượng khoảng cách không gian 3D và sai lệch tâm hình học của phương tiện; ngược lại vẽ box cắt xén phần nhìn thấy làm mô hình học sai hình dạng phương tiện.

---

## 2. Lớp và Thuộc tính

Phép thử phân định: *"Mô hình học máy có cần dự đoán thuộc tính này độc lập không?"* Nếu có $\rightarrow$ đưa vào Danh mục Lớp (`classes`). Nếu chỉ dùng phục vụ lọc dữ liệu, đánh giá độ khó hoặc kiểm soát chất lượng (QC) $\rightarrow$ đưa vào Thuộc tính (`attributes`).

### 2.1. Phân loại đối tượng (Classes)

Mỗi vật thể hợp lệ trong ảnh chỉ thuộc đúng **một** lớp duy nhất. Thành viên 102 đề xuất danh mục lớp cho Pha 1:

| Lớp | Định nghĩa thao tác (một câu) | Ví dụ từ tập 40 ảnh | Phản ví dụ / Dễ nhầm lẫn |
|---|---|---|---|
| `car` | Ô tô con từ 4–7 chỗ chở người, xe taxi, sedan, hatchback, SUV, wagon và xe bán tải (pickup) gầm thấp. | `img_001.jpg` (pickup đỗ), `img_002.jpg` (ô tô trên sàn giàn), `img_006.jpg`, `img_040.jpg`. | Xe tải chở hàng (`truck`), xe van khoang kín, xe mô hình đồ chơi (`img_038.jpg`). |
| `truck` | Xe tải chở hàng có thùng riêng, xe bồn, xe đầu kéo chuyên dụng hoặc xe kéo giàn chở ô tô. | `img_002.jpg` (xe đầu kéo chở ô tô), `img_007.jpg` (xe tải giao hàng ban đêm), `img_036.jpg`. | Xe bán tải nhẹ cá nhân (102 xếp vào `car`), xe buýt chở khách (`bus`). |
| `van` | Xe ô tô chở người hoặc hàng cỡ trung có khoang lái và khoang hàng sau liền một thân khối kín. | `img_005.jpg`, `img_015.jpg`, `img_016.jpg`. | Xe buýt lớn (`img_009.jpg`), xe tải có thùng rời cabin. |
| `bus` *(Đề xuất thêm)* | Xe buýt công cộng, xe khách liên tỉnh từ 16 chỗ ngồi trở lên phục vụ chở nhiều hành khách. | `img_009.jpg` (xe khách du lịch), `img_031.jpg` (xe buýt đêm), `img_032.jpg`, `img_040.jpg`. | Xe van nhỏ 7 chỗ, xe tải chở công nhân. |
| `tuk_tuk` *(Đề xuất thêm)* | Phương tiện cơ giới 3 bánh có động cơ dùng để chở khách hoặc chở hàng (xe lam, tuk-tuk, xe ba gác máy). | `img_004.jpg` (tuk-tuk xanh), `img_016.jpg`, `img_023.jpg`, `img_035.jpg` (xe 3 bánh chở bao hàng). | Xe xích lô đạp chân (`img_006.jpg`, `img_029.jpg`), xe máy 2 bánh. |
| `motorcycle` | Phương tiện 2 bánh có động cơ: xe gắn máy, xe tay ga, mô tô phân khối lớn, xe mô tô có sidecar gắn kèm. | `img_003.jpg`, `img_005.jpg`, `img_008.jpg`, `img_022.jpg` (sidecar), `img_026.jpg`, `img_030.jpg`. | Xe đạp không động cơ (`img_006.jpg`, `img_010.jpg`, `img_039.jpg`), xe ba bánh cơ giới. |
| `person` | Con người thật đang tham gia giao thông: người đi bộ, đứng, ngồi vỉa hè hoặc đang điều khiển phương tiện hở. | `img_001.jpg` (khách & người đứng), `img_005.jpg` (người đi xe máy), `img_014.jpg`, `img_026.jpg`, `img_034.jpg`. | Tượng đồng (`img_011.jpg`, `img_017.jpg`), ma-nơ-canh (`img_033.jpg`), hình in áp phích (`img_018.jpg`). |
| `ignore_region` | Vùng đánh dấu không tách riêng từng vật do khoảng cách quá xa ($< 20\text{ px}$) hoặc mật độ quá dày đặc. | `img_008.jpg`, `img_021.jpg`, `img_025.jpg` (người đi dạo ở xa), `img_030.jpg`, `img_032.jpg`. | Người hoặc phương tiện riêng lẻ nhìn rõ bộ phận và cao $\ge 20\text{ px}$. |

> **Xử lý đối tượng ngoài danh mục (Out-of-scope objects):**
> - *Xe đạp không động cơ, xe xích lô đạp chân (`img_006.jpg`, `img_010.jpg`, `img_029.jpg`, `img_039.jpg`):* v0 và danh mục cá nhân 102 chưa có lớp `bicycle`. **Quy tắc của 102:** Không gán nhãn cho phương tiện thô sơ, nhưng **bắt buộc gán nhãn `person`** cho người đạp xe/lái xích lô nếu nhìn rõ và cao $\ge 20\text{ px}$.
> - *Xe đẩy tay, xe diễu hành đồ chơi (`img_010.jpg`, `img_019.jpg`):* Không gán nhãn xe; gán `person` cho người điều khiển nếu nhận diện rõ.
> - *Đồ vật tĩnh, con vật, cây cối, cột đèn, biển báo, rào chắn:* Tuyệt đối không gán nhãn.

---

### 2.2. Thuộc tính (Attributes) với Ngưỡng định lượng

Mỗi bounding box hợp lệ (trừ vùng `ignore_region`) phải được gán đủ 3 thuộc tính đo lường khách quan:

| Thuộc tính | Kiểu | Giá trị | Định nghĩa và Ngưỡng đo lường cụ thể |
|---|---|---|---|
| `occluded_level` | `select` | `0` | **Không bị che khuất:** Diện tích nhìn thấy đạt từ $95\%$ đến $100\%$, vật thể hoàn toàn nguyên vẹn trong tầm quan sát. |
| | | `1` | **Che khuất nhẹ:** Bị vật khác (xe khác, người, cây cối, rào chắn) che khuất từ $> 5\%$ đến $30\%$ diện tích bề mặt ước tính. |
| | | `2` | **Che khuất vừa:** Bị che khuất từ $> 30\%$ đến $70\%$ diện tích bề mặt ước tính. |
| | | `3` | **Che khuất nặng:** Bị che khuất $> 70\%$ diện tích bề mặt, nhưng phần còn lại vẫn đủ đặc trưng cốt lõi để nhận dạng chắc chắn phân lớp. *(Nếu bị che $> 90\%$ không thể nhận dạng chắc chắn thì không vẽ box mà gom vào `ignore_region`)*. |
| `truncated` | `select` | `no` | **Nguyên vẹn:** Toàn bộ vật thể nằm gọn bên trong khung hình (phần bị viền ảnh cắt $< 5\%$ diện tích). |
| | | `yes` | **Bị mép ảnh cắt:** Vật thể bị ít nhất một trong bốn mép ảnh (trên, dưới, trái, phải) cắt ngang làm mất từ $\ge 5\%$ diện tích ước tính. |
| `can_review` | `checkbox` | `false` / `true` | Đánh dấu `true` khi người gán còn phân vân về lớp đối tượng, ranh giới hình học hoặc gặp trường hợp biên chưa được guideline định nghĩa rõ, cần đưa ra nhóm hội ý tại Pha 2. |

---

## 3. Quy tắc vẽ Bounding Box

- **R-01 · Chỉ gán đối tượng thực tế (Real-world only):** Chỉ gán nhãn cho người thật và phương tiện thật đang tham gia lưu thông hoặc đỗ trên đường phố. Tuyệt đối loại bỏ:
  - Tượng điêu khắc bằng kim loại, đồng, đá, xi măng (`img_011.jpg`, `img_017.jpg`).
  - Bia mộ tưởng niệm mô phỏng hình xe (`img_027.jpg`).
  - Ma-nơ-canh, hình nộm trưng bày trong cửa hiệu hoặc vỉa hè (`img_033.jpg`).
  - Đồ chơi, mô hình thu nhỏ trưng bày trong tủ kính (`img_038.jpg`).
  - Tranh vẽ, hình ảnh chân dung người/xe in 2D trên biển pano quảng cáo (`img_018.jpg`, `img_026.jpg`).
  - Ảnh ảo phản chiếu qua gương chiếu hậu xe hoặc mặt kính tòa nhà (`img_020.jpg`).
  - Xe của chính người chụp (ego-vehicle) chỉ lộ nắp capo mờ mép dưới ảnh.
- **R-02 · Box ôm sát phần nhìn thấy (Tight visible extent):**
  - Bounding box là hình chữ nhật nhỏ nhất bao trọn toàn bộ các pixel nhìn thấy thực tế của vật thể.
  - Không vẽ suy đoán hoặc kéo dài box qua phần bị vật cản che khuất.
  - Mũ bảo hiểm đang đội trên đầu thuộc box `person`; gương chiếu hậu gắn trên thân xe thuộc box xe.
  - Bóng đổ của phương tiện trên mặt đường và các vật dụng xách tay nhỏ (túi xách, điện thoại) không được tính vào bounding box.
- **R-03 · Tách biệt người và phương tiện (Separation of person and vehicle):**
  - Đối với xe máy (`motorcycle`), xe đạp, xe xích lô: Luôn vẽ **box riêng** cho từng người (`person`) và **box riêng** cho phương tiện. Các box được phép chồng lấn tự nhiên.
  - Xe máy chở 2–3 người: Vẽ 1 box `motorcycle` cho xe và vẽ độc lập 2–3 box `person` cho từng người ngồi trên xe (`img_005.jpg`, `img_026.jpg`).
- **R-04 · Người ngồi trong khoang kín / dưới mui xe:**
  - Người ngồi bên trong khoang kín của ô tô (`car`), xe tải (`truck`), xe van (`van`) hoặc ngồi dưới mui che kín của xe tuk-tuk (`img_004.jpg`, `img_016.jpg`): **Không gán box `person`**, coi người là một phần bên trong cấu trúc phương tiện.
  - Người điều khiển xe trên phương tiện hở không mui (xe máy, xe đạp, xe tải mui trần) hoặc ngồi nhô hẳn thân trên ra ngoài: **Bắt buộc gán box `person`**.
- **R-05 · Ranh giới phương tiện chở hàng cồng kềnh (`img_029.jpg`, `img_035.jpg`):**
  - *Quan điểm đề xuất của cá nhân 102:* Bounding box chỉ ôm trọn khung thân vỏ kết cấu cơ khí của phương tiện, **không kéo box bao phủ khối bao tải hoặc bó hàng cồng kềnh nhô cao vút**. Lý do: Việc kéo box ôm khối hàng dị hình sẽ làm biến dạng tỷ lệ khung hình (aspect ratio) chuẩn của phương tiện, gây nhiễu cho mô hình học nhận dạng thân xe. *(Đề xuất mang ra thảo luận tại Pha 2)*.
- **R-06 · Xe chuyên dụng chở xe khác (Car carrier truck - `img_002.jpg`):**
  - Gán 1 box `truck` bao toàn bộ thân xe đầu kéo cùng toàn bộ giàn sàn thép chở hàng.
  - Đồng thời gán từng box `car` riêng biệt cho mỗi ô tô con nằm trên giàn thép nếu nhìn thấy rõ các đường nét thân xe và chiều cao box đạt $\ge 20\text{ px}$. Gán thuộc tính `occluded_level=1` hoặc `2` tương ứng với phần bị khung giàn thép che khuất.
- **R-07 · Ngưỡng kích thước tối thiểu và Vùng bỏ qua (`ignore_region`):**
  - Đối tượng có chiều cao phần nhìn thấy $< 20\text{ px}$ trên ảnh gốc: Không gán box đối tượng cá thể.
  - Các cụm phương tiện hoặc dòng người ở cự ly quá xa, dày đặc đan xen không thể tách biệt chính xác ranh giới từng người (`img_008.jpg`, `img_021.jpg`, `img_025.jpg`, `img_030.jpg`): Bao toàn bộ cụm đó bằng một hình chữ nhật gán nhãn `ignore_region`. Vùng này vẽ sát cụm đối tượng, không trùm lên các đối tượng tiền cảnh rõ ràng đã được vẽ box riêng.
- **R-08 · Điều kiện thiếu sáng, thời tiết xấu (`img_007.jpg`, `img_013.jpg`, `img_014.jpg`):**
  - Trong điều kiện trời mưa, đường ướt phản quang hoặc ban đêm thiếu sáng, nếu mắt người vẫn nhận dạng được hình bóng và phân loại chắc chắn phương tiện thì vẫn tiến hành vẽ box ôm sát phần nhìn thấy và tick `can_review=true` nếu còn do dự. Nếu chỉ thấy vệt đèn mờ ảo không xác định được hình dạng thân xe thì không vẽ box.

---

## 4. Bảng phân tích Ca khó qua khảo sát 40 ảnh

Bảng tổng hợp 12 tình huống biên cụ thể trong bộ 40 ảnh thực tế mà `guideline_v0_starter.md` bỏ sót hoặc gây hiểu lầm, kèm lập luận đề xuất của thành viên 102:

| STT | Ảnh | Tình huống thực tế phát hiện | Mã Rule | Quyết định ban đầu của 102 | Lập luận kỹ thuật / Lý do đề xuất |
|:---:|---|---|:---:|---|---|
| 1 | `img_001.jpg` | Xe bán tải (pickup) màu bạc đỗ bên ngoài quán ăn lúc chạng vạng tối. | `R-02` | Gán `car`, gán đủ người ngồi ăn trên vỉa hè (`person`). | 102 phân loại pickup theo kích thước khung gầm và mục đích chở người dân dụng tương đương SUV/xe con. |
| 2 | `img_002.jpg` | Xe đầu kéo dài chở 7–8 ô tô con trên hai tầng giàn khung thép. | `R-06` | Gán 1 box `truck` bao cả xe chở, đồng thời gán từng box `car` riêng cho từng xe trên sàn. | Từng ô tô con là vật thể có nguy cơ rơi rớt độc lập; mô hình ADAS cần phát hiện vị trí từng ô tô con để tránh va chạm. |
| 3 | `img_004.jpg`, `img_016.jpg` | Xe tuk-tuk màu xanh đỗ trên phố; có hành khách ngồi trong khoang sau. | `R-04` | Bổ sung lớp `tuk_tuk`; người ngồi dưới mui không gán `person`. | Xe 3 bánh là phương tiện đặc thù đô thị châu Á; người dưới mui là khối liền với xe, không tách rời như xe máy. |
| 4 | `img_006.jpg`, `img_034.jpg`, `img_039.jpg` | Đoàn xích lô đạp chở khách du lịch trên đường phố Huế. | `R-03` | Không gán box xe xích lô (do chưa có lớp); gán box `person` cho người lái và người ngồi. | v0 thiếu lớp xe thô sơ; nhưng người thật tham gia giao thông bắt buộc phải được phát hiện để tránh tai nạn. |
| 5 | `img_009.jpg`, `img_031.jpg`, `img_040.jpg` | Xe buýt lớn chở khách, xe buýt đô thị lưu thông ban ngày và ban đêm. | `R-02` | Bổ sung lớp `bus` vào danh mục classes. | Xe buýt có kích thước cồng kềnh, điểm mù rộng và quỹ đạo dừng đỗ đón khách khác biệt hoàn toàn với `car` hay `truck`. |
| 6 | `img_011.jpg`, `img_017.jpg` | Tượng đồng nhân vật giả tưởng (`img_011`) và tượng tướng quân cưỡi ngựa đá (`img_017`). | `R-01` | **Tuyệt đối không gán box** (ảnh `img_017` giữ 0 annotation). | Tượng nghệ thuật bất động, không tham gia giao thông; gán `person` sẽ gây dương tính giả, làm xe tự hành phanh oan. |
| 7 | `img_018.jpg` | Tấm biển pano áp phích quảng cáo tranh cử in hình chân dung ứng viên. | `R-01` | **Không gán box**. | Hình ảnh in 2D trên mặt phẳng tĩnh, không có thể tích 3D thực tế trong không gian giao thông. |
| 8 | `img_020.jpg` | Cầu vồng và các phương tiện phản chiếu rõ nét qua mặt gương chiếu hậu ô tô. | `R-01` | **Không gán box**. | Đây là ảnh ảo quang học phản chiếu phía sau; gán nhãn sẽ làm mô hình ước tính sai vị trí vật thể phía trước mũi xe. |
| 9 | `img_024.jpg` | Xe ô tô station wagon màu đen, trên nóc có đặt một mô hình xe ô tô con màu vàng. | `R-01` | Gán `car` cho xe đen; xe vàng nhỏ trên nóc không gán, tick `can_review=true`. | Không có bằng chứng khẳng định xe vàng là xe thật; cần hỏi ý kiến nhóm xem có phải mô hình quảng cáo gắn liền nóc. |
| 10 | `img_027.jpg` | Bia mộ bằng đá granit điêu khắc nguyên khối hình chiếc xe bán tải trong nghĩa trang. | `R-01` | **Không gán box**. | Tác phẩm điêu khắc đá tĩnh trong hoa viên nghĩa trang, không phải phương tiện giao thông vận hành. |
| 11 | `img_029.jpg`, `img_035.jpg` | Xe máy chở đệm mút cồng kềnh (`029`) và xe ba bánh chất bao tải cao ngất (`035`). | `R-05` | Bounding box chỉ ôm thân xe, không kéo bao trùm khối hàng nhô cao; tick `can_review=true`. | Khối hàng nhô cao làm sai lệch tỷ lệ khuôn hình học của xe; cần đưa ra thảo luận tại Pha 2 để thống nhất với nhóm. |
| 12 | `img_037.jpg` | Xe bán tải pickup có gắn thêm nắp chụp thùng hàng bằng composite cao ngang nóc cabin. | `R-02` | Tạm thời gán `van`, đánh dấu `can_review=true` để họp nhóm chốt. | Ranh giới giữa pickup có nắp kín và xe van rất mỏng manh; cần quy tắc nhóm để thống nhất là `truck`, `car` hay `van`. |

---

## 5. Kiểm soát chất lượng (QC) và Kế hoạch thảo luận Pha 2

### 5.1. Ngưỡng cam kết chất lượng kiểm soát

Thành viên 102 cam kết tuân thủ các ngưỡng kiểm tra chất lượng chặt chẽ khi bước vào Pha 3:
1. **Độ bao phủ phân công:** Hoàn thành $100\%$ số ảnh được phân công theo `assignment.csv`, không bỏ sót bất kỳ ảnh nào (kể cả ảnh 0 annotation).
2. **Độ ôm sát ranh giới (IoU):** Box ôm sát mép nhìn thấy thực tế, đảm bảo sai số biên $\le 2\text{ px}$. Đạt ngưỡng IoU $\ge 0.85$ đối với các vật thể có chiều cao $\ge 50\text{ px}$ và IoU $\ge 0.70$ đối với vật thể nhỏ hơn $50\text{ px}$.
3. **Độ chính xác thuộc tính:** $100\%$ thuộc tính `occluded_level` và `truncated` được phân định đúng theo ngưỡng định lượng tại Mục 2.2; không sử dụng phán đoán cảm tính.

### 5.2. Các điểm trọng tâm mang ra phiên họp Pha 2

1. **Thống nhất phân lớp phương tiện 3 bánh và xe thô sơ:** Đề xuất nhóm bổ sung lớp `three_wheeler` (gồm tuk-tuk và xe ba gác) và xem xét có thêm lớp `bicycle` hay không.
2. **Chốt quy tắc bao hàng cồng kềnh (R-05 vs R-06 nhóm):** Thảo luận xem nên để box ôm thân xe (quan điểm 102) hay box bao cả hàng dính liền (quan điểm xe tự hành cần tránh toàn bộ khối hàng).
3. **Quy chuẩn lớp cho xe bán tải (Pickup):** Quyết định đưa toàn bộ pickup về `truck` hay giữ `car`.

### 5.3. Lịch sử sửa đổi

| Phiên bản | Ngày | Tác giả | Nội dung thay đổi chính | Căn cứ thực tế |
|:---:|:---:|:---:|---|---|
| `v0` | 2026-11-16 | Giảng viên | Bản starter khung cơ sở; 5 lớp đơn giản, thiếu ngưỡng định lượng thuộc tính, thiếu quy tắc ca biên. | Khung bài lab chung. |
| `v0.1_individual_102` | 2026-11-16 | `102` | Khảo sát độc lập 40 ảnh; đề xuất bổ sung lớp `bus`, `tuk_tuk`; định lượng chính xác 4 mức `occluded_level` và `truncated`; thiết lập 8 quy tắc vẽ box R-01 đến R-08; lập bảng phân tích 12 ca khó có ID ảnh chi tiết. | Toàn bộ 40 ảnh `img_001.jpg` – `img_040.jpg` trong `data/images/`. |
