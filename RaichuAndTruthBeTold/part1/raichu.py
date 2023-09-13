#
# raichu.py : Play the game of Raichu
#
# PLEASE PUT YOUR NAMES AND USER IDS HERE!
#
# Based on skeleton code by D. Crandall, Oct 2021
#
import sys
import time

import copy

def board_to_string(board, N):
    return "\n".join(board[i:i+N] for i in range(0, len(board), N))

def find_peices(mat):
    
    white_pichus = []
    white_pikachus = []
    white_raichus = []
    black_pichus = []
    black_pikachus = []
    black_raichus = []
    
    for i in range(len(mat)):
        for j in range(len(mat[i])):
            if mat[i][j] == 'w':
                white_pichus.append((i,j))
            elif mat[i][j] == 'W':
                white_pikachus.append((i,j))
            elif mat[i][j] == '@':
                white_raichus.append((i,j))
            elif mat[i][j] == 'b':
                black_pichus.append((i,j))
            elif mat[i][j] == 'B':
                black_pikachus.append((i,j))
            elif mat[i][j] == '$':
                black_raichus.append((i,j))
    
    return(white_pichus,white_pikachus,white_raichus,black_pichus,black_pikachus,black_raichus)

# def print_peices_pos(white_pichus,white_pikachus,white_raichus,black_pichus,black_pikachus,black_raichus):
    
