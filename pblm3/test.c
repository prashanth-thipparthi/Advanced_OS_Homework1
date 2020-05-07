#include <stdlib.h>
#include <stdio.h>
#include <string.h>
#include <stdint.h>
#include <sys/mman.h>

int main(){
    int *p1 = malloc(100);
    printf("address of p1 = %p", p1);
    return 0;
}
