import numpy as np

def chunks(l, n):
    for i in range(0, len(l), n):
        yield l[i:i+n]

def freedson_cut(val):
    if val < 100:
        return "sedentary"
    elif val < 1951:
        return "light"
    elif val < 5274:
        return "moderate"
    else:
        return "vigourous"

# Input : Second vertical counts
# Output : Second activity level estimation

def freedson(counts):
    minute_est = [freedson_cut(sum(x)) for x in chunks(counts, 60)]
    second_est = []
    [second_est.extend([x] * 60) for x in minute_est]
    return np.array(second_est)

def sasaki_cut(val):
    if val < 2690:
        return "light"
    elif val < 6166:
        return "moderate"
    elif val < 9642:
        return "vigourous"
    else:
        return "very vigourous"

# Input : Second vertical counts
# Output : Second activity level estimation

def sasaki(counts):
    minute_est = [sasaki_cut(sum(x)) for x in chunks(counts, 60)]
    second_est = []
    [second_est.extend([x] * 60) for x in minute_est]
    return np.array(second_est)

def nhanes_cut(val):
    if val < 100:
        return "sedentary"
    elif val < 2019:
        return "light"
    elif val < 5998:
        return "moderate"
    else:
        return "vigourous"

# Input : Second vertical counts
# Output : Second activity level estimation

def nhanes(counts):
    minute_est = [nhanes_cut(sum(x)) for x in chunks(counts, 60)]
    second_est = []
    [second_est.extend([x] * 60) for x in minute_est]
    return np.array(second_est)
    