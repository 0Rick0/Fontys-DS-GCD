#!/usr/bin/env python3
import mincemeat
import glob
import traceback
import sys
import operator


allStopWords = ['about', 'above', 'after', 'again', 'against', 'all', 'am', 'an', 'and', 'any', 'are', 'arent', 'as', 'at', 'be', 'because', 'been', 'before', 'being', 'below', 'between', 'both', 'but', 'by', 'cant', 'cannot', 'could', 'couldnt', 'did', 'didnt', 'do', 'does', 'doesnt', 'doing', 'dont', 'down', 'during', 'each', 'few', 'for', 'from', 'further', 'had', 'hadnt', 'has', 'hasnt', 'have', 'havent', 'having', 'he', 'hed', 'hell', 'hes', 'her', 'here', 'heres', 'hers', 'herself', 'him', 'himself', 'his', 'how', 'hows', 'i', 'id', 'ill', 'im', 'ive', 'if', 'in', 'into', 'is', 'isnt', 'it', 'its', 'itself', 'lets', 'me', 'more', 'most', 'mustnt', 'my', 'myself', 'no', 'nor', 'not', 'of', 'off', 'on', 'once', 'only', 'or', 'other', 'ought', 'our', 'ours ', 'ourselves', 'out', 'over', 'own', 'same', 'shant', 'she', 'shed', 'shell', 'shes', 'should', 'shouldnt', 'so', 'some', 'such', 'than', 'that', 'thats', 'the', 'their', 'theirs', 'them', 'themselves', 'then', 'there', 'theres', 'these', 'they', 'theyd', 'theyll', 'theyre', 'theyve', 'this', 'those', 'through', 'to', 'too', 'under', 'until', 'up', 'very', 'was', 'wasnt', 'we', 'wed', 'well', 'were', 'weve', 'werent', 'what', 'whats', 'when', 'whens', 'where', 'wheres', 'which', 'while', 'who', 'whos', 'whom', 'why', 'whys', 'with', 'wont', 'would', 'wouldnt', 'you', 'youd', 'youll', 'youre', 'youve', 'your', 'yours', 'yourself', 'yourselves']


def mapfn(k, v: str):
    import string
    import sys
    sys.path.insert(0, './Portfolio/')
    from MapReduce_code import allStopWords as stopwords
    trans = str.maketrans('', '', string.punctuation)
    for w in v.split():
        w = w.lower()
        w = w.translate(trans)
        if w in stopwords or len(w) <= 1:
            continue
        yield w, 1


def reducefn(k, vs):
    return sum(vs)


def read_file(filename):
    try:
        with open(filename, errors='ignore') as f:
            return f.read()
    except (IOError, UnicodeDecodeError):
        sys.stderr.write(filename + '\n')
        traceback.print_exc()
        return None


def read_all_files(small=True) -> tuple:
    if small:
        files = glob.glob('Gutenberg/Gutenberg Small/*.*')
    else:
        files = glob.glob('Gutenberg/Gutenberg SF/**.txt')
        files += glob.glob('Gutenberg/Gutenberg SF/**.htm')

    for file in files:
        yield file, read_file(file)


def main():
    s = mincemeat.Server()

    data = {f: d for f, d in read_all_files(False)}
    # print(data.keys())

    # The data source can be any dictionary-like object
    s.datasource = data
    s.mapfn = mapfn
    s.reducefn = reducefn

    print("Ready!")

    results = s.run_server(password="changeme")
    results = sorted(results.items(), key=operator.itemgetter(1), reverse=True)
    print("Top 20 results:")
    print(results[:20])

    print("All results in sorted.txt in TSV format")
    with open('sorted.txt', 'w') as f:
        f.write('\n'.join('%s\t%d' % result for result in results))


if __name__ == '__main__':
    main()
