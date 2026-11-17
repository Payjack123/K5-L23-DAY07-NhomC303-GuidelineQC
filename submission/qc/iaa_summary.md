# Tóm tắt IAA (taxonomy v1.0)

- Ảnh được so sánh (có >=2 người gán): **40**; số người gán: 4
- Lượt gán đủ **80/80**.
- IoU trung bình và % cùng lớp **chỉ tính trên các cặp box đã ghép** (IoU >= 0.5, ghép 1-1 không phân biệt lớp). Box chưa ghép được thống kê riêng ở cột bỏ sót/thừa.
- Mẫu số: 266 cặp box ghép (tổng mọi cặp người gán, ảnh chung).

| Cặp | Ảnh | Cặp box ghép | IoU TB | Cùng lớp | Cùng occluded_level | Cùng truncated | Chưa ghép (A/B) | Bỏ qua do ignore | Đạt IAA |
|---|---|---|---|---|---|---|---|---|---|
| **TỔNG** | 40 | 266 | 0.899 | 99.2% | 53.8% | 95.1% | 83/78 | 0 | ĐẠT |
| 101|102 | 6 | 27 | 1.000 | 96.3% | 63.0% | 100.0% | 0/0 | 0 | ĐẠT |
| 101|103 | 9 | 58 | 0.882 | 100.0% | 62.1% | 96.6% | 32/11 | 0 | ĐẠT |
| 101|104 | 5 | 57 | 0.883 | 98.2% | 52.6% | 86.0% | 23/18 | 0 | ĐẠT |
| 102|103 | 5 | 26 | 0.914 | 100.0% | 50.0% | 88.5% | 12/5 | 0 | ĐẠT |
| 102|104 | 9 | 69 | 0.891 | 100.0% | 42.0% | 100.0% | 12/26 | 0 | ĐẠT |
| 103|104 | 6 | 29 | 0.877 | 100.0% | 62.1% | 100.0% | 4/18 | 0 | ĐẠT |

Ngưỡng IAA: IoU TB >= 0.85, đồng thuận lớp >= 95%.

Số ca bất thường: 385 ({'co_can_review': 19, 'sai_thuoc_tinh': 131, 'iou_thap': 50, 'bo_sot_thua': 129, 'bat_dong_ignore': 53, 'sai_lop': 2, 'can_review_anh': 1}), trên 36 ảnh cần calibration.
