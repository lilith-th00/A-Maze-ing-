import sys
import config_validation
from search import Maze
""""
Your program must handle all errors gracefully: invalid configuration,
file not found, bad syntax, impossible maze parameters, etc.
It must never crash unexpectedly, and must always provide a clear
error message to the user.
"""


def main():
    args = sys.argv[1:]
    if args.__len__() > 1:
        print("Too many files , make sure to enter one file !!")
    elif args.__len__() < 1:
        print("You forgot to mention the config file !!")
    else:
        try:
            with open(sys.argv[1], 'r') as file:
                content = file.read()
                data = config_validation.validation(content)
                my_maze = Maze(data, 30)
               #my_maze.my_42()
                my_maze.wilson()
                #my_maze.dsf_algorith()
                #data = my_maze.bfs_algo()
                #my_maze.output_maze()
                my_maze.draw()
        except (FileNotFoundError, config_validation.ErrorInConfigFile) as e:
            print(e)


if __name__ == "__main__":
    main()
