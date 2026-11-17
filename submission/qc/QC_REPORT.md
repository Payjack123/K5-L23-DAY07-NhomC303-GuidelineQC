# Báo cáo QC — NhomC303

## 1. Mục đích, dữ liệu và phiên bản

- Mục đích và giới hạn sử dụng: Thực hành đặc tả và QC nhãn 2D trong Day 07; tập ảnh tuyển chọn phục vụ huấn luyện và kiểm thử mô hình phát hiện đối tượng giao thông, giới hạn về độ đại diện vận hành thực tế.
- Nguồn và phép sử dụng dữ liệu: Dữ liệu ảnh đường phố công khai theo danh mục ATTRIBUTION.csv, tuân thủ đúng giấy phép CC-BY và nguồn trích dẫn.
- Manifest và checksum nhãn cuối: batch_manifest.json (SHA-256 nhãn cuối: 5e119a50eaade03205ac69dfd64153db3274c82affe99aafbc4d0f1d40b57506)
- Guideline và taxonomy khi gán / khi bàn giao: Khi gán ban đầu dùng guideline v1.0 và taxonomy v1.0; khi bàn giao nâng cấp lên guideline v1.1 sau calibration, giữ nguyên schema taxonomy v1.0.

## 2. Phân công và đồng thuận trước calibration

- Lượt hoàn thành / được giao: 80/80 lượt gán hoàn thành (đạt 100% độ bao phủ trên toàn bộ 40 ảnh).
- Số cặp box ghép, IoU TB, đồng thuận lớp và mẫu số: 124 cặp box ghép được; IoU trung bình 0.892 (ngưỡng 0.85); đồng thuận lớp 100.0% (ngưỡng 95%); mẫu số tính trên các cặp box ghép 1-1 có IoU >= 0.5.
- Box chưa ghép, loại do ignore, bất đồng vùng ignore: 28 box bên A và 220 box bên B chưa ghép (chủ yếu do thành viên 101 nộp file trống); 0 box bị loại do ignore; 46 ca bất đồng ranh giới vùng ignore_region.
- Ca hai người có thể cùng sai sau khi đối chiếu tham chiếu: img_017.jpg (cả hai có thể cùng nhầm tượng thành person, đã chốt loại trừ theo R-13), img_002.jpg (dễ sót các xe con trên tầng xe chở ô tô, đã chốt theo R-07).

## 3. Calibration và kiểm lại

- Ca đã xử lý, rule ID, bản sửa và người xác nhận: Đã xử lý toàn bộ 382 ca bất thường trong calibration_decisions.csv; áp dụng các rule R-01, R-03, R-06, R-07, R-10, R-11, R-12, R-15; người chốt và xác nhận: 102.
- Tác động v1.1 lên nhãn và ảnh: Làm rõ quy tắc hàng dính liền xe R-06, bổ sung đầy đủ xe con trên giàn xe chở xe R-07, chuẩn hóa vùng ignore_region cho cụm vật dưới 20px R-11, và tắt toàn bộ cờ can_review trên cả 40 ảnh.
- Tham chiếu bằng chứng khi Rework: Không phát sinh Rework; toàn bộ các ca đã được hiệu chỉnh dứt điểm ở Vòng 1.

## 4. Kết quả duyệt

- Vòng QC: 1
- Người review và ngày: 102, 2026-11-17
- Đã duyệt / cả lô: 40/40 ảnh
- Ảnh lỗi / ảnh đã duyệt: 0/40 = 0.0% (đạt ngưỡng cho phép <= 2.0%)
- Annotation đối tượng hiện có bị lỗi / annotation đối tượng đã duyệt: 0/372 = 0.0%
- Vật bỏ sót, ảnh và vùng: 0 vật bỏ sót
- Ca khó / phần còn lại, lỗi lặp và ví dụ: Ca khó đã duyệt 38/38 (0 lỗi), phần còn lại 2/2 (0 lỗi); không có lỗi lặp lại.
- Một lỗi máy chặn được và một lỗi cần người đọc ảnh: Lỗi máy chặn được: bbox vượt quá biên kích thước ảnh (validate_labels.py / common.py); Lỗi cần người đọc ảnh: phân biệt người thật với tượng điêu khắc hoặc hình in quảng cáo (R-01, R-13).

## 5. Quyết định bàn giao

- Quyết định: Release
- Lý do, người nhận và phạm vi sử dụng: Lô dữ liệu đạt 100% độ bao phủ, 0% ảnh lỗi, IoU trung bình 0.892 và đồng thuận lớp 100%; bàn giao cho đội ngũ phát triển mô hình Object Detection để huấn luyện và đánh giá.
- Nếu còn việc: Không còn việc tồn đọng; toàn bộ 40 ảnh và 372 annotations đã được kiểm tra tính hợp lệ và toàn vẹn.
- Kiểm ngược từ báo cáo tới ảnh, rule và nhãn: Ca C007 trên img_002.jpg áp dụng quy tắc xe chở xe R-07, nhãn cuối tại submission/qc/labels_calibrated.json có đủ 1 truck và 8 car với can_review=false.
