import itertools
import sys
import random
from prp import format_length
from prp import write_doc
from prp import read_doc
from prp import header_val
from prp import generate_binary_array


# generate permutations
def generate_permutation(n):

    if (n > 3):
        print("please wait while system processess")

    # generate binary array n bit length
    binaryArray = generate_binary_array(n)

    # array permutations
    permutes = list(itertools.permutations(binaryArray, len(binaryArray)))
    return permutes


# permutation generated and written in file
def generate_permutegen(n, doc_path):
    fi = open(doc_path, 'w')

    permutes = generate_permutation(n)

    bin_array = generate_binary_array(n)

    print("\n\n-----------------------------------------------")
    print("permutations")
    print("------------------------------------------------")

    # print header
    result = 'd\t'
    for bi in bin_array:
        result += bi + '\t'
    print(result)
    fi.write(result + '\n')

    # print result
    for indx, permute in enumerate(permutes):
        result = "f" + str(indx) + "(d)" + "\t"
        for value in permute:
            result += value + '\t'
        print(result)
        fi.write(result + '\n')

    #number of permutations generated in total
    number_of_permutes = 'total permutations: ' + str(len(permutes))
    print(number_of_permutes)
    fi.write(number_of_permutes)

if __name__ == '__main__':
    availableOpt = ["-permutegen" ]
    output = ''

    # conditions for each value must match or else shows error
    if (sys.argv[1] == availableOpt[0]):  # for permutations
        n = int(sys.argv[2].split('=')[1])
        filocation = sys.argv[3]
        if (n <= 3):
            generate_permutegen(n, filocation)
        else:
            print('error')
            exit(0)
