import pickle

import numpy as np
import pytest
from astropy import units as u
from astropy.coordinates import (
    ITRS,
    CartesianDifferential,
    CartesianRepresentation,
    SkyCoord,
)
from astropy.tests.helper import assert_quantity_allclose
from astropy.time import Time
from numpy.testing import assert_allclose, assert_array_equal

from poliastro.bodies import (
    Body,
    Earth,
    Jupiter,
    Mars,
    Mercury,
    Moon,
    Neptune,
    Pluto,
    Saturn,
    Sun,
    Uranus,
    Venus,
)
from poliastro.constants import J2000, J2000_TDB
from poliastro.frames import (
    GCRS,
    HCRS,
    ICRS,
    HeliocentricEclipticJ2000,
    JupiterICRS,
    MarsICRS,
    MercuryICRS,
    NeptuneICRS,
    Planes,
    PlutoICRS,
    SaturnICRS,
    UranusICRS,
    VenusICRS,
    get_frame,
)
from poliastro.twobody import Orbit
from poliastro.twobody.orbit import OrbitSamplingWarning, TimeScaleWarning
from poliastro.twobody.propagation import cowell, kepler, mean_motion


@pytest.fixture()
def hyperbolic():
    r = [1.197659243752796e09, -4.443716685978071e09, -1.747610548576734e09] * u.km
    v = (
        [5.540549267188614e00, -1.251544669134140e01, -4.848892572767733e00]
        * u.km
        / u.s
    )
    epoch = Time("2015-07-14 07:59", scale="tdb")
    return Orbit.from_vectors(Sun, r, v, epoch)


def test_default_time_for_new_state():
    _d = 1.0 * u.AU  # Unused distance
    _ = 0.5 * u.one  # Unused dimensionless value
    _a = 1.0 * u.deg  # Unused angle
    _body = Sun  # Unused body
    expected_epoch = J2000
    ss = Orbit.from_classical(_body, _d, _, _a, _a, _a, _a)
    assert ss.epoch == expected_epoch


def test_state_raises_unitserror_if_elements_units_are_wrong():
    _d = 1.0 * u.AU  # Unused distance
    _ = 0.5 * u.one  # Unused dimensionless value
    _a = 1.0 * u.deg  # Unused angle
    wrong_angle = 1.0 * u.AU
    with pytest.raises(u.UnitsError) as excinfo:
        Orbit.from_classical(Sun, _d, _, _a, _a, _a, wrong_angle)
    assert (
        "UnitsError: Argument 'nu' to function 'from_classical' must be in units convertible to 'rad'."
        in excinfo.exconly()
    )


def test_state_raises_unitserror_if_rv_units_are_wrong():
    _d = [1.0, 0.0, 0.0] * u.AU
    wrong_v = [0.0, 1.0e-6, 0.0] * u.AU
    with pytest.raises(u.UnitsError) as excinfo:
        Orbit.from_vectors(Sun, _d, wrong_v)
    assert (
        "UnitsError: Argument 'v' to function 'from_vectors' must be in units convertible to 'm / s'."
        in excinfo.exconly()
    )


def test_parabolic_elements_fail_early():
    attractor = Earth
    ecc = 1.0 * u.one
    _d = 1.0 * u.AU  # Unused distance
    _a = 1.0 * u.deg  # Unused angle
    with pytest.raises(ValueError) as excinfo:
        Orbit.from_classical(attractor, _d, ecc, _a, _a, _a, _a)
    assert (
        "ValueError: For parabolic orbits use Orbit.parabolic instead"
        in excinfo.exconly()
    )


def test_bad_inclination_raises_exception():
    _d = 1.0 * u.AU  # Unused distance
    _ = 0.5 * u.one  # Unused dimensionless value
    _a = 1.0 * u.deg  # Unused angle
    _body = Sun  # Unused body
    bad_inc = 200 * u.deg
    with pytest.raises(ValueError) as excinfo:
        Orbit.from_classical(_body, _d, _, bad_inc, _a, _a, _a)
    assert (
        "ValueError: Inclination must be between 0 and 180 degrees" in excinfo.exconly()
    )


