#include <stdio.h>
#include <unistd.h>
#include <stdlib.h>
#include<sys/wait.h> 

int main(int argc, char *argv[])
{
    pid_t cpid;
    printf("We are in Hello.c\n");
    printf("PID of hello.c = %d\n", getpid());
    cpid = wait(NULL);
    char ch = getchar();
    return 0;
}
