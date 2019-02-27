from numpy import exp, log

from optimix import Function, Scalar

from .._util import format_function


class LinearCov(Function):
    """
    Linear covariance function, K = s⋅XXᵀ.

    The mathematical representation is s⋅XXᵀ, for an n×r matrix provided by the user
    and a scalar parameter s.

    Example
    -------

    .. doctest::

        >>> from glimix_core.cov import LinearCov
        >>> from numpy import dot
        >>> from numpy.random import RandomState
        >>>
        >>> X = RandomState(0).randn(2, 3)
        >>> cov = LinearCov()
        >>> cov.X = X
        >>> cov.scale = 1.3
        >>> cov.name = "K"
        >>> print(cov)
        LinearCov(): K
          scale: 1.3
    """

    def __init__(self):
        """
        Constructor.

        Parameters
        ----------
        X : array_like
            Matrix X from K = s⋅XXᵀ.
        """
        self._logscale = Scalar(0.0)
        self._X = None
        Function.__init__(self, "LinearCov", logscale=self._logscale)
        self._logscale.bounds = (-20.0, +10)

    @property
    def X(self):
        """
        Matrix X from K = s⋅XXᵀ.
        """
        return self._X

    @X.setter
    def X(self, X):
        self._X = X

    def fix_scale(self):
        self._fix("logscale")

    def unfix_scale(self):
        self._unfix("logscale")

    @property
    def scale(self):
        """
        Scale parameter.
        """
        return exp(self._logscale.value)

    @scale.setter
    def scale(self, scale):
        from numpy_sugar import epsilon

        scale = max(scale, epsilon.tiny)
        self._logscale.value = log(scale)

    def value(self):
        """
        Covariance matrix.

        Returns
        -------
        ndarray
            s⋅XXᵀ.
        """
        X = self.X
        return self.scale * (X @ X.T)

    def gradient(self):
        """
        Derivative of the covariance matrix over log(s).

        Returns
        -------
        logscale
            s⋅XXᵀ.
        """
        return dict(logscale=self.value())

    def __str__(self):
        return format_function(self, {}, [("scale", self.scale)])
