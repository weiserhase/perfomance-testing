#include <stdio.h>
#include <stdlib.h>

int main(int argc, char *argv[]) {
    if (argc != 2) {
        fprintf(stderr, "Usage: %s <number>\n", argv[0]);
        return 1;
    }
    unsigned long long n = strtoull(argv[1], NULL, 10);
    unsigned long long orig = n;
    printf("Prime factors of %llu: ", orig);
    for (unsigned long long i = 2; i <= n; i++) {
        while (n % i == 0) {
            printf("%llu ", i);
            n /= i;
        }
    }
    printf("\n");
    return 0;
}