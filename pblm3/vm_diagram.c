#include <stdlib.h>
#include <stdio.h>
#include <string.h>
#include <stdint.h>
#include <sys/mman.h>

/*
 Reference : https://blog.holbertonschool.com/hack-the-virtual-memory-drawing-the-vm-diagram/
*/

int stack_function1(int i){
    if(i==3)
        return 0;
    int a = 3;
    printf("stack_function1 Address: %p\n",&a);
    stack_function1(i+1);
    printf("In function 1\n");
    return 0;
}
int main(int ac, char **av, char **env){

    static int var = 999;
    static int abc;
    /* examining the executable memory
    */
    printf("Main Function Address: %p\n",(void *)main);
    printf("Address of var: %p\n",&var);
    printf("Address of abc: %p\n",&abc); 
    // end

    /*
    examining stack position
    */
    stack_function1(0);
    //end

    /*
    examining the heap position
    */
    int *p1 = malloc(50);
    printf("Address allocated for p1: %p\n",p1);
    
    int *p2 = malloc(50);
    printf("Address allocated for p2: %p\n",p2);
    //end

    free(p1);
    free(p2);

    uint8_t * first = mmap(NULL,4096, PROT_READ|PROT_WRITE, MAP_PRIVATE|MAP_ANONYMOUS, -1, 0);
    uint8_t * second = mmap(NULL,4096, PROT_READ|PROT_WRITE, MAP_PRIVATE|MAP_ANONYMOUS, -1, 0);

    printf("Address allocated for first: %p\n",first);
    printf("Address allocated for second: %p\n",second);

    /*command line arguments*/
    printf("\n");
    printf("Address of the array of arguments: %p\n", (void *)av);
    printf("Addresses of the arguments:\n\t");
    for (int i = 0; i < ac; i++)
    {
        printf("[%s]:%p ", av[i], av[i]);
    }
    printf("\n");
    printf("Address of the array of environment variables: %p\n", (void *)env);
    printf("Address of the first environment variable: %p\n", (void *)(env[0]));
}