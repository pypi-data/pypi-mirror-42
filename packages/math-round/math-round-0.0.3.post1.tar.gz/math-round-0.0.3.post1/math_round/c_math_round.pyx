cpdef mround(number, ndigits=0):
    result = int(number * 10 ** ndigits + 0.5)/10**ndigits
    if ndigits:
        return result
    else:
        return int(result)