def test_bad_hyperbolic_raises_exception():
    bad_a = 1.0 * u.AU
    ecc = 1.5 * u.one
    _inc = 100 * u.deg  # Unused inclination
    _a = 1.0 * u.deg  # Unused angle
    _body = Sun  # Unused body
    with pytest.raises(ValueError) as excinfo:
        Orbit.from_classical(_body, bad_a, ecc, _inc, _a, _a, _a)
    assert "Hyperbolic orbits have negative semimajor axis" in excinfo.exconly()


def test_apply_maneuver_changes_epoch():
    _d = 1.0 * u.AU  # Unused distance
    _ = 0.5 * u.one  # Unused dimensionless value
    _a = 1.0 * u.deg  # Unused angle
    ss = Orbit.from_classical(Sun, _d, _, _a, _a, _a, _a)
    dt = 1 * u.h
    dv = [0, 0, 0] * u.km / u.s
    orbit_new = ss.apply_maneuver([(dt, dv)])
    assert orbit_new.epoch == ss.epoch + dt


def test_orbit_from_ephem_with_no_epoch_is_today():
    # This is not that obvious http://stackoverflow.com/q/6407362/554319
    body = Earth
    ss = Orbit.from_body_ephem(body)
    assert (Time.now() - ss.epoch).sec < 1


def test_from_ephem_raises_warning_if_time_is_not_tdb_with_proper_time(recwarn):
    body = Earth
    epoch = Time("2017-09-29 07:31:26", scale="utc")
    expected_epoch_string = "2017-09-29 07:32:35.182"  # epoch.tdb.value

    Orbit.from_body_ephem(body, epoch)

    w = recwarn.pop(TimeScaleWarning)
    assert expected_epoch_string in str(w.message)


def test_circular_has_proper_semimajor_axis():
    alt = 500 * u.km
    attractor = Earth
    expected_a = Earth.R + alt
    ss = Orbit.circular(attractor, alt)
    assert ss.a == expected_a


def test_geosync_has_proper_period():
    expected_period = 1436 * u.min

    ss = Orbit.circular(Earth, alt=42164 * u.km - Earth.R)

    assert_quantity_allclose(ss.period, expected_period, rtol=1e-4)


def test_parabolic_has_proper_eccentricity():
    attractor = Earth
    _d = 1.0 * u.AU  # Unused distance
    _a = 1.0 * u.deg  # Unused angle
    expected_ecc = 1.0 * u.one
    ss = Orbit.parabolic(attractor, _d, _a, _a, _a, _a)
    assert_allclose(ss.ecc, expected_ecc)


def test_parabolic_has_zero_energy():
    attractor = Earth
    _d = 1.0 * u.AU  # Unused distance
    _a = 1.0 * u.deg  # Unused angle
    ss = Orbit.parabolic(attractor, _d, _a, _a, _a, _a)
    assert_allclose(ss.energy.value, 0.0, atol=1e-16)


def test_pqw_for_circular_equatorial_orbit():
    ss = Orbit.circular(Earth, 600 * u.km)
    expected_p = [1, 0, 0] * u.one
    expected_q = [0, 1, 0] * u.one
    expected_w = [0, 0, 1] * u.one
    p, q, w = ss.pqw()
    assert_allclose(p, expected_p)
    assert_allclose(q, expected_q)
    assert_allclose(w, expected_w)


def test_orbit_representation():
    ss = Orbit.circular(
        Earth, 600 * u.km, 20 * u.deg, epoch=Time("2018-09-08 09:04:00", scale="tdb")
    )
    expected_str = "6978 x 6978 km x 20.0 deg (GCRS) orbit around Earth (\u2641) at epoch 2018-09-08 09:04:00.000 (TDB)"

    assert str(ss) == repr(ss) == expected_str


