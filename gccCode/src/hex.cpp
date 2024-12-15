#include <iostream>
#include <inttypes.h>
#include <omp.h>
#include <ctime>
#include <sys/timeb.h>
#include <stdint.h>
#include <math.h>                   // pow()
#include <cuda_runtime.h>           // cudaFreeHost()
#include "CUDASieve/cudasieve.hpp"  // CudaSieve::getHostPrimes()

#define billion 1000000000

unsigned char color_name [] = {'b', 'p', 'r', 'y', 'g', 'c'};
//                            { 0 ,  1 ,  2 ,  3 ,  4 ,  5 }

// Timing functions
double CLOCK() {
  struct timespec t;
  clock_gettime(CLOCK_MONOTONIC,  &t);
  return (t.tv_sec * 1000)+(t.tv_nsec*1e-6);
}

int shift(int prev, int curr) {
  if(prev % 2 == 0) {
    return (prev + curr) % 6;
  }
  else {
    return (prev - curr + 6) % 6;
  }
}

// Input: START START_COLOR END
// Example: 0 4 100000000000
// Output: END_COLOR

/*
        1 B     = red
       10 B     = yellow
      100 B     = purple
    1 000 B     = green
    2 000 B     = purple
    3 000 B     = cyan
   10 000 B     = yellow
  100 000 B     = blue
1 000 000 B     = yellow
*/

int main(int argc, char **argv) {

    if (argc != 4 && argc != 5){
        printf ("ERROR: Incorrect number of arguments!\nExiting...\n");
        return -1;
    }
    
    char *tmp;
    
    unsigned long int startpoint = strtoul(argv[1], &tmp, 10);
    unsigned char start_color = atoi(argv[2]);
    unsigned long int endpoint = strtoul(argv[3], &tmp, 10);
    // set gpuNum with default of 0
    int gpuNum = argc == 5 ? atoi(argv[4]) : 0;
    
    if (endpoint <= startpoint){
        printf ("ERROR: Endpoint can't be after startpoint!\nExiting...\n");
        return -1;
    }
    
    if (endpoint <= 128){
        //printf ("ERROR: FIXME: CudaSieve can't receive number smaller than 128, we need to hard-code it.\n");
        unsigned char color = start_color;
        for(uint64_t i = startpoint; i < endpoint; i++) {
            int flag = 0;
            for(int j = 2; j <= i/2; ++j) {
                // condition for non prime number
                if(i%j==0) {
                    flag = 1;
                    break;
                }
            }

            if (flag == 0) {
                uint64_t currentModulo = i%6;
                if (i > 4){
                    // TODO Simplify this
                    if(currentModulo == 1) {
                        if(color % 2 == 0) {
                            color = (color + 5) % 6;
                        } else {
                            color = (color + 1) % 6;
                        }
                    } else { // current modulo is equal to 5
                        if(color % 2 == 0) {
                            color = (color + 1) % 6;
                        }
                        else {
                            color = (color + 5) % 6;
                        }
                    }
                }
            }
        }
        printf("%d\n", color);
        return 0;
    }
    
    unsigned int sizeInBillions = ceil((double)(endpoint-startpoint)/billion); 
    
    unsigned char* colors = new unsigned char [sizeInBillions+1]; // To include the startpoint color

    // Setting starting color
    colors[0] = start_color;
    
    
    // Setting up parallelism
    omp_set_num_threads(5);

    #pragma omp parallel for
    for (unsigned long int j = 0; j < sizeInBillions; j++){
        
        unsigned long int bottom = startpoint+j*pow(10,9);
        unsigned long int top    = bottom + pow(10,9);
        
        if (top > endpoint) top = endpoint;
        
        size_t   len;

        uint64_t * primes = CudaSieve::getHostPrimes(bottom, top, len, gpuNum);

        unsigned char color = 0;
        for(uint64_t i = 0; i < len; i++){
          uint64_t currentModulo = primes[i]%6;
          if (primes[i] > 4){
            // TODO Simplify this
            if(currentModulo == 1) {
              if(color % 2 == 0) {
                color = (color + 5) % 6;
              }
              else {
                color = (color + 1) % 6;
              }
            }
            else { // current modulo is equal to 5
              if(color % 2 == 0) {
                color = (color + 1) % 6;
              }
              else {
                color = (color + 5) % 6;
              }
            }
          }
        }
        colors[j+1] = color;

        // must be freed with this call b/c page-locked memory is used.
        cudaFreeHost(primes);
    }
    
    // Reset device
    cudaDeviceReset();

    for(uint64_t i = 0; i < sizeInBillions; i++) {
        colors[i+1] = shift(colors[i], colors[i+1]);
    }

    printf("%d\n", colors[sizeInBillions]);
    //printf("%c\n", color_name[colors[sizeInBillions]]);

    delete colors;
    return 0;
}
