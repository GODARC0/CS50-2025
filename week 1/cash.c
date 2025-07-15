
#include <cs50.h>
#include <stdio.h>

int get_cents(void);
int calc_quarter(int cents);
int calc_dimes(int cents);
int calc_nickles(int cents);
int calc_pennies(int cents);

int main(void)
{ // getting input from user
    int cents = get_cents();

    // calculating no. of quarters
    int quarter = calc_quarter(cents);
    cents = cents - quarter * 25;

    // calculating no. of dimes
    int dimes = calc_dimes(cents);
    cents = cents - dimes * 10;

    // calculating no. of nickles
    int nickles = calc_nickles(cents);
    cents = cents - nickles * 5;

    // calculating no. of pennies
    int pennies = calc_pennies(cents);
    cents = cents - pennies;

    // total no. of coins
    int coins = quarter + dimes + nickles + pennies;
    printf("%i\n", coins);
}

int get_cents(void)
{
    int cents;
    do
    {
        cents = get_int("cents owed: ");
    }
    while (cents < 0);
    return cents;
}

int calc_quarter(int cents)
{
    int quart = 0;
    while (cents >= 25)
    {
        cents = cents - 25;
        quart++;
    }
    return quart;
}

int calc_dimes(int cents)
{
    int dimes = 0;
    while (cents >= 10)
    {
        cents = cents - 10;
        dimes++;
    }
    return dimes;
}

int calc_nickles(int cents)
{
    int nick = 0;
    while (cents >= 5)
    {
        cents = cents - 5;
        nick++;
    }
    return nick;
}

int calc_pennies(int cents)
{
    int penn = 0;
    while (cents >= 1)
    {
        cents = cents - 1;
        penn++;
    }
    return penn;
}