#     print("white_pichus:",white_pichus)
#     print("white_pikachus:",white_pikachus)
#     print("white_raichus:",white_raichus)
#     print("black_pichus:",black_pichus)
#     print("black_pikachus:",black_pikachus)
#     print("black_raichus:",black_raichus)

    
def white_moves(mat, N):
    
    white_pichus,white_pikachus,white_raichus,black_pichus,black_pikachus,black_raichus = find_peices(mat)
    
    moves = []
    
    #white_pichus_moves
    
    temp = copy.deepcopy(mat)
    
    for x in range(len(white_pichus)):
        
        temp = copy.deepcopy(mat)

        i = white_pichus[x][0]
        j = white_pichus[x][1]

        if i + 1 < N and j + 1 < N:
            if mat[i+1][j+1] == '.':
                temp[i][j] = '.'
                if i + 1 == N - 1:
                    temp[i+1][j+1] = '@'
                else:
                    temp[i+1][j+1] = 'w'
                moves.append(temp)
            elif mat[i+1][j+1] == 'b':
                if i + 2 < N and j + 2 < N:
                    if mat[i+2][j+2] == '.':
                        temp[i][j] = '.'
                        temp[i+1][j+1] = '.'
                        if i + 2 == N - 1:
                            temp[i+2][j+2] = '@'
                        else:
                            temp[i+2][j+2] = 'w'
                        moves.append(temp)  
        
        temp = copy.deepcopy(mat)

        if i + 1 < N and j - 1 >= 0:
            if mat[i+1][j-1] == '.':
                temp[i][j] = '.'
                if i + 1 == N - 1:
                    temp[i+1][j-1] = '@'
                else:
                    temp[i+1][j-1] = 'w'
                moves.append(temp)
            elif mat[i+1][j-1] == 'b':
                if i + 2 < N and j - 2 >= 0:
                    if mat[i+2][j-2] == '.':
                        temp[i][j] = '.'
                        temp[i+1][j-1] = '.'
                        if i + 2 == N - 1:
                            temp[i+2][j-2] = '@'
                        else:
                            temp[i+2][j-2] = 'w'
                        moves.append(temp) 


    #white_pikachu_moves
    
    temp = copy.deepcopy(mat)
    
    for x in range(len(white_pikachus)):
        
        temp = copy.deepcopy(mat)
        i = white_pikachus[x][0]
        j = white_pikachus[x][1]

        if i + 1 < N:
            if mat[i+1][j] == '.':
                temp[i][j] = '.'
                if i + 1 == N - 1:
                    temp[i+1][j] = '@'
                else:
                    temp[i+1][j] = 'W'
                moves.append(temp)
                temp = copy.deepcopy(mat)
            elif i + 2 < N:
                if mat[i+2][j] == '.' and (mat[i+1][j] == 'b' or mat[i+1][j] == 'B'):
                    temp[i][j] = '.'
                    temp[i+1][j] = '.'
                    if i + 2 == N - 1:
                        temp[i+2][j] = '@'
                    else:
                        temp[i+2][j] = 'W'
                    moves.append(temp)
                    temp = copy.deepcopy(mat)
                
        if i + 2 < N:
            if mat[i+1][j] == '.' and mat[i+2][j] == '.':
                temp[i][j] = '.'
                if i + 2 == N - 1:
                    temp[i+2][j] = '@'
                else:
                    temp[i+2][j] = 'W'
                moves.append(temp)
                temp = copy.deepcopy(mat)
            elif i + 3 < N: 
                if mat[i+1][j] == '.' and (mat[i+2][j] == 'b' or mat[i+2][j] == 'B') and mat[i+3][j] == '.':
                    temp[i][j] = '.'
                    temp[i+2][j] = '.'
                    if i + 3 == N - 1:
                        temp[i+3][j] = '@'
                    else:
                        temp[i+3][j] = 'W'
                    moves.append(temp)
                    temp = copy.deepcopy(mat)
                
        if j + 1 < N:
            if mat[i][j+1] == '.':
                temp[i][j] = '.'
                temp[i][j+1] = 'W'
                moves.append(temp)
                temp = copy.deepcopy(mat)
            elif j + 2 < N:
                if mat[i][j+2] == '.' and (mat[i][j+1] == 'b' or mat[i][j+1] == 'B'):
                    temp[i][j] = '.'
                    temp[i][j+1] = '.'
                    temp[i][j+2] = 'W'
                    moves.append(temp)
                    temp = copy.deepcopy(mat)
                
        if j + 2 < N:
            if mat[i][j+1] == '.' and mat[i][j+2] == '.':
                temp[i][j] = '.'
                temp[i][j+2] = 'W'
                moves.append(temp)
                temp = copy.deepcopy(mat)
            elif j + 3 < N: 
                if mat[i][j+1] == '.' and (mat[i][j+2] == 'b' or mat[i][j+2] == 'B') and mat[i][j+3] == '.':
                    temp[i][j] = '.'
                    temp[i][j+2] = '.'
                    temp[i][j+3] = 'W'
                    moves.append(temp)
                    temp = copy.deepcopy(mat)
                
        if j - 1 >= 0:
            if mat[i][j-1] == '.':
                temp[i][j] = '.'
                temp[i][j-1] = 'W'
                moves.append(temp)
                temp = copy.deepcopy(mat)
            elif j - 2 >= 0: 
                if mat[i][j-2] == '.' and (mat[i][j-1] == 'b' or mat[i][j-1] == 'B'):
                    temp[i][j] = '.'
                    temp[i][j-1] = '.'
                    temp[i][j-2] = 'W'
                    moves.append(temp)
                    temp = copy.deepcopy(mat)
                
        if j - 2 >= 0:
            if mat[i][j-1] == '.' and mat[i][j-2] == '.':
                temp[i][j] = '.'
                temp[i][j-2] = 'W'
                moves.append(temp)
                temp = copy.deepcopy(mat)
            elif j - 3 >= 0: 
                if mat[i][j-1] == '.' and (mat[i][j-2] == 'b' or mat[i][j-2] == 'B') and mat[i][j-3] == '.':
                    temp[i][j] = '.'
                    temp[i][j-2] = '.'
                    temp[i][j-3] = 'W'
                    moves.append(temp)
                    temp = copy.deepcopy(mat)

    #white_raichus_moves
    
    directions = [
        [-1, 0],    # up
        [-1, 1],    # up right
        [0, 1],     # right
        [1, 1],     # down right
        [1, 0],     # down
        [1, -1],    # down left
        [0, -1],    # left
        [-1, -1],   # left up
        ]
    
    temp = copy.deepcopy(mat)
    
    for x in range(len(white_raichus)):
        
        temp = copy.deepcopy(mat)
        p = white_raichus[x][0]
        q = white_raichus[x][1]
        
        for d in directions:
            stop = False
            i = p
            j = q
            while not stop:
                
                i = i + d[0]
                j = j + d[1]
                #print(i,j)
                if (0 <= i < N) and not stop:
                    if (0 <= j < N) and not stop:
                        if not mat[i][j] == '.':
                            if mat[i][j] == 'b' or mat[i][j] == 'B' or mat[i][j] == '$':
                                end = False
                                r = i
                                s = j
                                while not end:
                                    r = r + d[0]
                                    s = s + d[1]
                                    if 0 <= r < N and 0 <= s < N and not end:
                                        if not mat[r][s] == '.':
                                            end = True
                                        else:
                                            temp[p][q] = '.'
                                            temp[i][j] = '.'
                                            temp[r][s] = '@'
                                            moves.append(temp)
                                            temp = copy.deepcopy(mat)
                                    else:
                                        end = True
                            
                            stop = True
                        else:
                            temp[p][q] = '.'
                            temp[i][j] = '@'
                            moves.append(temp)
                            temp = copy.deepcopy(mat)
                    else:
                        stop = True
                else:
                    stop = True
                    

    return moves


