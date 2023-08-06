def chunk(array, size=1):
    result = []

    if (size >= len(array)):
        result.append(array)
    else:
        result = append_list(array, size, result)

    return result

def append_list(array, size, result):
    if len(array) == 0:
        return result
    else:
        temp = array[0: size]
        result.append(temp)
        new_array = list(set(array) - set(temp))

        append_list(new_array, size, result)

    return result

def compact(array):
    return [i for i in array if i not in [False, None, '']]

def difference(array, values):
    return list(set(array) - set(values))

def drop(array, number=1):
    return array[number: len(array)]

def dropRight(array, number=1):
    if len(array) < number:
        return []
    return array[0: len(array) - number]

def fill(array, value, start=0, end=None):
    if end is None:
        end = len(array)

    for index, _ in enumerate(array):
        if index >= start and index < end:
            array[index] = value

    return array

def indexOf(array, value, fromIndex=0):
    result = None
    for index, item in enumerate(array):
        if index >= fromIndex and item == value:
            result = index
            break

    return result

def initial(array):
    return [item for index, item in enumerate(array) if index != len(array) - 1]

def pull(array, *args):
    return [i for i in array if i not in args]

if __name__ == '__main__':
    print(pull(['a', 'b', 'c', 'a', 'b', 'c'], 'a', 'c'))