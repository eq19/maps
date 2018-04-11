# prime-hexagon
The Prime Hexagon
![alt text](https://github.com/kaustubhcs/prime-hexagon/blob/master/poster/RISE%20Poster%20Prime%20Hexagon%202078%20(1)-1.jpg)

## Abstract


The distribution of integer prime numbers remains a mystery today. There has been no mathematical equation derived that explains which numbers will be prime. Ulam's Spiral and Primal Chaos Theory are just a few of the many attempts made in the past to unravel this mystery.

In this project, we leverage a novel approach to visualize prime numbers using overlapping hexagons that can bound all prime numbers. The Prime Hexagon is a mathematical structure developed by mathematician T. Gallion.  A Prime Hexagon is formed when integers are sequentially added to a field of tessellating equilateral triangles, where the path of the integers is changed whenever a prime number is encountered. Since prime numbers are never multiples of two or three, all numbers from "2" to infinity are confined within a 24-cell hexagon. 

We color-code the six hexagons, identifying patterns in key number sequences, including the Fibonacci sequence, powers of two and three, and power of pi. For the series of consecutive powers of pi, we have found that no two fall within the same six-cell hexagon. We have computed this for pi^32, which has less than a 1/400 chance of occurring randomly. 

We have used a distributed implementation of the CUDA Sieve and Hex Sieve algorithms to compute pi, enabling parallel execution on a GPU-based cluster. We use four NVIDIA V100 GPUs and four AMD EPYC 7551 CPUs, totaling 20,480 CUDA cores and 256 CPU cores, achieving a 9X speedup versus serial computation.


## Opportunity

CUDA function distributed across multiple GPU nodes sieves for primes, and writes relative location values for every 108th number to a 100-line file.
Files are sent to the hybrid1 node in the NUCAR server and all the values are shifted to line up with the previous file, finding the absolute location for each recorded number. 
Files are then sorted into file directory, where folder names correspond to the numbers stored in each file, as explained below. 
If user searches for a particular value, sieve function will be run with a lower bound of the nearest lesser indexed value, and an upper bound of the input. The absolute location/color of the input number can then be found.  

The numerical values are encoded in the file structure such that: 
The last 8 digits are removed, as they will all be ‘0’, as only every 108th number is stored
The next two digits correspond to the line in a file where the color value is located
The following two digits become the file name
Every next two digits becomes a directory name
In the event that a number is not long enough for the current file structure, ‘0’ will be padded onto the front of the number as to make it match
 
For example, the color value of 12345678987600000000 will be stored in 12/34/56/78/98.txt, line 76.

Files generated by the CUDA function and sent to the shift function on hybrid1 contain a "~" flag. A sample file name would be: 1234567898~.txt.
The shift function will remove the ‘~’ flag. A sample file name would be: 1234567898.txt
The sort function will create the directories if needed, and create a file in the corresponding directory, such that 1234567898.txt would become 12/34/56/78/98.txt


## Results
The use of our cluster meant we could parallelize the processes of both calculating prime numbers and sorting them in the sieves. The GPU cores caused a speedup of 9x and allowed for new options to be available in our storage and presentation. So far we have calculated up to 10^17 but plan to continue to higher numbers which will require the creation of a script to add integers greater than 128 bits. From his previous research, Tad has found that powers of Pi are significantly not random. Which is to say that the spin colors of theses powers were never the same consecutively. This is the behaviour that may link prime numbers to Pi.



## Impact
A better understanding of the distribution of prime numbers would be a major breakthrough in mathematics
A continued relationship with the powers of pi could indicate a connection to circular geometry
Other patterns can be analyzed to determine if they are related to the distribution of primes
The speed and scalability of the cluster allows Tad Gallion and other researchers to check values of numbers that are significantly higher than any individual computer could compute in a reasonable time constraint
The parallelization of the algorithm achieved a 9X speedup using CUDA GPU programming
Because the cluster is managed over the internet, new compute nodes can be added with minimal effort
Visualization tools enable researchers to explore the prime hexagon quickly and discover patterns that can be further analyzed
Understanding the pattern of prime numbers could have effects in cryptography
Many modern encryption algorithms depend on the factorization of very large primes which are hard to find