def black_moves(mat, N):
    
    moves = []
    
    white_pichus,white_pikachus,white_raichus,black_pichus,black_pikachus,black_raichus = find_peices(mat)
    
    #black_pichus_moves(mat, N, black_pichus):
    temp = copy.deepcopy(mat)
    
    for x in range(len(black_pichus)):
        i = black_pichus[x][0]
        j = black_pichus[x][1]
        temp = copy.deepcopy(mat)
        
        if i - 1 >= 0 and j + 1 < N:
            if mat[i-1][j+1] == '.':
                temp[i][j] = '.'
                if i - 1 == 0:
                    temp[i-1][j+1] = '$'
                else:
                    temp[i-1][j+1] = 'b'
                moves.append(temp)
            elif mat[i-1][j+1] == 'w':
                if i - 2 >= 0 and j + 2 < N: 
                    if mat[i-2][j+2] == '.':
                        temp[i][j] = '.'
                        temp[i-1][j+1] = '.'
                        if i - 2 == 0:
                            temp[i-2][j+2] = '$'
                        else:
                            temp[i-2][j+2] = 'b'
                        moves.append(temp)  
                    
        temp = copy.deepcopy(mat)       
        if i - 1 >= 0 and j - 1 >= 0:
            if mat[i-1][j-1] == '.':
                temp[i][j] = '.'
                if i - 1 == 0:
                    temp[i-1][j-1] = '$'
                else:
                    temp[i-1][j-1] = 'b'
                moves.append(temp)
            elif mat[i-1][j-1] == 'w':
                if i - 2 >= 0 and j - 2 >= 0: 
                    if mat[i-2][j-2] == '.':
                        temp[i][j] = '.'
                        temp[i-1][j-1] = '.'
                        if i - 2 == 0:
                            temp[i-2][j-2] = '$'
                        else:
                            temp[i-2][j-2] = 'b'
                        moves.append(temp) 


    #black_pikachu_moves
    
    temp = copy.deepcopy(mat)
    
    for x in range(len(black_pikachus)):
        
        temp = copy.deepcopy(mat)
        i = black_pikachus[x][0]
        j = black_pikachus[x][1]

        if i - 1 >= 0:
            if mat[i-1][j] == '.':
                temp[i][j] = '.'
                if i - 1 == 0:
                    temp[i-1][j] = '$'
                else:
                    temp[i-1][j] = 'B'
                moves.append(temp)
                temp = copy.deepcopy(mat)
            elif i - 2 >= 0: 
                if mat[i-2][j] == '.' and (mat[i-1][j] == 'w' or mat[i-1][j] == 'W'):
                    temp[i][j] = '.'
                    temp[i-1][j] = '.'
                    if i - 2 == 0:
                        temp[i-2][j] = '$'
                    else:
                        temp[i-2][j] = 'B'
                    moves.append(temp)
                    temp = copy.deepcopy(mat)
                
        if i - 2 >= 0:
            if mat[i-1][j] == '.' and mat[i-2][j] == '.':
                temp[i][j] = '.'
                if i - 2 == 0:
                    temp[i-2][j] = '$'
                else:
                    temp[i-2][j] = 'B'
                moves.append(temp)
                temp = copy.deepcopy(mat)
            elif i - 3 >= 0: 
                if mat[i-1][j] == '.' and (mat[i-2][j] == 'w' or mat[i-2][j] == 'W') and mat[i-3][j] == '.':
                    temp[i][j] = '.'
                    temp[i-2][j] = '.'
                    if i - 3 == 0:
                        temp[i-3][j] = '$'
                    else:
                        temp[i-3][j] = 'B'
                    moves.append(temp)
                    temp = copy.deepcopy(mat)
                
        if j + 1 < N:
            if mat[i][j+1] == '.':
                temp[i][j] = '.'
                temp[i][j+1] = 'B'
                moves.append(temp)
                temp = copy.deepcopy(mat)
            elif j + 2 < N: 
                if mat[i][j+2] == '.' and (mat[i][j+1] == 'w' or mat[i][j+1] == 'W'):
                    temp[i][j] = '.'
                    temp[i][j+1] = '.'
                    temp[i][j+2] = 'B'
                    moves.append(temp)
                    temp = copy.deepcopy(mat)
                
        if j + 2 < N:
            if mat[i][j+1] == '.' and mat[i][j+2] == '.':
                temp[i][j] = '.'
                temp[i][j+2] = 'B'
                moves.append(temp)
                temp = copy.deepcopy(mat)
            elif j + 3 < N: 
                if mat[i][j+1] == '.' and (mat[i][j+2] == 'w' or mat[i][j+2] == 'W') and mat[i][j+3] == '.':
                    temp[i][j] = '.'
                    temp[i][j+2] = '.'
                    temp[i][j+3] = 'B'
                    moves.append(temp)
                    temp = copy.deepcopy(mat)
                
        if j - 1 >= 0:
            if mat[i][j-1] == '.':
                temp[i][j] = '.'
                temp[i][j-1] = 'B'
                moves.append(temp)
                temp = copy.deepcopy(mat)
            elif j - 2 >= 0: 
                if mat[i][j-2] == '.' and (mat[i][j-1] == 'w' or mat[i][j-1] == 'W'):
                    temp[i][j] = '.'
                    temp[i][j-1] = '.'
                    temp[i][j-2] = 'B'
                    moves.append(temp)
                    temp = copy.deepcopy(mat)
                
        if j - 2 >= 0:
            if mat[i][j-1] == '.' and mat[i][j-2] == '.':
                temp[i][j] = '.'
                temp[i][j-2] = 'B'
                moves.append(temp)
                temp = copy.deepcopy(mat)
            elif j - 3 >= 0: 
                if mat[i][j-1] == '.' and (mat[i][j-2] == 'w' or mat[i][j-2] == 'W') and mat[i][j-3] == '.':
                    temp[i][j] = '.'
                    temp[i][j-2] = '.'
                    temp[i][j-3] = 'B'
                    moves.append(temp)
                    temp = copy.deepcopy(mat)

    #black_raichus_moves
    
    directions = [
        [-1, 0],    # up
        [-1, 1],    # up right
        [0, 1],     # right
        [1, 1],     # down right
        [1, 0],     # down
        [1, -1],    # down left
        [0, -1],    # left
        [-1, -1],   # left up
        ]
    
    temp = copy.deepcopy(mat)
    
    for x in range(len(black_raichus)):
        
        temp = copy.deepcopy(mat)
        p = black_raichus[x][0]
        q = black_raichus[x][1]
        
        for d in directions:
            stop = False
            i = p
            j = q
            while not stop:
                
                i = i + d[0]
                j = j + d[1]
                #print(i,j)
                if (0 <= i < N) and not stop:
                    if (0 <= j < N) and not stop:
                        if not mat[i][j] == '.':
                            if mat[i][j] == 'w' or mat[i][j] == 'W' or mat[i][j] == '@':
                                end = False
                                r = i
                                s = j
                                while not end:
                                    r = r + d[0]
                                    s = s + d[1]
                                    if 0 <= r < N and 0 <= s < N and not end:
                                        if not mat[r][s] == '.':
                                            end = True
                                        else:
                                            temp[p][q] = '.'
                                            temp[i][j] = '.'
                                            temp[r][s] = '$'
                                            moves.append(temp)
                                            temp = copy.deepcopy(mat)
                                    else:
                                        end = True
                                
                            
                            stop = True
                        else:
                            temp[p][q] = '.'
                            temp[i][j] = '$'
                            moves.append(temp)
                            temp = copy.deepcopy(mat)
                    else:
                        stop = True
                else:
                    stop = True
                    
    return moves
    

