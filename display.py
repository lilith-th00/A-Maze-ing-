top = 1
right = 2
bottom = 4
left = 8

def display(maze):
    rows = len(maze)
    cols = len(maze[0])
    for r in range(rows):
        for c in range(cols):
            if maze[r][c] & top:
                print("\033[35m███", end="")
            else:
                print("█  ", end="")
        print("█")    
            
        for c in range(cols):
            if maze[r][c] & left:
                print("█  ", end="")
            else:
                print("   ", end="")
        if maze[r][cols - 1] & right:
            print("█")
        else:
            print()
        if r == rows - 1:
            for c in range(cols):
                if maze[r][c] & bottom:
                    print("███", end="")
                else:
                    print("   ", end="")
            print("█") 


maze = [[15, 15, 15, 15, 15, 15, 15, 15, 15, 15, 15, 15, 15, 15], 
        [15, 4, 5, 2, 4, 5, 1, 2, 1, 4, 7, 5, 12, 15],
         [15, 5, 8, 8, 15, 4, 13, 12, 5, 6, 14, 12, 1, 15],
         [15, 15, 15, 15, 15, 15, 15, 15,15, 15, 15, 15, 15, 15]]
display(maze)
