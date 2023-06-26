from termcolor import colored
import colorama
from time import sleep
from os import system
from random import choice, randint, random
import msvcrt as inp


colorama.init()


red, green, blue = 'red', 'green', 'blue'
standing = 's'
moving = 'm'
colors = [
    'red',
    'green',
    'blue',
    'yellow',
    'magenta',
    'cyan'
]
shapes = [
    'cube',
    'line',
    'left l',
    'right l',
    'z',
    's',
    'plus'
]

cube = chr(int('2b1b', base=16))
empty = '  '
height = 22
width = 12
timing = 0.1
my_board = [([empty] * width).copy() for i in range(height)]
rows_removed = 0

class part:
    def __init__(self, color, index, state=moving):
        self.color = color
        self.state = state
        self.x = index[0]
        self.y = index[1]


class piece:
    def __init__(self):
        self.state = standing
        self.rotation = 0  # need to be random 0-1 / 0-3
        self.color = choice(colors)
        self.shape = choice(shapes)
        self.parts = [None, None, None, None]
        self.w = None
        self.h = None

    def create_piece(self):
        if self.shape == 'line':
            self.w = 1
            self.h = 4
            index = [[width // 2, -1], [width // 2, -2], [width // 2, -3], [width // 2, -4]]
        elif self.shape == 'cube':
            w = h = 2
            index = [[width // 2, -1], [width // 2 - 1, -1], [width // 2, -2], [width // 2 - 1, -2]]
        else:
            w = 3
            h = 2
            if self.shape == 'left l':
                index = [[width // 2, -1], [width // 2 - 1, -1], [width // 2, -2], [width // 2, -3]]
            elif self.shape == 'right l':
                index = [[width // 2, -1], [width // 2 + 1, -1], [width // 2, -2], [width // 2, -3]]
            elif self.shape == 'z':
                index = [[width // 2, -1], [width // 2, -2], [width // 2 + 1, -2], [width // 2 + 1, -3]]
            elif self.shape == 's':
                index = [[width // 2, -1], [width // 2, -2], [width // 2 - 1, -2], [width // 2 - 1, -3]]
            else:
                index = [[width // 2 + 1, -1], [width // 2 - 1, -1], [width // 2, -1], [width // 2, -2]]
        self.parts = [
            part(self.color, index[0]),
            part(self.color, index[1]),
            part(self.color, index[2]),
            part(self.color, index[3]),
        ]
        return self.parts

    def stop(self):
        self.state = standing


def pixel(pColor=None, end=''):
    if pColor == empty:
        print(empty, end=end)
        return
    print(colored(cube, pColor), end=end)


def border(t):
    print(colored(empty, 'white', 'on_white'), end=t)


def printBoard(board):
    system('cls')
    print()

    for _ in range(width + 1):
        border('')
    border('\n')

    for i in range(height):
        border('')
        for j in range(width):
            pixel(board[i][j])
        border('\n')

    for _ in range(width + 1):
        border('')
    border('\n')

#
# printBoard(my_board)
#
#
# my_board[-1][4] = red
# my_board[-1][5] = red
# my_board[-1][6] = red
# my_board[-2][4] = red
# printBoard(my_board)
# sleep(timing)
# for i in range(height-1):
#     for j in range(i, i-3, -1):
#         if j >= 0:
#             my_board[j][6] = green
#         if j-4 >= 0:
#             my_board[j-4][6] = empty
#     printBoard(my_board)
#     sleep(timing)
# for i in range(height-1):
#     my_board[i][3] = blue
#
#     if i > 0:
#         my_board[i-1][2] = blue
#         my_board[i-1][4] = blue
#     if i > 1:
#         my_board[i-2][2] = empty
#         my_board[i-2][3] = empty
#         my_board[i-2][4] = empty
#     printBoard(my_board)
#     sleep(timing)
#
# for i in range(height-5):
#     my_board[i][6] = 'yellow'
#     my_board[i][7] = 'yellow'
#     my_board[i][8] = 'yellow'
#     my_board[i][9] = 'yellow'
#
#     if i > 0:
#         my_board[i-1][6] = empty
#         my_board[i - 1][7] = empty
#         my_board[i - 1][8] = empty
#         my_board[i - 1][9] = empty
#
#     printBoard(my_board)
#     sleep(timing)


def move_down(piece):
    for i in piece:
        if i.y == height - 1:
            return
        if 0 <= i.y < height and my_board[i.y + 1][i.x] != empty:
            if i.y + 1 not in [z.y for z in piece if z.x == i.x]:
                return
    for i in piece:
        i.y += 1
        if i.y > 0:
            my_board[i.y-1][i.x] = empty
        if i.y >= 0:
            my_board[i.y][i.x] = i.color


def move_right(piece):
    for i in piece:
        if i.x == width-1:
            return
    for i in piece:
        if my_board[i.y][i.x + 1] != empty:
            if i.x + 1 not in [z.x for z in piece]:
                return
    for i in piece:
        if i.y >= 0:
            my_board[i.y][i.x] = empty
    for i in piece:
        i.x += 1
        if i.y >= 0:
            my_board[i.y][i.x] = i.color


def move_left(piece):
    for i in piece:
        if i.x == 0:
            return
    for i in piece:
        if my_board[i.y][i.x-1] != empty:
            if i.x - 1 not in [z.x for z in piece]:
                return
    for i in piece:
        if i.y >= 0:
            my_board[i.y][i.x] = empty
    for i in piece:
        i.x -= 1
        if i.y >= 0:
            my_board[i.y][i.x] = i.color


def bottom(piece):
    for i in piece:
        if i.y == height-1:
            return 's'
        if 0 <= i.y < height and my_board[i.y+1][i.x] != empty:
            if i.y+1 not in [z.y for z in piece if z.x == i.x]:
                return 's'
    return 'm'


def remove_row(row):
    global rows_removed
    rows_removed += 1
    for i in range(width):
        my_board[row][i] = empty
    for i in range(row, 0, -1):
        if i < height:
            for x in range(width):
                my_board[i][x] = my_board[i-1][x]
    for i in range(width):
        my_board[0][i] = empty



def move_check(p):
    if inp.kbhit():
        a = inp.getwche()
        if a == 'a':
            move_left(p)
        if a == 'd':
            move_right(p)
        if a == 's':
            move_down(p)
    inp.heapmin()


printBoard(my_board)
game = []
pieces = 0
while not any([x != empty for x in my_board[0]]):
    if pieces % 10 == 0:
        timing *= 0.8
    game.append(piece())
    i = game[pieces]
    my_piece = i.create_piece()
    i.state = bottom(my_piece)
    while i.state == moving:
        inp.heapmin()
        sleep(timing/4)
        move_check(my_piece)
        sleep(timing / 4)
        move_check(my_piece)
        sleep(timing / 4)
        move_check(my_piece)
        inp.heapmin()

        # if bottom(my_piece) == standing:
        #     break
        # sleep(1)
        # if random() < 0.3:
        #     move_left(my_piece)
        move_down(my_piece)
        sleep(timing / 5)
        if inp.kbhit():
            a = inp.getwche()
            if a == 'a':
                printBoard(my_board)
                move_left(my_piece)
            if a == 'd':
                printBoard(my_board)
                move_right(my_piece)
        inp.heapmin()

        # sleep(timing)
        printBoard(my_board)
        i.state = bottom(my_piece)
    sleep(timing)
    printBoard(my_board)
    row = height-1
    while row >= 0:

        if all([x != empty for x in my_board[row]]):
            remove_row(row)
            sleep(0.2)
            printBoard(my_board)
            row += 1
        row -= 1
    pieces += 1


output = """
                                                                                                                        
                     =========      ==      =      =========                                                          
                     =              = =     =      =        =                                                
                     =              =  =    =      =        =                                                
                     =========      =   =   =      =        =                                                
                     =              =    =  =      =        =                                                
                     =              =     = =      =        =                                                
                     =========      =      ==      =========                                                   
                                                                                                                        
"""
print(output)
input(f"\n\nfinished, {pieces} pieces, {rows_removed} rows removed\n")
