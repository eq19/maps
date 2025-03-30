# prime-hexagon

The Prime Hexagon is a simple mathematical structure that appears when integers are sequentially added to a field of tessellating equilateral triangles, provided the path of the integers is altered each time a prime number appears.

This code computes prime numbers, their positons in the prime hexagon, the polarity of the number, and the prime hexagon's overall rotation.
For more information go to hexspin.com.  Youtube:https://www.youtube.com/watch?v=fQL4KRH3wUQ

## Running

Compute the first set of output values

    python ./primespin.py --nvalues=10000000 --chunks 100

Resume a computation given a saved file:

    python ./primespin.py --startfile ./output-00000000000000107000-00000000000000108000.npz --chunks 100


##  Computing a prime number's position on the prime hexagon

TODO

## Command Line Help 

Run with the --help argument to see the help file.

```bash
python primespin.py --help
usage: primespin.py [-h] [--infile INFILE] [--viewvalues VIEWVALUES]
                    [--find FIND] [-c] [--dir DIR] [--basename BASENAME]
                    [--logfile LOGFILE] [--verbose VERBOSE] [--save-text]
                    [--save-binary] [--use-cython] [--no-use-cython]
                    [--nvalues NVALUES] [--skip SKIP] [--chunks CHUNKS]

Prime Spin Hexagons

optional arguments:
  -h, --help            show this help message and exit
  --infile INFILE       Input file to start processing chunks
  --viewvalues VIEWVALUES
                        Values to view in the file as a python slice, e.g.
                        1:100:
  --find FIND           Find values in files
  -c, --compress        flag to indicate whether or not to compress output
                        files
  --dir DIR             Directory to read/write files to
  --basename BASENAME   Basename of files to read and write
  --logfile LOGFILE     Save messagse to this log file
  --verbose VERBOSE     Print messages to the terminal
  --save-text           Flag to save text files
  --save-binary         Flag to save binary files
  --use-cython          Flag to use cython implementation if available
  --no-use-cython       Flag to not use cython implementation
  --nvalues NVALUES     number of values to process in a chunk
  --skip SKIP           number of values to skip in printing output
  --chunks CHUNKS       number of chunks to process
```

Here are a few sample command lines:

Generate 1000 files of 1B values each

    primespin.py --nvalues=1000000000 --chunks=1000 

or

     python3 primespin.py --nvalues=$(echo 10,000,000,000 | tr -d ,) --chunks=10000 --skip=0 --logfile run.log

Same thing but write out only every 1Mth value:

    primespin.py --nvalues=10000000000 --chunks=10 --skip=0

Now resume a computation starting at the specified file:

    primespin.py --chunks=10 --skip=0 --infile output-00000000009000000000-00000000010000000000.npz

### Skip argument

It turns out we don't always want to print out all the values we are computing. In fact, if we just want to be able to resume computations, we only need the last set of values in a range stored.

Use --skip=0 to save only a single value - the last set of values in the range.

--skip=1 is also valid to print out all values in the range.

But any other value is not going to work if you want to use chunks.

### Print Values from the NPZ files

Print some values from the binary .npz files

    primespin.py --viewvalues=:: --infile output-00000000009000000000-00000000010000000000.npz


Note viewvalues is evaluated as an [extended Python
slice](https://docs.python.org/2.3/whatsnew/section-slices.html). That is, the values are

   start:stop:step

Also any of those values can actually be negative values to indicate starting from the other end in the case of start and stop. If you make step negative it counts backward.

So let's print the last value in this file:

    primespin.py --viewvalues=-1:: --infile output-00000000009000000000-00000000010000000000.npz

### Find values in the NPZ Files

the --find argument takes a comma separated list of values. The program looks through the output directory for all files. The program searches for numbers and prints the surrounding prime hexagon values.


```bash
python primespin.py --find 2004698834,2005554573,8999550398
2015-11-30 00:32:46,658 - prime_hexagon - INFO - using numpy primehexagon implementation
2015-11-30 00:32:46,658 - prime_hexagon - INFO - looking for files matching pattern output/output-[0-9]*-[0-9]*.npz
2015-11-30 00:32:46,659 - prime_hexagon - INFO - found 10 files
(2004484351, 1, -1, 1145)
(2004698833, 1, -1, 1126)
----> 2004698834 <----
(2009838559, 3, -1, 1113)
(2010052483, 5, -1, 1115)

(2005341167, 0, 1, 1126)
(2005554553, 1, -1, 1146)
----> 2005554573 <----
(2011554973, 5, -1, 1131)
(2011769437, 1, -1, 1118)

(8999319293, 4, 1, 2052)
(8999550397, 1, -1, 2052)
----> 8999550398 <----
```

## Tests

the tests/ directory has some tests. To run them, you'll need to

```bash
pip install py.test
PYTHONPATH=. py.test -v --debug tests/test_prime_hex.py 
```
