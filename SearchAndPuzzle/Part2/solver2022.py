#!/usr/local/bin/python3
# solver2022.py : 2022 Sliding tile puzzle solver
#
# Code by: Chiranthan Shadaksharaswamy (cshadaks), Abhiroop Tejomay Kommalapati (akommala), Divya Jagabattula (djagabat)
#
# Based on skeleton code by D. Crandall & B551 Staff, Fall 2022
#

import sys
from copy import deepcopy
import math
import numpy as np

ROWS=5
COLS=5

def printable_board(board):
    return [ ('%3d ')*COLS  % board[j:(j+COLS)] for j in range(0, ROWS*COLS, COLS) ]

def move_right(board, row):
  """Move the given row to one position right"""
  board = deepcopy(board)
  board[row] = board[row][-1:] + board[row][:-1]
  return board

def move_left(board, row):
  """Move the given row to one position left"""
  board = deepcopy(board)
  board[row] = board[row][1:] + board[row][:1]
  return board

def rotate_right(board,row,residual):
    # board = deepcopy(board)
    board[row] = [board[row][0]] +[residual] + board[row][1:]
    residual=board[row].pop()
    return residual

def rotate_left(board,row,residual):
    # board = deepcopy(board)
    board[row] = board[row][:-1] + [residual] + [board[row][-1]]
    residual=board[row].pop(0)
    return residual

def move_clockwise(board):
    """Move the outer ring clockwise"""
    board = deepcopy(board)
    board[0]=[board[1][0]]+board[0]
    residual=board[0].pop()
    board=transpose_board(board)
    residual=rotate_right(board,-1,residual)
    board=transpose_board(board)
    residual=rotate_left(board,-1,residual)
    board=transpose_board(board)
    residual=rotate_left(board,0,residual)
    board=transpose_board(board)
    return board

def move_cclockwise(board):
    """Move the outer ring counter-clockwise"""
    board = deepcopy(board)
    board[0]=board[0]+[board[1][-1]]
    residual=board[0].pop(0)
    board=transpose_board(board)
    residual=rotate_right(board,0,residual)
    board=transpose_board(board)
    residual=rotate_right(board,-1,residual)
    board=transpose_board(board)
    residual=rotate_left(board,-1,residual)
    board=transpose_board(board)
    return board

def transpose_board(board):
  """Transpose the board --> change row to column"""
  return [list(col) for col in zip(*board)]

# return a list of possible successor states
def successors(state):
    board = deepcopy(state)
    s = []

    for i in range(ROWS):
        s.append((move_left(board, i), f'L{i + 1}'))

    for j in range(ROWS):
        s.append((move_right(board, j), f'R{j + 1}'))

    for i in range(COLS):
        s.append((transpose_board(move_left(transpose_board(board), i)), f'U{i + 1}'))

    for j in range(COLS):
        s.append((transpose_board(move_right(transpose_board(board), j)), f'D{j + 1}'))

    board = deepcopy(state)
    s.append((move_clockwise(board), 'Oc'))
    board = deepcopy(state)
    s.append((move_cclockwise(board), 'Occ'))

    # ic
    board = deepcopy(state)
    board=np.array(board)
    inner_board=board[1:-1,1:-1].tolist()
    inner_board = move_clockwise(inner_board)
    board[1:-1,1:-1]=np.array(inner_board)
    board=board.tolist()
    s.append((board, 'Ic'))

    # icc
    board = deepcopy(state)
    board=np.array(board)
    inner_board=board[1:-1,1:-1].tolist()
    inner_board = move_cclockwise(inner_board)
    board[1:-1,1:-1]=np.array(inner_board)
    board=board.tolist()
    s.append((board, 'Icc'))

    return s

# check if we've reached the goal
def is_goal(state):
    if state == [[1, 2, 3, 4, 5], [6, 7, 8, 9, 10], [11, 12, 13, 14, 15], [16, 17, 18, 19, 20], [21, 22, 23, 24, 25]]:
        return True
    return False
    

def h(state):
    cost = 0
    for i in range(ROWS):
        for j in range(COLS):
            x, y = math.ceil(state[i][j] / ROWS) - 1, state[i][j] % COLS - 1
            cost += min(abs(i - x), (ROWS - 1) - abs(i - x)) + min(abs(j - y), (COLS - 1) - abs(j - y))
    return cost


def convert_board(board):
    return [list(board[j:j+COLS]) for j in range(0, ROWS*COLS, COLS)]

def solve(initial_board):
    
    initial_board = convert_board(initial_board)
    fringe = []
    fringe += [(0, initial_board, []),]
    reached = [initial_board]
    reached_costs = [0]
    while len(fringe) > 0:
        fringe.sort(reverse=True)
        (_, state, path) = fringe.pop()
        
        if is_goal(state):
            return path
        
        for s, move in successors(state):
            cost = h(s) + len(path)
            print(cost, s, path)
            if s not in reached:
                reached.append(s)
                reached_costs.append(cost)
                fringe.append((cost, s, path + [move]))
            elif s in reached and cost < reached_costs[reached.index(s)]:
                index = reached.index(s)
                reached.pop(index)
                reached_costs.pop(index)
                reached.append(s)
                reached_costs.append(cost)
                fringe.append((cost, s, path + [move]))
    
    return path




# Please don't modify anything below this line
#
if __name__ == "__main__":
    if(len(sys.argv) != 2):
        raise(Exception("Error: expected a board filename"))

    start_state = []
    with open(sys.argv[1], 'r') as file:
        for line in file:
            start_state += [ int(i) for i in line.split() ]

    if len(start_state) != ROWS*COLS:
        raise(Exception("Error: couldn't parse start state file"))

    print("Start state: \n" +"\n".join(printable_board(tuple(start_state))))

    print("Solving...")
    route = solve(tuple(start_state))
    
    print("Solution found in " + str(len(route)) + " moves:" + "\n" + " ".join(route))
