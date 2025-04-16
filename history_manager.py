import time
import copy

class HistoryManager:
    def __init__(self, max_history=10):
        self.max_history = max_history
        self.history = {}  # Từ điển lưu trữ bản đồ theo tên
        self.timestamps = {}  # Từ điển lưu trữ thời gian tạo bản đồ
    
    def add_map(self, name, grid, start, end):
        # Tạo bản sao của bản đồ để tránh tham chiếu
        grid_copy = copy.deepcopy(grid)
        
        # Thêm bản đồ vào lịch sử
        self.history[name] = {
            "grid": grid_copy,
            "start": start,
            "end": end
        }
        
        # Lưu thời gian tạo
        self.timestamps[name] = time.time()
        
        # Nếu lịch sử vượt quá giới hạn, xóa bản đồ cũ nhất
        if len(self.history) > self.max_history:
            oldest_name = min(self.timestamps, key=self.timestamps.get)
            del self.history[oldest_name]
            del self.timestamps[oldest_name]
    
    def get_map(self, name):
        return self.history.get(name)
    
    def get_map_names(self):
        # Sắp xếp tên bản đồ theo thời gian tạo (mới nhất đầu tiên)
        return sorted(self.history.keys(), key=lambda name: self.timestamps.get(name, 0), reverse=True)
    
    def clear_history(self):
        self.history.clear()
        self.timestamps.clear()