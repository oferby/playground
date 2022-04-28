# https://www.youtube.com/watch?v=PIeiiceWe_w
phoneNumber = "3662277"
words = ["foo", "bar", "baz", "foobar", "emo", "cap", "car", "cat", "bqs"]
char_map = {'a': 2, 'b': 2, 'c': 2,
            'd': 3, 'e': 3, 'f': 3,
            'g': 4, 'h': 4, 'i': 4,
            'j': 5, 'k': 5, 'l': 5,
            'm': 6, 'n': 6, 'o': 6,
            'p': 7, 'q': 7, 'r': 7, 's': 7,
            't': 8, 'u': 8, 'v': 8,
            'w': 9, 'x': 9, 'y': 9, 'z': 9}

match_words = []


def translate(chars):
    numbers = []
    for char in chars:
        numbers.append(char_map[char])
    return numbers


phone_len = len(phoneNumber)
for word in words:
    numbers = translate(word)
    word_len = len(numbers)
    for i in range(phone_len - word_len + 1):
        match = True
        k = i
        for j in range(word_len):
            if numbers[j] != int(phoneNumber[k]):
                match = False
                break
            k += 1
        if match:
            match_words.append(word)
            break

print(match_words)
