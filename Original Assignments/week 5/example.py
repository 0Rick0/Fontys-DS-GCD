#!/usr/bin/env python3
import mincemeat
import glob
import traceback
import sys
import operator


def mapfn(k, v: str):
    import string
    from stopwords import allStopWords
    stopwords = allStopWords.keys()
    trans = str.maketrans('', '', string.punctuation)
    for w in v.split():
        w = w.lower()
        w = w.translate(trans)
        if w in stopwords or len(w) <= 1:
            continue
        yield w, 1


def reducefn(k, vs):
    return sum(vs)
    # result = 0
    # for v in vs:
    #     result += v
    # return result


def read_file(filename):
    try:
        with open(filename, encoding='ISO-8859-1') as f:
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

    results = s.run_server(password="changeme")
    results = sorted(results.items(), key=operator.itemgetter(1), reverse=True)
    print(results)
    with open('sorted.txt', 'w') as f:
        f.write('\n'.join('%s\t%d' % result for result in results))


if __name__ == '__main__':
    main()
