
#include <stdio.h>
#include <stdlib.h>
#include <math.h>

int main(int argc, char *argv[]){
    if (argc != 2) {
        fprintf(stderr, "Usage: %s <number>\n", argv[0]);
        return 1;
    }
    unsigned long long n = strtoull(argv[1], NULL, 10);
    unsigned long long orig = n;
    printf("Prime factors of %llu: ", orig);
    
    // Remove factors of 2.
    while(n % 2 == 0) {
        printf("2 ");
        n /= 2;
    }
    // Check odd divisors.
    for(unsigned long long i = 3; i <= sqrt(n); i += 2){
        while(n % i == 0) {
            printf("%llu ", i);
            n /= i;
        }
    }
    if(n > 2)
        printf("%llu ", n);
    printf("\n");
    return 0;
}