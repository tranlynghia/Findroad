### Maze Pathfinding v3

## Tổng quan

Maze Pathfinding v3 là một ứng dụng Python nâng cao cho phép tạo, chỉnh sửa và tìm đường trong các bản đồ mê cung. Ứng dụng cung cấp nhiều thuật toán tạo mê cung, thuật toán tìm đường, và các tính năng mô phỏng trực quan.





## Tính năng chính

- **Tạo bản đồ đa dạng**:

- Tạo bản đồ ngẫu nhiên với mật độ tường và đường đi tùy chỉnh
- Tạo mê cung tự động bằng nhiều thuật toán khác nhau (Recursive Backtracking, Prim's Algorithm, Binary Tree)
- Chỉnh sửa bản đồ thủ công
- Thay đổi kích thước bản đồ linh hoạt



- **Thuật toán tìm đường**:

- BFS (Breadth-First Search) - Tìm đường ngắn nhất trong không gian không có trọng số
- DFS (Depth-First Search) - Hiệu quả trong không gian tìm kiếm sâu
- Dijkstra - Tìm đường ngắn nhất với trọng số
- A* - Thuật toán tìm đường tối ưu sử dụng heuristic



- **Mô phỏng trực quan**:

- Xem quá trình tìm đường theo từng bước
- Điều chỉnh tốc độ mô phỏng
- Hiển thị các ô đã thăm và đường đi



- **So sánh thuật toán**:

- So sánh hiệu suất của các thuật toán tìm đường
- Phân tích theo thời gian thực thi, số ô đã thăm, độ dài đường đi



- **Quản lý lịch sử và lưu/tải**:

- Lưu bản đồ vào lịch sử
- Xuất/nhập bản đồ dưới dạng tệp JSON
- Quản lý nhiều bản đồ khác nhau





## Cài đặt

### Yêu cầu hệ thống

- Python 3.6 trở lên
- Tkinter (thường được cài đặt sẵn với Python)


### Cài đặt

1. Clone hoặc tải xuống repository này
2. Đảm bảo Python và Tkinter đã được cài đặt
3. Không cần cài đặt thêm thư viện nào khác


```shellscript
# Clone repository (nếu sử dụng Git)
git clone https://github.com/username/maze-pathfinding-v3.git
cd maze-pathfinding-v3

# Chạy ứng dụng
python main.py
```

## Hướng dẫn sử dụng

### Khởi động ứng dụng

Chạy tệp `main.py` để khởi động ứng dụng:

```shellscript
python main.py
```

### Giao diện người dùng

Giao diện được chia thành hai phần chính:

- **Bản đồ**: Hiển thị bản đồ mê cung với các ô khác nhau
- **Điều khiển**: Các tab chức năng để tương tác với ứng dụng


### Tab "Tạo bản đồ"





- **Thay đổi kích thước bản đồ**: Điều chỉnh số hàng và số cột của bản đồ
- **Mật độ tường/đường đi**: Điều chỉnh tỷ lệ phần trăm của tường và đường đi khi tạo bản đồ ngẫu nhiên
- **Loại ô để vẽ**: Chọn loại ô (Trống, Tường) để vẽ trên bản đồ
- **Thuật toán tạo mê cung**: Chọn thuật toán để tạo mê cung tự động
- **Các nút chức năng**:

- Tạo bản đồ ngẫu nhiên: Tạo bản đồ với tường và đường đi ngẫu nhiên
- Tạo mê cung: Tạo mê cung bằng thuật toán đã chọn
- Xóa bản đồ: Xóa tất cả tường và đường đi, giữ lại điểm bắt đầu và kết thúc





### Tab "Tìm đường"





- **Thuật toán tìm đường**: Chọn thuật toán để tìm đường (Auto, BFS, DFS, Dijkstra, A*)
- **Tốc độ mô phỏng**: Điều chỉnh tốc độ hiển thị quá trình tìm đường
- **Các nút chức năng**:

- Tìm đường (Ngay lập tức): Hiển thị kết quả tìm đường ngay lập tức
- Tìm đường (Mô phỏng): Hiển thị quá trình tìm đường từng bước
- Dừng mô phỏng: Dừng quá trình mô phỏng đang chạy
- Xóa đường đi: Xóa đường đi và các ô đã thăm
- Đặt điểm bắt đầu/kết thúc: Thay đổi vị trí điểm bắt đầu và kết thúc





### Tab "So sánh"





- **So sánh tất cả thuật toán**: Chạy tất cả các thuật toán tìm đường và so sánh hiệu suất
- **Kết quả so sánh**: Hiển thị kết quả so sánh theo thời gian, số ô đã thăm, độ dài đường đi


### Tab "Lịch sử & Lưu/Tải"





- **Lịch sử bản đồ**: Danh sách các bản đồ đã lưu
- **Các nút chức năng**:

- Lưu bản đồ hiện tại: Lưu bản đồ hiện tại vào lịch sử
- Xuất bản đồ: Lưu bản đồ hiện tại thành tệp JSON
- Nhập bản đồ: Tải bản đồ từ tệp JSON





## Cấu trúc dự án

```plaintext
maze_pathfinding_v3/
├── main.py                # Điểm khởi đầu của ứng dụng
├── maze_app.py            # Lớp ứng dụng chính
├── algorithms.py          # Các thuật toán tìm đường
├── algorithm_selector.py  # Bộ chọn thuật toán tốt nhất
├── maze_generator.py      # Các thuật toán tạo mê cung
└── history_manager.py     # Quản lý lịch sử bản đồ
```

## Giải thích thuật toán

### Thuật toán tìm đường

1. **BFS (Breadth-First Search)**

1. Tìm kiếm theo chiều rộng, khám phá tất cả các nút ở cùng một mức trước khi đi sâu hơn
2. Đảm bảo tìm được đường đi ngắn nhất trong không gian không có trọng số
3. Hiệu quả trong không gian tìm kiếm rộng



2. **DFS (Depth-First Search)**

1. Tìm kiếm theo chiều sâu, đi sâu nhất có thể trước khi quay lại
2. Hiệu quả về bộ nhớ và trong không gian tìm kiếm sâu
3. Không đảm bảo tìm được đường đi ngắn nhất



3. **Dijkstra**

1. Thuật toán tìm đường ngắn nhất trong đồ thị có trọng số
2. Mở rộng từ điểm bắt đầu theo thứ tự tăng dần của khoảng cách
3. Đảm bảo tìm được đường đi ngắn nhất



4. **A***

1. Thuật toán tìm đường tối ưu sử dụng hàm heuristic
2. Kết hợp khoảng cách thực tế và ước lượng khoảng cách đến đích
3. Hiệu quả hơn Dijkstra trong nhiều trường hợp





### Thuật toán tạo mê cung

1. **Recursive Backtracking**

1. Tạo mê cung bằng cách đi sâu và quay lui khi gặp ngõ cụt
2. Tạo ra mê cung với nhiều ngõ cụt và đường đi dài



2. **Prim's Algorithm**

1. Thuật toán tạo mê cung dựa trên thuật toán cây khung nhỏ nhất Prim
2. Tạo ra mê cung với nhiều nhánh và ít ngõ cụt



3. **Binary Tree**

1. Thuật toán đơn giản tạo mê cung theo cấu trúc cây nhị phân
2. Tạo ra mê cung có xu hướng thiên về một hướng





## Chú thích màu sắc

- **Trắng**: Ô trống
- **Xám đậm**: Tường
- **Xanh lá**: Điểm bắt đầu (S)
- **Đỏ**: Điểm kết thúc (E)
- **Xanh dương**: Đường đi
- **Vàng nhạt**: Ô đã thăm trong quá trình tìm đường


## Ví dụ sử dụng

### Tạo và giải mê cung

1. Khởi động ứng dụng
2. Chọn tab "Tạo bản đồ"
3. Chọn "Recursive Backtracking" trong danh sách thuật toán tạo mê cung
4. Nhấn "Tạo mê cung"
5. Chuyển sang tab "Tìm đường"
6. Chọn thuật toán "A*"
7. Nhấn "Tìm đường (Mô phỏng)" để xem quá trình tìm đường


### So sánh thuật toán

1. Tạo một mê cung phức tạp
2. Chuyển sang tab "So sánh"
3. Nhấn "So sánh tất cả thuật toán"
4. Xem kết quả so sánh hiệu suất của các thuật toán


### Lưu và tải bản đồ

1. Tạo một bản đồ ưng ý
2. Chuyển sang tab "Lịch sử & Lưu/Tải"
3. Nhấn "Lưu bản đồ hiện tại" và đặt tên
4. Để xuất bản đồ, nhấn "Xuất bản đồ" và chọn vị trí lưu
5. Để tải lại bản đồ, nhấn "Nhập bản đồ" và chọn tệp JSON


## Xử lý sự cố

- **Ứng dụng không khởi động**: Đảm bảo Python và Tkinter đã được cài đặt đúng cách
- **Không tìm thấy đường đi**: Kiểm tra xem có đường đi từ điểm bắt đầu đến điểm kết thúc không
- **Mô phỏng chậm**: Điều chỉnh tốc độ mô phỏng bằng thanh trượt trong tab "Tìm đường"
- **Lỗi khi tải bản đồ**: Đảm bảo tệp JSON có định dạng đúng


## Phát triển trong tương lai

- Thêm chức năng tạo mê cung 3D
- Thêm thuật toán tìm đường nâng cao như Jump Point Search
- Thêm chức năng xuất video mô phỏng
- Thêm chức năng tạo mê cung từ hình ảnh
- Thêm chức năng tạo mê cung nhiều tầng với cầu thang lên xuống
- Thêm giao diện đồ họa nâng cao với hiệu ứng và hoạt ảnh


## Đóng góp

Đóng góp và báo cáo lỗi luôn được chào đón! Vui lòng tạo issue hoặc pull request trên repository.

## Giấy phép

Dự án này được phân phối dưới giấy phép MIT. Xem tệp `LICENSE` để biết thêm chi tiết.
