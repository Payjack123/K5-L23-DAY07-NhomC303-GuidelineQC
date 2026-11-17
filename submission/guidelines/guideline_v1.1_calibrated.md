# Guideline gán nhãn — v1.1 (nhóm NhomC303, sau Calibration)

- Phiên bản: v1.1, hiệu chỉnh từ v1.0 sau Calibration (Pha 5); v1.0 tổng hợp từ guideline cá nhân 101, 102, 103, 104 và `guideline_v0_starter.md`
- Phạm vi: `img_001.jpg` đến `img_040.jpg` · Loại nhãn: bounding box 2D · Công cụ: CVAT Rectangle, xuất COCO 1.0
- Trạng thái: bản sau Calibration dùng để gộp nhãn cuối và bàn giao QC

---

## 1. Mục tiêu

Nhãn dùng để huấn luyện và đánh giá mô hình phát hiện **người và phương tiện thật** trên ảnh đường phố châu Á (camera giao thông, xe tự lái).
Nhãn sai có hai hậu quả: **bỏ sót** người hoặc xe làm hệ thống không tránh, **gán nhầm** vật không thật (tượng, hình in, phản chiếu) làm hệ thống phanh bất ngờ.
Vì vậy mọi quy tắc dưới đây ưu tiên hai điều: chỉ gán vật thật nhìn thấy được, và hai người gán độc lập phải ra cùng kết quả.

## 2. Lớp và thuộc tính

Phép thử: *"mô hình có phải đoán ra điều này không?"* Có → lớp. Không (chỉ để lọc, QC) → thuộc tính.

### Lớp (mỗi vật thuộc đúng một lớp)

| Lớp | Định nghĩa | Ví dụ | Phản ví dụ / dễ nhầm |
|---|---|---|---|
| `car` | Ô tô con, taxi, SUV, xe điện kín 4 bánh. | img_006, 012, 023, 040 | Pickup có thùng → `truck`; xe mô hình (img_038) → không gán |
| `truck` | Xe tải, xe đầu kéo, xe có thùng hàng riêng, **gồm pickup thùng hở hoặc có nắp**. | img_001, 002, 007, 012, 036, 037 | Xe thùng kín liền cabin → `van`; xe khách → `bus` |
| `van` | Xe thùng kín cỡ nhỏ, cabin và khoang sau liền một thân: minivan, van giao hàng. | img_005, 016 | Xe có thùng tách khỏi cabin → `truck` |
| `bus` | Xe buýt, xe khách, minibus chở nhiều hành khách. | img_009, 031, 037, 040 | Minivan gia đình → `van` |
| `motorcycle` | Xe hai bánh có động cơ: xe máy, scooter, mô tô, quad; xe có sidecar tính **một** box. | img_006, 008, 022, 026 | Xe đạp → `bicycle`; xe ba bánh → `three_wheeler` |
| `bicycle` | Xe đạp hai bánh không động cơ, kể cả xe đạp chở hàng. | img_003, 006, 010, 029, 039 | Xe có động cơ → `motorcycle` |
| `three_wheeler` | Xe ba bánh chở khách hoặc hàng: tuk-tuk, xe lam, ba gác máy, xích lô đạp. | img_004, 016, 023, 035, 040 | Xe hai bánh có sidecar → `motorcycle` |
| `person` | Người thật ở **ngoài** thân xe: đi bộ, đứng, ngồi, người cưỡi xe máy/xe đạp, người đạp xích lô, người đánh xe. | img_005, 014, 026, 034 | Tượng (017), ma-nơ-canh (033), hình in (018) → không gán |
| `other_vehicle` | Xe thật không thuộc các lớp trên: xe trâu bò kéo, xe đẩy, xe diễu hành tự chế. | img_010 (xe đẩy), 019 | Xe mô hình, đồ chơi, xe điêu khắc → không gán |
| `ignore_region` | Vùng chứa vật thuộc phạm vi nhưng không tách được từng vật: quá nhỏ (< 20 px) hoặc quá dày. Bỏ sót trong vùng này không tính lỗi. | img_008, 021, 025, 030, 032 | Vật rõ, đủ 20 px phải có box riêng |

Vật thật **không thuộc lớp nào** và không phải phương tiện (con vật, cột, cây, biển báo, hàng rời): không gán.
Không phân biệt được hai lớp từ bằng chứng trong ảnh: không đoán, chọn lớp nghiêng về và tick `can_review`.

### Thuộc tính

