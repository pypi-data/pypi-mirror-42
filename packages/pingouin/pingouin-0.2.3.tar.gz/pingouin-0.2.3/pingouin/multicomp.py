# Author: Raphael Vallat <raphaelvallat9@gmail.com>
# Date: April 2018
# Code borrowed from statsmodel and mne.stats
import numpy as np

__all__ = ["fdr", "bonf", "holm", "multicomp"]


def _ecdf(x):
    """No frills empirical cdf used in fdrcorrection."""
    nobs = len(x)
    return np.arange(1, nobs + 1) / float(nobs)


def fdr(pvals, alpha=0.05, method='indep'):
    """P-values correction with False Discovery Rate (FDR).

    Correction for multiple comparison using FDR.

    This covers Benjamini/Hochberg for independent or positively correlated and
    Benjamini/Yekutieli for general or negatively correlated tests.

    Parameters
    ----------
    pvals : array_like
        set of p-values of the individual tests.
    alpha : float
        error rate
    method : 'indep' | 'negcorr'
        If 'indep' it implements Benjamini/Hochberg for independent or if
        'negcorr' it corresponds to Benjamini/Yekutieli.

    Returns
    -------
    reject : array, bool
        True if a hypothesis is rejected, False if not
    pval_corrected : array
        pvalues adjusted for multiple hypothesis testing to limit FDR

    Examples
    --------
    FDR correction of an array of p-values

        >>> from pingouin import fdr
        >>> pvals = [.50, .003, .32, .054, .0003]
        >>> reject, pvals_corr = bonf(pvals, alpha=.05)
        >>> print(reject, pvals_corr)

    **Output:**

    [False True False False  True] [0.5  0.0075  0.4  0.09  0.0015]
    """
    pvals = np.asarray(pvals)
    shape_init = pvals.shape
    pvals = pvals.ravel()

    pvals_sortind = np.argsort(pvals)
    pvals_sorted = pvals[pvals_sortind]
    sortrevind = pvals_sortind.argsort()

    if method in ['i', 'indep', 'p', 'poscorr']:
        ecdffactor = _ecdf(pvals_sorted)
    elif method in ['n', 'negcorr']:
        cm = np.sum(1. / np.arange(1, len(pvals_sorted) + 1))
        ecdffactor = _ecdf(pvals_sorted) / cm
    else:
        raise ValueError("Method should be 'indep' and 'negcorr'")

    reject = pvals_sorted < (ecdffactor * alpha)
    if reject.any():
        rejectmax = max(np.nonzero(reject)[0])
    else:
        rejectmax = 0
    reject[:rejectmax] = True

    pvals_corrected_raw = pvals_sorted / ecdffactor
    pvals_corrected = np.minimum.accumulate(pvals_corrected_raw[::-1])[::-1]
    pvals_corrected[pvals_corrected > 1.0] = 1.0
    pvals_corrected = pvals_corrected[sortrevind].reshape(shape_init)
    reject = reject[sortrevind].reshape(shape_init)
    return reject, pvals_corrected


def bonf(pvals, alpha=0.05):
    """P-values correction with Bonferroni method.

    Parameters
    ----------
    pvals : array_like
        set of p-values of the individual tests.
    alpha : float
        error rate

    Returns
    -------
    reject : array, bool
        True if a hypothesis is rejected, False if not
    pval_corrected : array
        pvalues adjusted for multiple hypothesis testing

    Examples
    --------
    Bonferroni correction of an array of p-values

        >>> from pingouin import bonf
        >>> pvals = [.50, .003, .32, .054, .0003]
        >>> reject, pvals_corr = bonf(pvals, alpha=.05)
        >>> print(reject, pvals_corr)

    **Output:**

    [False True False False  True] [1.  0.015   1.  0.27  0.0015]
    """
    pvals = np.asarray(pvals)
    pvals_corrected = pvals * float(pvals.size)
    pvals_corrected[pvals_corrected > 1.0] = 1.0
    reject = pvals_corrected < alpha
    return reject, pvals_corrected


