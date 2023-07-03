###################################
# CS B551 Fall 2022, Assignment #3
#
# Your names and user ids:
#
# (Based on skeleton code by D. Crandall)
#


import random
import math
import copy


# We've set up a suggested code structure, but feel free to change it. Just
# make sure your code still works with the label.py and pos_scorer.py code
# that we've supplied.
#
class Solver:
    # Calculate the log of the posterior probability of a given sentence
    #  with a given part-of-speech labeling. Right now just returns -999 -- fix this!
    
    def __init__(self):
        self.p_words = {}
        self.p_word_tag = {}
        self.tags = ["adj", "adv", "adp", "conj", "det", "noun", "num", "pron", "prt", "verb", "x", "."]
        self.pos_tags = {
            "adj": 0, "adv": 0, "adp": 0, "conj": 0, "det": 0, "noun": 0, "num": 0, "pron": 0, "prt": 0, "verb": 0, "x": 0,  ".": 0
        }
        self.p_pos_tags = {
            "adj": 0, "adv": 0, "adp": 0, "conj": 0, "det": 0, "noun": 0, "num": 0, "pron": 0, "prt": 0, "verb": 0, "x": 0,  ".": 0
        }
        self.emission = {}
        self.p_emission = {}
        self.transition = {}
        self.transition2 = {}
        self.p_transition = {}
        self.p_transition2 = {}
    
    def posterior(self, model, sentence, label):
        words = list(sentence)
        tags = list(label)
        if model == "Simple":
            p = 0
            for i in range(len(words)):
                if words[i] in self.p_emission and tags[i] in self.p_emission[words[i]]:
                    p += math.log10(self.p_emission[words[i]][tags[i]]) + \
                        math.log10(self.pos_tags[tags[i]]/sum(self.pos_tags.values()))
                else:
                    p += math.log10(0.00000001) + \
                        math.log10(self.pos_tags[tags[i]]/sum(self.pos_tags.values()))
            return p
        elif model == "HMM":
        
            p_1 = math.log(self.pos_tags[tags[0]] / sum(self.pos_tags.values()),10)
            x, y = 0, 0
            
            for i in range(len(tags)):
                if words[i] in self.p_emission and tags[i] in self.p_emission[words[i]]:
                    x += math.log(self.p_emission[words[i]][tags[i]],10)
                else:
                    x += math.log(0.00000001,10)
                if i != 0:
                    if tags[i-1] in self.p_transition and tags[i] in self.p_transition[tags[i-1]]:
                        y += math.log(self.p_transition[tags[i - 1]][tags[i]],10)
                    else:
                        y += math.log(0.00000001,10)
                
            return p_1 + x + y
        
        elif model == "Complex":
            return self.prob_c_mcc(words, tags)
        else:
            print("Unknown algo!")

    # Do the training!
    #
    def train(self, data):
    
        #print("################################ Start Training ################################")
        #print(len(data))
        
        
        total_count = 0
        
        for x in range(len(data)):
            for y in data[x][1]:
                self.pos_tags[y] = self.pos_tags[y] + 1
                total_count = total_count + 1
        
        #print(pos_tags)
        #print(total_count)
        
        
        for key, value in self.pos_tags.items():
            self.p_pos_tags[key] = value / total_count
            
        #print(pos_tags)
        
        
        words = {}
        
        words_count = 0
        for x in range(len(data)):
            for y in data[x][0]:
                if y in self.p_words:
                    words[y] = words[y] + 1
                else:
                    words[y] = 1
                    self.p_words[y] = 0
                words_count = words_count + 1
                    
        #print(words_count)
        
        for key, value in words.items():
            self.p_words[key] = value / words_count
            
        #print(p_words)
        
        
        
        for x in range(len(data)):
            for y in range(len(data[x][0])):
                if data[x][0][y]+"|"+data[x][1][y] in self.p_word_tag:
                    self.p_word_tag[data[x][0][y]+"|"+data[x][1][y]] = self.p_word_tag[data[x][0][y]+"|"+data[x][1][y]] + 1
                else:
                    self.p_word_tag[data[x][0][y]+"|"+data[x][1][y]] = 1
                    
        for key, value in self.p_word_tag.items():
            self.p_word_tag[key] = value / words[key.split('|')[0]]
            
        
        
        for x in range(len(data)):
            for y in range(len(data[x][0])):
                if data[x][0][y] in self.emission:
                    if data[x][1][y] in self.emission[data[x][0][y]]:
                        self.emission[data[x][0][y]][data[x][1][y]] = self.emission[data[x][0][y]][data[x][1][y]] + 1
                    else:
                        self.emission[data[x][0][y]][data[x][1][y]] = 1
                else:
                    self.emission[data[x][0][y]] = {data[x][1][y] : 1}
        
        for key, value in self.emission.items():
            for x,y in value.items():
                if key in self.p_emission:
                    self.p_emission[key][x] = y / sum(self.emission[key].values())
                else:
                    self.p_emission[key] = { x: y / sum(self.emission[key].values())}
        
        previous_pos = None
        before_previous = None
        for x in range(len(data)):
            i = 0
            for y in data[x][1]:
                if previous_pos is not None:
                    if previous_pos in self.transition:
                        if y in self.transition[previous_pos]:
                            self.transition[previous_pos][y] = self.transition[previous_pos][y] + 1
                        else:
                            self.transition[previous_pos][y] = 1
                    else:
                        self.transition[previous_pos] = {y : 1}
                
                if (before_previous and previous_pos) is not None:
                    if before_previous in self.transition2:
                        if previous_pos in self.transition2[before_previous]:
                            if y in self.transition2[before_previous][previous_pos]:
                                self.transition2[before_previous][previous_pos][y] = self.transition2[before_previous][previous_pos][y] + 1
                            else:
                                self.transition2[before_previous][previous_pos][y] = 1
                        else:
                            self.transition2[before_previous][previous_pos] = {y:1}
                    else:
                        self.transition2[before_previous] = {previous_pos:{y:1}}
                        
                previous_pos = y
        		
                if i > 1:
                    before_previous = data[x][1][i-1]
                else:
                    before_previous = None
        		    
                i = i + 1
        
        for key,value in self.transition.items():
            #print(key, value)
            for x,y in value.items():
                #print(y / sum(self.transition[key].values()))
                if key in self.p_transition:
                    self.p_transition[key][x] = y / sum(self.transition[key].values())
                else:
                    self.p_transition[key] = { x: y / sum(self.transition[key].values())}



        #print("p_word_tag:",self.p_word_tag)
        #print("tags:",self.tags)
        #print("pos_tags",self.pos_tags)
        #print("p_pos_tags",self.p_pos_tags)
        #print("emission",self.emission)
        #print("p_emission",self.p_emission)
        #print("transition:",self.transition)
        #print("transition2:",self.transition2)
        #print("p_transition:",self.p_transition)
        
        #print("################################ End Training ################################")

        pass

    # Functions for each algorithm. Right now this just returns nouns -- fix this!
    #
    def simplified(self, sentence):
        pos = []
        for word in sentence:
            #print(word)
            p = {}
            for t in self.tags:
                if (word+"|"+t) in self.p_word_tag:
                    #print(self.p_word_tag[word+"|"+t], self.p_words[word])
                    p[t+"|"+word] = self.p_word_tag[word+"|"+t] * self.p_pos_tags[t]
                else:
                    p[t+"|"+word] = 0
            pos.append(max(p, key=p.get).split('|')[0])
            
        return pos

    def hmm_viterbi(self, sentence):
        
        words = list(sentence)
        hmm = [{}]
        hmm_tags = {}
       
        for t in self.tags:
            if words[0] in self.p_emission and t in self.p_emission[words[0]]:
                hmm[0][t] = self.p_pos_tags[t] * self.p_emission[words[0]][t]
            else:
                hmm[0][t] = self.p_pos_tags[t] * 0.00000001
            hmm_tags[t] = [t]
       
        for l in range(1, len(words)):
            hmm.append({})
            c = {}
            
            for current_t in self.tags:
                m = -math.inf
                
                for prev in self.tags:
                    if words[l] in self.p_emission and current_t in self.p_emission[words[l]]:
                        if current_t in self.p_transition[prev]:
                            v = hmm[l-1][prev] * self.p_transition[prev][current_t] * self.p_emission[words[l]][current_t]
                        else:
                            v = hmm[l-1][prev] * 0.00000001 * self.p_emission[words[l]][current_t]
                    else:
                        if current_t in self.p_transition[prev]:
                            v = hmm[l-1][prev] * self.p_transition[prev][current_t] * 0.00000001
                        else:
                            v = hmm[l-1][prev] * 0.00000001 * 0.00000001
                
                    if v > m:
                        m = v
                        s = prev
                hmm[l][current_t] = m
                c[current_t] = hmm_tags[s] + [current_t]


            hmm_tags = c

        max = -math.inf
        last = len(words) - 1
        
        for t in self.tags:
            if hmm[last][t] >= max:
                max  = hmm[last][t]
                tag = t
        s = tag
        
        return hmm_tags[s]
    
    def get_p_transition2(self, pos1,pos2,pos3):
        
        if pos1 in self.p_transition2 and pos2 in self.p_transition2[pos1] and pos3 in self.p_transition2[pos1][pos2]:
            return self.p_transition2[pos1][pos2][pos3]
        
        if pos1 in self.transition2 and pos2 in self.transition2[pos1] and pos3 in self.transition2[pos1][pos2]:
            value = self.transition2[pos1][pos2][pos3]/sum(self.transition2[pos1][pos2].values())
            self.p_transition2[pos1]  = { pos2 : {pos3 : value}  }
            return value
        return 0.00000001
        
    def prob_c_mcc(self, words, s):

        p_1 = math.log(self.p_pos_tags[s[0]],10)
        x, y, z = 0, 0, 0

        for i in range(len(s)):
            if words[i] in self.p_emission and s[i] in self.p_emission[words[i]]:
                x = x + math.log(self.p_emission[words[i]][s[i]],10)
            else:
                x = x + 0.00000001
            if i != 0:
                if s[i - 1] in self.p_transition and s[i] in self.p_transition[s[i - 1]]:
                    y = y + math.log(self.p_transition[s[i - 1]][s[i]],10)
                else:
                    y = y + 0.00000001
            if i != 0 and i != 1:
                z = z + math.log(self.get_p_transition2(s[i - 2], s[i - 1], s[i]),10)

        return p_1+x+y+z
        
    def complex_mcmc(self, sentence):
    
        words = list(sentence)
        samples = []
        c_tags = []
        
        s = self.simplified(sentence)
        iter= 50
        ignore = 5

        for i in range(iter):
            
            for x in range(len(words)):
                p = [0] * len(self.tags)
                log_p = [0] * len(self.tags)
            
                for y in range(len(self.tags)):
                    s[x] = self.tags[y]
                    log_p[y] = self.prob_c_mcc(words, s)

                a = min(log_p)
                for z in range(len(log_p)):
                    log_p[z] -= a
                    p[z] = math.pow(10, log_p[z])

                add = sum(p)
                p = [q / add for q in p]
                
                r = random.random()
                t = 0
                for z in range(len(p)):
                    t += p[z]
                    if r < t:
                        s[x] = self.tags[z]
                        break
        
            if i >= ignore:
                samples.append(s)

        for l in range(len(words)):
            tags_c = {}
            for s in samples:
                if s[l] in tags_c:
                    tags_c[s[l]] = tags_c[s[l]] + 1
                else:
                    tags_c[s[l]] = 1
            c_tags.append(tags_c)
            
            
        mcc_tags = [max(c_tags[l], key = c_tags[l].get) for l in range(len(words))]
    
        return [ t.lower() for t in mcc_tags ]



    # This solve() method is called by label.py, so you should keep the interface the
    #  same, but you can change the code itself. 
    # It should return a list of part-of-speech labelings of the sentence, one
    #  part of speech per word.
    #
    def solve(self, model, sentence):
    
        if model == "Simple":
            return self.simplified(sentence)
        elif model == "HMM":
            return self.hmm_viterbi(sentence)
        elif model == "Complex":
            return self.complex_mcmc(sentence)
        else:
            print("Unknown algo!")

