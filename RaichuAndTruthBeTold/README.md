# a2-release-res

## Part 1 - Raichu

### Problem 
The problem deals with playing an N X N grid with 3 kinds of pieces  (Pichus,  Pikachus,  and  Raichus) of  two  different  colors  (black  and  white). Each pieces having different rules of movement.  
Two players alternate turns, with White going first. This is a classic example of 'AI playing games' with multiple states in each levels. The program accepts the arguments with the player (Pichu) (w or b). The task is to decide a recommended single move for the given player(w or b) with the given current board state, and display the new state of the board after making that move. The current board is considered and evaluated to predict the best possible move for the player in the input.

### Implementation Overview
This can be implemented using Minmax algorithm where it consist of 2 players namely called as Minimizer and Maximizer. Assuming the 'w' or 'b' in out input as a maximizer and the opposit player as a minimizer, the maximizer always wants to improve its score and the minimizer always wants to minimize its score, speaking of which, the 'Score' or the cost is the value obtained after subtracting the number of maximizers from minimizers or vice versa and adding the total sum of different pieces. The move corresponding to the best score will be considered as the best move and printed as the output.

### Abstraction
* Initial State: Any state with (Pichu, Pikachu and Raichu) at their positions as per the input. 
* Final State: State or board with next best possible move favouring our maximizer
* Successor Function: Function that gives the best possible move for our maximizer by evaluating all the possible moves of the minimizer to the maximizers move
* State Space : Set of all possible move for all the pieces in the board

### Functions Used
* find_best_move - to find the set of best moves in the given time
* find_peices - to get all the positions of the pieces in current state
* minimax_white - to get the best move for white
* minimax_black - to get the best move for black
* white_moves - to get all the possible moves for white pieces
* black_moves - to get all the possible moves for black pieces
* winner - to declare the winner after all pieces of the opposite player is been dissolved
* evaluate - to find the score or cost for the board state

### Code Modification and Challenges faced
In this problem, Initially the positions of the pieces in the given board are identified. Once these positions are known, the possible moves for each and every piece from the initial board are listed down in a list for 'white_moves' and 'black_moves' separately. 
Since the movement rules for Pichu, Pikachu and Raichu are different, the logical conditions for Pichu was pretty straight forward since it was diagonal (one step for movement and 2 step for jump over a pichu of different color). 
The logical conditions for Pikachu was a little more than pichu as it included 3 different non diagonal directional moves but with 1, 2, or 3 possible movements including the jump over pichu and pikachu. 

Also, as the piece of a Pichu or Pikachu reached the nth line of the grid, the same piece had to be transformed into Raichu, the logical movement conditions for Raichu was pretty complicated. This is because it involved movements for multiple squares with multiple directions like (forward, backward, left, right and diagonal) that could also jump over any of the piece of opposite color.
The list of all possible 8 directions are added to the list to move the Raichu. for the number of Raichus in the board, the movements for all possible directions is looped over to evaluate the possibility of the Raichu movement according to the rules stated. Implementing a logic for this code was a challenging task. 

The scores obtained from 'evaluate' function are assigned to 'MaxEval' and compared with the previous scores for each board evaluation, if both the values match and are equal to each other, the move that lead to that score is picked as the best move. for example: if the given player is 'w', the 'minimax' function for white piece calls the minimax for black piece recursively to whatever the depth required to obtain the Min or Max value. Similarly, if the given player is 'b', the 'minimax' function for black piece calls the minimax for white piece recursively to whatever the depth required to obtain the Min or Max value. The 'winner' function returns the player whose opposite player moves list is empty, this means all the pieces of the opposite plyer has been dissolved. This is how Raichu is played well and declared victory.

## Part 2 - Truth be Told

### Problem
The task is to classify reviews into faked or legitimate, for 20 hotels in Chicago. By writing a program that estimates the Naive 
Bayes  parameters  from  training  data, the parameters can be used to classify the reviews in the testing data.

### Implementation Overview
The given set of words in the sentence(s) (test data['objects']) are classified into the target class (test data['labels']) using the Naive Bayes algorithm. Each word's frequency is calculated and recorded in dictionaries, from which the likelihood that a word belongs to the class (truthful, deceptive) is derived. Prior to calculating probability, we added +1 to the count of all words in the dictionary in order to account for the situation where a word's frequency is zero. Based on the outcome of both probabilities, the target class is determined.

### Pre-processing 
Data is stripped of special characters and converted to lower case for all words in sentences to increase classification accuracy.

### Functions used
classifier() - The only function where posterior probablity is calculated using the likelihood and prior but ignoring marginilization.

delete_some_things(dictionary) is an unused function - it was used to isolate certain neutral or frequently used words, such as the, a, and an. A variant of this function was also used to delete all key and value pairs from dictionary whoe's frrequency is more the 2000.

### Code- Modification and Challenges faced
Depending on the "label" of the training class, the frequency of every word in train_data["objects"] is stored in one of two dictionaries (word_dix_truth or word_dix_decit). At this stage, the pre-processing techniques was used, and posterior probability was calculated. Initially, posterior probability was approaching zero because the likelihood(s) were small values, which led to inaccurate classifications. In order to solve this problem, we applied log transformation to the prior and likelihood and summed them rather than multiplying them all. While calculating the probability to prevent the numerator of likelihood from becoming zero we have add 1 to the frequency of all words so that the numerator is greater then 1 at all times.









