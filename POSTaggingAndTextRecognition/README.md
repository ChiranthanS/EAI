# dmancha-cshadaks-dbraj-a3

## Part 1: Part-of-speech tagging.

The goal of the problem is to mark every word in a sentence with its corresponding part of speech. These are Noun, Adjective, Verb, etc.

We have to implement this using three different Bayes Networks:
1. Simple Bayes Net
2. HMM
3. Complicated model

We have 3 datasets:
1. Training data: Which we will use to train the models and do any pre-computations that are required for implementing the bayes net's 
2. Tiny test data: This we will use to debug and test our code while designing and implementing our solution
3. Test data: This is the final test dataset that we will test our model on and calculate the accuracies

## Training the data

First step is to use the training dataset to do all the pre-computations
We find the following from the training data:
1. Probability of words
2. POS tags
3. Probability of the POS tags
4. Probability of words given tags
5. Emission count
6. Emission probabilities
7. Transition count
8. Transition probabilities
9. Second level transition count
10. Second level transition probabilities

All of these are stored as dictionaries, because of the easy access to data and they cost only constant time to fetch any data

## 1. Simple Bayes Net

We use naive bayes inference to predict the most likely tag of the words in each sentence

Basically our job is to estimate the most-probable tag si for each word Wi, the mathematical formulation for this is:

si* = argmax P(Si = si|W)

Now, P(S|W) = P(W|S) * P(S) / P(W)

We can ignore P(W) as its value is same for all the tags for that word

Other two quantities can be fetched from the trained dictionaries
  

We find the max value of them and assign the tag to the word

## 2. HMM

This is a richer bayes net that manages dependencies between the words
This can be achivend my using Viterbi algorithm, which finds the maximum a posteriori (MAP) tag for the sentence

For implementing this, we have found the emission and transition probabilities from the training data.

## 3. Complicated model

This model incorporates even richer dependencies. So it's not HMM and viterbi cannot be used. So we have to use gibbs sampling.
Here every tag depends on the previous two tags.
So while training we have calculated second level transition probabilities, which will be used here.

## Accuracy

On testing the code on the given test data, below accuracies were found:

==> So far scored 2000 sentences with 29442 words.

1. Simple:

  Words Correct: 90.90%
  
  Sentences correct: 34.80%

2. HMM:

  Words Correct: 94.45%
  
  Sentences correct: 51.75%

3. Complex:
  
  Words Correct: 16.27%
  
  Sentences correct: 0.00%
  

Note: The accuracy for complex model is not very good, we tried to implement different approaches, increasing the interations, but due to time contraint we were unable to improve the accuracy.



## Part 2: Reading text

The goal is to identify the text in the image. We are required to resolve ambiguities using the structural properties of the language because these images are noisy and the assumption made is that there are only English letters in the sentence.

## Implementation Overview

Training the data using bc.train, emission probabilities were calculated using hit or miss ratio and transition probabilities as well. The text in the given test images must be identified using Simple Bayes net and HMM with MAP inference. For each character in the Simple Bayes net, the maximum hit or miss ratio is calculated and assigned. If there were more than 340 blank spaces, they were classified as spaces. To prevent probabilities from rising above 1, transition probability was normalized between 9 raised to the power 96 and 9 raised to the power 99.

## Functions Used

training_fn() - used to find transition probabilities calculated using bc.train and find frequency of the given characters.

Lst_cpr() - Used to find Hit or miss ratio after comparing the lists

Lst_comparer() - Used to compare train and test letters and returns letters with high hit or miss ratio

hmm_fndr() - This function is made to calculate the viterbi algorithm

simple() - This function is used to calculate Simple Bayes net

## Code - Modification and Challanges faced

While attempting to normalize the data, we attempted to set the values  from -infinity to +infinity, which resulted in a highly inaccurate classification model. However, after adding weights to our emission probabilities and normalizing transition probabilities between 9 raised to the power 96 and 9 raised to the power 99, we were able to accurately fill our 2d array and identify the text.
