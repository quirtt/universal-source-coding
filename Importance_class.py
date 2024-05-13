import sys
from collections import defaultdict

class Importance_calculations:

    def __init__(self, file):
        self.data = self.filter(file)

    def filter(self, str):
        str = str.lower()
        i = [x for x in range(97)] 
        j = [x for x in range(123,256)]
        k = i + j
        for c in [chr(i) for i in k]:
            str = str.replace(c, '')
        return str

    def importance_dictionary(self):
        dictionary = []
        counter = defaultdict(int)
        phrase = ""
        for char in self.data:
            new_phrase = phrase + char
            
            if new_phrase in dictionary:
                phrase = new_phrase
            else:
                counter[phrase] += 1
                dictionary.append(new_phrase)
                # phrase = char
                phrase = ''
        print('importance dictionary:', dictionary)
        return counter, dictionary

    def rank(self):
        counter, dictionary = self.importance_dictionary()
        dictionary.sort(key=lambda str: len(str)*counter[str], reverse=True)
        return dictionary, counter
    
    def importance_sorting(self):
        ranked_dict, counter = self.rank()
        print(counter)
        return ranked_dict, counter
    
    def encode_rank(self):
        ranked_dict, _ = self.rank()
        ranking_levels = {}
        rank = 1
        for e in ranked_dict:
            ranking_levels[e] = rank
            rank += 1
        print('ranking_levels:', ranking_levels)
        return ranking_levels

#testing puposes only
#file = open('no_rel/data.txt', 'r')
#text = file.readlines()[2]
#text = "aababbabbaababba"
#Test = Importance_calculations(text)
#z,_ = Test.importance_sorting()
#print(_)
#print(Test.importance_registry())