def test_orbit_no_frame_representation():
    date_launch = Time("2011-11-26 15:02", scale="utc")
    r = [61445.76498656, 24827.93010168, 0.0] * u.km
    v = [-0.42581645, -0.18867869, 0.0] * u.km / u.s
    ss = Orbit.from_vectors(Moon, r, v, date_launch)
    expected_str = "106 x -142299 km x 180.0 deg orbit around Moon (\u263E) at epoch 2011-11-26 15:02:00.000 (UTC)"

    assert str(ss) == repr(ss) == expected_str


def test_sample_numpoints():
    _d = 1.0 * u.AU  # Unused distance
    _ = 0.5 * u.one  # Unused dimensionless value
    _a = 1.0 * u.deg  # Unused angle
    _body = Sun  # Unused body
    ss = Orbit.from_classical(_body, _d, _, _a, _a, _a, _a)
    positions = ss.sample(values=50)
    assert len(positions) == 50


@pytest.mark.parametrize("num_points", [3, 5, 7, 9, 11, 101])
def test_sample_num_points(num_points):
    # Data from Vallado, example 2.4
    r0 = [1131.340, -2282.343, 6672.423] * u.km
    v0 = [-5.64305, 4.30333, 2.42879] * u.km / u.s
    ss0 = Orbit.from_vectors(Earth, r0, v0)

    # TODO: Test against the perigee and apogee
    # expected_ss = ss0.propagate(ss0.period / 2)

    rr = ss0.sample(num_points)

    assert len(rr) == num_points
    # assert_quantity_allclose(rr[num_points // 2].data.xyz, expected_ss.r)


@pytest.mark.parametrize("method", [mean_motion, cowell, kepler])
def test_sample_big_orbits(method):
    # See https://github.com/poliastro/poliastro/issues/265
    ss = Orbit.from_vectors(
        Sun,
        [-9018878.6, -94116055, 22619059] * u.km,
        [-49.950923, -12.948431, -4.2925158] * u.km / u.s,
    )
    positions = ss.sample(15, method=method)
    assert len(positions) == 15


def test_hyperbolic_nu_value_check(hyperbolic):
    positions = hyperbolic.sample(100)

    assert isinstance(positions, HCRS)
    assert len(positions) == 100


def test_hyperbolic_modulus_wrapped_nu():
    ss = Orbit.from_vectors(
        Sun,
        [-9.77441841e07, 1.01000539e08, 4.37584668e07] * u.km,
        [23.75936985, -43.09599568, -8.7084724] * u.km / u.s,
    )
    num_values = 3

    positions = ss.sample(num_values)

    assert_quantity_allclose(positions[0].data.xyz, ss.r)


@pytest.mark.parametrize("min_anomaly", [-30 * u.deg, -10 * u.deg])
@pytest.mark.parametrize("max_anomaly", [10 * u.deg, 30 * u.deg])
def test_sample_hyperbolic_limits(hyperbolic, min_anomaly, max_anomaly):
    num_points = 50

    coords = hyperbolic.sample(
        num_points, min_anomaly=min_anomaly, max_anomaly=max_anomaly
    )

    assert len(coords) == num_points


def test_sample_hyperbolic_outside_limits(hyperbolic):
    with pytest.warns(OrbitSamplingWarning, match="anomaly outside range, clipping"):
        hyperbolic.sample(3, min_anomaly=-np.pi * u.rad)

    with pytest.warns(OrbitSamplingWarning, match="anomaly outside range, clipping"):
        hyperbolic.sample(3, max_anomaly=np.pi * u.rad)


def test_orbit_is_pickable(hyperbolic):
    pickled = pickle.dumps(hyperbolic)
    ss_result = pickle.loads(pickled)

    assert_array_equal(hyperbolic.r, ss_result.r)
    assert_array_equal(hyperbolic.v, ss_result.v)
    assert ss_result.epoch == hyperbolic.epoch


