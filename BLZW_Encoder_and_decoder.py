import sys
from sys import argv
from struct import *

# taking the input file and the number of bits from command line
# defining the maximum table size
# opening the input file
# reading the input file and storing the file data into data variable
input_file, n = argv[1:]                
maximum_table_size = pow(2,int(n))      
file = open(input_file)                 
data = file.read()                      

# Building and initializing the dictionary.
dictionary_size = 256                   
dictionary = {chr(i): i for i in range(dictionary_size)}    
string = ""             # String is null.
compressed_data = []    # variable to store the compressed data.

# iterating through the input symbols.
# LZW Compression algorithm
for symbol in data:                     
    string_plus_symbol = string + symbol # get input symbol.
    if string_plus_symbol in dictionary: 
        string = string_plus_symbol
    else:
        compressed_data.append(dictionary[string])
        if(len(dictionary) <= maximum_table_size):
            dictionary[string_plus_symbol] = dictionary_size
            dictionary_size += 1
        string = symbol

if string in dictionary:
    compressed_data.append(dictionary[string])

# storing the compressed string into a file (byte-wise).
#out = input_file.split(".")[0]
#output_file = open(out + ".lzw", "wb")
#for data in compressed_data:
#    output_file.write(pack('>H',int(data)))   
#output_file.close()
#file.close()


# taking the compressed file input and the number of bits from command line
# defining the maximum table size
# opening the compressed file
# defining variables
input_file, n = argv[1:]            
maximum_table_size = pow(2,int(n))
file = open(input_file, "rb")
compressed_data = []
next_code = 256
decompressed_data = ""
string = ""

# Reading the compressed file.
while True:
    rec = file.read(2)
    if len(rec) != 2:
        break
    (data, ) = unpack('>H', rec)
    compressed_data.append(data)

# Building and initializing the dictionary.
dictionary_size = 256
dictionary = dict([(x, chr(x)) for x in range(dictionary_size)])

# iterating through the codes.
# LZW Decompression algorithm
for code in compressed_data:
    if not (code in dictionary):
        dictionary[code] = string + (string[0])
    decompressed_data += dictionary[code]
    if not(len(string) == 0):
        dictionary[next_code] = string + (dictionary[code][0])
        next_code += 1
    string = dictionary[code]

# storing the decompressed string into a file.
out = input_file.split(".")[0]
output_file = open(out + "_decoded.txt", "w")
for data in decompressed_data:
    output_file.write(data)
    
output_file.close()
file.close()
