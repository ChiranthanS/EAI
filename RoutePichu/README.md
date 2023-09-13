# a0-release

## [Route_pichu]

## Abstract

* Initial State: Pichu 'p' is located within the walls of the map, where 'X' represents the walls and '@' represent the final destination

* Goal State: Pichu 'p' should reach the final destination '@'

* Fringe: Is the stack which holds successive states.

* Visited is a stack which holds visited nodes, route is a stack which traverses the optimal path pichu covered using DFS.


* State Space: Defined as all positions on the map where pichu can travel before reaching destination '@'

## Modifications

Changed the search function by adding route, visited and direction list(s). Since the code provided was running in infinite loop, I added a visited list to keep track of the nodes visited and only add elements 

to the list visited and fringe if it was never visited before. Every time we check for the possibility of the node (top of fringe which will be popped) being the destination, if it’s not and not in visited we append it to visited and fringe.

Function increases the path length by 1 every time a new node is visited to keep track of the path. I used Dir string to return directions as i appended the movements (U, D,L,R) to the list direction

We use DFS to traverse the entire map till we attain the goal state or fringe is empty.

In the current I have not used a heuristic or an algorithm which supports it like A*, but using an algorithm which can make use of an heuristic like Manhattan distance can yield better results, using a heuristic 

would help us select a node which brings us closer to the solution if there is one.

## [Arrange Pichus]

##Abstract

* Initial state: There is one pichu 'p' at a given position in the map

* Goal: To check if its feasible to fit K number of pitches where no pichu can see each other in row, column or diagonal.

* Successor function: defined gives all possible states from the present state where all K pichus can be placed following the constrains of row and diagonal where pichus can't see each other

* State space: Set of all states with pichu inserted anywhere in the house map without restrictions.

## Modifications

Made modifications to successor function by adding the function verify_R_C_D(house_map,r,c) which validated if no pichu is present in rows, columns or diagonal(s)

The verify_R_C_D(house_map,r,c) function internally calls checkDiagonal() (which checks if pichu is present in the diagonal of the map, by internally calling Diagonal_UpL(),diagonal_UpR(), diagonal_LoR() and diagonal_LoL)

View_Up() (to check if any elements are present on the line to the top), View_Down(to check if any elements are present on the line to the bottom)

View_Left() (check if elements are present to the left line of pichu), View_Right() ((check if elements are present to the right line of pichu))

If all the function return, then we can come to the conclusion that it’s a safe state and append the state to fringe and visited.

Direction function checks if 'X' or '@' is present along the lines and returns true for the case. But if it’s a 'p' along the search route it returns false.

Node are traversed line in breadth first fashion and I checked the rows and columns iteratively using a while loop and an if condition such that rows and columns I traverse always lies within the map

an edge case is handled to check if initial state is the final state by comparing it with the input k taken via command line.
  


