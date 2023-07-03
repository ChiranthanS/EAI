#!/usr/bin/python
#
# Perform optical character recognition, usage:
#     python3 ./image2text.py train-image-file.png train-text.txt test-image-file.png
# 
# Authors: (insert names here)
# (based on skeleton code by D. Crandall, Oct 2020)
#

from PIL import Image, ImageDraw, ImageFont
import sys
import operator
import math

CHARACTER_WIDTH=14
CHARACTER_HEIGHT=25


def load_letters(fname):
    im = Image.open(fname)
    px = im.load()
    (x_size, y_size) = im.size
    #print(im.size)
    #print(int(x_size / CHARACTER_WIDTH) * CHARACTER_WIDTH)
    result = []
    for x_beg in range(0, int(x_size / CHARACTER_WIDTH) * CHARACTER_WIDTH, CHARACTER_WIDTH):
        result += [ [ "".join([ '*' if px[x, y] < 1 else ' ' for x in range(x_beg, x_beg+CHARACTER_WIDTH) ]) for y in range(0, CHARACTER_HEIGHT) ], ]
    return result

def load_training_letters(fname):
    TRAIN_LETTERS="ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789(),.-!?\"' "
    letter_images = load_letters(fname)
    return { TRAIN_LETTERS[i]: letter_images[i] for i in range(0, len(TRAIN_LETTERS) ) }

#####
# main program
if len(sys.argv) != 4:
    raise Exception("Usage: python3 ./image2text.py train-image-file.png train-text.txt test-image-file.png")

(train_img_fname, train_txt_fname, test_img_fname) = sys.argv[1:]
train_letters = load_training_letters(train_img_fname)
test_letters = load_letters(test_img_fname)
## Below is just some sample code to show you how the functions above work. 
# You can delete this and put your own code here!

