# SeekTruth.py : Classify text objects into two categories
#
# PLEASE PUT YOUR NAMES AND USER IDs HERE
#
# Based on skeleton code by D. Crandall, October 2021
#

import sys
import re
import math

def load_file(filename):
    objects=[]
    labels=[]
    with open(filename, "r") as f:
        for line in f:
            parsed = line.strip().split(' ',1)
            labels.append(parsed[0] if len(parsed)>0 else "")
            objects.append(parsed[1] if len(parsed)>1 else "")

    return {"objects": objects, "labels": labels, "classes": list(set(labels))}

# classifier : Train and apply a bayes net classifier
#
# This function should take a train_data dictionary that has three entries:
#        train_data["objects"] is a list of strings corresponding to reviews
#        train_data["labels"] is a list of strings corresponding to ground truth labels for each review
#        train_data["classes"] is the list of possible class names (always two)
#
# and a test_data dictionary that has objects and classes entries in the same format as above. It
# should return a list of the same length as test_data["objects"], where the i-th element of the result
# list is the estimated classlabel for test_data["objects"][i]
#
# Do not change the return type or parameters of this function!
#
'''
def delete_some_things(word_dix_truth):
    #stock = ['the','and','a','to','was','i','in','we','of','for','is','it','at','on','with','that','were','as','an','are','be','all','so','us','me','this','our','you','my','hotel','room','very','had','not','but','great','they','from','have','there','chicago','stay','when','would','staff','service','rooms','','one','stayed','location','if','no','just','out','about','again','here','by','get','go','becauses','what','did','because','their','which','will','even','more','place','after','up','or','he','im','id','see','off','like','has','could','didnt','got','she','her','much','some','hadnt','them','than','could','night','only']
    #stock = ['the','and','a','to','was','i','in','we','of','for','is','it','at','on','with','that','were','as','an','are','be','all','so','us','me','this','our','you','my','hotel','room','very','had','not','but','great','they','from','have','there','chicago','stay','when','would','staff','service','rooms','','one','stayed','location','if','no','just','out','about','again','here','by','get','go','becauses','what','did','because','their','which','will','even','more','place','after','up','or','he','im','id','see','off','like','has','could','didnt','got','she','her','much','some','hadnt','them','than','could','only','night']
    stock = ['the','and','to','i','we']
    for i in range(len(stock)):
        if stock[i] in word_dix_truth:
            del word_dix_truth[stock[i]]
    
    return word_dix_truth


def delete_some_things(test_dict):
    res = {}
    K = 2000
    for key in test_dict:
        if not (isinstance(test_dict[key], int) and test_dict[key] > K):
            res[key] = test_dict[key]
            
    return res

'''