| Thuộc tính | Giá trị | Ý nghĩa và ngưỡng |
|---|---|---|
| `occluded_level` | `0`, `1`, `2`, `3` | Tỉ lệ diện tích vật bị **vật khác** che: `0` là không bị che (≤ 5%); `1` là trên 5% đến 30%; `2` là trên 30% đến 70%; `3` là trên 70% nhưng phần thấy vẫn đủ xác định lớp. Không xác định được lớp thì không vẽ box (xem R-10). |
| `truncated` | `no`, `yes` | `yes` khi **mép ảnh** cắt mất một phần vật (từ khoảng 5% diện tích ước tính); bị vật khác che không phải truncated. Vật vừa bị che vừa bị cắt thì ghi cả hai thuộc tính. |
| `can_review` | tick / không | Tick khi vẽ được box nhưng còn phân vân lớp, biên hoặc quy tắc áp dụng, để reviewer xem lại. |

## 3. Quy tắc vẽ box

- **R-01 · Chỉ gán vật thật.** Chỉ gán người và phương tiện thật, nhìn thấy và nhận dạng được. Mỗi vật một box riêng, các box được phép chồng lấn.
- **R-02 · Chọn lớp theo định nghĩa mục 2.** Không tự tạo lớp ngoài taxonomy, không gộp lớp theo cảm tính.
- **R-03 · Box ôm phần nhìn thấy.** Hình chữ nhật nhỏ nhất chứa phần nhìn thấy của vật, không thừa nền, không cắt mất phần thấy được; không ước đoán phần khuất. Mũ bảo hiểm đang đội thuộc box người, gương gắn trên xe thuộc box xe; bóng đổ và đồ xách nhỏ nằm ngoài box.
- **R-04 · Người trên xe.** Mỗi xe một box xe, mỗi người nhìn thấy rõ một box `person`, kể cả người ngồi sau và xe chở 3–4 người; box được chồng lấn.
- **R-05 · Người trong khoang.** Người ngồi trong khoang kín hoặc dưới mui (ô tô, tuk-tuk có mui) **không gán**. Người ngồi ngoài thân xe hoặc trên xe không mui (xe máy, xe đạp, xích lô, xe mui trần) gán `person`.
- **R-06 · Hàng dính liền xe.** Hàng chất cao hoặc nhô ra mà dính liền với xe thì **một box bao cả xe và hàng**, vì xe tự lái phải tránh cả phần hàng. Lớp là lớp của xe (img_001, 012, 029, 035). Hàng rời không gắn với xe và vật người đang xách thì ngoài box.
- **R-07 · Xe chở xe (img_002).** Một box `truck` bao cả xe đầu kéo, giàn và xe chở; thêm một box `car` riêng cho mỗi ô tô thấy rõ và cao từ 20 px.
- **R-08 · Xe ba bánh và xe súc vật kéo.** Xe ba bánh: một box bao cả thân và mui. Xe trâu bò kéo: `other_vehicle`, một box bao cả xe và con vật kéo; người đánh xe ngồi ngoài gán `person`.
- **R-09 · Cắt mép ảnh.** Box dừng ở mép ảnh, `truncated` = yes theo ngưỡng mục 2 (img_005, 008, 012, 015, 016, 032, 034, 040). **v1.1:** khi hai người lệch `truncated`, chọn theo hình học: box chạm mép ảnh thì `yes`, ngược lại `no`.
- **R-10 · Che khuất.** Đặt `occluded_level` theo ngưỡng mục 2. Xe nhìn thấy một phần rõ thì một box. Chỉ lộ vài điểm, không xác định được lớp thì không vẽ box mà gom vào `ignore_region`. **v1.1:** khi hai người lệch `occluded_level`, chọn mức cao hơn trong hai mức.
- **R-11 · Vật nhỏ.** Chiều cao box phần nhìn thấy < 20 px: không gán box đối tượng, dùng `ignore_region` sát vùng có vật (kể cả khi chỉ có một vật; img_013, 025, 039).
- **R-12 · Đám đông và xe dày đặc.** Gán riêng từng người hoặc xe còn tách được (đủ 20 px), gom phần không tách được vào `ignore_region`. Vùng ignore sát cụm, không phủ các box đã gán; không dùng ignore để né quyết định về vật nhìn thấy rõ (img_008, 021, 030, 032).
- **R-13 · Vật không thật: không gán.** Tượng và xe điêu khắc (img_011, 017), bia mộ hình xe (img_027), ma-nơ-canh (img_033), xe mô hình và đồ chơi (img_038), hình người/xe in trên biển quảng cáo hoặc tranh tường (img_018, 026), phản chiếu trong gương hoặc kính và xe của chính mình, ego (img_020). Xe thật cỡ thật trong showroom hoặc bảo tàng vẫn gán.
- **R-14 · Thiếu sáng, nhoè.** Xác định được lớp và biên thì gán (img_007, 013, 031); không chắc thì tick `can_review`; không xác định được thì `ignore_region` (img_014, 015).
- **R-15 · Ca mơ hồ.** Tick `can_review` kèm ghi chú, không tự đoán. Ảnh không thể vẽ box thì ghi vấn đề cấp ảnh vào `image_issues.csv`. Ảnh không có vật thuộc phạm vi là hợp lệ khi đã kiểm tra, không cần annotation.

