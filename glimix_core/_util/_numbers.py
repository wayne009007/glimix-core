from numpy import finfo, log, clip, inf

__all__ = ["logmax", "safe_log"]

logmax = log(finfo(float).max)


def safe_log(x):
    from numpy_sugar import epsilon

    return log(clip(x, epsilon.small, inf))