@pytest.mark.parametrize(
    "attractor, expected_frame_class",
    [
        (Sun, HCRS),
        (Mercury, MercuryICRS),
        (Venus, VenusICRS),
        (Earth, GCRS),
        (Mars, MarsICRS),
        (Jupiter, JupiterICRS),
        (Saturn, SaturnICRS),
        (Uranus, UranusICRS),
        (Neptune, NeptuneICRS),
        (Pluto, PlutoICRS),
    ],
)
def test_orbit_has_proper_frame(attractor, expected_frame_class):
    # Dummy data
    r = [1e09, -4e09, -1e09] * u.km
    v = [5e00, -1e01, -4e00] * u.km / u.s
    epoch = Time("2015-07-14 07:59", scale="tdb")

    ss = Orbit.from_vectors(attractor, r, v, epoch)

    assert ss.frame.is_equivalent_frame(expected_frame_class(obstime=epoch))
    assert ss.frame.obstime == epoch


def test_orbit_from_custom_body_raises_error_when_asked_frame():
    attractor = Body(Sun, 1 * u.km ** 3 / u.s ** 2, "_DummyPlanet")

    r = [1e09, -4e09, -1e09] * u.km
    v = [5e00, -1e01, -4e00] * u.km / u.s

    ss = Orbit.from_vectors(attractor, r, v)

    with pytest.raises(NotImplementedError) as excinfo:
        ss.frame
    assert (
        "Frames for orbits around custom bodies are not yet supported"
        in excinfo.exconly()
    )


@pytest.mark.parametrize(
    "body", [Sun, Mercury, Venus, Earth, Mars, Jupiter, Saturn, Uranus, Neptune]
)
def test_orbit_from_ephem_is_in_icrs_frame(body):
    ss = Orbit.from_body_ephem(body)

    assert ss.frame.is_equivalent_frame(ICRS())


def test_orbit_accepts_ecliptic_plane():
    r = [1e09, -4e09, -1e09] * u.km
    v = [5e00, -1e01, -4e00] * u.km / u.s

    ss = Orbit.from_vectors(Sun, r, v, plane=Planes.EARTH_ECLIPTIC)

    assert ss.frame.is_equivalent_frame(HeliocentricEclipticJ2000(obstime=J2000))


def test_orbit_represent_as_produces_correct_data():
    r = [1e09, -4e09, -1e09] * u.km
    v = [5e00, -1e01, -4e00] * u.km / u.s

    ss = Orbit.from_vectors(Sun, r, v)

    expected_result = CartesianRepresentation(
        *r, differentials=CartesianDifferential(*v)
    )

    result = ss.represent_as(CartesianRepresentation)

    # We can't directly compare the objects, see https://github.com/astropy/astropy/issues/7793
    assert (result.xyz == expected_result.xyz).all()
    assert (
        result.differentials["s"].d_xyz == expected_result.differentials["s"].d_xyz
    ).all()


@pytest.mark.parametrize("value", [1 * u.h, 10 * u.deg])
def test_orbit_propagate_retains_plane(value):
    r = [1e09, -4e09, -1e09] * u.km
    v = [5e00, -1e01, -4e00] * u.km / u.s

    ss = Orbit.from_vectors(Sun, r, v, plane=Planes.EARTH_ECLIPTIC)

    orig_frame = ss.frame

    final_ss = ss.propagate(1 * u.h)
    expected_frame = orig_frame.replicate_without_data(obstime=final_ss.epoch)

    assert final_ss.frame.is_equivalent_frame(expected_frame)


@pytest.mark.remote_data
def test_from_horizons_raise_valueerror():
    with pytest.raises(ValueError) as exep:
        Orbit.from_horizons(name="Dummy")
    assert (
        "ValueError: Unknown target (Dummy). Maybe try different id_type?"
        in exep.exconly()
    )