def winner(mat, player):
    
    white_pichus,white_pikachus,white_raichus,black_pichus,black_pikachus,black_raichus = find_peices(mat)
    
    if player == 'w':
        if black_pichus == [] and black_pikachus == [] and black_raichus == []:
            return True
        else:
            return False
        
    else:
        if white_pichus == [] and white_pikachus == [] and white_raichus == []:
            return True
        else:
            return False
    
def evaluate(mat):
    
    white_pichus,white_pikachus,white_raichus,black_pichus,black_pikachus,black_raichus = find_peices(mat)
    cost = 0
    cost = cost + 9 * len(white_raichus)
    cost = cost - 9 * len(black_raichus)
    
    for (x,y) in white_pichus:
        if x + 1 < N and (y + 1 < N and y - 1 >= 0):
            if mat[x+1][y+1] == 'b' or mat[x+1][y-1] == 'b' or x + 1 == N - 1:
                cost = cost + 9
            else:
                cost = cost + 1
        else:
            cost = cost + 1
    
    for (x,y) in black_pichus:
        if x - 1 >= 0 and (y + 1 < N and y - 1 >= 0):
            if mat[x-1][y+1] == 'w' or mat[x-1][y-1] == 'w' or x - 1 == 0:
                cost = cost - 9
            else:
                cost = cost - 1
        else:
            cost = cost - 1
            
    for (x,y) in white_pikachus:
        if x + 3 < N or x + 2 < N:
            if mat[x+2][y] == 'b' or mat[x+2][y] == 'B' or x + 2 == N - 1:
                cost = cost + 9
            elif mat[x+1][y] == 'b' or mat[x+1][y] == 'B' or x + 1 == N - 1:
                cost = cost + 9
            elif mat[x+1][y] == '.' or mat[x+2][y] == '.':
                cost = cost + 9
            elif y + 3 < N or y + 2 < N:
                if mat[x][y+2] == 'b' or mat[x][y+2] == 'B':
                    cost = cost + 9
                elif mat[x][y+1] == 'b' or mat[x][y+1] == 'B':
                    cost = cost + 9
                elif y - 3 >= 0 or y - 2 >= 0:
                    if mat[x][y-2] == 'b' or mat[x][y-2] == 'B':
                        cost = cost + 9
                    elif mat[x][y-1] == 'b' or mat[x][y-1] == 'B':
                        cost = cost + 9
                    elif mat[x+1][y+1] == 'b' or mat[x+1][y+1] == 'B' or mat[x+2][y+1] == 'b' or mat[x+2][y+1] == 'B' or x + 2 == N - 1 or x + 1 == N - 1:
                        cost = cost + 5
                    elif mat[x+1][y-1] == 'b' or mat[x+1][y-1] == 'B' or mat[x+2][y-1] == 'b' or mat[x+2][y-1] == 'B' or x + 2 == N - 1 or x + 1 == N - 1:
                        cost = cost + 5
                    else:
                        cost = cost + 2
                else:
                    cost = cost + 1
            else:
                cost = cost + 1
        else:
            cost = cost + 1
                
    for (x,y) in black_pikachus:
        if x - 3 >= 0 or x - 2 >= 0:
            if mat[x-2][y] == 'w' or mat[x-2][y] == 'W' or x - 2 == 0:
                cost = cost - 9
            elif mat[x-1][y] == 'w' or mat[x-1][y] == 'W' or x - 1 == 0:
                cost = cost - 9
            elif mat[x-1][y] == '.' or mat[x-2][y] == '.':
                cost = cost - 5
            elif y + 3 < N or y + 2 < N:
                if mat[x][y+2] == 'w' or mat[x][y+2] == 'W':
                    cost = cost - 9
                elif mat[x][y+1] == 'w' or mat[x][y+1] == 'W':
                    cost = cost - 9
                elif y - 3 >= 0 or y - 2 >= 0:
                    if mat[x][y-2] == 'w' or mat[x][y-2] == 'W':
                        cost = cost - 9
                    elif mat[x][y-1] == 'w' or mat[x][y-1] == 'W':
                        cost = cost - 9
                    elif mat[x-1][y+1] == 'w' or mat[x-1][y+1] == 'W' or mat[x-2][y+1] == 'w' or mat[x-2][y+1] == 'W' or x - 1 == 0 or x - 2 == 0:
                        cost = cost - 5
                    elif mat[x-1][y-1] == 'w' or mat[x-1][y-1] == 'W' or mat[x-2][y-1] == 'w' or mat[x-2][y-1] == 'W' or x - 1 == 0 or x - 2 == 0:
                        cost = cost - 5
                    else:
                        cost = cost - 2
                else:
                    cost = cost - 1
            else:
                cost = cost - 1
        else:
            cost = cost - 1
        
    
    return(cost)
    
