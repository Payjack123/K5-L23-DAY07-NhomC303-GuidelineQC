# Tóm tắt IAA (taxonomy v1.0)

- Ảnh được so sánh (có >=2 người gán): **40**; số người gán: 4
- Lượt gán đủ **80/80**.
- IoU trung bình và % cùng lớp **chỉ tính trên các cặp box đã ghép** (IoU >= 0.5, ghép 1-1 không phân biệt lớp). Box chưa ghép được thống kê riêng ở cột bỏ sót/thừa.
- Mẫu số: 124 cặp box ghép (tổng mọi cặp người gán, ảnh chung).

| Cặp | Ảnh | Cặp box ghép | IoU TB | Cùng lớp | Cùng occluded_level | Cùng truncated | Chưa ghép (A/B) | Bỏ qua do ignore | Đạt IAA |
|---|---|---|---|---|---|---|---|---|---|
| **TỔNG** | 40 | 124 | 0.892 | 100.0% | 48.4% | 97.6% | 28/220 | 0 | ĐẠT |
| 101|102 | 6 | 0 | n/a | n/a | n/a | n/a | 0/27 | 0 | N/A |
| 101|103 | 9 | 0 | n/a | n/a | n/a | n/a | 0/69 | 0 | N/A |
| 101|104 | 5 | 0 | n/a | n/a | n/a | n/a | 0/75 | 0 | N/A |
| 102|103 | 5 | 26 | 0.914 | 100.0% | 50.0% | 88.5% | 12/5 | 0 | ĐẠT |
| 102|104 | 9 | 69 | 0.891 | 100.0% | 42.0% | 100.0% | 12/26 | 0 | ĐẠT |
| 103|104 | 6 | 29 | 0.877 | 100.0% | 62.1% | 100.0% | 4/18 | 0 | ĐẠT |

Ngưỡng IAA: IoU TB >= 0.85, đồng thuận lớp >= 95%.

Số ca bất thường: 594 ({'co_can_review': 231, 'sai_thuoc_tinh': 65, 'bo_sot_thua': 228, 'iou_thap': 24, 'bat_dong_ignore': 46}), trên 38 ảnh cần calibration.