@pytest.mark.remote_data
def test_orbits_are_same():
    epoch = Time("2018-07-23")
    # Orbit Parameters of Ceres
    # Taken from https://ssd.jpl.nasa.gov/horizons.cgi
    ss = Orbit.from_classical(
        Sun,
        2.767107584017257 * u.au,
        0.07554802949294502 * u.one,
        27.18502520750381 * u.deg,
        23.36913256044832 * u.deg,
        132.2919806192451 * u.deg,
        21.28958091587153 * u.deg,
        epoch,
    )
    ss1 = Orbit.from_horizons(name="Ceres", epoch=epoch)
    assert ss.pqw()[0].value.all() == ss1.pqw()[0].value.all()
    assert ss.r_a == ss1.r_a
    assert ss.a == ss1.a


@pytest.mark.remote_data
def test_plane_is_set_in_horizons():
    plane = Planes.EARTH_ECLIPTIC
    ss = Orbit.from_horizons(name="Ceres", plane=plane)
    assert ss.plane == plane


@pytest.mark.parametrize(
    "attractor,angular_velocity,expected_a,expected_period",
    [
        (
            Earth,
            (2 * np.pi / 23.9345) * u.rad / u.hour,
            42164205 * u.m,
            23.9345 * u.hour,
        ),
        (
            Mars,
            (2 * np.pi / 24.6228) * u.rad / u.hour,
            20427595 * u.m,
            24.6228 * u.hour,
        ),
    ],
)
def test_geostationary_creation_from_angular_velocity(
    attractor, angular_velocity, expected_a, expected_period
):
    ss = Orbit.geostationary(attractor=attractor, angular_velocity=angular_velocity)
    assert_quantity_allclose(ss.a, expected_a, rtol=1.0e-7)
    assert_quantity_allclose(ss.period, expected_period, rtol=1.0e-7)


@pytest.mark.parametrize(
    "attractor,period,expected_a",
    [
        (Earth, 23.9345 * u.hour, 42164205 * u.m),
        (Mars, 24.6228 * u.hour, 20427595 * u.m),
    ],
)
def test_geostationary_creation_from_period(attractor, period, expected_a):
    ss = Orbit.geostationary(attractor=attractor, period=period)
    assert_quantity_allclose(ss.a, expected_a, rtol=1.0e-7)
    assert_quantity_allclose(ss.period, period, rtol=1.0e-7)


@pytest.mark.parametrize(
    "attractor,period,hill_radius,expected_a",
    [
        (Earth, 23.9345 * u.hour, 0.01 * u.AU, 42164205 * u.m),
        (Mars, 24.6228 * u.hour, 1000000 * u.km, 20427595 * u.m),
    ],
)
def test_geostationary_creation_with_Hill_radius(
    attractor, period, hill_radius, expected_a
):
    ss = Orbit.geostationary(
        attractor=attractor, period=period, hill_radius=hill_radius
    )
    assert_quantity_allclose(ss.a, expected_a, rtol=1.0e-7)
    assert_quantity_allclose(ss.period, period, rtol=1.0e-7)


@pytest.mark.parametrize("attractor", [Earth, Mars])
def test_geostationary_input(attractor):
    with pytest.raises(ValueError) as excinfo:
        ss = Orbit.geostationary(attractor=attractor)

    assert (
        "ValueError: At least one among angular_velocity or period must be passed"
        in excinfo.exconly()
    )


@pytest.mark.parametrize(
    "attractor,period,hill_radius", [(Venus, 243.025 * u.day, 1000000 * u.km)]
)
def test_geostationary_non_existence_condition(attractor, period, hill_radius):
    with pytest.raises(ValueError) as excinfo:
        ss = Orbit.geostationary(
            attractor=attractor, period=period, hill_radius=hill_radius
        )

    assert (
        "Geostationary orbit for the given parameters doesn't exist"
        in excinfo.exconly()
    )


