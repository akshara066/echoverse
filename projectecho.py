# ------------------------------------------------------
# Echo Verse Program
# Author: Example Program
# This program takes a line of verse from the user
# and prints it back in an "echo style".
# ------------------------------------------------------

# Function 1: Echo each word separately
def word_by_word_echo(line):
    echo_text = ""   # store echo result
    words = line.split()   # split into words
    for word in words:
        echo_text += word + "\n"          # print original word
        echo_text += word.lower() + "...\n"  # print echo
    return echo_text


# Function 2: Shrink the line step by step
def shrinking_echo(line):
    echo_text = ""
    while len(line) > 0:
        echo_text += line + "\n"
        line = line[:-1]   # remove last character
    return echo_text


# Main program starts here
print("====================================")
print("       E C H O   V E R S E ")
print("====================================")

# Step 1: Input from user
verse = input("Enter a line of verse: ")

# Step 2: Show menu to user
print("\nChoose the type of echo effect:")
print("1. Word by Word Echo")
print("2. Shrinking Line Echo")

choice = input("Enter your choice (1 or 2): ")

# Step 3: Display output based on choice
print("\n----------- Echo Output -----------\n")

if choice == "1":
    print(word_by_word_echo(verse))
elif choice == "2":
    print(shrinking_echo(verse))
else:
    print("Invalid choice! Showing Word by Word Echo by default:\n")
    print(word_by_word_echo(verse))

print("----------- End of Program -----------")