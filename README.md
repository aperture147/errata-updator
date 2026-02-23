Errata Updator
====

Đây là một công cụ nhỏ, sử dụng Solr API (thó được) từ trang [Errata Search](https://access.redhat.com/errata-search/) để lấy các Errata rồi soạn thảo thành 1 file HTML tổng kết. Mục đích là từ file HTML này ta copy được nội dung để gửi cho các khách hàng yêu cầu cần cập nhật Errata hàng tuần/quý/tháng.

## Tính năng:

- [x] Lọc Errata theo product, severity, thời gian
- [x] Exclude Errata theo keyword
- [ ] CLI để không phải modify code Python
- [ ] Custom template email theo mong muốn

## Chuẩn bị:

1. Clone repo này về:
```sh
git clone https://github.com/aperture147/errata-updator
```

2. Tạo venv và activate nó lên:
```sh
cd errata-updator
python3 -m venv venv
source ./venv/bin/activate
```

3. Install hết các package trong `requirements.txt`:
```sh
pip install -r requirements.txt
```

## Chạy:
```sh
python3 main.py
```

Đầu ra sẽ là file `erratas.html`.

## Customize:
### Thay đổi tên sản phẩm:
Tạm thời chưa có CLI nên danh sách product anh em vui lòng vào trang [Errata Search](https://access.redhat.com/errata-search/) để lấy. 
Portal product sẽ có dạng:
```
{tên product}|{variant}|{version}|{CPU architecture}
```
Ví dụ (`*` có nghĩa là lấy hết, nhớ dấu cách phải escape ra):
```
Red\ Hat\ Enterprise\ Linux|*|*|x86_64
```

Tìm mục `portal_product_filter` để thay thế tên product.

### Thay đổi severity:
Thay ở mục `SEVERITY_LIST` trong `main.py`

### Thay excluded keyword:
Thay ở mục `excluded_keywords`