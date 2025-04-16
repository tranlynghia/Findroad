from collections import deque
import heapq

# Định nghĩa các loại ô
EMPTY = 0
WALL = 1
START = 2
END = 3
PATH = 4
VISITED = 5

# Hàm kiểm tra xem một ô có hợp lệ không
def is_valid(grid, row, col):
    rows = len(grid)
    cols = len(grid[0])
    return 0 <= row < rows and 0 <= col < cols and grid[row][col] != WALL

# Thuật toán BFS (Breadth-First Search)
def bfs(grid, start, end, return_visited=False):
    start_x, start_y = start
    end_x, end_y = end
    rows = len(grid)
    cols = len(grid[0])
    
    # Mảng đánh dấu các ô đã thăm
    visited = [[False for _ in range(cols)] for _ in range(rows)]
    
    # Hàng đợi chứa các ô cần thăm
    queue = deque([(start_x, start_y)])
    
    # Mảng lưu trữ đường đi
    parent = {}
    
    # Mảng lưu trữ thứ tự các ô đã thăm (cho mô phỏng)
    visited_order = []
    
    visited[start_y][start_x] = True
    visited_order.append((start_x, start_y))
    
    # Các hướng di chuyển: lên, phải, xuống, trái
    directions = [(0, -1), (1, 0), (0, 1), (-1, 0)]
    
    while queue:
        x, y = queue.popleft()
        
        # Nếu đã đến đích
        if (x, y) == (end_x, end_y):
            path = reconstruct_path(parent, end)
            if return_visited:
                return path, visited_order
            return path
        
        # Thử các hướng di chuyển
        for dx, dy in directions:
            new_x, new_y = x + dx, y + dy
            
            if is_valid(grid, new_y, new_x) and not visited[new_y][new_x]:
                visited[new_y][new_x] = True
                visited_order.append((new_x, new_y))
                queue.append((new_x, new_y))
                parent[(new_x, new_y)] = (x, y)
    
    # Không tìm thấy đường đi
    if return_visited:
        return [], visited_order
    return []

# Thuật toán DFS (Depth-First Search)
def dfs(grid, start, end, return_visited=False):
    start_x, start_y = start
    end_x, end_y = end
    rows = len(grid)
    cols = len(grid[0])
    
    # Mảng đánh dấu các ô đã thăm
    visited = [[False for _ in range(cols)] for _ in range(rows)]
    
    # Mảng lưu trữ đường đi
    parent = {}
    
    # Mảng lưu trữ thứ tự các ô đã thăm (cho mô phỏng)
    visited_order = []
    
    # Ngăn xếp chứa các ô cần thăm
    stack = [(start_x, start_y)]
    
    while stack:
        x, y = stack.pop()
        
        if visited[y][x]:
            continue
            
        visited[y][x] = True
        visited_order.append((x, y))
        
        # Nếu đã đến đích
        if (x, y) == (end_x, end_y):
            path = reconstruct_path(parent, end)
            if return_visited:
                return path, visited_order
            return path
        
        # Các hướng di chuyển: lên, phải, xuống, trái
        directions = [(0, -1), (1, 0), (0, 1), (-1, 0)]
        
        # Thử các hướng di chuyển
        for dx, dy in directions:
            new_x, new_y = x + dx, y + dy
            
            if is_valid(grid, new_y, new_x) and not visited[new_y][new_x]:
                stack.append((new_x, new_y))
                parent[(new_x, new_y)] = (x, y)
    
    # Không tìm thấy đường đi
    if return_visited:
        return [], visited_order
    return []

