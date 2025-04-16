import tkinter as tk
from tkinter import ttk, messagebox, filedialog, simpledialog
import json
import time
import random
from algorithms import bfs, dfs, dijkstra, astar
from algorithm_selector import select_best_algorithm
from maze_generator import generate_maze, MAZE_ALGORITHMS
from history_manager import HistoryManager

# Định nghĩa các hằng số
CELL_SIZE = 30
DEFAULT_ROWS = 20
DEFAULT_COLS = 20

# Định nghĩa các loại ô
EMPTY = 0
WALL = 1
START = 2
END = 3
PATH = 4
VISITED = 5  # Ô đã thăm trong quá trình tìm đường

# Màu sắc tương ứng
COLORS = {
    EMPTY: "white",
    WALL: "#374151",
    START: "#22c55e",
    END: "#ef4444",
    PATH: "#3b82f6",
    VISITED: "#fde68a"  # Màu vàng nhạt cho ô đã thăm
}

class MazeApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Trình tạo bản đồ ngẫu nhiên v3")
        self.geometry(f"{DEFAULT_COLS*CELL_SIZE + 500}x{DEFAULT_ROWS*CELL_SIZE + 100}")
        self.resizable(True, True)
        
        # Khởi tạo biến
        self.rows = DEFAULT_ROWS
        self.cols = DEFAULT_COLS
        self.grid = [[EMPTY for _ in range(self.cols)] for _ in range(self.rows)]
        self.start = (0, 1)
        self.end = (self.cols-1, self.rows-4)
        self.grid[self.start[1]][self.start[0]] = START
        self.grid[self.end[1]][self.end[0]] = END
        
        self.is_setting_start = False
        self.is_setting_end = False
        self.selected_tile = WALL
        self.wall_density = 20
        self.path_density = 15
        self.algorithm = "Auto"
        self.maze_algorithm = "Recursive Backtracking"
        self.animation_speed = 50  # ms giữa các bước
        self.is_animating = False
        self.animation_id = None
        self.visited_cells = []
        self.path_cells = []
        self.current_step = 0
        
        # Khởi tạo quản lý lịch sử
        self.history_manager = HistoryManager()
        
        # Tạo giao diện
        self.create_widgets()
        self.draw_grid()
        
    def create_widgets(self):
        # Tạo frame chính
        main_frame = ttk.Frame(self)
        main_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Tạo frame cho bản đồ
        self.canvas_frame = ttk.LabelFrame(main_frame, text="Bản đồ")
        self.canvas_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        
        # Tạo canvas để vẽ bản đồ
        self.canvas = tk.Canvas(
            self.canvas_frame, 
            width=self.cols*CELL_SIZE, 
            height=self.rows*CELL_SIZE,
            bg="gray90"
        )
        self.canvas.pack(padx=10, pady=10)
        self.canvas.bind("<Button-1>", self.on_canvas_click)
        
        # Tạo frame cho các điều khiển
        controls_frame = ttk.LabelFrame(main_frame, text="Điều khiển")
        controls_frame.pack(side=tk.RIGHT, fill=tk.BOTH, padx=10)
        
        # Notebook để tổ chức các tab
        notebook = ttk.Notebook(controls_frame)
        notebook.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        # Tab 1: Tạo bản đồ
        map_tab = ttk.Frame(notebook)
        notebook.add(map_tab, text="Tạo bản đồ")
        
        # Kích thước bản đồ
        size_frame = ttk.LabelFrame(map_tab, text="Kích thước bản đồ")
        size_frame.pack(fill=tk.X, padx=5, pady=5)
        
        ttk.Button(size_frame, text="Thay đổi kích thước", command=self.change_map_size).pack(padx=5, pady=5)
        
        # Mật độ tường
        ttk.Label(map_tab, text="Mật độ tường (%)").pack(anchor=tk.W, padx=5, pady=5)
        self.wall_density_var = tk.IntVar(value=self.wall_density)
        wall_density_scale = ttk.Scale(
            map_tab, 
            from_=0, 
            to=50, 
            orient=tk.HORIZONTAL,
            variable=self.wall_density_var,
            command=lambda _: self.wall_density_var.set(int(self.wall_density_var.get()))
        )
        wall_density_scale.pack(fill=tk.X, padx=5, pady=5)
        ttk.Label(map_tab, textvariable=self.wall_density_var).pack(anchor=tk.E, padx=5)
        
        # Mật độ đường đi
        ttk.Label(map_tab, text="Mật độ đường đi (%)").pack(anchor=tk.W, padx=5, pady=5)
        self.path_density_var = tk.IntVar(value=self.path_density)
        path_density_scale = ttk.Scale(
            map_tab, 
            from_=0, 
            to=50, 
            orient=tk.HORIZONTAL,
            variable=self.path_density_var,
            command=lambda _: self.path_density_var.set(int(self.path_density_var.get()))
        )
        path_density_scale.pack(fill=tk.X, padx=5, pady=5)
        ttk.Label(map_tab, textvariable=self.path_density_var).pack(anchor=tk.E, padx=5)
        
        # Loại ô để vẽ
        ttk.Label(map_tab, text="Loại ô để vẽ").pack(anchor=tk.W, padx=5, pady=5)
        self.tile_var = tk.StringVar(value="Tường")
        tile_combo = ttk.Combobox(
            map_tab, 
            textvariable=self.tile_var,
            values=["Trống", "Tường"],
            state="readonly"
        )
        tile_combo.pack(fill=tk.X, padx=5, pady=5)
        tile_combo.bind("<<ComboboxSelected>>", self.on_tile_selected)
        
        # Thuật toán tạo mê cung
        ttk.Label(map_tab, text="Thuật toán tạo mê cung").pack(anchor=tk.W, padx=5, pady=5)
        self.maze_algorithm_var = tk.StringVar(value=self.maze_algorithm)
        maze_algorithm_combo = ttk.Combobox(
            map_tab, 
            textvariable=self.maze_algorithm_var,
            values=list(MAZE_ALGORITHMS.keys()),
            state="readonly"
        )
        maze_algorithm_combo.pack(fill=tk.X, padx=5, pady=5)
        
        # Các nút tạo bản đồ
        ttk.Button(map_tab, text="Tạo bản đồ ngẫu nhiên", command=self.generate_random_map).pack(fill=tk.X, padx=5, pady=5)
        ttk.Button(map_tab, text="Tạo mê cung", command=self.generate_maze).pack(fill=tk.X, padx=5, pady=5)
        ttk.Button(map_tab, text="Xóa bản đồ", command=self.clear_grid).pack(fill=tk.X, padx=5, pady=5)
        
        # Tab 2: Tìm đường
        pathfinding_tab = ttk.Frame(notebook)
        notebook.add(pathfinding_tab, text="Tìm đường")
        
        # Thuật toán tìm đường
        ttk.Label(pathfinding_tab, text="Thuật toán tìm đường").pack(anchor=tk.W, padx=5, pady=5)
        self.algorithm_var = tk.StringVar(value=self.algorithm)
        algorithm_combo = ttk.Combobox(
            pathfinding_tab, 
            textvariable=self.algorithm_var,
            values=["Auto", "BFS", "DFS", "Dijkstra", "A*"],
            state="readonly"
        )
        algorithm_combo.pack(fill=tk.X, padx=5, pady=5)
        
        # Tốc độ mô phỏng
        ttk.Label(pathfinding_tab, text="Tốc độ mô phỏng").pack(anchor=tk.W, padx=5, pady=5)
        self.speed_var = tk.IntVar(value=self.animation_speed)
        speed_scale = ttk.Scale(
            pathfinding_tab, 
            from_=1, 
            to=200, 
            orient=tk.HORIZONTAL,
            variable=self.speed_var,
            command=lambda _: self.speed_var.set(int(self.speed_var.get()))
        )
        speed_scale.pack(fill=tk.X, padx=5, pady=5)
        ttk.Label(pathfinding_tab, textvariable=self.speed_var).pack(anchor=tk.E, padx=5)
        
        # Các nút điều khiển tìm đường
        ttk.Button(pathfinding_tab, text="Tìm đường (Ngay lập tức)", command=self.run_algorithm_instant).pack(fill=tk.X, padx=5, pady=5)
        ttk.Button(pathfinding_tab, text="Tìm đường (Mô phỏng)", command=self.run_algorithm_animated).pack(fill=tk.X, padx=5, pady=5)
        ttk.Button(pathfinding_tab, text="Dừng mô phỏng", command=self.stop_animation).pack(fill=tk.X, padx=5, pady=5)
        ttk.Button(pathfinding_tab, text="Xóa đường đi", command=self.clear_path).pack(fill=tk.X, padx=5, pady=5)
        
        # Các nút đặt điểm bắt đầu/kết thúc
        ttk.Button(pathfinding_tab, text="Đặt điểm bắt đầu", command=self.set_start_point).pack(fill=tk.X, padx=5, pady=5)
        ttk.Button(pathfinding_tab, text="Đặt điểm kết thúc", command=self.set_end_point).pack(fill=tk.X, padx=5, pady=5)
        
        # Tab 3: So sánh thuật toán
        compare_tab = ttk.Frame(notebook)
        notebook.add(compare_tab, text="So sánh")
        
        ttk.Button(compare_tab, text="So sánh tất cả thuật toán", command=self.compare_algorithms).pack(fill=tk.X, padx=5, pady=5)
        
        # Kết quả so sánh
        self.compare_result = tk.Text(compare_tab, height=15, width=40)
        self.compare_result.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        # Tab 4: Lịch sử & Lưu/Tải
        history_tab = ttk.Frame(notebook)
        notebook.add(history_tab, text="Lịch sử & Lưu/Tải")
        
        # Lịch sử bản đồ
        ttk.Label(history_tab, text="Lịch sử bản đồ").pack(anchor=tk.W, padx=5, pady=5)
        self.history_listbox = tk.Listbox(history_tab, height=10)
        self.history_listbox.pack(fill=tk.X, padx=5, pady=5)
        self.history_listbox.bind("<Double-1>", self.load_from_history)
        
        # Các nút lưu/tải
        ttk.Button(history_tab, text="Lưu bản đồ hiện tại", command=self.save_to_history).pack(fill=tk.X, padx=5, pady=5)
        ttk.Button(history_tab, text="Xuất bản đồ", command=self.export_map).pack(fill=tk.X, padx=5, pady=5)
        ttk.Button(history_tab, text="Nhập bản đồ", command=self.import_map).pack(fill=tk.X, padx=5, pady=5)
        
        # Trạng thái
        status_frame = ttk.LabelFrame(controls_frame, text="Trạng thái")
        status_frame.pack(fill=tk.X, padx=5, pady=5)
        
        self.status_var = tk.StringVar()
        ttk.Label(status_frame, textvariable=self.status_var, wraplength=300).pack(padx=5, pady=5)
        
        # Chú thích
        legend_frame = ttk.LabelFrame(controls_frame, text="Chú thích")
        legend_frame.pack(fill=tk.X, padx=5, pady=5)
        
        legend_items = [
            ("Trống", EMPTY),
            ("Tường", WALL),
            ("Điểm bắt đầu", START),
            ("Điểm kết thúc", END),
            ("Đường đi", PATH),
            ("Đã thăm", VISITED)
        ]
        
        legend_grid = ttk.Frame(legend_frame)
        legend_grid.pack(padx=5, pady=5)
        
        for i, (name, value) in enumerate(legend_items):
            row, col = divmod(i, 2)
            canvas = tk.Canvas(legend_grid, width=20, height=20, bg=COLORS[value], highlightthickness=1, highlightbackground="gray")
            canvas.grid(row=row, column=col*2, padx=5, pady=2)
            ttk.Label(legend_grid, text=name).grid(row=row, column=col*2+1, sticky=tk.W, padx=5, pady=2)
    
    def on_tile_selected(self, event):
        tile_name = self.tile_var.get()
        if tile_name == "Trống":
            self.selected_tile = EMPTY
        elif tile_name == "Tường":
            self.selected_tile = WALL
    
    def draw_grid(self):
        self.canvas.delete("all")
        for row in range(self.rows):
            for col in range(self.cols):
                x1, y1 = col * CELL_SIZE, row * CELL_SIZE
                x2, y2 = x1 + CELL_SIZE, y1 + CELL_SIZE
                
                if row < len(self.grid) and col < len(self.grid[0]):
                    cell_type = self.grid[row][col]
                    color = COLORS[cell_type]
                    
                    self.canvas.create_rectangle(x1, y1, x2, y2, fill=color, outline="gray")
                    
                    if cell_type == START:
                        self.canvas.create_text(x1 + CELL_SIZE//2, y1 + CELL_SIZE//2, text="S", font=("Arial", 12, "bold"))
                    elif cell_type == END:
                        self.canvas.create_text(x1 + CELL_SIZE//2, y1 + CELL_SIZE//2, text="E", font=("Arial", 12, "bold"))
    
    def on_canvas_click(self, event):
        col = event.x // CELL_SIZE
        row = event.y // CELL_SIZE
        
        if col < 0 or col >= self.cols or row < 0 or row >= self.rows:
            return
        
        if self.is_setting_start:
            # Xóa điểm bắt đầu cũ
            old_start_x, old_start_y = self.start
            self.grid[old_start_y][old_start_x] = EMPTY
            
            # Đặt điểm bắt đầu mới
            self.start = (col, row)
            self.grid[row][col] = START
            self.is_setting_start = False
            self.status_var.set("Đã đặt điểm bắt đầu mới.")
        
        elif self.is_setting_end:
            # Xóa điểm kết thúc cũ
            old_end_x, old_end_y = self.end
            self.grid[old_end_y][old_end_x] = EMPTY
            
            # Đặt điểm kết thúc mới
            self.end = (col, row)
            self.grid[row][col] = END
            self.is_setting_end = False
            self.status_var.set("Đã đặt điểm kết thúc mới.")
        
        else:
            # Không cho phép thay đổi điểm bắt đầu và kết thúc trực tiếp
            if (col, row) == self.start or (col, row) == self.end:
                return
            
            self.grid[row][col] = self.selected_tile
        
        self.draw_grid()
    
    def change_map_size(self):
        try:
            new_rows = simpledialog.askinteger("Số hàng", "Nhập số hàng (5-50):", minvalue=5, maxvalue=50)
            if new_rows is None:
                return
                
            new_cols = simpledialog.askinteger("Số cột", "Nhập số cột (5-50):", minvalue=5, maxvalue=50)
            if new_cols is None:
                return
            
            # Lưu lại điểm bắt đầu và kết thúc nếu có thể
            old_start = self.start
            old_end = self.end
            
            # Tạo lưới mới
            new_grid = [[EMPTY for _ in range(new_cols)] for _ in range(new_rows)]
            
            # Sao chép dữ liệu từ lưới cũ sang lưới mới
            for row in range(min(self.rows, new_rows)):
                for col in range(min(self.cols, new_cols)):
                    new_grid[row][col] = self.grid[row][col]
            
            # Cập nhật kích thước
            self.rows = new_rows
            self.cols = new_cols
            self.grid = new_grid
            
            # Điều chỉnh kích thước canvas
            self.canvas.config(width=self.cols*CELL_SIZE, height=self.rows*CELL_SIZE)
            
            # Kiểm tra và điều chỉnh điểm bắt đầu và kết thúc
            start_x, start_y = old_start
            end_x, end_y = old_end
            
            if start_x >= new_cols or start_y >= new_rows:
                self.start = (0, 0)
                self.grid[0][0] = START
            else:
                self.start = old_start
                self.grid[start_y][start_x] = START
                
            if end_x >= new_cols or end_y >= new_rows:
                self.end = (new_cols-1, new_rows-1)
                self.grid[new_rows-1][new_cols-1] = END
            else:
                self.end = old_end
                self.grid[end_y][end_x] = END
            
            self.draw_grid()
            self.status_var.set(f"Đã thay đổi kích thước bản đồ thành {new_rows}x{new_cols}.")
            
        except Exception as e:
            messagebox.showerror("Lỗi", f"Không thể thay đổi kích thước: {str(e)}")
    
    def generate_random_map(self):
        # Tạo bản đồ trống
        self.grid = [[EMPTY for _ in range(self.cols)] for _ in range(self.rows)]
        
        # Đặt điểm bắt đầu và kết thúc
        start_x, start_y = self.start
        end_x, end_y = self.end
        self.grid[start_y][start_x] = START
        self.grid[end_y][end_x] = END
        
        # Lấy giá trị mật độ từ thanh trượt
        self.wall_density = self.wall_density_var.get()
        self.path_density = self.path_density_var.get()
        
        # Tạo các ô ngẫu nhiên trên bản đồ
        for row in range(self.rows):
            for col in range(self.cols):
                # Bỏ qua điểm bắt đầu và kết thúc
                if (col, row) == self.start or (col, row) == self.end:
                    continue
                
                random_value = random.random() * 100
                
                if random_value < self.wall_density:
                    self.grid[row][col] = WALL
                elif random_value < self.wall_density + self.path_density:
                    self.grid[row][col] = PATH
        
        self.draw_grid()
        self.status_var.set("Đã tạo bản đồ ngẫu nhiên mới.")
    
    def generate_maze(self):
        algorithm_name = self.maze_algorithm_var.get()
        if algorithm_name not in MAZE_ALGORITHMS:
            messagebox.showerror("Lỗi", "Thuật toán không hợp lệ.")
            return
        
        # Tạo mê cung
        self.grid = generate_maze(self.rows, self.cols, algorithm_name, self.start, self.end)
        
        self.draw_grid()
        self.status_var.set(f"Đã tạo mê cung bằng thuật toán {algorithm_name}.")
    
    def clear_grid(self):
        self.grid = [[EMPTY for _ in range(self.cols)] for _ in range(self.rows)]
        self.grid[self.start[1]][self.start[0]] = START
        self.grid[self.end[1]][self.end[0]] = END
        self.draw_grid()
        self.status_var.set("Đã xóa bản đồ.")
    
    def clear_path(self):
        for row in range(self.rows):
            for col in range(self.cols):
                if self.grid[row][col] == PATH or self.grid[row][col] == VISITED:
                    self.grid[row][col] = EMPTY
        
        self.draw_grid()
        self.status_var.set("Đã xóa đường đi.")
    
    def set_start_point(self):
        self.is_setting_start = True
        self.is_setting_end = False
        self.status_var.set("Nhấp vào vị trí mới cho điểm bắt đầu.")
    
    def set_end_point(self):
        self.is_setting_end = True
        self.is_setting_start = False
        self.status_var.set("Nhấp vào vị trí mới cho điểm kết thúc.")
    
    def run_algorithm_instant(self):
        if not self.start or not self.end:
            messagebox.showerror("Lỗi", "Vui lòng đặt điểm bắt đầu và kết thúc.")
            return
        
        # Xóa đường đi cũ
        self.clear_path()
        
        # Chọn thuật toán
        selected_algorithm = self.algorithm_var.get()
        if selected_algorithm == "Auto":
            selected_algorithm = select_best_algorithm(self.grid)
        
        start_time = time.time()
        
        # Chạy thuật toán tìm đường
        if selected_algorithm == "BFS":
            path, visited = bfs(self.grid, self.start, self.end, return_visited=True)
        elif selected_algorithm == "DFS":
            path, visited = dfs(self.grid, self.start, self.end, return_visited=True)
        elif selected_algorithm == "Dijkstra":
            path, visited = dijkstra(self.grid, self.start, self.end, return_visited=True)
        elif selected_algorithm == "A*":
            path, visited = astar(self.grid, self.start, self.end, return_visited=True)
        else:
            path, visited = [], []
        
        end_time = time.time()
        time_taken = end_time - start_time
        
        if path:
            # Đánh dấu đường đi trên bản đồ
            for x, y in path:
                if (x, y) != self.start and (x, y) != self.end:
                    self.grid[y][x] = PATH
            
            self.draw_grid()
            self.status_var.set(f"Thuật toán: {selected_algorithm}, Số bước: {len(path)}, Thời gian: {time_taken:.4f}s, Ô đã thăm: {len(visited)}")
        else:
            self.status_var.set(f"Thuật toán: {selected_algorithm}, Không tìm thấy đường đi. Ô đã thăm: {len(visited)}")
    
    def run_algorithm_animated(self):
        if not self.start or not self.end:
            messagebox.showerror("Lỗi", "Vui lòng đặt điểm bắt đầu và kết thúc.")
            return
        
        # Xóa đường đi cũ
        self.clear_path()
        
        # Dừng mô phỏng hiện tại nếu có
        self.stop_animation()
        
        # Chọn thuật toán
        selected_algorithm = self.algorithm_var.get()
        if selected_algorithm == "Auto":
            selected_algorithm = select_best_algorithm(self.grid)
        
        # Chạy thuật toán tìm đường
        if selected_algorithm == "BFS":
            path, visited = bfs(self.grid, self.start, self.end, return_visited=True)
        elif selected_algorithm == "DFS":
            path, visited = dfs(self.grid, self.start, self.end, return_visited=True)
        elif selected_algorithm == "Dijkstra":
            path, visited = dijkstra(self.grid, self.start, self.end, return_visited=True)
        elif selected_algorithm == "A*":
            path, visited = astar(self.grid, self.start, self.end, return_visited=True)
        else:
            path, visited = [], []
        
        if not visited:
            self.status_var.set(f"Thuật toán: {selected_algorithm}, Không có ô nào được thăm.")
            return
        
        # Lưu trữ thông tin cho mô phỏng
        self.visited_cells = visited
        self.path_cells = path
        self.current_step = 0
        self.is_animating = True
        self.animation_speed = self.speed_var.get()
        
        # Bắt đầu mô phỏng
        self.animate_step()
        self.status_var.set(f"Đang mô phỏng thuật toán {selected_algorithm}...")
    
    def animate_step(self):
        if not self.is_animating:
            return
        
        if self.current_step < len(self.visited_cells):
            # Hiển thị ô đang thăm
            x, y = self.visited_cells[self.current_step]
            if (x, y) != self.start and (x, y) != self.end:
                self.grid[y][x] = VISITED
            
            self.current_step += 1
            self.draw_grid()
            
            # Lên lịch bước tiếp theo
            self.animation_id = self.after(self.animation_speed, self.animate_step)
        elif self.path_cells:
            # Hiển thị đường đi sau khi đã thăm tất cả các ô
            for x, y in self.path_cells:
                if (x, y) != self.start and (x, y) != self.end:
                    self.grid[y][x] = PATH
            
            self.draw_grid()
            self.is_animating = False
            self.status_var.set(f"Hoàn thành mô phỏng. Đã thăm {len(self.visited_cells)} ô, tìm thấy đường đi với {len(self.path_cells)} bước.")
        else:
            self.is_animating = False
            self.status_var.set(f"Hoàn thành mô phỏng. Đã thăm {len(self.visited_cells)} ô, không tìm thấy đường đi.")
    
    def stop_animation(self):
        self.is_animating = False
        if self.animation_id:
            self.after_cancel(self.animation_id)
            self.animation_id = None
    
    def compare_algorithms(self):
        if not self.start or not self.end:
            messagebox.showerror("Lỗi", "Vui lòng đặt điểm bắt đầu và kết thúc.")
            return
        
        # Xóa đường đi cũ
        self.clear_path()
        
        # Xóa kết quả cũ
        self.compare_result.delete(1.0, tk.END)
        
        algorithms = ["BFS", "DFS", "Dijkstra", "A*"]
        results = []
        
        for algo in algorithms:
            start_time = time.time()
            
            if algo == "BFS":
                path, visited = bfs(self.grid, self.start, self.end, return_visited=True)
            elif algo == "DFS":
                path, visited = dfs(self.grid, self.start, self.end, return_visited=True)
            elif algo == "Dijkstra":
                path, visited = dijkstra(self.grid, self.start, self.end, return_visited=True)
            elif algo == "A*":
                path, visited = astar(self.grid, self.start, self.end, return_visited=True)
            
            end_time = time.time()
            time_taken = end_time - start_time
            
            results.append({
                "algorithm": algo,
                "path_length": len(path) if path else 0,
                "visited_cells": len(visited),
                "time": time_taken,
                "found_path": bool(path)
            })
        
        # Hiển thị kết quả
        self.compare_result.insert(tk.END, "So sánh thuật toán tìm đường:\n\n")
        
        # Sắp xếp theo thời gian
        results.sort(key=lambda x: x["time"])
        
        self.compare_result.insert(tk.END, "Xếp hạng theo thời gian:\n")
        for i, result in enumerate(results):
            status = "Tìm thấy đường đi" if result["found_path"] else "Không tìm thấy đường đi"
            self.compare_result.insert(tk.END, f"{i+1}. {result['algorithm']}: {result['time']:.6f}s, {result['visited_cells']} ô đã thăm, {result['path_length']} bước, {status}\n")
        
        # Sắp xếp theo số ô đã thăm
        results.sort(key=lambda x: x["visited_cells"])
        
        self.compare_result.insert(tk.END, "\nXếp hạng theo số ô đã thăm:\n")
        for i, result in enumerate(results):
            status = "Tìm thấy đường đi" if result["found_path"] else "Không tìm thấy đường đi"
            self.compare_result.insert(tk.END, f"{i+1}. {result['algorithm']}: {result['visited_cells']} ô đã thăm, {result['time']:.6f}s, {result['path_length']} bước, {status}\n")
        
        # Sắp xếp theo độ dài đường đi (nếu tìm thấy)
        valid_results = [r for r in results if r["found_path"]]
        if valid_results:
            valid_results.sort(key=lambda x: x["path_length"])
            
            self.compare_result.insert(tk.END, "\nXếp hạng theo độ dài đường đi:\n")
            for i, result in enumerate(valid_results):
                self.compare_result.insert(tk.END, f"{i+1}. {result['algorithm']}: {result['path_length']} bước, {result['time']:.6f}s, {result['visited_cells']} ô đã thăm\n")
        
        self.status_var.set("Đã hoàn thành so sánh thuật toán.")
    
    def save_to_history(self):
        name = simpledialog.askstring("Tên bản đồ", "Nhập tên cho bản đồ:")
        if not name:
            return
        
        self.history_manager.add_map(name, self.grid, self.start, self.end)
        self.update_history_list()
        self.status_var.set(f"Đã lưu bản đồ '{name}' vào lịch sử.")
    
    def update_history_list(self):
        self.history_listbox.delete(0, tk.END)
        for name in self.history_manager.get_map_names():
            self.history_listbox.insert(tk.END, name)
    
    def load_from_history(self, event):
        selected_index = self.history_listbox.curselection()
        if not selected_index:
            return
        
        name = self.history_listbox.get(selected_index[0])
        map_data = self.history_manager.get_map(name)
        
        if map_data:
            self.grid = map_data["grid"]
            self.start = map_data["start"]
            self.end = map_data["end"]
            
            # Kiểm tra kích thước bản đồ
            if len(self.grid) != self.rows or len(self.grid[0]) != self.cols:
                self.rows = len(self.grid)
                self.cols = len(self.grid[0])
                self.canvas.config(width=self.cols*CELL_SIZE, height=self.rows*CELL_SIZE)
            
            self.draw_grid()
            self.status_var.set(f"Đã tải bản đồ '{name}' từ lịch sử.")
    
    def export_map(self):
        file = filedialog.asksaveasfilename(
            defaultextension=".json",
            filetypes=[("JSON Files", "*.json"), ("All Files", "*.*")]
        )
        
        if file:
            data = {
                "grid": self.grid,
                "start": self.start,
                "end": self.end,
                "rows": self.rows,
                "cols": self.cols
            }
            
            with open(file, 'w') as f:
                json.dump(data, f)
            
            self.status_var.set(f"Đã xuất bản đồ vào {file}")
    
    def import_map(self):
        file = filedialog.askopenfilename(
            filetypes=[("JSON Files", "*.json"), ("All Files", "*.*")]
        )
        
        if file:
            try:
                with open(file, 'r') as f:
                    data = json.load(f)
                
                self.grid = data.get("grid", [[EMPTY for _ in range(self.cols)] for _ in range(self.rows)])
                self.start = tuple(data.get("start", (0, 0)))
                self.end = tuple(data.get("end", (self.cols-1, self.rows-1)))
                
                # Kiểm tra kích thước bản đồ
                new_rows = data.get("rows", len(self.grid))
                new_cols = data.get("cols", len(self.grid[0]))
                
                if new_rows != self.rows or new_cols != self.cols:
                    self.rows = new_rows
                    self.cols = new_cols
                    self.canvas.config(width=self.cols*CELL_SIZE, height=self.rows*CELL_SIZE)
                
                self.draw_grid()
                self.status_var.set(f"Đã nhập bản đồ từ {file}")
            except Exception as e:
                messagebox.showerror("Lỗi", f"Không thể đọc tệp: {str(e)}")