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
    #successfully filtered the sample
    def code_book(self):
        dictionary = []
        accum = ''
        for i in self.data:
            pat = accum + i
            if pat in dictionary:
                accum = pat
            else:
                dictionary.append(pat)
                accum = ''
        return dictionary
    #we've built the iterative dictionary
    def occurances(self):
        dictionary = self.code_book()
        encode = {}
        for i in dictionary:
            encode[i] = self.data.count(i)
        return encode 
    #we've built the encode hashmap
    def rank(self):
        occur = self.occurances()
        code_book = self.code_book()
        code_book.sort(key=lambda str: len(str)*occur[str], reverse=True)
        return code_book
    #implemented the rank array
    def importance_sorting(self):
        ranked = self.rank()
        occurances = self.occurances()

        for i in range(len(ranked)-1):
            x = ranked[i]
            idx_sub = i + 1
            while idx_sub< len(ranked):
                z = ranked[idx_sub]
                if z in x:
                    occurances[z] = occurances[z] - occurances[x]*(x.count(z))
                idx_sub += 1 
            ranked.sort(key=lambda str: len(str)*occurances[str], reverse=True)
        return ranked, occurances
    #final ranking is done!
    def normalize_dict_values(self, dictionary):
        min_value = abs(min(dictionary.values()))
        for i in dictionary.keys():
            dictionary[i] += min_value
        normalizer = sum(dictionary.values()) 
        normalized_dict = {}
        for key, value in dictionary.items():
            normalized_value = value / normalizer
            normalized_dict[key] = round(normalized_value, 4)
        return normalized_dict
    def importance_registry(self):
        _,unnorm = self.importance_sorting()
        importance = self.normalize_dict_values(unnorm)
        return importance


#testing puposes only
#file = open('no_rel/data.txt', 'r')
#text = file.readlines()[2]
#text = "aababbabbaababba"
#Test = Importance_calculations(text)
#z,_ = Test.importance_sorting()
#print(_)
#print(Test.importance_registry())