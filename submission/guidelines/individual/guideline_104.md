# Guideline gán nhãn — v0.1 — 104

- Phiên bản: v0.1
- Ngày: 2026-11-16
- Người viết / duyệt: 104 / …

## 1. Mục tiêu

Phạm vi gồm 40 ảnh từ `img_001.jpg` đến `img_040.jpg`. Vẽ hình chữ nhật trong CVAT và xuất COCO 1.0.

Nhãn dùng để huấn luyện mô hình phát hiện người và phương tiện trên ảnh đường phố. Mỗi box đại diện cho một cá thể thuộc phạm vi. Cần rà kỹ người bị che trong dòng xe, người ngồi sau xe máy và các vật dễ bị nhận nhầm là xe hoặc người thật.

## 2. Lớp và thuộc tính

### Lớp

| Lớp | Định nghĩa (một câu) | Ví dụ | Phản ví dụ / dễ nhầm với |
|---|---|---|---|
| `car` | Ô tô con, SUV, taxi. | Ô tô đen bên trái trong `img_023.jpg`. | Pickup có thùng hàng phía sau thuộc `truck`. |
| `truck` | Xe tải có cabin và sàn hoặc thùng hàng tách biệt, gồm pickup. | Xe tải xanh trong `img_036.jpg` và pickup có nắp thùng trong `img_037.jpg`. | Xe có khoang sau liền thân thuộc `van`. |
| `van` | Xe cỡ nhỏ có cabin và khoang phía sau nằm trong cùng thân xe kín. | Xe bạc phía sau các tay lái trong `img_005.jpg`. | Xe thùng kín có thùng tách khỏi cabin thuộc `truck`. |
| `motorcycle` | Xe máy, scooter hoặc mô tô, gồm cả sidecar gắn vào mô tô nếu có. | Xe đỏ trong `img_026.jpg` và mô tô có sidecar trong `img_022.jpg`. | Tuk-tuk trong `img_004.jpg` và xích lô trong `img_023.jpg` nằm ngoài lớp này. |
| `person` | Người thật nhìn thấy trực tiếp, gồm người đi bộ, đang lái hoặc ngồi trên xe. | Hai người ngồi trên xe đỏ trong `img_026.jpg`. | Tượng người trong `img_017.jpg`, hình người trên bảng trong `img_018.jpg` và ma-nơ-canh trong `img_033.jpg`. |
| `ignore_region` | Vùng cần bỏ qua vì có đối tượng thuộc phạm vi nhưng quá nhỏ hoặc quá dày để vẽ từng đối tượng đáng tin cậy. | Phần xa của dòng xe trong `img_021.jpg` nếu khi soi ảnh gốc vẫn không tách được từng cá thể. | Người hoặc xe đủ rõ ở tiền cảnh cần box riêng. Xe mô hình trong `img_038.jpg` nằm ngoài phạm vi. |

Bỏ qua vật ngoài phạm vi như xe buýt, xe đạp, xích lô, tuk-tuk, động vật và hàng hóa. Người thật trên hoặc cạnh các vật đó vẫn được gán nếu đủ rõ và đủ kích thước.

### Thuộc tính

| Thuộc tính | Giá trị | Cách chọn |
|---|---|---|
| `occluded_level` | `0`, `1`, `2`, `3` | Ước lượng tỷ lệ phần đối tượng trong khung bị vật khác che. `0` là 0%, `1` là trên 0% và dưới 25%, `2` là từ 25% đến dưới 50%, `3` là từ 50% trở lên. Nếu khó chọn giữa hai mức, chọn mức phù hợp nhất và bật `can_review`. |
| `truncated` | `no`, `yes` | `yes` khi mép ảnh cắt mất một phần đối tượng, còn lại dùng `no`. Đối tượng vừa bị vật che vừa bị cắt ở mép thì ghi cả hai thuộc tính. |
| `can_review` | Tắt, bật | Bật khi xác định được một đối tượng để vẽ nhưng còn phân vân lớp, biên hoặc mức che. Nếu chưa đủ căn cứ để vẽ box, ghi tên ảnh, vị trí và câu hỏi để reviewer kiểm tra. |

## 3. Quy tắc vẽ box

- **R-01 · Bám phần nhìn thấy.** Dùng hình chữ nhật nhỏ nhất chứa các phần nhìn thấy của cùng một đối tượng. Nếu hai phần bị ngăn bởi vật che nhưng rõ ràng thuộc cùng một đối tượng, đặt một box chứa cả hai. Dừng box tại mép ảnh. Mũ bảo hiểm đang đội thuộc box người. Gương gắn trên xe thuộc box xe. Bóng đổ, đồ xách tay và hàng chở nằm ngoài phạm vi box của đối tượng.
- **R-02 · Người và phương tiện.** Vẽ một box cho từng người và một box cho từng xe. Box có thể giao nhau. Chỉ tính các phần của người trong box `person` và các phần của xe trong box phương tiện. Áp dụng tương tự với người ngồi trên xe đang đỗ hoặc người đẩy xe.
- **R-03 · Xe chở xe.** Vẽ cabin, khung và giàn chở vào cùng box của xe chở. Mỗi xe thật được chở là một đối tượng riêng nếu còn nhận diện được và đủ kích thước. Biên box xe chở kết thúc ở kết cấu của chính xe chở.
- **R-04 · Vật mô phỏng, phản chiếu và xe chủ.** Bỏ hình người hoặc xe trên bảng in, màn hình hay trong gương. Bỏ tượng, ma-nơ-canh và đồ chơi. Bỏ phần xe gắn camera khi nó lọt vào khung hình. Xe thật đang đỗ hoặc trưng bày vẫn được xét. Nếu ảnh khó phân biệt xe thật cải trang với mô hình, ghi ca cần duyệt.
- **R-05 · Vật nhỏ.** Đo chiều cao box phần nhìn thấy trên ảnh gốc. Từ 20 px trở lên và nhận diện được thì vẽ riêng. Dưới 20 px thì dùng `ignore_region` sát vùng có vật thuộc phạm vi, kể cả khi chỉ có một vật nhỏ.
- **R-06 · Cụm chen dày.** Vẽ riêng từng người hoặc xe còn tách được. Dùng `ignore_region` cho phần không thể tách từng cá thể. Giữ vùng bỏ qua sát cụm đó và tránh phủ các box đã gán riêng.

