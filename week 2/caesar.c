#include <cs50.h>
#include <ctype.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

int main(int argc, string argv[])
{
    // exiting code when input format is wrong
    if (argc != 2)
    {
        printf("Usage: ./caesar key\n");
        return 1;
    }
    // checking if all the input are integers
    for (int i = 0; i < strlen(argv[1]); i++)
    {
        if (!isdigit(argv[1][i]))
        {
            printf("Usage: ./caesar key\n");
            return 1;
        }
    }
    // assigning the integer as a key
    int con = atoi(argv[1]);
    // getting input from  user
    string plaintext = get_string("plain text: ");
    // printing the cipher text
    printf("ciphertext: ");
    // converting plain text into cipher text
    for (int j = 0; j < strlen(plaintext); j++)
    {
        if (isupper(plaintext[j]))
        {

            printf("%c", (plaintext[j] - 65 + con) % 26 + 65);
        }
        else if (islower(plaintext[j]))
        {

            printf("%c", (plaintext[j] - 97 + con) % 26 + 97);
        }
        else
        {
            printf("%c", plaintext[j]);
        }
    }
    // to move cursor to next line
    printf("\n");
}