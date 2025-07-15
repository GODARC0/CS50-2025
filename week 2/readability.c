#include <cs50.h>
#include <ctype.h>
#include <math.h>
#include <stdio.h>
#include <string.h>

int main(void)
{
    // inputs
    string text = get_string("text:");
    int let = 0;
    int wrd = 1;
    int sent = 0;
    // loops to identify all the words letters and sentence

    for (int i = 0; i < strlen(text); i++)
    {
        if (isalpha(text[i]))
        {
            let++;
        }
        else if (text[i] == ' ')
        {
            wrd++;
        }
        else if (text[i] == '.' || text[i] == '?' || text[i] == '!')
        {
            sent++;
        }
    }
    // getting value for L and S for index
    float L = (float) let / (float) wrd * 100;
    float S = (float) sent / (float) wrd * 100;

    // getting grade from formula
    int index = round(0.0588 * L - 0.296 * S - 15.8);
    // printing grade
    if (index < 1)
    {
        printf("Before Grade 1\n");
    }
    else if (index > 16)
    {
        printf("Grade 16+\n");
    }
    else
    {
        printf("Grade %i\n", index);
    }
}