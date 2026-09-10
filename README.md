# Gravity Assist Robustness Explorer

> **Status: Work in progress.** A nominal deterministic Jupiter flyby can now
> be propagated, measured, and visualised. Validation, Monte Carlo uncertainty
> propagation, and stochastic differential equation modelling are planned
> extensions.

## Project goal

This project will simulate a spacecraft performing a gravity-assist flyby of
Jupiter and investigate how uncertainty changes the outcome of the encounter.

The final aim is to determine how the timing of a trajectory-correction
manoeuvre affects the correction velocity and reserve propellant required to
reach a desired post-flyby trajectory.

## Research question

> How do initial navigation uncertainty and continuous stochastic acceleration
> disturbances affect the timing and propellant requirements of trajectory
> corrections before a Jupiter gravity assist?

## Why this matters

A gravity assist is sensitive to the spacecraft's incoming position and
velocity. Small errors before closest approach can alter its flyby altitude,
turning angle, outgoing direction, and heliocentric velocity. A deterministic
trajectory alone therefore cannot describe the operational risk surrounding a
real encounter.

This project will compare three increasingly realistic models:

1. A nominal deterministic flyby.
2. Monte Carlo propagation of uncertain initial conditions.
3. A stochastic differential equation with continuous acceleration noise.

The comparison will be used to study when a correction should be made and how
much propellant should be reserved for uncertainty.

## Mathematical model

### Deterministic dynamics

The initial flyby model will use the Sun, Jupiter, and a spacecraft of
negligible mass. The Sun and Jupiter affect the spacecraft, while the
spacecraft does not affect either massive body.

The deterministic equations are

```text
dr/dt = v
dv/dt = a(r, t),
```

where `a(r, t)` is the combined gravitational acceleration. These ordinary
differential equations will be integrated using the fourth-order Runge-Kutta
method (RK4).

### Monte Carlo uncertainty

Arrival position, arrival velocity, or manoeuvre execution errors will first
be sampled from chosen probability distributions. Each sample then follows an
ordinary deterministic trajectory. This propagates initial uncertainty but is
not, by itself, stochastic calculus.

### Continuous stochastic disturbances

Continuous unmodelled acceleration will later be represented by the stochastic
differential equation

```text
dr_t = v_t dt
dv_t = a(r_t, t) dt + B dW_t,
```

where `W_t` is a three-dimensional Wiener process and `B` controls the scale
and direction of the disturbance. This model will be simulated with an SDE
method such as Euler-Maruyama rather than RK4.

The noise must be physically interpreted and calibrated; it will not be added
solely to make the model stochastic.

## Units

- Distance: kilometres
- Time: seconds
- Velocity: kilometres per second
- Mass: kilograms
- Acceleration: kilometres per second squared

## Current implementation

The repository currently provides a working deterministic flyby model:

- `CelestialBody` and `OrbitalState` data models;
- gravitational acceleration from multiple bodies;
- a reusable RK4 step and fixed-step trajectory propagator;
- packing of the Jupiter and spacecraft states into a 12-component vector;
- a restricted three-body derivative for a fixed Sun, moving Jupiter, and
  massless spacecraft;
- a 50-day nominal Jupiter encounter propagated at 60-second intervals;
- calculation of closest-approach time, centre distance, and surface altitude;
- comparison of incoming and outgoing velocities at equal Jupiter distances;
- calculation of turning angle and heliocentric speed change;
- a three-dimensional close-up containing a correctly scaled Jupiter and the
  nearby spacecraft trajectory.

Automated tests, refined asymptotic-state estimation, Monte Carlo experiments,
and SDE integration have not yet been implemented.

## Current project layout

```text
.
├── experiments/
│   └── deterministic_flyby.py
├── gravity_assist/
│   ├── __init__.py
│   ├── constants.py
│   ├── forces.py
│   ├── integrators.py
│   ├── models.py
│   └── simulation.py
├── .gitignore
└── README.md
```

## Development roadmap

### Phase 1: validate the deterministic foundation

- Test the celestial-body and orbital-state validation.
- Check gravitational acceleration against a hand-calculated case.
- Test the general RK4 step using a differential equation with a known result.
- Check that the 12-component derivative has the correct shape and values.

### Phase 2: build the deterministic Jupiter flyby

- Add a full heliocentric trajectory plot.
- Check the result at several RK4 timesteps.
- Document the source and interpretation of the initial conditions.

### Phase 3: measure the flyby outcome

- Detect closest approach and calculate flyby altitude. **Completed.**
- Measure the turning angle and outgoing direction. **Completed.**
- Compare incoming and outgoing heliocentric velocity. **Completed.**
- Reject trajectories that intersect Jupiter or violate model assumptions.

### Phase 4: introduce manoeuvres

- Apply an impulsive trajectory-correction manoeuvre before the encounter.
- Define a target post-flyby state or target outcome.
- Find the correction velocity required at different manoeuvre times.
- Convert correction velocity into propellant using the rocket equation.

### Phase 5: propagate initial uncertainty with Monte Carlo

- Choose and justify distributions for arrival and manoeuvre errors.
- Generate many uncertain initial states.
- Propagate each sample through the deterministic flyby model.
- Study the distributions of closest approach, outgoing velocity, correction
  cost, and failed encounters.

### Phase 6: add stochastic calculus

- Define a physically meaningful continuous acceleration-noise model.
- Implement Euler-Maruyama and verify its `sqrt(dt)` noise scaling.
- Compare SDE paths with the deterministic and initial-uncertainty models.
- Perform time-step and sample-size convergence checks.

### Phase 7: produce the research result

- Compare early and late correction strategies.
- Estimate expected correction cost and upper-tail propellant requirements.
- Recommend a reserve covering a stated proportion of simulated encounters.
- Report sensitivity to assumptions about uncertainty and disturbance strength.

## Validation principles

Results will not be treated as meaningful until the model passes appropriate
checks. These include deterministic time-step convergence, conservation tests,
Monte Carlo sample-size convergence, and SDE time-step convergence. Any noise
parameters and probability distributions will be stated explicitly.

## Intended final output

The finished project will contain a reproducible numerical experiment,
visualisations of nominal and uncertain flybys, distributions of correction
costs, and a qualified recommendation for correction timing and propellant
reserve.

It is a robustness study rather than a mission-design tool. The limitations of
the restricted-body model, simplified manoeuvres, assumed ephemerides, and
chosen uncertainty distributions will be documented alongside the results.

## Running the current experiment

The current code requires Python 3.10 or later, NumPy, and Matplotlib. From the
project root, install the dependencies if necessary and run:

```bash
python -m pip install numpy matplotlib
python -m experiments.deterministic_flyby
```

The experiment propagates a 50-day trajectory, reports the closest-approach
time and altitude, and opens a correctly scaled three-dimensional close-up of
the encounter. With the current nominal initial conditions, closest approach
occurs after approximately 13.14 days at an altitude of approximately
371,210 km above Jupiter's surface.
