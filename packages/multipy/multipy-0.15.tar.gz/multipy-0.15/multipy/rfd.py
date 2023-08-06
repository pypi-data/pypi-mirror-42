import numpy as np

def rfd(pvals, alpha=0.05):
    m = len(pvals)
    sort_ind = np.argsort(pvals)
    r = np.sum(pvals < alpha) - int(m*alpha)
    k = [i for i, p in enumerate(pvals[sort_ind]) if (p < alpha) & (i < r)]
    significant = np.zeros(m, dtype='bool')
    if k:
        significant[sort_ind[0:k[-1]+1]] = True
    return significant