def test_perigee_and_apogee():
    expected_r_a = 500 * u.km
    expected_r_p = 300 * u.km
    a = (expected_r_a + expected_r_p) / 2
    ecc = expected_r_a / a - 1
    _a = 1.0 * u.deg  # Unused angle
    ss = Orbit.from_classical(Earth, a, ecc, _a, _a, _a, _a)
    assert_allclose(ss.r_a.to(u.km).value, expected_r_a.to(u.km).value)
    assert_allclose(ss.r_p.to(u.km).value, expected_r_p.to(u.km).value)


def test_convert_from_rv_to_coe():
    # Data from Vallado, example 2.6
    attractor = Earth
    p = 11067.790 * u.km
    ecc = 0.83285 * u.one
    inc = 87.87 * u.deg
    raan = 227.89 * u.deg
    argp = 53.38 * u.deg
    nu = 92.335 * u.deg
    expected_r = [6525.344, 6861.535, 6449.125] * u.km
    expected_v = [4.902276, 5.533124, -1.975709] * u.km / u.s

    r, v = Orbit.from_classical(
        attractor, p / (1 - ecc ** 2), ecc, inc, raan, argp, nu
    ).rv()

    assert_quantity_allclose(r, expected_r, rtol=1e-5)
    assert_quantity_allclose(v, expected_v, rtol=1e-5)


def test_convert_from_coe_to_rv():
    # Data from Vallado, example 2.5
    attractor = Earth
    r = [6524.384, 6862.875, 6448.296] * u.km
    v = [4.901327, 5.533756, -1.976341] * u.km / u.s

    expected_p = 11067.79 * u.km
    expected_ecc = 0.832853 * u.one
    expected_inc = 87.870 * u.deg
    expected_raan = 227.89 * u.deg
    expected_argp = 53.38 * u.deg
    expected_nu = 92.335 * u.deg

    ss = Orbit.from_vectors(attractor, r, v)

    _, ecc, inc, raan, argp, nu = ss.classical()
    p = ss.p

    assert_quantity_allclose(p, expected_p, rtol=1e-4)
    assert_quantity_allclose(ecc, expected_ecc, rtol=1e-4)
    assert_quantity_allclose(inc, expected_inc, rtol=1e-4)
    assert_quantity_allclose(raan, expected_raan, rtol=1e-4)
    assert_quantity_allclose(argp, expected_argp, rtol=1e-4)
    assert_quantity_allclose(nu, expected_nu, rtol=1e-4)


def test_perifocal_points_to_perigee():
    _d = 1.0 * u.AU  # Unused distance
    _ = 0.5 * u.one  # Unused dimensionless value
    _a = 1.0 * u.deg  # Unused angle
    ss = Orbit.from_classical(Sun, _d, _, _a, _a, _a, _a)
    p, _, _ = ss.pqw()
    assert_allclose(p, ss.e_vec / ss.ecc)


def test_arglat_within_range():
    r = [3539.08827417, 5310.19903462, 3066.31301457] * u.km
    v = [-6.49780849, 3.24910291, 1.87521413] * u.km / u.s
    ss = Orbit.from_vectors(Earth, r, v)
    assert 0 * u.deg <= ss.arglat <= 360 * u.deg


def test_pqw_returns_dimensionless():
    r_0 = ([1, 0, 0] * u.au).to(u.km)
    v_0 = ([0, 6, 0] * u.au / u.year).to(u.km / u.day)
    ss = Orbit.from_vectors(Sun, r_0, v_0)

    p, q, w = ss.pqw()

    assert p.unit == u.one
    assert q.unit == u.one
    assert w.unit == u.one


def test_from_coord_fails_if_no_time_differential():
    pos = [30000, 0, 0] * u.km
    cartrep = CartesianRepresentation(*pos)

    # Method fails if coordinate instance doesn't contain a differential with respect to time
    with pytest.raises(ValueError) as excinfo:
        ss = Orbit.from_coords(Earth, SkyCoord(cartrep))
    assert (
        "ValueError: Coordinate instance doesn't have a differential with respect to time"
        in excinfo.exconly()
    )


