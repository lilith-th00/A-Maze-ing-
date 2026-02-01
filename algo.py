import random
import sys
direction = {
    "N" : (0, -1, 0b0001, 0b0010),
    "S" : (0, +1, 0b0010, 0b0001),
    "W" : (-1, 0, 0b1000, 0b0010),
    "E" : (+1, 0, 0b0010, 0b1000),
}

def dfs(data: dict):
    x, y = data['ENTRY']
    d_x, d_y = data['EXIT']
    h = data['HEIGHT']
    w = data['WIDTH']

    maze = [[0b1111 for _ in range(w)] for _ in range(h)]
    visited = [[False for _ in range(w)] for _ in range(h)]

    def my_algo(x:int, y:int):
        visited[x][y] = True
        if x == d_x and y == d_y:
            return True
        keys = [key for key in direction]
        random.shuffle(keys)

        i = 0
        while i < 4:
            r_x, r_y, r_dir, n_dir = direction[keys[i]]
            n_x, n_y = x + r_x, y + r_y
            if 0 <= n_x < w and 0 <= n_y < h:
                if not visited[n_x][n_y]:
                    maze[x][y] = maze[x][y] & ~r_dir
                    maze[n_x][n_y] = maze[n_x][n_y] & ~n_dir
                    if my_algo(n_x, n_y):
                        return True
            i += 1
        return False
    
    my_algo(x, y)
    return maze
