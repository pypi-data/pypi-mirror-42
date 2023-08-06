import numpy as np

from poliastro.core.angles import M_to_nu, nu_to_M
from poliastro.core.elements import coe2rv, rv2coe
from poliastro.core.stumpff import c2, c3

from ._jit import jit


def func_twobody(t0, u_, k, ad, ad_kwargs):
    """Differential equation for the initial value two body problem.

    This function follows Cowell's formulation.

    Parameters
    ----------
    t0 : float
        Time.
    u_ : ~numpy.ndarray
        Six component state vector [x, y, z, vx, vy, vz] (km, km/s).
    k : float
        Standard gravitational parameter.
    ad : function(t0, u, k)
        Non Keplerian acceleration (km/s2).
    ad_kwargs : optional
        perturbation parameters passed to ad.

    """
    ax, ay, az = ad(t0, u_, k, **ad_kwargs)

    x, y, z, vx, vy, vz = u_
    r3 = (x ** 2 + y ** 2 + z ** 2) ** 1.5

    du = np.array([vx, vy, vz, -k * x / r3 + ax, -k * y / r3 + ay, -k * z / r3 + az])
    return du


@jit
def mean_motion(k, r0, v0, tof):
    r"""Propagates orbit using mean motion. This algorithm depends on the geometric shape of the
    orbit.

    For the case of the strong elliptic or strong hyperbolic orbits:

    ..  math::

        M = M_{0} + \frac{\mu^{2}}{h^{3}}\left ( 1 -e^{2}\right )^{\frac{3}{2}}t

    .. versionadded:: 0.9.0


    Parameters
    ----------
    k : float
        Standar Gravitational parameter
    r0 : ~astropy.units.Quantity
        Initial position vector wrt attractor center.
    v0 : ~astropy.units.Quantity
        Initial velocity vector.
    tof : float
        Time of flight (s).

    Note
    ----
    This method takes initial :math:`\vec{r}, \vec{v}`, calculates classical orbit parameters,
    increases mean anomaly and performs inverse transformation to get final :math:`\vec{r}, \vec{v}`
    The logic is based on formulae (4), (6) and (7) from http://dx.doi.org/10.1007/s10569-013-9476-9

    """

    # get the initial true anomaly and orbit parameters that are constant over time
    p, ecc, inc, raan, argp, nu0 = rv2coe(k, r0, v0)

    # get the initial mean anomaly
    M0 = nu_to_M(nu0, ecc)
    # strong elliptic or strong hyperbolic orbits
    if np.abs(ecc - 1.0) > 1e-2:
        a = p / (1.0 - ecc ** 2)
        # given the initial mean anomaly, calculate mean anomaly
        # at the end, mean motion (n) equals sqrt(mu / |a^3|)
        M = M0 + tof * np.sqrt(k / np.abs(a ** 3))
        nu = M_to_nu(M, ecc)

    # near-parabolic orbit
    else:
        q = p * np.abs(1.0 - ecc) / np.abs(1.0 - ecc ** 2)
        # mean motion n = sqrt(mu / 2 q^3) for parabolic orbit
        M = M0 + tof * np.sqrt(k / 2.0 / (q ** 3))
        nu = M_to_nu(M, ecc)

    return coe2rv(k, p, ecc, inc, raan, argp, nu)


@jit
def kepler(k, r0, v0, tof, numiter):
    r"""Solves Kepler's Equation by applying a Newton-Raphson method.

    If the position of a body along its orbit wants to be computed
    for an specific time, it can be solved by terms of the Kepler's Equation:

    .. math::
        E = M + e\sin{E}

    In this case, the equation is written in terms of the Universal Anomaly:

    .. math::

        \sqrt{\mu}\Delta t = \frac{r_{o}v_{o}}{\sqrt{\mu}}\chi^{2}C(\alpha \chi^{2}) + (1 - \alpha r_{o})\chi^{3}S(\alpha \chi^{2}) + r_{0}\chi

    This equation is solved for the universal anomaly by applying a Newton-Raphson numerical method.
    Once it is solved, the Lagrange coefficients are returned:

    .. math::

        \begin{align}
            f &= 1 \frac{\chi^{2}}{r_{o}}C(\alpha \chi^{2}) \\
            g &= \Delta t - \frac{1}{\sqrt{\mu}}\chi^{3}S(\alpha \chi^{2}) \\
            \dot{f} &= \frac{\sqrt{\mu}}{rr_{o}}(\alpha \chi^{3}S(\alpha \chi^{2}) - \chi) \\
            \dot{g} &= 1 - \frac{\chi^{2}}{r}C(\alpha \chi^{2}) \\
        \end{align}

    Lagrange coefficients can be related then with the position and velocity vectors:

    .. math::
        \begin{align}
            \vec{r} &= f\vec{r_{o}} + g\vec{v_{o}} \\
            \vec{v} &= \dot{f}\vec{r_{o}} + \dot{g}\vec{v_{o}} \\
        \end{align}

    Parameters
    ----------

    k: float
        Standard gravitational parameter
    r0: ~numpy.array
        Initial position vector
    v0: ~numpy.array
        Initial velocity vector
    numiter: int
        Number of iterations

    Returns
    -------
    f: float
        First Lagrange coefficient
    g: float
        Second Lagrange coefficient
    fdot: float
        Derivative of the first coefficient
    gdot: float
        Derivative of the second coefficient


    Note
    ----
    The theoretical procedure is explained in section 3.7 of Curtis in really
    deep detail. For analytical example, check in the same book for example 3.6.
    """

    # Cache some results
    dot_r0v0 = np.dot(r0, v0)
    norm_r0 = np.dot(r0, r0) ** 0.5
    sqrt_mu = k ** 0.5
    alpha = -np.dot(v0, v0) / k + 2 / norm_r0

    # First guess
    if alpha > 0:
        # Elliptic orbit
        xi_new = sqrt_mu * tof * alpha
    elif alpha < 0:
        # Hyperbolic orbit
        xi_new = (
            np.sign(tof)
            * (-1 / alpha) ** 0.5
            * np.log(
                (-2 * k * alpha * tof)
                / (
                    dot_r0v0
                    + np.sign(tof) * np.sqrt(-k / alpha) * (1 - norm_r0 * alpha)
                )
            )
        )
    else:
        # Parabolic orbit
        # (Conservative initial guess)
        xi_new = sqrt_mu * tof / norm_r0

    # Newton-Raphson iteration on the Kepler equation
    count = 0
    while count < numiter:
        xi = xi_new
        psi = xi * xi * alpha
        c2_psi = c2(psi)
        c3_psi = c3(psi)
        norm_r = (
            xi * xi * c2_psi
            + dot_r0v0 / sqrt_mu * xi * (1 - psi * c3_psi)
            + norm_r0 * (1 - psi * c2_psi)
        )
        xi_new = (
            xi
            + (
                sqrt_mu * tof
                - xi * xi * xi * c3_psi
                - dot_r0v0 / sqrt_mu * xi * xi * c2_psi
                - norm_r0 * xi * (1 - psi * c3_psi)
            )
            / norm_r
        )
        if abs(xi_new - xi) < 1e-7:
            break
        else:
            count += 1
    else:
        raise RuntimeError("Maximum number of iterations reached")

    # Compute Lagrange coefficients
    f = 1 - xi ** 2 / norm_r0 * c2_psi
    g = tof - xi ** 3 / sqrt_mu * c3_psi

    gdot = 1 - xi ** 2 / norm_r * c2_psi
    fdot = sqrt_mu / (norm_r * norm_r0) * xi * (psi * c3_psi - 1)

    return f, g, fdot, gdot