## 4. Ca khó và bất đồng đã chốt

Bảng liệt kê chỗ các bản cá nhân quyết khác nhau và quyết định của v1.0. Chỗ cả bốn bản cùng quy tắc (người và xe máy tách box, vật không thật, vật nhỏ 20 px, ignore cho đám đông) thì không nhắc lại.

| Ảnh | Tình huống | Các bản cá nhân | Quyết định v1.0 | Lý do |
|---|---|---|---|---|
| img_004, 016, 023, 035, 040 | Tuk-tuk, xích lô | 101: `three_wheeler` (xích lô → `bicycle`); 102: `tuk_tuk`, xích lô không gán; 103: `three_wheeler` gồm xích lô; 104: không gán | Lớp `three_wheeler` gồm cả xích lô đạp (R-08) | Cùng cấu tạo 3 bánh chở khách/hàng; không gán thì mô hình bỏ sót vật cản thật |
| img_009, 031, 037, 040 | Xe buýt, minibus | 101, 102, 103: thêm `bus`; 104: không gán | Thêm lớp `bus` | Xuất hiện ở ≥ 4 ảnh, kích thước và hành vi khác `car`/`truck` |
| img_003, 006, 010, 029, 039 | Xe đạp | 101, 103: thêm `bicycle`; 102, 104: không gán | Thêm lớp `bicycle` | Xuất hiện ở ≥ 5 ảnh; bỏ thì người đạp xe mất phương tiện đi kèm |
| img_010, 019 | Xe đẩy, xe diễu hành tự chế | 103: `other_vehicle`; 101, 104: `car` + `can_review` hoặc không nêu lớp riêng | Thêm lớp `other_vehicle`; img_019 gán `other_vehicle`, tài xế `person`, tick `can_review` | Cần một lớp cho xe thật không thuộc lớp nào thay vì bỏ qua hoặc ép vào `car` |
| img_001, 012, 028, 036, 037 | Pickup thùng hở hoặc có nắp | 101: `car`; 102: `car`, img_037 `van`; 103, 104: `truck` | `truck` (R-02) | Khớp định nghĩa `truck` của v0 "có thùng hàng riêng"; cabin và thùng nhìn thấy tách biệt |
| img_002 | Đầu kéo chở 7 ô tô | 101, 102, 104: `truck` + `car` từng xe; 103: một box `truck` bao cả | Một `truck` bao cả xe chở **và** một `car` riêng cho mỗi xe thấy rõ (R-07) | Kết hợp: hàng dính liền xe thì box ôm cả (R-06), mỗi ô tô thật vẫn là vật cần phát hiện |
| img_029, 035 | Hàng nhô ra hoặc chất cao trên xe | 101, 102, 104: box không bao hàng; 103: một box bao cả hàng | Hàng dính liền xe thì một box bao cả (R-06) | Xe tự lái phải tránh cả khối hàng; hàng rời không gắn xe thì ngoài box |
| img_028 | Pickup thật chở tượng ngựa | 104: `truck` theo xe; 103: bao cả tượng | Một box `truck` bao cả tượng, không gán riêng con ngựa | Tượng là hàng dính liền xe, không phải vật cần phát hiện riêng |
| img_004, 016, 035, 019 | Người dưới mui tuk-tuk, người trên xe mui trần | 101, 104: gán nếu nhìn rõ; 103: dưới mui không gán | Dưới mui hoặc trong khoang: không gán; xe mui trần, người ngoài thân xe: gán (R-05) | Người trong khoang kín không phải đối tượng độc lập với xe |
| img_024 | Xe vàng đặt trên nóc xe đen | 101: phân biệt thật/mô hình; 103: không gán xe vàng | Xe đen `car`; xe vàng không gán, tick `can_review` trên xe đen | Không xác định được xe vàng là xe thật hay mô hình |
| img_022 | Xe sidecar, ảnh đen trắng, nhỏ | 103, 104: một box `motorcycle` | Một box `motorcycle` gồm cả sidecar | Sidecar gắn liền và di chuyển cùng xe |
| (thuộc tính) | Ngưỡng `occluded_level` | 101, 102: 30%/70%; 103: 5%/50%/80%; 104: 25%/50% | 5% / 30% / 70% | Hai bản dùng chung, tách đều ba mức và đo được bằng mắt |
| (thuộc tính) | Điều kiện `truncated` | 101, 104: mép ảnh cắt; 103: ≥ 5% diện tích | `yes` khi mép ảnh cắt mất từ khoảng 5% | Tránh đánh dấu khi chỉ lệch vài pixel |

