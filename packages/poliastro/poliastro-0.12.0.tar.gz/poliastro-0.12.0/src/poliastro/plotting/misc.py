from typing import Union

from poliastro.bodies import (
    Earth,
    Jupiter,
    Mars,
    Mercury,
    Neptune,
    Saturn,
    Uranus,
    Venus,
)
from poliastro.plotting.core import OrbitPlotter2D, OrbitPlotter3D
from poliastro.twobody import Orbit


def plot_solar_system(outer=True, epoch=None, use_3d=False):
    """
    Plots the whole solar system in one single call.

    .. versionadded:: 0.9.0

    Parameters
    ------------
    outer : bool, optional
        Whether to print the outer Solar System, default to True.
    epoch : ~astropy.time.Time, optional
        Epoch value of the plot, default to J2000.
    use_3d : bool, optional
        Produce 3D plot, default to False.

    """
    bodies = [Mercury, Venus, Earth, Mars]
    if outer:
        bodies.extend([Jupiter, Saturn, Uranus, Neptune])

    if use_3d:
        op = OrbitPlotter3D()  # type: Union[OrbitPlotter3D, OrbitPlotter2D]
    else:
        op = OrbitPlotter2D()
        op.set_frame(*Orbit.from_body_ephem(Earth, epoch).pqw())  # type: ignore

    for body in bodies:
        orb = Orbit.from_body_ephem(body, epoch)
        op.plot(orb, label=str(body))

    return op
