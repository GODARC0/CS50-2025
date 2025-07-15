a = 1
l = 0  # assigning variables
s = 0
# getting user input
text = (input("text : "))

# designating all the components of readability
for char in text:
    if (char == ' '):
        a += 1

    elif (char == '.' or char == '?' or char == '!'):
        s += 1

    elif (char.isalpha()):
        l += 1

# formula for finding grade
index = round(0.0588 * l/a * 100 - 0.296 * s/a * 100 - 15.8)

# getting output
if (index < 1):
    print("Before Grade 1")

elif (index >= 16):
    print("Grade 16+")

else:
    print("Grade", index)