## 4. Ca khó

| Ảnh | Tình huống | Rule ID | Quyết định | Lý do |
|---|---|---|---|---|
| `img_002.jpg` | Xe chở nhiều ô tô trên hai tầng. | R-03 | Một `truck` cho xe chở, thêm một `car` cho mỗi ô tô thấy rõ và đủ kích thước. | Xe trên giàn là các cá thể riêng. |
| `img_004.jpg`, `img_035.jpg` | Tuk-tuk đỗ hoặc tham gia giao thông. | Phạm vi lớp | Bỏ qua tuk-tuk. Gán riêng người hoặc xe máy đủ điều kiện. | Bánh xe và khoang chở khách dễ làm nhầm tuk-tuk với `motorcycle` hoặc `van`. |
| `img_005.jpg` | Nhiều người và xe máy che xe bạc phía sau. | R-01, R-02 | Vẽ `van` theo phần thân thấy được. Vẽ riêng từng người đủ rõ và điền mức che cho từng đối tượng. | Người ở trước là cá thể riêng. Biên box van căn theo các phần van còn thấy. |
| `img_019.jpg` | Xe vàng diễu hành có người lái và nhân vật chuột. | R-04 | Đề xuất `car` cho xe vàng và bật `can_review`. Xét riêng người lái thật. Ghi câu hỏi về nhân vật chuột nếu chưa phân biệt được hóa trang với đạo cụ. | Có bánh, thân xe cỡ thật và người lái. Vai trò của nhân vật chuột chưa rõ từ ảnh. |
| `img_020.jpg` | Hình phản chiếu trong gương chiếu hậu. | R-04 | Bỏ nội dung trong gương và phần xe chủ lọt khung. | Hình trong gương là ảnh phản chiếu của cảnh. |
| `img_021.jpg`, `img_025.jpg` | Đám đông, nhiều đối tượng ở xa. | R-05, R-06 | Khi soi ảnh gốc, vẽ riêng cá thể phân biệt được và cao ít nhất 20 px. Khoanh vùng nhỏ cho phần quá xa hoặc chen dày còn lại. | Tách đối tượng rõ giúp giảm bỏ sót. Vùng bỏ qua giới hạn chỗ không thể gán nhất quán. |
| `img_026.jpg` | Hai người ngồi trên cùng xe đỏ, bánh xe bị cắt ở mép dưới. | R-01, R-02 | Hai `person` và một `motorcycle`. Đặt `truncated=yes` cho xe. Xét riêng thuộc tính của từng người. | Ba cá thể. Mép ảnh cắt phần bánh của xe. |
| `img_027.jpg`, `img_028.jpg` | Tượng pickup trên bệ và pickup thật chở vật hình ngựa. | R-03, R-04 | Bỏ pickup trên bệ trong `img_027.jpg`. Gán `truck` cho pickup trong `img_028.jpg`, lấy biên theo xe. | Bệ và biển giới thiệu nhận diện tượng. Vật hình ngựa là vật chở. |
| `img_037.jpg` | Pickup có nắp khoang hàng phía sau. | Phạm vi lớp | Gán `truck`. | Cabin và thùng pickup nhìn thấy tách biệt dù có nắp. |
| `img_038.jpg` | Xe mô hình và búp bê trong tủ kính. | R-04 | Bỏ qua các vật trưng bày này. | Bộ sưu tập trong tủ gồm đồ chơi và mô hình. |

## 5. QC và phiên bản

- Rà các lỗi bỏ sót, thừa, sai lớp, sai vị trí hoặc kích thước và sai thuộc tính. Ghi tên ảnh, vị trí và Rule ID cho ca cần trao đổi.
- Ngưỡng kiểm box là IoU **0,85** với box cao từ 50 px và **0,70** với box thấp hơn 50 px. IAA ghép box một-một với IoU từ 0,5, sau đó kiểm IoU trung bình từ **0,85** và tỷ lệ cùng lớp từ **95%**. Báo riêng các trường hợp không ghép được.
- Reviewer xem các ca `can_review` và vấn đề cấp ảnh. Nhóm thống nhất cách xử lý trong calibration. Ghi lý do và tăng phiên bản khi đổi quy tắc làm thay đổi nhãn.
- Ngưỡng bàn giao áp dụng sau khi review toàn bộ lô là **không quá 2% ảnh lỗi**. Bản này chỉ định nghĩa cách gán và cách kiểm.

| Phiên bản | Thay đổi | Lý do (ca nào) |
|---|---|---|
| v0.1 | Thêm ngưỡng che, quy tắc box người–xe, phân biệt pickup/van, trường hợp xe chở xe và vật mô phỏng. | Các ca `img_002.jpg`, `img_005.jpg`, `img_019.jpg`, `img_026.jpg`, `img_027.jpg` và `img_037.jpg` cần quyết định rõ để các lượt gán có thể đối chiếu. |
