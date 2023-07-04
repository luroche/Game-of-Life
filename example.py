import pandas as pd
from game_of_life import gameOfLife

'''
Board size 10x10
Insert the initial points

'''
#points = [[0,0],[1,0], [0,1], [2,0]]
points = [[0,0],[1,0], [1,1], [2,0]]


def main():
    gameOfLife(initial_points = points)
    
if __name__ == '__main__':
    main()