
#include <stdio.h>
#include <stdlib.h>
#include <math.h>
#include <time.h>
unsigned long long gcd(unsigned long long a, unsigned long long b) {
    while(b != 0) {
        unsigned long long t = b;
        b = a % b;
        a = t;
    }
    return a;
}

unsigned long long f(unsigned long long x, unsigned long long c, unsigned long long mod) {
    return ((x * x) % mod + c) % mod;
}

unsigned long long pollard_rho(unsigned long long n) {
    if(n % 2 == 0) return 2;
    unsigned long long x = rand() % n;
    unsigned long long y = x;
    unsigned long long c = rand() % n;
    unsigned long long d = 1;
    while(d == 1) {
        x = f(x, c, n);
        y = f(f(y, c, n), c, n);
        d = gcd((x > y) ? x - y : y - x, n);
        if(d == n) return pollard_rho(n);
    }
    return d;
}

void factorize(unsigned long long n) {
    if(n == 1) return;
    // Check for primality (naively) for small n.
    int isPrime = 1;
    for(unsigned long long i = 2; i <= sqrt(n); i++){
        if(n % i == 0) { isPrime = 0; break; }
    }
    if(isPrime) {
        printf("%llu ", n);
        return;
    }
    unsigned long long divisor = pollard_rho(n);
    factorize(divisor);
    factorize(n / divisor);
}
int main(int argc, char *argv[]){
    if(argc != 2){
        fprintf(stderr, "Usage: %s <number>\n", argv[0]);
        return 1;
    }
    srand(time(NULL));
    unsigned long long n = strtoull(argv[1], NULL, 10);
    printf("Prime factors of %llu: ", n);
    
    clock_t begin = clock();

    factorize(n);
    clock_t end = clock();
    double ts = (double)(end-begin) / CLOCKS_PER_SEC; 
    // print("%f", ts);
    printf("%f\n", ts);
    printf("\n");
    return 0;
}