class Decoding:

    def __init__(self, unambiguous):
        self.code = unambiguous 
    
    def nearest_closing_bracket(self, idx):
        j = 1
        while self.code[idx+j] != ')':
            j+=1
        return idx+j, self.code[idx+1:idx+j]
    
    def farthest_ending_digit(self, idx):
        j = 0
        while self.code[idx+j].isnumeric():
            j += 1
        return idx+j-1, self.code[idx:idx+j]
    
    def return_key(self, dictionary, idx):
        return list(dictionary.keys())[list(dictionary.values()).index(idx)]
    
    def decoder(self):
        dictionary = {}
        decode = ''
        i = 0
        while i < len(self.code):
            if self.code[i] == '#':
                if self.code[i+2] == '(': 
                    ending_bracket, inside = self.nearest_closing_bracket(i+2)
                    dictionary[self.code[i+1]] = int(inside)
                    i = 1+ending_bracket
                    decode += self.code[i+1]
                else:
                    ending_location, address = self.farthest_ending_digit(i+2)
                    dictionary[self.code[i+1]] = int(address)
                    i = 1 + ending_location
                    decode += self.code[i+1]
            else:
                j, prev = self.farthest_ending_digit(i)
                if self.code[j+2] == '(':
                    ending_bracket, inside = self.nearest_closing_bracket(j+2)
                    dictionary[self.return_key(dictionary, int(prev))+self.code[j+1]] = int(inside)
                    decode += self.return_key(dictionary, int(prev))+self.code[j+1]
                    i = 1+ending_bracket
                else:
                    ending_location, address = self.farthest_ending_digit(j+2)
                    dictionary[self.return_key(dictionary, int(prev))+self.code[j+1]] = int(address)
                    decode += self.return_key(dictionary, int(prev))+self.code[j+1]
                    i = 1 + ending_location
        print(dictionary)
        return decode