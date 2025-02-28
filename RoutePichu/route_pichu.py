#!/usr/local/bin/python3
#
# route_pichu.py : a maze solver
#
# Submitted by : Chiranthan Shadaksharaswamy
#
# Based on skeleton code provided in CSCI B551, Fall 2022.

import sys

# Parse the map from a given filename
def parse_map(filename):
        with open(filename, "r") as f:
                return [[char for char in line] for line in f.read().rstrip("\n").split("\n")][3:]
                
# Check if a row,col index pair is on the map
def valid_index(pos, n, m):
        return 0 <= pos[0] < n  and 0 <= pos[1] < m

# Find the possible moves from position (row, col)
def moves(map, row, col):
        moves=((row+1,col), (row-1,col), (row,col-1), (row,col+1))

        # Return only moves that are within the house_map and legal (i.e. go through open space ".")
        return [ move for move in moves if valid_index(move, len(map), len(map[0])) and (map[move[0]][move[1]] in ".@" ) ]

def directions(r1,c1,r2,c2):
        if r2-r1 == 1:
            return('U') 
        elif r2-r1 == -1:
            return('D')
        elif c1-c2 == 1:
            return('R')
        elif c2-c1 == 1:
            return('L')
        else:
            return('null')
    
# Perform search on the map
#
# This function MUST take a single parameter as input -- the house map --
# and return a tuple of the form (move_count, move_string), where:
# - move_count is the number of moves required to navigate from start to finish, or -1
#    if no such route exists
# - move_string is a string indicating the path, consisting of U, L, R, and D characters
#    (for up, left, right, and down)

def search(house_map):
        # Find pichu start position
        route = []
        visited = []
        direction = []
        dir_str=""
        pichu_loc=[(row_i,col_i) for col_i in range(len(house_map[0])) for row_i in range(len(house_map)) if house_map[row_i][col_i]=="p"][0]
        fringe=[(pichu_loc,0)]

        while fringe:
                (curr_move, curr_dist)=fringe.pop()
                if (curr_dist > 1):
                    pqr = curr_dist-1
                    direction = direction[:pqr]
                    route = route[:pqr+1]
                for move in moves(house_map, *curr_move):
                    if house_map[move[0]][move[1]]=="@":
                        route.append(curr_move)
                        r2,c2 = route[-2]
                        r1,c1 = route[-1]
                        dire = directions(r1,c1,r2,c2)
                        if (dire != 'null'):
                            direction.append(dire)
                        route.append(move)
                        r2,c2 = route[-2]
                        r1,c1 = route[-1]
                        dire = directions(r1,c1,r2,c2)
                        if (dire != 'null'):
                            direction.append(dire)
                        
                        for i in range(len(direction)):
                            dir_str=dir_str+str(direction[i])
                        return (curr_dist+1,dir_str) #Dummy
                    else:
                        if (move not in visited):
                            visited.append(move)
                            fringe.append((move, curr_dist + 1))
                            #Last element is popped
                            if curr_move not in route:
                                route.append(curr_move)
                            
                            # Determine the directions
                            if (len(route)>1):
                                r2,c2 = route[-2]
                                r1,c1 = route[-1]
                                dire = directions(r1,c1,r2,c2)
                                if (dire != 'null'):
                                    direction.append(dire)
                                
        return ([-1,""])    
                          
                
                    
                
                                           

# Main Function
if __name__ == "__main__":
        house_map=parse_map(sys.argv[1])
        print("Shhhh... quiet while I navigate!")
        solution = search(house_map)
        print("Here's the solution I found:")
        print(str(solution[0]) + " " + solution[1])