def holm(pvals, alpha=.05):
    """P-values correction with Holm method.

    Parameters
    ----------
    pvals : array_like
        set of p-values of the individual tests.
    alpha : float
        error rate

    Returns
    -------
    reject : array, bool
        True if a hypothesis is rejected, False if not
    pval_corrected : array
        pvalues adjusted for multiple hypothesis testing

    Examples
    --------
    Holm correction of an array of p-values

        >>> from pingouin import holm
        >>> pvals = [.50, .003, .32, .054, .0003]
        >>> reject, pvals_corr = holm(pvals, alpha=.05)
        >>> print(reject, pvals_corr)

    **Output:**

    [False True False False True] [0.64  0.012  0.64  0.162  0.0015]
    """
    pvals = np.asarray(pvals)
    shape_init = pvals.shape
    pvals = pvals.ravel()

    pvals_sortind = np.argsort(pvals)
    pvals_sorted = pvals[pvals_sortind]
    sortrevind = pvals_sortind.argsort()
    ntests = pvals.size

    notreject = pvals_sorted > alpha / np.arange(ntests, 0, -1)
    nr_index = np.nonzero(notreject)[0]
    if nr_index.size == 0:
        # nonreject is empty, all rejected
        notrejectmin = ntests
    else:
        notrejectmin = np.min(nr_index)
    notreject[notrejectmin:] = True
    reject = ~notreject
    pvals_corrected_raw = pvals_sorted * np.arange(ntests, 0, -1)
    pvals_corrected = np.maximum.accumulate(pvals_corrected_raw)
    pvals_corrected[pvals_corrected > 1.0] = 1.0
    pvals_corrected = pvals_corrected[sortrevind].reshape(shape_init)
    reject = reject[sortrevind].reshape(shape_init)
    reject = pvals_corrected < alpha
    return reject, pvals_corrected


def multicomp(pvals, alpha=0.05, method='holm'):
    '''P-values correction for multiple tests.

    Parameters
    ----------
    pvals : array_like
        uncorrected p-values
    alpha : float
        Significance level
    method : string
        Method used for testing and adjustment of pvalues. Can be either the
        full name or initial letters. Available methods are ::

        'bonf' : one-step Bonferroni correction
        'holm' : step-down method using Bonferroni adjustments
        'fdr_bh' : Benjamini/Hochberg FDR correction
        'fdr_by' : Benjamini/Yekutieli FDR correction


    Returns
    -------
    reject : array, boolean
        true for hypothesis that can be rejected for given alpha
    pvals_corrected : array
        p-values corrected for multiple tests

    See Also
    --------
    pairwise_ttests : Pairwise post-hocs T-tests

    Examples
    --------
    FDR correction of an array of p-values

        >>> from pingouin import multicomp
        >>> pvals = [.50, .003, .32, .054, .0003]
        >>> reject, pvals_corr = multicomp(pvals, method='fdr_bh')
        >>> print(reject, pvals_corr)

    **Output:**

    [False True False False  True] [0.5  0.0075  0.4  0.09  0.0015]
    '''
    if not isinstance(pvals, (list, np.ndarray)):
        err = "pvals must be a list or a np.ndarray"
        raise ValueError(err)

    if method.lower() in ['b', 'bonf', 'bonferroni']:
        reject, pvals_corrected = bonf(pvals, alpha=alpha)
    elif method.lower() in ['h', 'holm']:
        reject, pvals_corrected = holm(pvals, alpha=alpha)
    elif method.lower() in ['fdr_bh']:
        reject, pvals_corrected = fdr(pvals, alpha=alpha, method='indep')
    elif method.lower() in ['fdr_by']:
        reject, pvals_corrected = fdr(pvals, alpha=alpha, method='negcorr')
    elif method.lower() == 'none':
        return None, None
    else:
        raise ValueError('Multiple comparison method not recognized')
    return reject, pvals_corrected
