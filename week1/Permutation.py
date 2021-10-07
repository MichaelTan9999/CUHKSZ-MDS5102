from copy import deepcopy

def permutate(candidates):
    if len(candidates) == 1:
        return [candidates]
    else:
        answers = []
        for i in candidates:
            others = deepcopy(candidates)
            others.remove(i)
            # print(others)
            for subque in permutate(others):
                subque.insert(0, i)
                answers.append(subque)
        return answers
    

if __name__ == '__main__':
    candidates = [int(i) for i in input('Enter some numbers: ').split()]
    print(candidates)
    print(permutate(candidates))

