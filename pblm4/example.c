#include <stdio.h>
#include <unistd.h>
#include <stdlib.h>
#include<sys/wait.h> 

int main(int argc, char *argv[])
{
    pid_t cpid;
    char *args[] = {"Hello", "C", "Programming", NULL};
    if(fork() == 0){
        // child process
	//char ch = getchar();
	printf("PID of child before child exec = %d\n", getpid());  
	execv("./hello", args);
        printf("Child program");
        cpid = wait(NULL);
        char ch = getchar();
    }else{
        // parent process
        printf("parent program");
        printf("PID of example.c = %d\n", getpid());  
        cpid = wait(NULL);
    }
    printf("Back to example.c");
    return 0;
}