def minimax_white(depth, mat, player, N, a, b):
    
    if depth == 0 or winner(mat,'w'):
        #print(evaluate(mat), "".join(["".join([str(item) for item in sublist]) for sublist in mat]))
        return evaluate(mat), mat
   
    if player == 'w':
        maxEval = float('-inf')
        best_move = None
        for move in white_moves(mat, N):
            evaluation = minimax_white(depth-1, move, 'b', N, a, b)[0]
            maxEval = max(maxEval, evaluation)
            if maxEval == evaluation:
                best_move = move
            a = max(a,evaluation)
            if b <= a:
                break
        
        return maxEval, best_move
    else:
        minEval = float('inf')
        best_move = None
        for move in black_moves(mat, N):
            evaluation = minimax_white(depth-1, move, 'w', N, a, b)[0]
            minEval = min(minEval, evaluation)
            if minEval == evaluation:
                best_move = move
            b = min(b,evaluation)
            if b <= a:
                break
            
        return minEval, best_move

    
def minimax_black(depth, mat, player, N, a, b):
    
    if depth == 0 or winner(mat,'b'):
        return evaluate(mat), mat

    if player == 'b':
        maxEval = float('-inf')
        best_move = None
        for move in black_moves(mat, N):
            evaluation = minimax_black(depth-1, move, 'w', N, a, b)[0]
            maxEval = max(maxEval, evaluation)
            if maxEval == evaluation:
                best_move = move
            
            a = max(a,evaluation)
            if b <= a:
                break

        return maxEval, best_move
    else:
        minEval = float('inf')
        best_move = None
        for move in white_moves(mat, N):
            evaluation = minimax_black(depth-1, move, 'b', N, a, b)[0]
            minEval = min(minEval, evaluation)
            if minEval == evaluation:
                best_move = move
            
            b = min(b,evaluation)
            if b <= a:
                break

        return minEval, best_move

