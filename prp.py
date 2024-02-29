import itertools
import sys
import random

# write function
def write_doc(doc_path, data):
    with open(doc_path, 'w') as f:
        f.write(data)


# read function
def read_doc(doc_path):
    with open(doc_path, 'r') as f:
        contents = f.read()
        return contents

# binary to string convertion function
def format_length(for_len):
    m = '{:0' + str(for_len) + 'b}'
    return m

# header value generation function
def header_val(arr):
    result = '\td\t'
    for i in arr:
        result += i + '\t'
    return result

# create random IV
def generate_random_IV(n):
    n_length = int(n)
    IV = ''.join(str(random.randint(0, 1)) for i in range(n_length))
    return IV

# array generated of n binary bit
def generate_binary_array(n):
    binaryArray = []
    binary = ''
    count = 0
    while True:
        binary = format_length(n).format(count)
        if len(binary) > n:
            break
        binaryArray.append(binary)
        count += 1
    return binaryArray

