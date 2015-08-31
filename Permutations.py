def permutations(word):
    """
    Generate all strings that can be composed from the letters in word
    in any order.

    Returns a list of all strings that can be formed from the letters
    in word.

    >>>permutations('12')
    >>>['', '1', '2', '12', '21']
    """
    if len(word) == 0:
        return ['']
    if len(word) == 1:
        return ['', word]
    result = []
    
    rest_strings = permutations(word[1:])        
    for string in rest_strings:
        result.append(string)
        for ind in range(0, len(string)+1):
            result.append(string[:ind] + word[0] + string[ind:])
    return result
