def remove_duplicates(list1):
    """
    Eliminate duplicates in a sorted list.

    Returns a new sorted list with the same elements in list1, but with no duplicates.

    Iterative.
    """
    result_list = []
    if len(list1) == 0:
        return []
    else:
        result_list.append(list1[0])
        for item in list1:       
            if result_list[len(result_list)-1] < item:
                result_list.append(item)  
        return result_list

def intersect(list1, list2):
    """
    Compute the intersection of two sorted lists.

    Returns a new sorted list containing only elements that are in
    both list1 and list2.

    Iterative.
    """
    result_list = []
    for item in list1:
        if item in list2:
            result_list.append(item)

    return result_list

def merge(list1, list2):
    """
    Merge two sorted lists.

    Returns a new sorted list containing all of the elements that
    are in either list1 and list2.

    Iterative. Uses next function.
    """
    result_list = []
    for item1 in list1:
        result_list.append(item1)
    for item2 in list2:
        result_list.append(item2)
    result_list = merge_sort(result_list)
    return result_list
                
def merge_sort(list1):
    """
    Sort the elements of list1.

    Return a new sorted list with the same elements as list1.

    Recursive.
    """
    if list1 == []:
        return list1
    else:
        pivot = list1[0]
        before = [item for item in list1 if item < pivot]
        pivots = [item for item in list1 if item == pivot]
        after = [item for item in list1 if item > pivot]
        return merge_sort(before) + pivots + merge_sort(after)

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
