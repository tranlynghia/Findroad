def is_dense(grid):
    wall_count = sum(cell == 1 for row in grid for cell in row)
    total = len(grid) * len(grid[0])
    return (wall_count / total) > 0.3

def select_best_algorithm(grid, has_weights=False):
    if has_weights:
        return "A*"
    if is_dense(grid):
        return "DFS"
    return "BFS"