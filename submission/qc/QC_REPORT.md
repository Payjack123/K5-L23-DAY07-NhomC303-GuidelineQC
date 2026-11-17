# Báo cáo QC — NhomC303

## 1. Mục đích, dữ liệu và phiên bản

- Mục đích và giới hạn sử dụng: Thực hành đặc tả và QC nhãn 2D trong Day 07; tập ảnh tuyển chọn để luyện ca biên, độ đại diện cho dữ liệu vận hành chưa được đánh giá.
- Nguồn và phép sử dụng dữ liệu: Ảnh theo `data/ATTRIBUTION.csv`, giữ nguyên ghi công và giấy phép của từng ảnh.
- Manifest và checksum nhãn cuối: `submission/qc/batch_manifest.json`; SHA-256 nhãn cuối `ed9c61d0d72bffcaab6989ab257ca29d931677c3a7585629d4d77119d0ab93df`.
- Guideline và taxonomy khi gán / khi bàn giao: gán bằng guideline v1.0 và taxonomy v1.0; bàn giao guideline v1.1 (làm rõ R-09, R-10, xác nhận R-02), taxonomy giữ v1.0, mục `rules` không đổi.

## 2. Phân công và đồng thuận trước calibration

- Lượt hoàn thành / được giao: 80/80 lượt gán, mỗi ảnh có 2 người gán độc lập (K = 2).
- Số cặp box ghép, IoU TB, đồng thuận lớp và mẫu số: 266 cặp box ghép (IoU ≥ 0,5); IoU TB 0,899 (ngưỡng 0,85); đồng thuận lớp 99,2% (ngưỡng 95%); cùng `occluded_level` 53,8%; cùng `truncated` 95,1%.
- Box chưa ghép, loại do ignore, bất đồng vùng ignore: 83 box chưa ghép bên A và 78 bên B; 0 box loại do ignore; 53 ca bất đồng liên quan vùng `ignore_region`. Tổng 385 ca bất thường trên 36 ảnh.
- Ca hai người có thể cùng sai sau khi đối chiếu tham chiếu: IAA không bắt được các lỗi hai người cùng mắc, tìm ra khi xem ảnh ở QC vòng 2: img_037 (pickup có nắp gán `other_vehicle`, R-02), img_035 (tuk-tuk chở hàng gán `other_vehicle`, R-08), img_004 (người dưới mui, R-05), img_017, 020, 033 (`ignore_region` đặt lên tượng, phản chiếu, ma-nơ-canh, R-13).

## 3. Calibration và kiểm lại

- Ca đã xử lý, rule ID, bản sửa và người xác nhận: 385 ca, mỗi ca một dòng trong `submission/qc/calibration_decisions.csv` (người chốt 103, kiểm lại bởi 102 ở QC vòng 3). Quy tắc dùng: R-01, R-02, R-03, R-06, R-08, R-09, R-10, R-11, R-12, R-13, R-15.
- Tác động v1.1 lên nhãn và ảnh: thay đổi mang tính `semantic` (xem `guideline_change.json`), nên kiểm lại cả lô 40 ảnh. Nhãn cuối `labels_calibrated.json`: 40 ảnh, 409 annotation (396 box vật và 13 `ignore_region`), toàn bộ `can_review` đã đóng.
- Tham chiếu bằng chứng khi Rework: vòng 2 (`reviews/round-02/`) ghi 9/40 ảnh lỗi (22,5%), gồm 9 lỗi `thua`, 2 lỗi `sai_lop`, 1 lỗi `sai_vi_tri_kich_thuoc`, quyết định Rework. Đã sửa các ảnh img_004, 016, 017, 020, 022, 024, 033, 035, 037, lưu vào bản nhãn mới, rồi duyệt lại ở vòng 3. Giữ nguyên vòng 1 và vòng 2.

## 4. Kết quả duyệt

- Vòng QC: 3
- Người review và ngày: 102, 2026-11-17
- Đã duyệt / cả lô: 40/40 ảnh
- Ảnh lỗi / ảnh đã duyệt: 0/40 = 0,0% (ngưỡng ≤ 2,0%)
- Annotation đối tượng hiện có bị lỗi / annotation đối tượng đã duyệt: 0/396 = 0,0%
- Vật bỏ sót, ảnh và vùng: 0 vật bỏ sót ghi riêng
- Ca khó / phần còn lại, lỗi lặp và ví dụ: ca khó 36/36 (0 lỗi), phần còn lại 4/4 (0 lỗi); ở vòng 2, lỗi lặp là `ignore_region` đặt lên vật không thật (img_017, 020, 033) và lỗi gán lớp xe ba bánh và pickup (img_035, 037), xem `reviews/round-02/qc_review.csv`
- Một lỗi máy chặn được và một lỗi cần người đọc ảnh: lỗi máy chặn được: box vượt biên ảnh hoặc box thấp hơn 20 px (`validate_labels.py`, R-11); lỗi cần người đọc ảnh: hai người cùng gán sai lớp pickup có nắp thành `other_vehicle` (img_037, R-02), điểm số IAA không phát hiện

## 5. Quyết định bàn giao

- Quyết định: Release
- Lý do, người nhận và phạm vi sử dụng: bốn người gán độc lập đủ 80/80 lượt; IAA đạt ngưỡng (IoU TB 0,899, đồng thuận lớp 99,2%); vòng 3 ghi 0/40 ảnh lỗi sau khi sửa các lỗi ở vòng 2. Người nhận: nhóm phát triển mô hình phát hiện đối tượng; phạm vi thực hành và đánh giá, không dùng cho vận hành thực tế. Giới hạn đã biết: `occluded_level` chỉ khớp 53,8% giữa hai người gán vì ngưỡng 5/30/70% vẫn đo bằng mắt.
- Nếu còn việc: không còn việc tồn đọng; toàn bộ 40 ảnh và 396 box vật đã duyệt ở vòng 3.
- Kiểm ngược từ báo cáo tới ảnh, rule và nhãn: ca img_037 (box 218,139,508,357): quy tắc R-02, phiếu `reviews/round-02/qc_review.csv` ghi sai lớp `other_vehicle`, nhãn cuối `labels_calibrated.json` ghi `truck`, vòng 3 ghi hợp lệ.