@pytest.mark.parametrize(
    "attractor", [Earth, Jupiter, Mars, Mercury, Neptune, Saturn, Sun, Uranus, Venus]
)
def test_orbit_creation_using_skycoord(attractor):
    vel = [0, 2, 0] * u.km / u.s
    cartdiff = CartesianDifferential(*vel)

    pos = [30000, 0, 0] * u.km
    cartrep = CartesianRepresentation(*pos, differentials=cartdiff)

    coord = SkyCoord(cartrep, frame="icrs")
    o = Orbit.from_coords(attractor, coord)

    inertial_frame_at_body_centre = get_frame(
        attractor, Planes.EARTH_EQUATOR, obstime=coord.obstime
    )

    coord_transformed_to_irf = coord.transform_to(inertial_frame_at_body_centre)
    pos_transformed_to_irf = coord_transformed_to_irf.cartesian.xyz
    vel_transformed_to_irf = coord_transformed_to_irf.cartesian.differentials["s"].d_xyz

    assert (o.r == pos_transformed_to_irf).all()
    assert (o.v == vel_transformed_to_irf).all()


@pytest.mark.remote_data
@pytest.mark.parametrize(
    "attractor", [Earth, Jupiter, Mars, Mercury, Neptune, Saturn, Sun, Uranus, Venus]
)
@pytest.mark.parametrize("frame", [ITRS, GCRS])
@pytest.mark.parametrize("obstime", [J2000, J2000_TDB])
def test_orbit_creation_using_frame_obj(attractor, frame, obstime):
    vel = [0, 2, 0] * u.km / u.s
    cartdiff = CartesianDifferential(*vel)

    pos = [30000, 0, 0] * u.km
    cartrep = CartesianRepresentation(*pos, differentials=cartdiff)

    coord = frame(cartrep, obstime=obstime)
    o = Orbit.from_coords(attractor, coord)

    inertial_frame_at_body_centre = get_frame(
        attractor, Planes.EARTH_EQUATOR, obstime=coord.obstime
    )

    coord_transformed_to_irf = coord.transform_to(inertial_frame_at_body_centre)

    pos_transformed_to_irf = coord_transformed_to_irf.cartesian.xyz
    vel_transformed_to_irf = coord_transformed_to_irf.cartesian.differentials["s"].d_xyz

    assert_quantity_allclose(o.r, pos_transformed_to_irf, atol=1e-5 * u.km)
    assert_quantity_allclose(o.v, vel_transformed_to_irf, atol=1e-5 * u.km / u.s)


@pytest.mark.parametrize("obstime", [J2000, J2000_TDB])
def test_from_coord_fails_for_multiple_positions(obstime):
    cartdiff = CartesianDifferential(
        [[0, 1, 0], [-0.1, 0.9, 0]] * u.km / u.s, xyz_axis=1
    )
    cartrep = CartesianRepresentation(
        [[1, 0, 0], [0.9, 0.1, 0]] * u.km, differentials=cartdiff, xyz_axis=1
    )
    coords = GCRS(cartrep, representation_type=CartesianRepresentation, obstime=obstime)

    with pytest.raises(ValueError) as excinfo:
        ss = Orbit.from_coords(Earth, coords)
    assert (
        "ValueError: Coordinate instance must represents exactly 1 position, found: 2"
        in excinfo.exconly()
    )


def test_from_coord_if_coord_is_not_of_shape_zero():
    pos = [0, 1, 0]
    vel = [1, 0, 0]
    cartdiff = CartesianDifferential([vel] * u.km / u.s, xyz_axis=1)
    cartrep = CartesianRepresentation([pos] * u.km, differentials=cartdiff, xyz_axis=1)
    coords = GCRS(cartrep, representation_type=CartesianRepresentation, obstime=J2000)

    ss = Orbit.from_coords(Earth, coords)

    assert_quantity_allclose(ss.r, pos * u.km, rtol=1e-5)
    assert_quantity_allclose(ss.v, vel * u.km / u.s, rtol=1e-5)
