
# global variables
change = 0
coin = 0

# prompting user until getting the correct input
while change <= 0:
    try:
        change = float(input("change : "))
    except ValueError:
        print("give a valid value")

# defining function to count coins


def cashier(toreduce):
    global change
    global coin
    while change >= toreduce:

        change = round(change - toreduce, 10)
        coin += 1


# calling function
cashier(0.25)
cashier(0.10)
cashier(0.05)
cashier(0.01)

print("coin : ", coin)