# Thuật toán Dijkstra
def dijkstra(grid, start, end, return_visited=False):
    start_x, start_y = start
    end_x, end_y = end
    rows = len(grid)
    cols = len(grid[0])
    
    # Mảng lưu trữ khoảng cách từ điểm bắt đầu đến mỗi ô
    distance = [[float('inf') for _ in range(cols)] for _ in range(rows)]
    
    # Mảng đánh dấu các ô đã thăm
    visited = [[False for _ in range(cols)] for _ in range(rows)]
    
    # Mảng lưu trữ đường đi
    parent = {}
    
    # Mảng lưu trữ thứ tự các ô đã thăm (cho mô phỏng)
    visited_order = []
    
    # Khoảng cách từ điểm bắt đầu đến chính nó là 0
    distance[start_y][start_x] = 0
    
    # Hàng đợi ưu tiên chứa các ô cần thăm
    priority_queue = [(0, start_x, start_y)]
    
    # Các hướng di chuyển: lên, phải, xuống, trái
    directions = [(0, -1), (1, 0), (0, 1), (-1, 0)]
    
    while priority_queue:
        dist, x, y = heapq.heappop(priority_queue)
        
        # Nếu ô này đã được thăm với khoảng cách ngắn hơn
        if visited[y][x]:
            continue
        
        visited[y][x] = True
        visited_order.append((x, y))
        
        # Nếu đã đến đích
        if (x, y) == (end_x, end_y):
            path = reconstruct_path(parent, end)
            if return_visited:
                return path, visited_order
            return path
        
        # Thử các hướng di chuyển
        for dx, dy in directions:
            new_x, new_y = x + dx, y + dy
            
            if is_valid(grid, new_y, new_x) and not visited[new_y][new_x]:
                # Khoảng cách mới = khoảng cách hiện tại + 1
                new_dist = dist + 1
                
                if new_dist < distance[new_y][new_x]:
                    distance[new_y][new_x] = new_dist
                    parent[(new_x, new_y)] = (x, y)
                    heapq.heappush(priority_queue, (new_dist, new_x, new_y))
    
    # Không tìm thấy đường đi
    if return_visited:
        return [], visited_order
    return []

# Thuật toán A*
def astar(grid, start, end, return_visited=False):
    start_x, start_y = start
    end_x, end_y = end
    rows = len(grid)
    cols = len(grid[0])
    
    # Hàm tính khoảng cách Manhattan
    def heuristic(x, y):
        return abs(x - end_x) + abs(y - end_y)
    
    # Mảng lưu trữ khoảng cách từ điểm bắt đầu đến mỗi ô
    g_score = [[float('inf') for _ in range(cols)] for _ in range(rows)]
    
    # Mảng lưu trữ tổng khoảng cách (g + h)
    f_score = [[float('inf') for _ in range(cols)] for _ in range(rows)]
    
    # Mảng đánh dấu các ô đã thăm
    visited = [[False for _ in range(cols)] for _ in range(rows)]
    
    # Mảng lưu trữ đường đi
    parent = {}
    
    # Mảng lưu trữ thứ tự các ô đã thăm (cho mô phỏng)
    visited_order = []
    
    # Khoảng cách từ điểm bắt đầu đến chính nó là 0
    g_score[start_y][start_x] = 0
    f_score[start_y][start_x] = heuristic(start_x, start_y)
    
    # Hàng đợi ưu tiên chứa các ô cần thăm
    priority_queue = [(f_score[start_y][start_x], 0, start_x, start_y)]
    
    # Các hướng di chuyển: lên, phải, xuống, trái
    directions = [(0, -1), (1, 0), (0, 1), (-1, 0)]
    
    while priority_queue:
        _, g, x, y = heapq.heappop(priority_queue)
        
        # Nếu ô này đã được thăm
        if visited[y][x]:
            continue
        
        visited[y][x] = True
        visited_order.append((x, y))
        
        # Nếu đã đến đích
        if (x, y) == (end_x, end_y):
            path = reconstruct_path(parent, end)
            if return_visited:
                return path, visited_order
            return path
        
        # Thử các hướng di chuyển
        for dx, dy in directions:
            new_x, new_y = x + dx, y + dy
            
            if is_valid(grid, new_y, new_x) and not visited[new_y][new_x]:
                # Khoảng cách mới = khoảng cách hiện tại + 1
                tentative_g = g + 1
                
                if tentative_g < g_score[new_y][new_x]:
                    # Tìm thấy đường đi tốt hơn
                    parent[(new_x, new_y)] = (x, y)
                    g_score[new_y][new_x] = tentative_g
                    f_score[new_y][new_x] = tentative_g + heuristic(new_x, new_y)
                    heapq.heappush(priority_queue, (f_score[new_y][new_x], tentative_g, new_x, new_y))
    
    # Không tìm thấy đường đi
    if return_visited:
        return [], visited_order
    return []

# Hàm tái tạo đường đi từ điểm bắt đầu đến điểm kết thúc
def reconstruct_path(parent, end):
    path = []
    current = end
    
    while current in parent:
        path.append(current)
        current = parent[current]
    
    # Đảo ngược đường đi để có thứ tự từ điểm bắt đầu đến điểm kết thúc
    return path[::-1]