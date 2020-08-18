import numpy as np

def in_range(Points, Ranges):
    results = np.zeros_like(Ranges[:,0])
    for i, Range in enumerate(Ranges):
        count = 0
        for j, Point in enumerate(Points[count:]):
            if Point in range(Range[0], Range[-1]):
                results[i] = 1
                count = count+1
                break
            if j == len(Points) - 1:
                results[i] = 0
    return results

def true_positive_rate(results):
    return (np.sum(results)/np.size(results))*100

def false_positive_rate(results):
    return (1-np.sum(results)/np.size(results))*100
