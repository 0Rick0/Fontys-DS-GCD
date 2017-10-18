# Example of Map Reduce
In this document an example will be given for map reduce.

To run the example, run `map_reduce.sh` on a *NIX compatible system.

# The functions
The map function is responsible for the cleaning and mapping of the data.

It splits it into words, ignores common words like it and the etc, removes punctuation and makes it lowercase.

Afterwards it yields (returns one value and waits for the next to be requested) the word in combination with 1.
```python
def mapfn(k, v: str):
    # imports
    import string
    import sys
    sys.path.insert(0, './Portfolio/')
    from MapReduce_code import allStopWords as stopwords
    
    # Remove punctuation
    trans = str.maketrans('', '', string.punctuation)
    for w in v.split():
        # clean input and return and yeild an countable tuple
        w = w.lower()
        w = w.translate(trans)
        if w in stopwords or len(w) <= 1:
            continue
        yield w, 1
```

The reduce function will sum all values per word. This means it will add all those ones.

This concludes to the word count.
```python
def reducefn(k, vs):
    # sum all values
    return sum(vs)
```

# Performance
You can see how this application can scale using multiple processes.
When running with 2 worker processes, it runs for about 28 seconds for the large dataset.
When running with 8 workers, this decreases to 17 seconds. A 10 seconds difference!

This shows the greatest strength of map-reduce, it scales really well to multiple processors.
You can basically keep adding more workers to increase the processing speed.

I can't go above eight because I only have 8 threads on my CPU and the performance would start to decrease due to timesharing.

System specs:
 - i7-7700HQ@2.80GHz
 - 16GB DDR4@2400MHz