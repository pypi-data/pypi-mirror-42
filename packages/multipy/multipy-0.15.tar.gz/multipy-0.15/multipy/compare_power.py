import matplotlib.pyplot as plt

import numpy as np

from fdr import lsu, qvalue, tst
from fwer import sidak, holm_bonferroni, hochberg
from data import square_grid_model
from permutation import tfr_permutation_test
from rft import rft_2d
from util import grid_model_counts, roc
from viz import plot_grid_model

from scipy.stats import norm

import seaborn as sns

"""Specify simulation settings."""
nl, sl = 90, 30
N = 25
alpha = 0.05
n_iter = 20
deltas = np.linspace(0.5, 1.5, 20)
n_deltas = len(deltas)
methods = ['uncorrected', 'sidak', 'holm', 'hochberg', 'fdr', 'tst',
           'qvalue', 'permutation', 'rft']
n_methods = len(methods)

tp = np.zeros([n_methods, n_deltas, n_iter])

for i in np.arange(0, n_iter):
    print('Iteration %2d' % i)
    for j in np.arange(0, n_deltas):
        X, X_tstats, X_raw, Y_raw = square_grid_model(nl, sl, N, deltas[j],
                                                      equal_var=True)
        # 1: sidak
        Y_sidak = sidak(X.flatten(), alpha=alpha)
        Y_sidak = Y_sidak.reshape(nl, nl)

        # 2: holm
        Y_holm = holm_bonferroni(X.flatten(), alpha=alpha)
        Y_holm = Y_holm.reshape(nl, nl)

        # 3: hochberg
        Y_hochberg = hochberg(X.flatten(), alpha=alpha)
        Y_hochberg = Y_hochberg.reshape(nl, nl)

        # 4: bh fdr
        Y_fdr = lsu(X.flatten(), q=alpha)
        Y_fdr = Y_fdr.reshape(nl, nl)

        # 5: tst
        Y_tst = tst(X.flatten(), q=alpha)
        Y_tst = Y_tst.reshape(nl, nl)

        # 6: qvalue
        Y_qvalue, _ = qvalue(X.flatten(), threshold=alpha)
        Y_qvalue = Y_qvalue.reshape(nl, nl)

        # 7: permutation
        Y_permutation = tfr_permutation_test(X_raw, Y_raw, n_permutations=100,
                                             alpha=alpha, threshold=1)

        # 8: rft
        Y_rft, Y_smooth, _ = rft_2d(X_tstats, fwhm=15, alpha=alpha, verbose=True)
        # No reshape needed since already in correct form.

        """Computer power for each method."""
        tp[0, j, i] = grid_model_counts(X<alpha, nl, sl)[0]
        tp[1, j, i] = grid_model_counts(Y_sidak, nl, sl)[0]
        tp[2, j, i] = grid_model_counts(Y_holm, nl, sl)[0]
        tp[3, j, i] = grid_model_counts(Y_hochberg, nl, sl)[0]
        tp[4, j, i] = grid_model_counts(Y_fdr, nl, sl)[0]
        tp[5, j, i] = grid_model_counts(Y_tst, nl, sl)[0]
        tp[6, j, i] = grid_model_counts(Y_qvalue, nl, sl)[0]
        tp[7, j, i] = grid_model_counts(Y_permutation, nl, sl)[0]
        tp[8, j, i] = grid_model_counts(Y_rft, nl, sl)[0]


pwr = tp / (sl ** 2)

#fig = plt.figure(figsize=(8, 7))
#
#ax = fig.add_subplot(111)
#sns.boxplot(data=pwr, ax=ax)
#
#ax.set_xticklabels(methods)
#ax.set_ylabel('Power')
#
#fig.tight_layout()
#plt.show()

"""Visualize the results."""
z = norm.ppf(0.995) # 99% confidence interval

sns.set_style('darkgrid')
fig = plt.figure(figsize=(8, 7))

ax = fig.add_subplot(111)

"""Compute TPR confidence intervals."""
for k in np.arange(0, n_methods):
    yerr = (z * np.std(pwr, axis=2)[k, :]) / np.sqrt(n_iter)
    ax.errorbar(x=deltas, y=np.mean(pwr, axis=2)[k, :], yerr=yerr)

"""Label the axes etc."""
ax.set_xlabel("Effect size (Cohen's d)")
ax.set_ylabel('True positive or reproducibility rate')
ax.set_xlim([deltas[0]-0.05, deltas[-1]+0.05])
ax.set_ylim([-0.05, 1.05])
ax.legend(methods, loc=4)

fig.tight_layout()
plt.show()

