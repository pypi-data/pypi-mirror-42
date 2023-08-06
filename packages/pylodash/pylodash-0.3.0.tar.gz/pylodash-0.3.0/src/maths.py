import math

def add(augend, addend):
    return augend + addend

def ceil(number, precision=0):
    multiplier = 10 ** precision
    return math.ceil(number * multiplier) / multiplier

def divide(dividend, divisor):
    return dividend / divisor

def floor(number, precision=0):
    multiplier = 10 ** precision
    return math.floor(number * multiplier) / multiplier

def max(array):
    if len(array) == 0:
        return None

    max = 0
    for item in array:
        if item > max:
            max = item

    return max

def mean(array):
    return sum(array) / len(array)

def min(array):
    if len(array) == 0:
        return None

    min = array[0]
    for item in array:
        if item < min:
            min = item

    return min

def multiply(multiplier, multiplicand):
    return multiplier * multiplicand

def substract(minuend, subtrahend):
    return minuend - subtrahend

def sum(array):
    result = 0
    for i in array:
        result += i

    return result

if __name__ == "__main__":
    print(sum([]))