## 5. QC và phiên bản

- Mọi thay đổi làm đổi nhãn đều **tăng phiên bản** guideline; cập nhật `taxonomy.json` khớp. Từ khi khóa v1.0 tới hết Pha 3 không đổi.
- Ca `can_review` và vấn đề cấp ảnh: reviewer xem, nhóm chốt ở calibration. Ghi **Rule ID** vào nhật ký QC để nối ca bất đồng với quy tắc.
- 5 loại lỗi khi QC: bỏ sót, thừa, sai lớp, sai vị trí hoặc kích thước, sai thuộc tính.
- Ngưỡng (giữ nguyên `rules` trong `taxonomy.json`): box cao từ 50 px đạt khi IoU ≥ 0,85, box thấp hơn đạt khi IoU ≥ 0,7; ghép box một-một với IoU ≥ 0,5, rồi IAA: IoU trung bình ≥ 0,85, đồng thuận lớp ≥ 95%; Release khi ≤ 2% số ảnh có lỗi.
- IAA thấp: cả hai người cùng lệch thì sửa guideline; chỉ một người lệch thì hướng dẫn lại. IAA chỉ đo mức đồng thuận, không chứng minh nhãn đúng: cần xem ảnh gốc vì cả nhóm có thể cùng sai.

| Phiên bản | Thay đổi | Lý do (ca nào) |
|---|---|---|
| v0 | Bản khởi đầu của giảng viên | — |
| v1.0 | Thêm `bus`, `bicycle`, `three_wheeler`, `other_vehicle`; định nghĩa lại `truck` (gồm pickup); định lượng `occluded_level` và `truncated`; quy tắc R-01 đến R-15 | img_002 (xe chở xe), 004, 023, 035 (xe ba bánh và hàng), 009, 031 (bus), 010, 019 (xe đặc biệt), 017, 027, 033, 038 (vật không thật), 021, 030 (đám đông) |
| v1.1 | Làm rõ R-09, R-10; xác nhận R-02 cho pickup (`truck`); áp dụng R-11, R-12 khi gộp nhãn | img_012, 028 (pickup bị gán `car`), toàn lô (lệch `occluded_level`, `truncated`), img_034, 021, 011 (ignore) |

## 6. Quyết định hiệu chỉnh sau Calibration (v1.1)

Căn cứ: IAA 4 người trên 40 ảnh, 385 ca bất thường trên 36 ảnh (xem `submission/qc/iaa_summary.md`, `calibration_decisions.csv`). Mỗi ca có một dòng quyết định kèm mã quy tắc.

1. **Pickup là `truck` (R-02).** Hai ca `sai_lop` (img_012, 028): 101 gán `car`, cùng một vật gán `truck` ở người kia. Chốt `truck`, vì v1.0 đã quy định pickup thuộc lớp này. Đây là lỗi chưa nắm quy tắc của một người, không phải guideline mơ hồ.
2. **Lệch `occluded_level` (R-10).** Hai người lệch mức thì chọn mức cao hơn. Lệch này là nhóm ca nhiều nhất (131 ca) vì ngưỡng 5/30/70% vẫn phải ước lượng bằng mắt.
3. **Lệch `truncated` (R-09).** Chọn theo hình học: box chạm mép ảnh thì `yes`.
4. **Box chỉ một người vẽ (R-01, R-11).** Giữ nếu cao từ 20 px và nhìn thấy rõ; bỏ nếu thấp hơn 20 px. Box trùng một box đã gộp (cùng lớp, IoU từ 0,5) chỉ giữ một.
5. **Vùng `ignore_region` (R-12).** Giữ vùng khi vật bên trong thấp dưới 20 px hoặc không tách được; bỏ vùng khi người kia đã vẽ riêng được các vật cao từ 20 px bên trong. Ca cấp ảnh img_034 chốt tách từng box.
6. **`can_review` (R-15).** Đã rà các box đang cắm cờ và đóng cờ trên bản nhãn cuối khi hai người cùng vẽ hoặc box đạt R-01.
7. **Lỗi cả hai người cùng mắc, phát hiện ở QC vòng 2.** IAA không bắt được các lỗi này vì hai người đồng ý với nhau nhưng cùng sai quy tắc. Đã sửa sau khi xem ảnh: tuk-tuk chở hàng là `three_wheeler` và chỉ một box bao cả hàng (R-06, R-08, img_035); pickup có nắp thùng là `truck` (R-02, img_037); người dưới mui tuk-tuk không gán (R-05, img_004); xe sidecar một box `motorcycle` (img_022); không đặt `ignore_region` lên tượng, phản chiếu, ma-nơ-canh (R-13, img_017, 020, 033); xe vàng trên nóc xe đen không gán (R-13, img_024); không để hai box cho cùng một pickup (R-03, img_016).
