#! /usr/bin/python3
vowel_count = 0
consonsnts_count = 0
name_list = ["VaIBHa", "ViJaY", "VIDHuN"]
VOWEL = ["A", "E", "I", "O", "U"]
for name in name_list:
    vowel_count = 0
    consonsnts_count = 0
    for letter in name:
        if letter.upper() in VOWEL:
            vowel_count = vowel_count + 1
    print("The Number of Vowel in", name, "is:", vowel_count) 
for name in name_list:
    vowel_count = 0
    consonsnts_count = 0
    for letter in name:
        if letter.upper() not in VOWEL:
            consonsnts_count = consonsnts_count + 1
    print("The Number of Consonants in", name, "is:", consonsnts_count)
