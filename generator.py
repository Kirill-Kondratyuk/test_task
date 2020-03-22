from itertools import product

chars = ['a', 'b', 'c', 'd', 'e', 'f',
         'g', 'h', 'i', 'g', 'k', 'l',
         'm', 'n', 'o', 'p', 'q', 'r',
         's', 't', 'u', 'v', 'w', 'x',
         'y', 'z']

words = []

for i in range(1, 4):
    for comb in product(chars, repeat=i):
        words.append(''.join(comb))
        print(''.join(comb))

for word in words:
    string = word
    if word != words[-1]:
        string += '\n'
    with open('dict.txt', 'a') as f:
        f.write(string)


wordlist = words
sublist_length = len(wordlist)//10
lists = [wordlist[x:x+sublist_length] for x in range(0, len(wordlist), sublist_length)]
