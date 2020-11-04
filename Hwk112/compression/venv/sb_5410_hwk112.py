import pickle
import re

def compress(uncompressed):
    """Compress a string to a list of output symbols."""

    # Build the dictionary.
    dict_size = 256
    dictionary = dict((chr(i), i) for i in range(dict_size))
    # in Python 3: dictionary = {chr(i): i for i in range(dict_size)}

    w = ""
    result = []
    for c in uncompressed:
        wc = w + c
        if wc in dictionary:
            w = wc
        else:
            result.append(dictionary[w])
            # Add wc to the dictionary.
            dictionary[wc] = dict_size
            dict_size += 1
            w = c

    # Output the code for w.
    if w:
        result.append(dictionary[w])
    return result
#end def decompress(compressed):


def decompress(compressed):
    """Decompress a list of output ks to a string."""
    from io import StringIO

    # Build the dictionary.
    dict_size = 256
    dictionary = dict((i, chr(i)) for i in range(dict_size))
    # in Python 3: dictionary = {i: chr(i) for i in range(dict_size)}

    # use StringIO, otherwise this becomes O(N^2)
    # due to string concatenation in a loop
    result = StringIO()
    w = chr(compressed.pop(0))
    result.write(w)
    for k in compressed:
        if k in dictionary:
            entry = dictionary[k]
        elif k == dict_size:
            entry = w + w[0]
        else:
            raise ValueError('Bad compressed k: %s' % k)
        result.write(entry)

        # Add w+entry[0] to the dictionary.
        dictionary[dict_size] = w + entry[0]
        dict_size += 1

        w = entry
    return result.getvalue()
#end def decompress(compressed):

def read_file(fname, ext, enc):
    # open file for 'r'eading
    with open(fname + ext, 'r', encoding=enc) as file:
        dat = file.read()   #read file
        dat = perform_re(dat)
        return dat #.upper()
#end read_file(fname):

def perform_re(text):
    # try to keep original file with limited lossless factor
    text = re.sub('[^A-Za-z0-9 \!\?\.\*\(\)\r\n]+', '', text)
    return text
#end def perform_re(text):

def write_results(fname, data):
    #open file for 'w'riting
    with open(fname, 'wb') as file:
        pickle.dump(data, file)
#end def write_results(fname, data):

def print_results(fname, ext, enc):
    # open file for 'r'eading
    with open(fname + ext, 'r', encoding=enc) as file:
        # print first 45 characteers of the file
        char = file.read(45)
        print(char)
    file.close()
#end def print_results(fname, data):

def load_pickle(path):
    with open(path, 'rb') as file:
        try:
            while True:
                yield pickle.load(file)
        except EOFError:
            pass
#end def load_pickle(path):

def read_pickle(path):
    with open(path, 'ab') as file:
        for item in load_pickle(path):
            repr(item)
    return item
#end def load_pickle(path):

def main():
    # Read the original file
    FILE_NAME = 'alice'
    text = read_file(FILE_NAME, '.txt', 'utf-8')

    # Compress the file
    compressed = compress(text)

    # Save the compressed file using pickle
    write_results(FILE_NAME + '.pickle', compressed)

    # read the pickle
    pickle_file = read_pickle(FILE_NAME + '.pickle')

    # Decompress the pickle file
    decompressed = decompress(pickle_file)

    # print first 45 characters of decompressed file
    i = 0
    # Iterate over the string
    for element in decompressed:
        print(element, end='')
        if i > 45:
            break
        i += 1
    print("\n")
#end def main():


if __name__ == '__main__':
    main()