import random

# Định nghĩa các loại ô
EMPTY = 0
WALL = 1
START = 2
END = 3
PATH = 4

# Thuật toán tạo mê cung bằng Recursive Backtracking
def recursive_backtracking(rows, cols, start, end):
    # Tạo lưới toàn tường
    grid = [[WALL for _ in range(cols)] for _ in range(rows)]
    
    # Đảm bảo số hàng và số cột là số lẻ
    if rows % 2 == 0:
        rows -= 1
    if cols % 2 == 0:
        cols -= 1
    
    # Hàm đệ quy để tạo mê cung
    def carve_passages(x, y, grid):
        # Đánh dấu ô hiện tại là đường đi
        grid[y][x] = EMPTY
        
        # Các hướng di chuyển: lên, phải, xuống, trái
        directions = [(0, -2), (2, 0), (0, 2), (-2, 0)]
        random.shuffle(directions)
        
        for dx, dy in directions:
            new_x, new_y = x + dx, y + dy
            
            # Kiểm tra xem ô mới có nằm trong lưới không
            if 0 <= new_x < cols and 0 <= new_y < rows and grid[new_y][new_x] == WALL:
                # Đánh dấu ô giữa là đường đi
                grid[y + dy//2][x + dx//2] = EMPTY
                carve_passages(new_x, new_y, grid)
    
    # Bắt đầu từ một ô ngẫu nhiên (phải là ô lẻ)
    start_x = random.randrange(1, cols, 2)
    start_y = random.randrange(1, rows, 2)
    carve_passages(start_x, start_y, grid)
    
    # Đặt điểm bắt đầu và kết thúc
    start_x, start_y = start
    end_x, end_y = end
    
    # Đảm bảo điểm bắt đầu và kết thúc là đường đi
    grid[start_y][start_x] = EMPTY
    grid[end_y][end_x] = EMPTY
    
    # Tạo đường đi từ điểm bắt đầu và kết thúc đến mê cung
    # Tìm ô đường đi gần nhất với điểm bắt đầu
    min_dist = float('inf')
    nearest_empty = None
    
    for y in range(rows):
        for x in range(cols):
            if grid[y][x] == EMPTY:
                dist = abs(x - start_x) + abs(y - start_y)
                if dist < min_dist:
                    min_dist = dist
                    nearest_empty = (x, y)
    
    if nearest_empty:
        x, y = nearest_empty
        # Tạo đường đi từ điểm bắt đầu đến ô đường đi gần nhất
        while (x, y) != (start_x, start_y):
            if x < start_x:
                x += 1
            elif x > start_x:
                x -= 1
            elif y < start_y:
                y += 1
            elif y > start_y:
                y -= 1
            grid[y][x] = EMPTY
    
    # Tìm ô đường đi gần nhất với điểm kết thúc
    min_dist = float('inf')
    nearest_empty = None
    
    for y in range(rows):
        for x in range(cols):
            if grid[y][x] == EMPTY:
                dist = abs(x - end_x) + abs(y - end_y)
                if dist < min_dist:
                    min_dist = dist
                    nearest_empty = (x, y)
    
    if nearest_empty:
        x, y = nearest_empty
        # Tạo đường đi từ điểm kết thúc đến ô đường đi gần nhất
        while (x, y) != (end_x, end_y):
            if x < end_x:
                x += 1
            elif x > end_x:
                x -= 1
            elif y < end_y:
                y += 1
            elif y > end_y:
                y -= 1
            grid[y][x] = EMPTY
    
    # Đặt điểm bắt đầu và kết thúc
    grid[start_y][start_x] = START
    grid[end_y][end_x] = END
    
    return grid

# Thuật toán tạo mê cung bằng Prim's Algorithm
def prims_algorithm(rows, cols, start, end):
    # Tạo lưới toàn tường
    grid = [[WALL for _ in range(cols)] for _ in range(rows)]
    
    # Đảm bảo số hàng và số cột là số lẻ
    if rows % 2 == 0:
        rows -= 1
    if cols % 2 == 0:
        cols -= 1
    
    # Bắt đầu từ một ô ngẫu nhiên (phải là ô lẻ)
    start_x = random.randrange(1, cols, 2)
    start_y = random.randrange(1, rows, 2)
    grid[start_y][start_x] = EMPTY
    
    # Danh sách các bức tường có thể phá
    walls = []
    
    # Các hướng di chuyển: lên, phải, xuống, trái
    directions = [(0, -2), (2, 0), (0, 2), (-2, 0)]
    
    # Thêm các bức tường xung quanh ô bắt đầu
    for dx, dy in directions:
        new_x, new_y = start_x + dx, start_y + dy
        if 0 <= new_x < cols and 0 <= new_y < rows:
            walls.append((start_x + dx//2, start_y + dy//2, new_x, new_y))
    
    # Thuật toán Prim
    while walls:
        # Chọn một bức tường ngẫu nhiên
        wall_index = random.randint(0, len(walls) - 1)
        wall_x, wall_y, cell_x, cell_y = walls.pop(wall_index)
        
        # Nếu ô bên kia bức tường chưa được thăm
        if grid[cell_y][cell_x] == WALL:
            # Phá bức tường
            grid[wall_y][wall_x] = EMPTY
            grid[cell_y][cell_x] = EMPTY
            
            # Thêm các bức tường mới
            for dx, dy in directions:
                new_x, new_y = cell_x + dx, cell_y + dy
                if 0 <= new_x < cols and 0 <= new_y < rows and grid[new_y][new_x] == WALL:
                    walls.append((cell_x + dx//2, cell_y + dy//2, new_x, new_y))
    
    # Đặt điểm bắt đầu và kết thúc
    start_x, start_y = start
    end_x, end_y = end
    
    # Đảm bảo điểm bắt đầu và kết thúc là đường đi
    grid[start_y][start_x] = EMPTY
    grid[end_y][end_x] = EMPTY
    
    # Tạo đường đi từ điểm bắt đầu và kết thúc đến mê cung
    # Tìm ô đường đi gần nhất với điểm bắt đầu
    min_dist = float('inf')
    nearest_empty = None
    
    for y in range(rows):
        for x in range(cols):
            if grid[y][x] == EMPTY:
                dist = abs(x - start_x) + abs(y - start_y)
                if dist < min_dist:
                    min_dist = dist
                    nearest_empty = (x, y)
    
    if nearest_empty:
        x, y = nearest_empty
        # Tạo đường đi từ điểm bắt đầu đến ô đường đi gần nhất
        while (x, y) != (start_x, start_y):
            if x < start_x:
                x += 1
            elif x > start_x:
                x -= 1
            elif y < start_y:
                y += 1
            elif y > start_y:
                y -= 1
            grid[y][x] = EMPTY
    
    # Tìm ô đường đi gần nhất với điểm kết thúc
    min_dist = float('inf')
    nearest_empty = None
    
    for y in range(rows):
        for x in range(cols):
            if grid[y][x] == EMPTY:
                dist = abs(x - end_x) + abs(y - end_y)
                if dist < min_dist:
                    min_dist = dist
                    nearest_empty = (x, y)
    
    if nearest_empty:
        x, y = nearest_empty
        # Tạo đường đi từ điểm kết thúc đến ô đường đi gần nhất
        while (x, y) != (end_x, end_y):
            if x < end_x:
                x += 1
            elif x > end_x:
                x -= 1
            elif y < end_y:
                y += 1
            elif y > end_y:
                y -= 1
            grid[y][x] = EMPTY
    
    # Đặt điểm bắt đầu và kết thúc
    grid[start_y][start_x] = START
    grid[end_y][end_x] = END
    
    return grid

# Thuật toán tạo mê cung bằng Binary Tree
def binary_tree(rows, cols, start, end):
    # Tạo lưới toàn tường
    grid = [[WALL for _ in range(cols)] for _ in range(rows)]
    
    # Đảm bảo số hàng và số cột là số lẻ
    if rows % 2 == 0:
        rows -= 1
    if cols % 2 == 0:
        cols -= 1
    
    # Tạo đường đi tại các ô lẻ
    for y in range(1, rows, 2):
        for x in range(1, cols, 2):
            grid[y][x] = EMPTY
            
            # Chọn ngẫu nhiên hướng Bắc hoặc Đông
            directions = []
            if y > 1:  # Có thể đi lên
                directions.append((0, -1))
            if x > 1:  # Có thể đi sang trái
                directions.append((-1, 0))
            
            if directions:
                dx, dy = random.choice(directions)
                grid[y + dy][x + dx] = EMPTY
    
    # Đặt điểm bắt đầu và kết thúc
    start_x, start_y = start
    end_x, end_y = end
    
    # Đảm bảo điểm bắt đầu và kết thúc là đường đi
    grid[start_y][start_x] = EMPTY
    grid[end_y][end_x] = EMPTY
    
    # Tạo đường đi từ điểm bắt đầu và kết thúc đến mê cung
    # Tìm ô đường đi gần nhất với điểm bắt đầu
    min_dist = float('inf')
    nearest_empty = None
    
    for y in range(rows):
        for x in range(cols):
            if grid[y][x] == EMPTY:
                dist = abs(x - start_x) + abs(y - start_y)
                if dist < min_dist:
                    min_dist = dist
                    nearest_empty = (x, y)
    
    if nearest_empty:
        x, y = nearest_empty
        # Tạo đường đi từ điểm bắt đầu đến ô đường đi gần nhất
        while (x, y) != (start_x, start_y):
            if x < start_x:
                x += 1
            elif x > start_x:
                x -= 1
            elif y < start_y:
                y += 1
            elif y > start_y:
                y -= 1
            grid[y][x] = EMPTY
    
    # Tìm ô đường đi gần nhất với điểm kết thúc
    min_dist = float('inf')
    nearest_empty = None
    
    for y in range(rows):
        for x in range(cols):
            if grid[y][x] == EMPTY:
                dist = abs(x - end_x) + abs(y - end_y)
                if dist < min_dist:
                    min_dist = dist
                    nearest_empty = (x, y)
    
    if nearest_empty:
        x, y = nearest_empty
        # Tạo đường đi từ điểm kết thúc đến ô đường đi gần nhất
        while (x, y) != (end_x, end_y):
            if x < end_x:
                x += 1
            elif x > end_x:
                x -= 1
            elif y < end_y:
                y += 1
            elif y > end_y:
                y -= 1
            grid[y][x] = EMPTY
    
    # Đặt điểm bắt đầu và kết thúc
    grid[start_y][start_x] = START
    grid[end_y][end_x] = END
    
    return grid

# Danh sách các thuật toán tạo mê cung
MAZE_ALGORITHMS = {
    "Recursive Backtracking": recursive_backtracking,
    "Prim's Algorithm": prims_algorithm,
    "Binary Tree": binary_tree
}

# Hàm tạo mê cung
def generate_maze(rows, cols, algorithm_name, start, end):
    if algorithm_name in MAZE_ALGORITHMS:
        return MAZE_ALGORITHMS[algorithm_name](rows, cols, start, end)
    else:
        # Mặc định sử dụng Recursive Backtracking
        return recursive_backtracking(rows, cols, start, end)