# used to find transition probabilities calculated using bc.train and find frequency of the given characters.
class decoder:
    
    
    def training_fn(self):

        fl_rdr = train_txt_fname
        xlist = []
        file = open(fl_rdr,'r')
        for ln in file:
            d = tuple([w for w in ln.split()])
            xlist += [[d]]


        DIX_tnsn = {}


        for term in xlist:
            smt = (" ").join(term[0])
            for i in range(0,len(smt)-1):
                if (smt[i] in TRAIN_LETTERS) and (smt[i+1] in TRAIN_LETTERS) and ((smt[i]+"#"+smt[i+1]) in DIX_tnsn):
                    DIX_tnsn[smt[i] + "#" + smt[i + 1]] = DIX_tnsn[smt[i] + "#" + smt[i + 1]]+1

                else:
                    if (smt[i] in TRAIN_LETTERS) and (smt[i+1] in TRAIN_LETTERS):
                        DIX_tnsn[smt[i] + "#" + smt[i + 1]] = 1


        cnt_tnsn = {}
        i = 0
        while i < len(TRAIN_LETTERS):
            p_cnt = 0
            for dxky in DIX_tnsn.keys():
                if(TRAIN_LETTERS[i]==dxky.split('#')[0]):
                    p_cnt = p_cnt+DIX_tnsn[dxky]
            if p_cnt !=0:
                cnt_tnsn[TRAIN_LETTERS[i]] = p_cnt
            i+=1

        for dxky in DIX_tnsn.keys():
            DIX_tnsn[dxky] = (DIX_tnsn[dxky]) / (float(cnt_tnsn[dxky.split("#")[0]]))


        char_1_fq = {}
        TOTAL = sum(DIX_tnsn.values())
        for dxky in DIX_tnsn.keys():
            DIX_tnsn[dxky] = DIX_tnsn[dxky] / float(TOTAL)

        for term in xlist:        
            for word in term[0]:
                if word[0] in TRAIN_LETTERS:
                    if (word[0]) in char_1_fq:
                        char_1_fq[word[0]] = char_1_fq[word[0]] + 1
                    else:
                        char_1_fq[word[0]] = 1


        TOTAL = sum(char_1_fq.values())
        for dxky in char_1_fq.keys():
            char_1_fq[dxky] = char_1_fq[dxky]/float(TOTAL)

        cnt_char = 0
        chr_fq_dx = {}
        for term in xlist:

            smt = (" ").join(term[0])
            for char in smt:
                if char in TRAIN_LETTERS:
                    cnt_char = cnt_char+1
                    if char in chr_fq_dx:
                        chr_fq_dx[char] = chr_fq_dx[char] + 1
                    else:
                        chr_fq_dx[char] = 1


        for dxky in chr_fq_dx.keys():
            chr_fq_dx[dxky] = (chr_fq_dx[dxky]+math.pow(10,10))/(float(cnt_char)+math.pow(10,10))

        TOTAL = sum(chr_fq_dx.values())

        for dxky in chr_fq_dx.keys():
            chr_fq_dx[dxky] = chr_fq_dx[dxky]/float(TOTAL)

        return [chr_fq_dx,DIX_tnsn,char_1_fq]


    #Used to compare train and test letters and returns letters with high hit or miss ratio
    def Lst_comparer(self,ltr_prcs,f1):
        DIX_LTR = {}
        for i in TRAIN_LETTERS:
            trk = 0
            ms = 1
            _Cnt = 0
            for k in range(0, len(ltr_prcs)):
                for things in range(0, len(ltr_prcs[k])):
                    if ltr_prcs[k][things] == ' ' and train_letters[i][k][things] == ' ':
                        _Cnt = _Cnt + 1
                        pass
                    else:
                        if ltr_prcs[k][things] == train_letters[i][k][things]:
                            trk = trk + 1
                        else:
                            ms = ms + 1
                DIX_LTR[' '] = 0.2
                if _Cnt > 340:
                    DIX_LTR[i] = _Cnt
                else:
                    DIX_LTR[i] = trk / float(ms)

        TOTAL = 0
        for key in DIX_LTR.keys():
            if key != " ":
                TOTAL = TOTAL + DIX_LTR[key]
            else:
                TOTAL = TOTAL + 2
        for key in DIX_LTR.keys():
            if key != " ":
                if DIX_LTR[key] != 0:
                    DIX_LTR[key] = DIX_LTR[key] / float(TOTAL)
                else:
                    DIX_LTR[key] = 0.00001

        if f1==0:
            returnLetter = dict(sorted(DIX_LTR.items(), key=operator.itemgetter(1), reverse=True)[:3])
        if f1==1:
            returnLetter = DIX_LTR

        return returnLetter

    # Used to find Hit or miss ratio after comparing the lists
    def Lst_cpr(self,ltr_prcs):

        DIX_LTR = {}
        for i in TRAIN_LETTERS:
            trk = 0
            k = 0
            ms = 1
            _Cnt = 0
            while (k < len(ltr_prcs)):
                for things in range(0, len(ltr_prcs[k])):
                    if ltr_prcs[k][things] == ' ' and train_letters[i][k][things] == ' ':
                        _Cnt = _Cnt + 1
                        pass
                    else:
                        if ltr_prcs[k][things] == train_letters[i][k][things]:
                            trk = trk + 1
                        else:
                            ms = ms + 1
                k+=1                

            DIX_LTR[' '] = 0.2
            if _Cnt > 340:
                DIX_LTR[i] = _Cnt / float(350)
            else:
                DIX_LTR[i] = trk/float(ms)

        return max(DIX_LTR.items(), key=operator.itemgetter(1))[0]

    #This function is made to calculate the viterbi algorithm
    def hmm_fndr(self,test_letters):

        l = ['0']*len(test_letters)

        A2D = []
        for i in range(0, len(TRAIN_LETTERS)):
            string = []
            for j in range(0, len(test_letters)):
                string.append([0,''])
            A2D.append(string)

        ltr_1 = d1.Lst_comparer(test_letters[0],0)
        for r in range(0,len(TRAIN_LETTERS)):
            if (TRAIN_LETTERS[r]) in char_1_fq and (TRAIN_LETTERS[r]) in ltr_1 and ltr_1[TRAIN_LETTERS[r]]!=0:
                A2D[r][0] = [- math.log10(ltr_1[TRAIN_LETTERS[r]]),'q1']

        for c in range(1,len(test_letters)):
            DIX_LTR = d1.Lst_comparer(test_letters[c],0)

            if (' ') in DIX_LTR:
                l[c] = " "

            for key in DIX_LTR.keys():
                string = {}
                for r in range(0,len(TRAIN_LETTERS)):
                    if (TRAIN_LETTERS[r]+"#"+key) in DIX_tnsn and key in DIX_LTR:
                        string[TRAIN_LETTERS[r]] = 0.1 * A2D[r][c-1][0]- math.log10(DIX_tnsn[TRAIN_LETTERS[r]+"#"+key])- 10 * math.log10(DIX_LTR[key])
                kjhm = 0
                Maxkey = ''
                for i in string.keys():
                    if kjhm < string[i]:
                        kjhm = string[i]
                        Maxkey = i
                if Maxkey != '':
                    A2D[TRAIN_LETTERS.index(key)][c] = [string[Maxkey],Maxkey]

        maxi = math.pow(9, 99)
        #maxi = float('inf')
        for r in range(0, len(TRAIN_LETTERS)):
            if maxi > A2D[r][0][0] and A2D[r][0][0] != 0:
                maxi = A2D[r][0][0]
                l[0] = TRAIN_LETTERS[r]

        for c in range(1, len(test_letters)):
            mini = math.pow(9, 96)
            #mini = float('-inf')
            for r in range(0, len(TRAIN_LETTERS)):
                if A2D[r][c][0] != 0 and A2D[r][c][0] < mini and r != len(TRAIN_LETTERS)-1 and l[c]!=' ':
                    mini = A2D[r][c][0]
                    l[c] = TRAIN_LETTERS[r]

        i = 1
        while(i<len(test_letters)):
            mini = math.pow(9, 96)
            #mini = float('-inf')
            for r in range(0, len(TRAIN_LETTERS)):
                if A2D[r][i][0] != 0 and A2D[r][i][0] < mini and r != len(TRAIN_LETTERS) - 1 and l[i]!=' ':
                    mini = A2D[r][i][0]
                    l[i] = TRAIN_LETTERS[r]
            i+=1

        maxi = math.pow(9, 99)
        #maxi = float('inf')
        for r in range(0, len(TRAIN_LETTERS)):
            if maxi > A2D[r][0][0] and A2D[r][0][0] != 0:
                maxi = A2D[r][0][0]
                l[0] = TRAIN_LETTERS[r]

        c = len(test_letters)-2
        while(c > 0):
            strLrg = ''
            mini = math.pow(10, 100)
            for ROW in range(0, len(TRAIN_LETTERS)):
                for r in range(0,len(TRAIN_LETTERS)):
                    if strLrg == '':
                        if mini > A2D[r][c][0] and A2D[r][c][0] != 0:
                            mini = A2D[r][c][0]
                            strLrg = TRAIN_LETTERS[r]
                if (TRAIN_LETTERS[ROW] + "#" + strLrg) in DIX_tnsn:
                    A2D[ROW][c][0] = A2D[ROW][c][0] - math.log10(DIX_tnsn[TRAIN_LETTERS[ROW]+"#"+strLrg])
            c-=1


        return "".join(l)

    # This function is used to calculate Simple Bayes net    
    def simple(self,test_letters):
        l = ''
        for ltr in test_letters:
            l = l + d1.Lst_cpr(ltr)
        return  l
    
d1 = decoder()
TRAIN_LETTERS = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789(),.-!?\"' "
[chr_fq_dx, DIX_tnsn, char_1_fq] = d1.training_fn()
print ("Simple: " + d1.simple(test_letters))
print ("HMM: " + d1.hmm_fndr(test_letters))

