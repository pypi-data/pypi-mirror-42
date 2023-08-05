import numpy as np
import pandas as pd
import pandas_flavor as pf
import scipy.stats as scpstats
import scipy.special as scpspec
#from .renorm import renormalise, close
from ..util.math import orthagonal_basis
import logging

logging.getLogger(__name__).addHandler(logging.NullHandler())
logger = logging.getLogger(__name__)


def close(X: np.ndarray):
    if X.ndim == 2:
        return np.divide(X, np.sum(X, axis=1)[:, np.newaxis])
    else:
        return np.divide(X, np.sum(X, axis=0))

@pf.register_series_method
@pf.register_dataframe_method
def renormalise(df: pd.DataFrame, components: list = [], scale=100.0):
    """
    Renormalises compositional data to ensure closure.

    Parameters
    ------------
    df: pd.DataFrame
        Dataframe to renomalise.
    components: list
        Option subcompositon to renormalise to 100. Useful for the use case
        where compostional data and non-compositional data are stored in the
        same dataframe.
    scale: float, 100.
        Closure parameter. Typically either 100 or 1.
    """
    dfc = df.copy(deep=True)
    if components:
        cmpnts = [c for c in components if c in dfc.columns]
        dfc.loc[:, cmpnts] = scale * dfc.loc[:, cmpnts].divide(
            dfc.loc[:, cmpnts].sum(axis=1).replace(0, np.nan), axis=0
        )
        return dfc
    else:
        dfc = dfc.divide(dfc.sum(axis=1).replace(0, 100.0), axis=0) * scale
        return dfc


def additive_log_ratio(X: np.ndarray, ind: int = -1, null_col=False):
    """
    Inverse Additive Log Ratio transformation.

    Parameters
    ---------------
    X: np.ndarray
        Array on which to perform the inverse transformation.
    ind: int
        Index of column used as denominator.
    """

    Y = X.copy()
    assert Y.ndim in [1, 2]
    dimensions = Y.shape[Y.ndim - 1]
    if ind < 0:
        ind += dimensions

    if Y.ndim == 2:
        Y = np.divide(Y, Y[:, ind][:, np.newaxis])
        if not null_col:
            Y = Y[:, [i for i in range(dimensions) if not i == ind]]
    else:
        Y = np.divide(X, X[ind])
        if not null_col:
            Y = Y[[i for i in range(dimensions) if not i == ind]]

    return np.log(Y)


def inverse_additive_log_ratio(Y: np.ndarray, ind=-1, null_col=False):
    """
    Inverse Centred Log Ratio transformation.

    Parameters
    ---------------
    X: np.ndarray
        Array on which to perform the inverse transformation.
    ind: int
        Index of column used as denominator.
    """
    assert Y.ndim in [1, 2]

    X = Y.copy()
    dimensions = X.shape[X.ndim - 1]
    if not null_col:
        idx = np.arange(0, dimensions + 1)

        if ind != -1:
            idx = np.array(list(idx[idx < ind]) + [-1] + list(idx[idx >= ind + 1] - 1))

        # Add a zero-column and reorder columns
        if Y.ndim == 2:
            X = np.concatenate((X, np.zeros((X.shape[0], 1))), axis=1)
            X = X[:, idx]
        else:
            X = np.append(X, np.array([0]))
            X = X[idx]

    # Inverse log and closure operations
    X = np.exp(X)
    X = close(X)
    return X


def alr(*args, **kwargs):
    """
    Short form of Additive Log Ratio transformation.

    Parameters
    ---------------
    Y: np.ndarray
        Array on which to perform the inverse transformation.
    ind: int
        Index of column used as denominator.
    """
    return additive_log_ratio(*args, **kwargs)


def inv_alr(*args, **kwargs):
    """
    Short form of Inverse Additive Log Ratio transformation.

    Parameters
    ---------------
    Y: np.ndarray
        Array on which to perform the inverse transformation.
    ind: int
        Index of column used as denominator.
    """
    return inverse_additive_log_ratio(*args, **kwargs)


def clr(X: np.ndarray):
    """
    Centred Log Ratio transformation.

    Parameters
    ---------------
    X: np.ndarray
        Array on which to perform the transformation.
    """
    X = np.divide(X, np.sum(X, axis=1)[:, np.newaxis])  # Closure operation
    Y = np.log(X)  # Log operation
    Y -= 1 / X.shape[1] * np.nansum(Y, axis=1)[:, np.newaxis]
    return Y


def inv_clr(Y: np.ndarray):
    """
    Inverse Centred Log Ratio transformation.

    Parameters
    ---------------
    Y: np.ndarray
        Array on which to perform the inverse transformation.
    """
    # Inverse of log operation
    X = np.exp(Y)
    # Closure operation
    X = np.divide(X, np.nansum(X, axis=1)[:, np.newaxis])
    return X


def ilr(X: np.ndarray):
    """
    Isotmetric Log Ratio transformation.

    Parameters
    ---------------
    X: np.ndarray
        Array on which to perform the transformation.
    """
    d = X.shape[1]
    Y = clr(X)
    psi = orthagonal_basis(X)  # Get a basis
    psi = orthagonal_basis(clr(X))  # trying to get right algorithm
    assert np.allclose(psi @ psi.T, np.eye(d - 1))
    return Y @ psi.T


def inv_ilr(Y: np.ndarray, X: np.ndarray = None):
    """
    Inverse Isometric Log Ratio transformation.

    Parameters
    ---------------
    Y: np.ndarray
        Array on which to perform the inverse transformation.
    """
    psi = orthagonal_basis(X)
    C = Y @ psi
    X = inv_clr(C)  # Inverse log operation
    return X


def boxcox(
    X: np.ndarray,
    lmbda=None,
    lmbda_search_space=(-1, 5),
    search_steps=100,
    return_lmbda=False,
):
    """
    Box-Cox transformation.

    Parameters
    ---------------
    Y: np.ndarray
        Array on which to perform the transformation.
    lmbda: {None, np.float}
        Lambda value used to forward-transform values. If none, it will be calculated
        using the mean
    """
    if isinstance(X, pd.DataFrame) or isinstance(X, pd.Series):
        _X = X.values
    else:
        _X = X.copy()

    if lmbda is None:
        l_search = np.linspace(*lmbda_search_space, search_steps)
        llf = np.apply_along_axis(scpstats.boxcox_llf, 0, np.array([l_search]), _X.T)
        if llf.shape[0] == 1:
            mean_llf = llf[0]
        else:
            mean_llf = np.nansum(llf, axis=0)

        lmbda = l_search[mean_llf == np.nanmax(mean_llf)]
    if _X.ndim < 2:
        out = scpstats.boxcox(_X, lmbda)
    elif _X.shape[0] == 1:
        out = scpstats.boxcox(np.squeeze(_X), lmbda)
    else:
        out = np.apply_along_axis(scpstats.boxcox, 0, _X, lmbda)

    if isinstance(_X, pd.DataFrame) or isinstance(_X, pd.Series):
        _out = X.copy()
        _out.loc[:, :] = out
        out = _out

    if return_lmbda:
        return out, lmbda
    else:
        return out


def inv_boxcox(Y: np.ndarray, lmbda):
    """
    Inverse Box-Cox transformation.

    Parameters
    ---------------
    Y: np.ndarray
        Array on which to perform the transformation.
    lmbda: np.float
        Lambda value used to forward-transform values.
    """
    return scpspec.inv_boxcox(Y, lmbda)
