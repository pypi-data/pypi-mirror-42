# -*- encoding: utf-8 -*-
"""Functions for computing reproducibility values.

Author: Tuomas Puoliväli
Email: tuomas.puolivali@helsinki.fi
License: Revised 3-clause BSD
Last modified: 31th December 2018

References:

[1] Heller R, Bogomolov M, Benjamini Y (2014): Deciding whether follow-up
studies have replicated findings in a preliminary large-scale omics study.
The Proceedings of the National Academy of Sciences of the United States
of America 111(46):16262-16267.

"""

import numpy as np


def fdr_rvalue(R, m_primary, l, emphasis=0.5):
    """Function for computing reproducibility values (r-values) using the
    method suggested by Heller et al.

    Input arguments:
    ================
    R : list of tuples
      Primary and follow-up study P-values.
    m_primary : int
      Number of features examined in the primary study.
    emphasis: float
      Emphasis given to the follow-up study. Must be a value on the open
      interval (0, 1).
    """

    """Get the number of features selected for follow-up."""
    m_followup, _ = np.shape(R)

    e = np.zeros([m_followup, 1])

    for i in np.arange(0, m_followup):
        c = (1-emphasis) / ((1-l) * (1-emphasis*x))
        p1 = R[i, 0] / c
        p2 = (R[i, 1] * m_followup) / (m_primary * emphasis)
        e[i] = np.max(p1, p2)