def find_best_move(board, N, player, timelimit):
    # This sample code just returns the same board over and over again (which
    # isn't a valid move anyway.) Replace this with your code!
    #
#     while True:
#         time.sleep(1)
#         yield board
    
    mat = [list(board[i:i+N]) for i in range(0, len(board), N)]
#     print(mat)

    white_pichus,white_pikachus,white_raichus,black_pichus,black_pikachus,black_raichus = find_peices(mat)
    #print_peices_pos(white_pichus,white_pikachus,white_raichus,black_pichus,black_pikachus,black_raichus)
    #moves = []
    
    #moves.append(white_pichus_moves(mat.copy(), N, white_pichus)) # 7
    #moves.append(black_pichus_moves(mat, N, black_pichus)) # 7
    #moves.append(white_pikachu_moves(mat, N, white_pikachus)) # 15
    #moves.append(black_pikachu_moves(mat, N, black_pikachus)) # 15
    #moves.append(white_raichus_moves(mat, N, white_raichus)) 
    #moves.append(black_raichus_moves(mat, N, black_raichus))
    
#     print(len(white_moves(mat,N)))
#     print(len(black_moves(mat,N)))
    
    timeout = time.time() + timelimit*0.9
#     print(time.time())
#     print(timeout)
    depth = 1
    if player == 'w':
        while time.time() < timeout:
#             print("Depth:", depth)
            cost, move = minimax_white(depth, mat, player, N, float('-inf'), float('inf'))
#             print("Depth:",depth)
#             print(cost,move)
#             print("".join(["".join([str(item) for item in sublist]) for sublist in move]))
            board = "".join(["".join([str(item) for item in sublist]) for sublist in move])
            depth = depth + 1
            yield board
    else:
        while time.time() < timeout:
            cost, move = minimax_black(depth, mat, player, N, float('-inf'), float('inf'))
            board = "".join(["".join([str(item) for item in sublist]) for sublist in move])
            depth = depth + 1
            yield board

if __name__ == "__main__":
    if len(sys.argv) != 5:
        raise Exception("Usage: Raichu.py N player board timelimit")
        
    (_, N, player, board, timelimit) = sys.argv
    N=int(N)
    timelimit=int(timelimit)
    if player not in "wb":
        raise Exception("Invalid player.")

    if len(board) != N*N or 0 in [c in "wb.WB@$" for c in board]:
        raise Exception("Bad board string.")

    print("Searching for best move for " + player + " from board state: \n" + board_to_string(board, N))
    print("Here's what I decided:")
    for new_board in find_best_move(board, N, player, timelimit):
        print(new_board)
