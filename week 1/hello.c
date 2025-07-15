#include <cs50.h>
//
#include <stdio.h>
int main(void)
{
    // greets the user
    string name = get_string("what is your good name?");

    printf("hello, %s\n", name);
}