def classifier(train_data, test_data):
    # This is just dummy code -- put yours here!
    #print("Classes",test_data["classes"]) -> Only Truthful and deceit
    #print("Objects",test_data["objects"]) -> Remaining shiz
    tful = 0
    for i in range(len(train_data["labels"])):
        if train_data["labels"][i] == "truthful":
            tful+=1
    tdec = len(train_data["labels"]) - tful
    
    word_dix_truth = {}
    word_dix_decit = {}
    
    for i in range(len(train_data["objects"])):
        sentence = train_data["objects"][i].split()
        if train_data["labels"][i] == "truthful":
            for i in range(len(sentence)):
                sentence[i] = re.sub('[^\w\s]', '', sentence[i])
                if sentence[i].lower() not in word_dix_truth:
                    temp = {sentence[i].lower():1}
                    word_dix_truth.update(temp)
                else:
                    updater = {sentence[i].lower():word_dix_truth.get(sentence[i].lower())+1}
                    word_dix_truth.update(updater)
        else:
            for i in range(len(sentence)):
                sentence[i] = re.sub('[^\w\s]', '', sentence[i])
                if sentence[i].lower() not in word_dix_decit:
                    temp = {sentence[i].lower():1}
                    word_dix_decit.update(temp)
                else:
                    updater = {sentence[i].lower():word_dix_decit.get(sentence[i].lower())+1}
                    word_dix_decit.update(updater)
    '''    
    for i in range(len(word_dix_truth)):
        updater = {list(word_dix_truth.keys())[i]:list(word_dix_truth.values())[i]/sum(word_dix_truth.values())+1}
        word_dix_truth.update(updater)
        
    for i in range(len(word_dix_decit)):
        updater = {list(word_dix_decit.keys())[i]:list(word_dix_decit.values())[i]/sum(word_dix_decit.values())+1}
        word_dix_decit.update(updater)
    '''
    #Testing phase begins here
    #word_dix_truth = delete_some_things(word_dix_truth)
    #word_dix_decit = delete_some_things(word_dix_decit)
        
    classifier_list = []
    
   
    for i in range(len(test_data["objects"])):
        P_T = math.log(tful/len((train_data["labels"])))
        P_D = math.log(1.0 - P_T)
        sentence = test_data["objects"][i].split()
        for j in range(len(sentence)):
            #print("j val is",j)
            sentence[j] = re.sub('[^\w\s]', '', sentence[j])
            if (sentence[j].lower() in word_dix_truth): 
                n = word_dix_truth.get(sentence[j].lower())+1
                P_T = P_T + math.log((n/(sum(word_dix_truth.values())+len(word_dix_truth))))
            else:
                n = 1
                P_T = P_T + math.log((n/(sum(word_dix_truth.values())+len(word_dix_truth))))
                
            if (sentence[j].lower() in word_dix_decit): 
                n = word_dix_decit.get(sentence[j].lower())+1
                P_D = P_D + math.log((n/(sum(word_dix_decit.values())+len(word_dix_decit))))
            else:
                n = 1
                P_D = P_D + math.log((n/(sum(word_dix_decit.values())+len(word_dix_decit))))
                #print(sentence[j].lower(),word_dix_decit.get(sentence[j].lower()),word_dix_truth.get(sentence[j].lower()))
               
            '''
            if (sentence[j].lower() in word_dix_truth) and (sentence[j].lower() not in word_dix_decit):
                n = word_dix_truth.get(sentence[j].lower())+1
                #if P_T * (n/(sum(word_dix_truth.values())+len(word_dix_truth)))!=0:
                P_T = P_T * (n/(sum(word_dix_truth.values())+len(word_dix_truth)))
                #if P_D * (1/(sum(word_dix_decit.values())+1))!=0:
                P_D = P_D * (1/(sum(word_dix_decit.values())+1))
                
            if (sentence[j].lower() not in word_dix_truth) and (sentence[j].lower() in word_dix_decit):
                n = word_dix_decit.get(sentence[j].lower())+1
                #if P_D * (n/(sum(word_dix_decit.values())+1))!=0:
                P_D = P_D * (n/(sum(word_dix_decit.values())+1))
                #if P_T * (1/(sum(word_dix_truth.values())+len(word_dix_decit)))!=0:
                P_T = P_T * (1/(sum(word_dix_truth.values())+len(word_dix_decit)))
            '''
                
        if P_T > P_D:
            classifier_list.append("truthful")
        else:
            classifier_list.append("deceptive")
        
       
    #print(dict(sorted(word_dix_truth.items(), key=lambda item:item[1])))
    #print(dict(sorted(word_dix_decit.items(), key=lambda item:item[1])))
    return classifier_list
    #return [test_data["classes"][1]] * len(test_data["objects"])


if __name__ == "__main__":
    if len(sys.argv) != 3:
        raise Exception("Usage: classify.py train_file.txt test_file.txt")

    (_, train_file, test_file) = sys.argv
    # Load in the training and test datasets. The file format is simple: one object
    # per line, the first word one the line is the label.
    train_data = load_file(train_file)
    test_data = load_file(test_file)
    if(sorted(train_data["classes"]) != sorted(test_data["classes"]) or len(test_data["classes"]) != 2):
        raise Exception("Number of classes should be 2, and must be the same in test and training data")

    # make a copy of the test data without the correct labels, so the classifier can't cheat!
    test_data_sanitized = {"objects": test_data["objects"], "classes": test_data["classes"]}

    results= classifier(train_data, test_data_sanitized)

    # calculate accuracy
    correct_ct = sum([ (results[i] == test_data["labels"][i]) for i in range(0, len(test_data["labels"])) ])
    #print(test_data["labels"])
    print("Classification accuracy = %5.2f%%" % (100.0 * correct_ct / len(test_data["labels"])))
