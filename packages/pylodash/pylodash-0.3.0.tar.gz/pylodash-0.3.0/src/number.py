from random import randint, uniform

def clamp(number, lower, upper):
    if check_clamp(number, lower, upper):
        return number
    if check_clamp(lower, number, upper):
        return lower
    if check_clamp(upper, number, lower):
        return upper

def check_clamp(a, b, c):
    return is_between(b, a, c) or is_between(c, a, b)

def is_between(a, b, c):
    return a <= b <= c

def inRange(number, start, end=None):
    if (end == None):
        end = start
        start = 0

    return baseInRange(number, start, end)

def baseInRange(number, start, end):
    return number >= min(start, end) and number < max(start, end)

def random(lower=0, upper=1, floating=False):
    floating = (isinstance(lower, float) or isinstance(upper, float) or floating is True or upper is True)
    if upper < lower:
        upper, lower = lower, upper

    if floating:
        rnd = uniform(lower, upper)
    else:
        rnd = randint(lower, upper)

    return rnd

if __name__ == "__main__":
    print(random(5, True))