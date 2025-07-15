
#include <cs50.h>
#include <stdio.h>

int printRow(int block);

int main(void)
{
    int height = 0;
    // getting height of pyramid from user
    do
    {
        height = get_int("what is the height of pyramid?\n");
        // prompting again for correct input
    }
    while (height < 1);
    // making pattern of pyramid
    for (int i = 1; i <= height; i++)
    {
        for (int j = 1; j <= height; j++)
        {
            if (j <= height - i)
                printf(" ");

            else
                printf("#");
        }
        // for next line
        printf("\n");
    }
}
