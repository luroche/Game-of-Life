#################### IMPORTS ####################
import time
from enum import Enum
import pandas as pd
from turtle import Turtle, Screen


#################### CONSTANTS AND ENUMS ####################
class __CONSTANSTS:
    NAME_GAME = "Game of life"
    BOARD_COLOR = "black"
    SNAKE_COLOR = "white"
    FOOD_COLOR = "blue"
    SC_WIDTH = 600
    SC_HEIGHT = 600

class __STATUS_e(Enum):
    ALIVE = 0
    DEAD = 1

top_left        = [-1, 1]
top             = [0, 1]
top_right       = [1,1]
left            = [-1, 0]
right           = [1, 0]
bottom_left     = [-1, -1]
bottom          = [0, -1]
bottom_right    = [1, -1]

all_neighbors = [top_left, top, top_right, left, right, bottom_left, bottom, bottom_right]


#################### PROGRAM ####################
def __createPiece(x:int, y:int) -> Turtle:
    x = x * 25
    y = y * 25
    new_segment = Turtle("square")
    new_segment.shapesize(1,1,0)
    new_segment.color("black")
    new_segment.penup()
    new_segment.goto(x, y)    
    return new_segment


def __born(object : Turtle) -> None:
    '''  
    Gives life to the piece
    Init: object: Turtle = Object
    Return = None
    '''
    if object.position() == (0,0):
        object.color("red")
    else:
        object.color("white")


def __kill(segment: Turtle) -> None:
    '''  
    kill the piece
    Init: object: Turtle = Object
    Return = None
    '''
    segment.color("black")


def __neighbors(df: pd.DataFrame) -> pd.DataFrame:
    '''
    check how many neighbors each piece has.
    Init: df: pd.Dataframe = Dataframe of all points.
    Return: dataframe with updated number of neighbors
    '''
    df['neighbors'] = None
    for index, row in df.iterrows():
        neighbors_row = 0
        x_point = row['x']
        y_point = row['y']
        new_df = df.drop(index = index)
        for index2, row2 in new_df.iterrows():
            if row2['status'] == __STATUS_e.ALIVE:
                dif_position = [abs(row2['x'] - x_point), row2['y'] - y_point]
                if dif_position in all_neighbors:
                    neighbors_row += 1
        df['neighbors'][index] = neighbors_row
    return df


def __normative(df: pd.DataFrame) -> pd.DataFrame:
    '''
    Normative of game of life. kill or born the pieces.
    Init: df: pd.Dataframe = Dataframe of all pieces.
    return: pd.Dataframe = Dataframe with new status.
    '''
    for index, row in df.iterrows():
        if row['status'] == __STATUS_e.DEAD and row['neighbors'] == 3:
            __born(row['object'])
            df.loc[index]['status'] = __STATUS_e.ALIVE
        elif row['status'] == __STATUS_e.ALIVE and (row['neighbors'] == 0 or row['neighbors'] == 1 or row['neighbors'] > 3):
            __kill(row['object'])
            df.loc[index]['status'] = __STATUS_e.DEAD
        elif row['status'] == __STATUS_e.ALIVE and (row['neighbors'] == 2 or row['neighbors'] == 3):
            df.loc[index]['status'] = __STATUS_e.ALIVE
    return df


def gameOfLife(initial_points: list) -> None:
    '''
    Principal program.
    Init: initial_points: list = initial points that are alive
    return = None
    '''
    # CREATE SCREEN
    sc = Screen()
    sc.setup(width = __CONSTANSTS.SC_WIDTH, height = __CONSTANSTS.SC_HEIGHT)
    sc.bgcolor(__CONSTANSTS.BOARD_COLOR)
    sc.title(__CONSTANSTS.NAME_GAME)
    sc.tracer(0)

    df = pd.DataFrame(columns=['object', 'x', 'y', 'status'])
    board_size = 5
    column = board_size
    while column != -board_size:
        row = -board_size
        while row != board_size:
            new_object = __createPiece(row, column)
            new_df = pd.DataFrame({'object': [new_object], 'x': [row], 'y':[column], 'status': [__STATUS_e.DEAD]})
            df = pd.concat([df, new_df], ignore_index=True)
            row +=1
        column -= 1
    sc.update()
    
    #ALIVE THE INITIAL POINTS
    for point in initial_points:
        filtro = (df['x'] == point[0]) & (df['y'] == point[1])
        df_filtro = df[filtro].reset_index()
        df.loc[filtro, 'status'] = __STATUS_e.ALIVE
        __born(df_filtro['object'][0])
    sc.update()

    #LOOP PLAY
    while True:
        try:
            df = __neighbors(df)
            df = __normative(df)
            time.sleep(1)
            sc.update()
        except:
            break