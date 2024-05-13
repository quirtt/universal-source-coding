class Encoding:

    def __init__(self, phrase, rankings_encode):
        self.data = phrase 
        self.encode_order = rankings_encode
        print(rankings_encode)

    def encoder(self):
        
        accum = ''
        encoded = ''
        appeared_before = []
        code_with_space = []
        for s in self.data:
            #print(accum)
            pattern = accum+s
            if pattern in appeared_before:
                accum = pattern 
            else:
                appeared_before.append(pattern)
                # print('appeared', appeared_before)
                if len(pattern) == 1:
                    encoded += '# '+pattern+' '
                    code_with_space.append("#"+pattern) 
                else:
                    encoded = encoded + str(self.encode_order[accum]) +' '+s+' '
                    code_with_space.append(str(self.encode_order[accum])+s)
                accum = ''
        #print(address_code)
        return encoded, appeared_before

    def encoded(self):
        code,_ = self.encoder()
        return code.replace(' ', '')

    def ambiguity_solver(self,):
        code_with_space,list_code = self.encoder()
        accumulator = code_with_space.split()
        running_dictionary = {}
        unambiguous = ''
        #print(accumulator)

        def return_key(dictionary, idx):
            return list(dictionary.keys())[list(dictionary.values()).index(idx)]

        for i in range(len(list_code)-1):
            s = accumulator[2*i], accumulator[2*i+1] 
            if s[0] != '#' :
                if (accumulator[2*i+2] != '#') and (int(accumulator[2*i+2]) not in list(running_dictionary.values())):
                    unambiguous += ''.join(s)
                    prev = return_key(running_dictionary, int(s[0]))
                    running_dictionary[prev + s[1]] = int(accumulator[2*i+2])
                elif (accumulator[2*i+2] != '#') and (int(accumulator[2*i+2]) in list(running_dictionary.values())):
                    prev = return_key(running_dictionary, int(s[0]))
                    actual_rank = self.encode_order[prev+s[1]]
                    running_dictionary[prev + s[1]] = actual_rank
                    unambiguous = unambiguous+''.join(s)+'('+str(actual_rank)+')'      
                else:
                    prev = return_key(running_dictionary, int(s[0]))
                    actual_rank = self.encode_order[prev + s[1]]
                    running_dictionary[prev + s[1]] = actual_rank
                    unambiguous = unambiguous + ''.join(s) + '(' + str(actual_rank) + ')'
            if s[0] == '#':
                if accumulator[2*i+2] == '#':
                    actual_rank = self.encode_order[s[1]]
                    running_dictionary[s[1]] = actual_rank
                    unambiguous = unambiguous + ''.join(s) + '(' + str(actual_rank) + ')'
                elif accumulator[2*i+2] != '#' and (int(accumulator[2*i+2]) in list(running_dictionary.values())) :
                    actual_rank = self.encode_order[s[1]]
                    running_dictionary[s[1]] = actual_rank
                    unambiguous = unambiguous+''.join(s)+'('+str(actual_rank)+')'
                else:
                    actual_rank = int(accumulator[2*i+2])
                    running_dictionary[s[1]] = actual_rank 
                    unambiguous = unambiguous + ''.join(s)
        unambiguous += accumulator[-2]+accumulator[-1]
        #print(running_dictionary)
        return unambiguous