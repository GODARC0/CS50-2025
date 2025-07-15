
#include <cs50.h>
#include <stdio.h>
#include <string.h>

// assigning all the points for each letter
int points[] = {1, 3, 3, 2, 1, 4, 2, 4, 1, 8, 5, 1, 3, 1, 1, 3, 10, 1, 1, 1, 1, 4, 4, 8, 4, 10};
int scores(string play);
int main(void)
{
    // getting input from user
    string play1 = get_string("player1: ");
    string play2 = get_string("player2: ");

    // calculating the score
    int scr1 = scores(play1);
    int scr2 = scores(play2);
    // comparing the scores and declaring winner
    if (scr1 > scr2)
    {
        printf("player 1 wins! \n");
    }
    else if (scr1 < scr2)
    {
        printf("player 2 wins! \n");
    }
    else
    {
        printf("tie \n");
    }
}

int scores(string play)
{
    int score = 0;
    // for loop to go through every letter of word
    for (int i = 0; i < strlen(play); i++)
    {
        // for upper case letters
        if (play[i] >= 65 && play[i] <= 90)
        {
            score = score + points[play[i] - 65];
        }
        // for lower case letter
        if (play[i] >= 97 && play[i] <= 122)
        {
            score = score + points[play[i] - 97];
        }
    }
    return score;
}
