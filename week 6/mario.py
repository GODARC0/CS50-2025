height = 0
# getting user input
while height < 1 or height > 8:
    try:
        height = int(input("Height : "))  # prompting for input until it is in required range
    except ValueError:
        print("height must be an int")  # prompting invalid input
# printing required output
for i in range(height):
    print(" " * (height - 1 - i), end="")
    print("#" * (i + 1))