"""
Tiny app to check if a string has properly closed brakets or not.
"""

sample11 = "({[]})"
sample12 = "({}[])"
sample13 = "({})[]"
sample14 = "(){}[]"
sample21 = "({}[)]"
sample22 = "({}([]"

brakets = [["(",")"],["{","}"],["[","]"]]

def determine_opening_braket_type(opening_braket):
    """
    returns closing braket of the same type as starting braket from input
    """
    for b in brakets:
        if opening_braket == b[0]:
            return b[1]
        
def determine_closing_braket_type(closing_braket):
    """
    returns closing braket of the same type as starting braket from input
    """
    for b in brakets:
        if closing_braket == b[1]:
            return b[0]        

def get_blocks(test):
    queue = []
    for ind in range(len(test)):
        if determine_opening_braket_type(test[ind]) is not None:
            queue.append(test[ind])
        elif determine_closing_braket_type(test[ind]) is not None and determine_closing_braket_type(test[ind]) == queue[-1]:
            queue.remove(determine_closing_braket_type(test[ind]))
    return queue
    
def check(test):
    if len(get_blocks(test)) == 0:
        return "Valid"
    else:
        return "Invalid"

print (check(sample11))
print (check(sample12))
print (check(sample13))
print (check(sample14))
print (check(sample21))   