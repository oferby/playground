# You just need to take string input from stdin and print the string in which all
# whitespaces have been stripped from the end of the string.

text = input()
text_len = len(text)

# run from the end to start until we hit none space char
for i in range(text_len - 1, -1, -1):
    if text[i] != ' ':
        print(text[0:i+1])
        break
