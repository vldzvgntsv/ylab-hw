from itertools import combinations


def bananas(s):
    result = set()
    pattern = 'banana'
    for combination in combinations(enumerate(s), 6):
        word = ['-' for _ in range(len(s))]
        j = 0
        for i, letter in combination:
            if letter == pattern[j]:
                word[i] = letter
                j += 1
            else:
                break
        if j == len(pattern):
            result.add(''.join(word))
    return result


assert bananas("banann") == set()
assert bananas("banana") == {"banana"}
assert bananas("bbananana") == {"b-an--ana", "-banana--", "-b--anana", "b-a--nana", "-banan--a",
                     "b-ana--na", "b---anana", "-bana--na", "-ba--nana", "b-anan--a",
                     "-ban--ana", "b-anana--"}
assert bananas("bananaaa") == {"banan-a-", "banana--", "banan--a"}
assert bananas("bananana") == {"ban--ana", "ba--nana", "bana--na", "b--anana", "banana--", "banan--a"}

s = input()
print(bananas(s))
