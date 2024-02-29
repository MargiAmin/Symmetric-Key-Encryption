import itertools
import sys
import random
from prp import format_length
from prp import write_doc
from prp import read_doc
from prp import header_val
from prp import generate_binary_array
from prp import generate_random_IV


# generate pseudorandom permutations
def generate_prp_permutations(binaryArray, l_array):
    # total permutations
    count = len(l_array)
    lst = range(0, count)
    result = []
    print("\n\n---------------------------------------------------------------------------------------------------------------------------------------------")
    print("Pseduorandom_Permutations")
    print("------------------------------------------------------------------------------------------------------------------------------------------------")

    # pseudorandom permutations created
    for i in range(count):
        perms = []
        randoms = random.sample(range(count), count)
        for j in randoms:
            j = j % len(binaryArray)
            perms.append(binaryArray[j])
        result.append(perms)
    return result


# write and print in the doc
def generate_prp(n, l, doc_path):
    fi = open(doc_path, 'w')  # write permutations

    n_array = generate_binary_array(n)

    l_array = generate_binary_array(l)

    permutes = generate_prp_permutations(n_array, l_array)

    # print header values
    print(header_val(l_array))
    fi.write('\t' + header_val(l_array) + '\n')

    # printing the pseudo random permutations
    for indx, perm in enumerate(permutes):
        result = 'k=' + str(l_array[indx]) + ',f(d)\t'
        for p in perm:
            result += p + '\t'
        print(result)
        fi.write(result + '\n')

# cbc encryption
def generate_enc_cbc(m, l, k, pseudo_permutes, filocation):
    result = []
    file = open(pseudo_permutes)

    content = file.readlines()

    # arranging key value
    keyval = 'k=' + str(k)
    keyrowline = [s for s in content if keyval in s]
    keyrowarr = keyrowline[0].split('\t')
    keyrowarr = keyrowarr[1:-1]

    # arraging them in array
    m, l, k = str(m), str(l), str(k)
    chunks, chunk_size = len(m), len(k)
    sep_m = [m[i:i + chunk_size] for i in range(0, chunks, chunk_size)]

    # generating random IV value
    IV = generate_random_IV(l)
    print('IV=', IV)

    temp_IV = IV

    # calculate cipher text
    for m_val in sep_m:
        # xor the message with IV or cn
        xor = int(m_val, 2) ^ int(temp_IV, 2)
        # looking for the value in permutations under the given key
        c = keyrowarr[xor]

        result.append(c)
        temp_IV = c

    # arranging result for printing and writing in doc
    cipher = ' '.join(result)
    print(IV + ',', cipher)
    write_doc(filocation, IV + ',' + cipher)


#  cbc decryption
def generate_dec_cbc(l, k, pseudo_permutes, ciphertextfile):
    result = []
    file = open(pseudo_permutes)

    content = file.readlines()

    keyval = 'k=' + str(k)
    keyrowline = [s for s in content if keyval in s]
    keyrowarr = keyrowline[0].split('\t')
    keyrowarr = keyrowarr[1:-1]  # removing unwanted text for resulting permutations of certain key

    # openign cipher text doc and extracting cipher text from file
    ciphertext_content = open(ciphertextfile, 'r')
    content = ciphertext_content.read()

    # splitting IV and cipher text
    split_content = content.split(',')
    IV = split_content[0]
    # splitting cipher text into bit l
    ciphertext = split_content[1].split(' ')

    # temp_IV for to iterate during XOR
    temp_IV = IV
    result = ''

    # iterating through ciphertext array to decrypt value
    for c in ciphertext:
        # find value of cipher text
        indx = keyrowarr.index(c)

        # XOR the inversed cipher text value with IV
        m = indx ^ int(temp_IV, 2)

        # formatting the result to binary
        m_bin = format_length(l).format(m)
        result += m_bin
        temp_IV = c

    # ciphertext
    print(result)


# ecb encryption
def generate_enc_ecb(m, l, k, pseudo_permutes, filocation):
    result = []
    file = open(pseudo_permutes)
    content = file.readlines()

    keyval = 'k=' + str(k)
    keyrowline = [s for s in content if keyval in s]
    keyrowarr = keyrowline[0].split('\t')
    keyrowarr = keyrowarr[1:-1]  # removing unwanted text for resulting permutations of certain key

    # seperating message and arraging them in array
    m, l, k = str(m), str(l), str(k)
    chunks, chunk_size = len(m), len(k)
    sep_m = [m[i:i + chunk_size] for i in range(0, chunks, chunk_size)]

    result = ''

    # looking for value for provided key for  corresponding message
    for m_val in sep_m:
        c = keyrowarr[int(m_val, 2)]
        result += c

    # print ciphertext
    print(result)
    write_doc(filocation, result)


if __name__ == '__main__':
    availableOpt = [ '-prpgen', '-enc_cbc', '-dec_cbc', '-enc_ecb']
    output = ''

    # conditions for each value must match or else shows error
    # pseudo random permutations
    if (sys.argv[1] == availableOpt[0]):
        n = int(sys.argv[2].split('=')[1])
        l = int(sys.argv[3].split('=')[1])
        filocation = sys.argv[4]
        if (n <= 4):
            generate_prp(n, l, filocation)
        else:
            print('error:invalid input')
            exit(0)
    # CBC encryption
    elif (sys.argv[1] == availableOpt[1]):
        m = int(sys.argv[2].split('=')[1])
        l = int(sys.argv[3].split('=')[1])
        k = int(sys.argv[4].split('=')[1])
        pseudo_permutes = sys.argv[5]
        filocation = sys.argv[6]
        generate_enc_cbc(m, l, k, pseudo_permutes, filocation)
        # CBC decryption
    elif (sys.argv[1] == availableOpt[2]):  # for CBC decryption
        l = int(sys.argv[2].split('=')[1])
        k = int(sys.argv[3].split('=')[1])
        pseudo_permutes = sys.argv[4]
        ciphertext = sys.argv[5]
        generate_dec_cbc(l, k, pseudo_permutes, ciphertext)
        # ECB encryption
    elif (sys.argv[1] == availableOpt[3]):  # for ECB encryption
        m = int(sys.argv[2].split('=')[1])
        l = int(sys.argv[3].split('=')[1])
        k = int(sys.argv[4].split('=')[1])
        pseudo_permutes = sys.argv[5]
        filocation = sys.argv[6]
        generate_enc_ecb(m, l, k, pseudo_permutes, filocation)
