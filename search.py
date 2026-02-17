import random
import pygame
from collections import deque

class Maze:
    direction = {
    "N" : (0, -1, "N", "S"),
    "S" : (0, +1, "S", "N"),
    "E" : (+1, 0, "E", "W"),
    "W" : (-1, 0, "W", "E"),
}
    def __init__(self, maze_data, cell_size):
        self.width = maze_data['WIDTH']
        self.height = maze_data['HEIGHT']
        self.m_entry = maze_data['ENTRY']
        self.m_exit = maze_data['EXIT']
        self.perfect = maze_data['PERFECT']
        self.cell_size = cell_size
        self.out_file = maze_data['OUTPUT_FILE']
        self.cells = self.create_cells(self.width, self.height)
        self.dirs = []
    
    class Cell:
        def __init__(self, x, y):
            self.x = x
            self.y = y
            self.walls = {
                "S": True,
                "N": True,
                "W": True,
                "E": True
            }
            self.is_visited = False
            self.path = False
            
    def create_cells(self, width, height):
        cells = []
        for col in range(height):
            row_data = []
            for row in range(width):
                row_data.append(self.Cell(row, col))
            cells.append(row_data)
        return cells

    
    def my_42(self):
        w = int(self.width / 2)
        h = int(self.height / 2)
        i = 0
        while i < 4:
            self.cells[(h + 2) - i][w - 2].is_visited = True
            i += 1
        i = 0
        while i < 2:
            self.cells[h][(w - 3) - i].is_visited = True
            self.cells[(h - 2) + i][w - 4].is_visited = True
            i += 1
            self.cells[h - 1][w + 2].is_visited = True
            self.cells[h + 1][w].is_visited = True
        i = 0
        while i < 3:
            self.cells[h - 2][w + i].is_visited = True
            self.cells[h + 2][w + i].is_visited = True
            self.cells[h][w + i].is_visited = True
            i += 1


    def dsf_algorith(self):
        stack = []
        x, y = 0, 0

        self.cells[y][x].is_visited = True
        stack.append((x, y))
        while stack:
            x, y = stack[-1]
           
            key = list(self.direction.keys())
            random.shuffle(key)
            found = False
            i = 0
            while i < 4:
                m_x, m_y, m_dir, n_dir = self.direction[key[i]]
                n_x, n_y = x+m_x, y+m_y
                if 0 <= n_x < self.width and 0 <= n_y < self.height:
                    if not self.cells[n_y][n_x].is_visited:
                        self.cells[y][x].walls[m_dir] = False
                        self.cells[n_y][n_x].walls[n_dir] = False
                        self.cells[n_y][n_x].is_visited = True
                        stack.append((n_x, n_y))
                        found = True
                        break
                i += 1
            if not found:
                stack.pop()
    
    def bfs_algo(self):
        for r in range(len(self.cells)):
            for c in range(len(self.cells[0])):
                self.cells[r][c].is_visited = False

        x, y = self.m_entry
        d_x, d_y = self.m_exit
        
        queue = []
        queue.append((x, y))
        data = deque()
        self.cells[y][x].is_visited = True

        parent = {}

        while queue:
            x, y = queue.pop(0)

            if x == d_x and y == d_y:
                break

            key = list(self.direction.keys())

            i = 0
            while i < 4:
                n_x, n_y, m_dir, n_dir = self.direction[key[i]]
                m_x, m_y = x + n_x, y + n_y

                if 0 <= m_x < self.width and 0 <= m_y < self.height:
                    if (not self.cells[y][x].walls[m_dir]
                        and not self.cells[m_y][m_x].walls[n_dir]
                        and not self.cells[m_y][m_x].is_visited):
                        self.cells[m_y][m_x].is_visited = True
                        parent[(m_x, m_y)] = ((x, y), m_dir)
                        queue.append((m_x, m_y))

                i += 1

        
        cur = (d_x, d_y)
        while cur != self.m_entry:
            (m_x, m_y), d = parent[cur]
            if (m_x, m_y) != self.m_entry:
                data.appendleft((m_x, m_y))
            x, y = cur
            self.cells[y][x].path = True
            cur = (m_x, m_y)
            self.dirs.append(d)
        
        x, y = self.m_entry
        self.cells[y][x].path = True
        self.dirs.reverse()
        return data
           
    def output_maze(self):
        with open(self.out_file, 'w') as f:
            for i in range(len(self.cells)):
                for j in range(len(self.cells[0])):
                    count = 0
                    if self.cells[i][j].walls['N']:
                        count += 1
                    if self.cells[i][j].walls['S']:
                        count += 4
                    if self.cells[i][j].walls['E']:
                        count += 2
                    if self.cells[i][j].walls['W']:
                        count += 8
                    h = format(count, "X")
                    f.write(h)
                f.write("\n")
            f.write("\n")
            x, y = self.m_entry
            m_x, m_y = self.m_exit
            f.write(f"{x},{y}\n")
            f.write(f"{m_x},{m_y}\n")
            for x in self.dirs:
                f.write(x)    


    def draw(self):
        pygame.init()
        win = pygame.display.set_mode((1000, 1000))
        pygame.display.set_caption("waaaaaaaa")
        clock = pygame.time.Clock()
        
        r = self.height
        w = self.width
        cell = 24
        width, height = win.get_size()
        x = (width // 2) - (w * cell // 2)
        y = (height // 2) - (r * cell // 2) 
        l = int(cell/2)
        blue = (0, 0, 255)
        red = (255, 0, 0)
        s_x, s_y = self.m_entry
        d_x, d_y = self.m_exit
        pygame.draw.circle(win, blue, (x + s_x*cell +l, y+s_y*cell+l), 5)
        pygame.draw.circle(win, red, (x + d_x*cell+l, y+d_y*cell+l), 5)
        for i in range(r):
            for j in range(w):

                if self.cells[i][j].walls['N']:
                    pygame.draw.rect(win, (0, 255, 0), (x+ j*cell, y+i*cell, cell, 2))
                else:
                    pygame.draw.rect(win, (0 , 0, 0), (x+ j*cell, y+i*cell, cell, 2))
                
            for j in range(w):
                if self.cells[i][j].walls['W']:
                    pygame.draw.rect(win, (0, 255, 0), (x+ j*cell, y+i*cell, 2, cell))
                else:
                    pygame.draw.rect(win, (0, 0, 0), (x+ j*cell, y+i*cell, 0, cell))
                if self.cells[i][w-1].walls['E']:
                    pygame.draw.rect(win, (0, 255, 0), (x+ w*cell, y+i*cell, 2, cell))

            if i+1 == r:
                for j in range(w):
                    if self.cells[i][j].walls['S']:
                        pygame.draw.rect(win, (0, 255, 0), (x+ j*cell, y+r*cell, cell, 2))
                    else:
                        pygame.draw.rect(win, (0, 0, 0), (x+ j*cell, y+r*cell, cell, 2))
            
        
        #for cor in data:
         #   n_x, n_y = cor
          #  pygame.draw.rect(win, (0, 0, 255), (x+ n_x*cell+2, y+n_y*cell+2, cell- 2*2, cell-2*2))
            

        pygame.display.update()

        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False

        pygame.quit()
    
    def wilson_algo(self):
        unvisited = []

        for r in range(len(self.cells)):
            for c in range(len(self.cells[0])):
                unvisited.append((c, r))
        
        start = random.choice(unvisited)
        unvisited.remove(start)
        x, y = start
        self.cells[y][x].is_visited = True
    
        while unvisited:
            x, y = random.choice(unvisited)
            path = [(x, y)]

            while (x, y) in unvisited:

                valid_move = False

                while not valid_move:
                    dir_key = random.choice(list(self.direction.keys()))
                    dx, dy, _, _ = self.direction[dir_key]
                    nx, ny = x + dx, y + dy

                    if 0 <= nx < self.width and 0 <= ny < self.height \
                        and not self.cells[ny][nx].is_blocked:
                        valid_move = True

                if (nx, ny) in path:
                    index = path.index((nx, ny))
                    path = path[:index + 1]
                else:
                    path.append((nx, ny))

                x, y = nx, ny

            while len(path) > 1:
                x, y = path.pop(0)
                nx, ny = path[0]   # next cell

    # break walls
                if (x + 1, y) == (nx, ny):
                    self.cells[y][x].walls['E'] = False
                    self.cells[ny][nx].walls['W'] = False

                elif (x - 1, y) == (nx, ny):
                    self.cells[y][x].walls['W'] = False
                    self.cells[ny][nx].walls['E'] = False

                elif (x, y + 1) == (nx, ny):
                    self.cells[y][x].walls['S'] = False
                    self.cells[ny][nx].walls['N'] = False

                elif (x, y - 1) == (nx, ny):
                    self.cells[y][x].walls['N'] = False
                    self.cells[ny][nx].walls['S'] = False

    # mark visited
                if (x, y) in unvisited:
                    unvisited.remove((x, y))
                    self.cells[y][x].is_visited = True

                if (nx, ny) in unvisited:
                    unvisited.remove((nx, ny))
                    self.cells[ny][nx].is_visited = True
    

