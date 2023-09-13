#!/usr/local/bin/python3
#
# arrange_pichus.py : arrange agents on a grid, avoiding conflicts
#
# Submitted by : Chiranthan Shadaksharaswamy
#
# Based on skeleton code in CSCI B551, Fall 2021.

import sys

# Parse the map from a given filename
def parse_map(filename):
	with open(filename, "r") as f:
		return [[char for char in line] for line in f.read().rstrip("\n").split("\n")][3:]

# Count total # of pichus on house_map
def count_pichus(house_map):
    return sum([ row.count('p') for row in house_map ] )

# Return a string with the house_map rendered in a human-pichuly format
def printable_house_map(house_map):
    return "\n".join(["".join(row) for row in house_map])
    
# Add a pichu to the house_map at the given position, and return a new house_map (doesn't change original)
def add_pichu(house_map, row, col):
    return house_map[0:row] + [house_map[row][0:col] + ['p',] + house_map[row][col+1:]] + house_map[row+1:]

# Get list of successors of given house_map state
def successors(house_map):
    return [add_pichu(house_map, r, c) for r in range(0, len(house_map)) for c in range(0,len(house_map[0])) if (house_map[r][c] == '.' and  verify_R_C_D(house_map,r,c))]

# check if house_map is a goal state
def is_goal(house_map, k):
    return count_pichus(house_map) == k 

def verify_R_C_D(house_map,r,c):
    return View_Up(house_map,r,c) and View_Down(house_map,r,c) and View_Left(house_map,r,c) and View_Right(house_map,r,c) and checkDiagonal(house_map,r,c)
    
    
def checkDiagonal(house_map,r,c):
    return Diagonal_UpL(house_map,r,c) and diagonal_UpR(house_map,r,c) and diagonal_LoR(house_map,r,c) and diagonal_LoL(house_map,r,c)
  

def Diagonal_UpL(house_map,r,c):
    while ((0<=r<len(house_map)) and (0<= c <len(house_map[0]))):
        if house_map[r][c] in "X@":
            return True
        elif house_map[r][c]=="p":
            return False
        else:
            r=r-1
            c=c-1
    return True

def diagonal_UpR(house_map,r,c):
    while ((0<=r<len(house_map)) and (0<= c <len(house_map[0]))):
        if house_map[r][c] in "X@":
            return True
        elif house_map[r][c]=="p":
            return False
        else:
            r=r-1
            c=c+1
    return True

def diagonal_LoL(house_map,r,c):
    while ((0<=r<len(house_map)) and (0<= c <len(house_map[0]))):
        if house_map[r][c] in "X@":
            return True
        elif house_map[r][c]=="p":
            return False
        else:
            r=r+1
            c=c-1
    return True

def diagonal_LoR(house_map,r,c):
    while ((0<=r<len(house_map)) and (0<= c <len(house_map[0]))):
        if house_map[r][c] in "X@":
            return True
        elif house_map[r][c]=="p":
            return False
        else:
            r=r+1
            c=c+1
    return True

def View_Up(house_map,r,c):
    while ((0<=r<len(house_map)) and (0<= c <len(house_map[0]))):
        if house_map[r][c] in "X@":
            return True
        elif house_map[r][c]=="p":
            return False
        else:
            r=r-1
    return True

def View_Down(house_map,r,c):
    while ((0<=r<len(house_map)) and (0<= c <len(house_map[0]))):
        if house_map[r][c] in "X@":
            return True
        elif house_map[r][c]=="p":
            return False
        else:
            r=r+1
    return True

def View_Left(house_map,r,c):
    while ((0<=r<len(house_map)) and (0<= c <len(house_map[0]))):
        if house_map[r][c] in "X@":
            return True
        elif house_map[r][c]=="p":
            return False
        else:
            c=c-1
    return True

def View_Right(house_map,r,c):
    while ((0<=r<len(house_map)) and (0<= c <len(house_map[0]))):
        if house_map[r][c] in "X@":
            return True
        elif house_map[r][c]=="p":
            return False
        else:
            c=c+1
    return True
    

# Arrange agents on the map
#
# This function MUST take two parameters as input -- the house map and the value k --
# and return a tuple of the form (new_house_map, success), where:
# - new_house_map is a new version of the map with k agents,
# - success is True if a solution was found, and False otherwise.
#
def solve(initial_house_map,k):
    
    if (k==1) and is_goal(initial_house_map,k):
        return (initial_house_map,True)
  
    fringe = [initial_house_map]
    visited=[]
    while len(fringe) > 0:
        succ=successors(fringe.pop())
        for new_house_map in succ:
            if is_goal(new_house_map,k):
                return(new_house_map,True)
            else:
                if new_house_map not in visited:
                    fringe.append(new_house_map)
                    visited.append(new_house_map)
    return (new_house_map,False)

    

# Main Function
if __name__ == "__main__":
    house_map=parse_map(sys.argv[1])
    # This is k, the number of agents
    k = int(sys.argv[2])
    print ("Starting from initial house map:\n" + printable_house_map(house_map) + "\n\nLooking for solution...\n")
    solution = solve(house_map,k)
    print ("Here's what we found:")
    print (printable_house_map(solution[0]) if solution[1] else "False")


